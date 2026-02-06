#!/bin/bash
#
# Budget Variance Analyzer - Monthly Financial Report Generator
# Compares actual expenses vs projected budget, identifies variances,
# flags anomalies, and generates visual reports with recommendations.
#

set -euo pipefail

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'

# Symbols
UP_ARROW='▲'
DOWN_ARROW='▼'
CHECK='✓'
WARNING='⚠'
ALERT='🚨'
MONEY='💰'
CHART='📊'

# Default values
BUDGET_FILE="${BUDGET_FILE:-budget.csv}"
EXPENSES_FILE="${EXPENSES_FILE:-expenses.csv}"
OUTPUT_DIR="${OUTPUT_DIR:-./reports}"
MONTH="${MONTH:-$(date +%Y-%m)}"
THRESHOLD_WARNING="${THRESHOLD_WARNING:-10}"
THRESHOLD_CRITICAL="${THRESHOLD_CRITICAL:-25}"

# ANSI Bar chart characters
BAR_FULL='█'
BAR_LIGHT='░'

# Display usage
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Budget Variance Analyzer - Compare actual expenses vs budget

OPTIONS:
    -b, --budget FILE       Budget projections CSV (default: budget.csv)
    -e, --expenses FILE     Actual expenses CSV (default: expenses.csv)
    -m, --month MONTH       Month to analyze (YYYY-MM, default: current)
    -o, --output DIR        Output directory for reports (default: ./reports)
    -w, --warning PCT       Warning threshold % (default: 10)
    -c, --critical PCT      Critical threshold % (default: 25)
    -i, --init              Create sample input files
    -h, --help              Show this help

REQUIRED CSV FORMATS:
    budget.csv: category,allocated_amount
    expenses.csv: date,category,amount,description

ENVIRONMENT VARIABLES:
    BUDGET_FILE             Default budget file path
    EXPENSES_FILE           Default expenses file path
    OUTPUT_DIR              Default output directory

EXAMPLES:
    $(basename "$0") --init                          # Create sample files
    $(basename "$0") -m 2024-01                      # Analyze January 2024
    $(basename "$0") -b my_budget.csv -e my_exp.csv  # Use custom files

EOF
}

# Initialize sample data files
init_sample_files() {
    echo -e "${CYAN}Creating sample data files...${RESET}"
    
    cat > budget.csv << 'EOF'
# Budget Projections
# Format: category,allocated_amount
category,allocated_amount
Housing,2000
Food,600
Transportation,400
Utilities,300
Entertainment,200
Healthcare,150
Shopping,300
Savings,500
Miscellaneous,150
EOF
    echo -e "${GREEN}${CHECK} Created budget.csv${RESET}"

    cat > expenses.csv << 'EOF'
# Actual Expenses
# Format: date,category,amount,description
2024-01-05,Housing,1800,Monthly rent
2024-01-08,Food,85.50,Grocery shopping
2024-01-10,Transportation,45.50,Gas station
2024-01-12,Utilities,125.00,Electric bill
2024-01-15,Food,125.30,Grocery run
2024-01-18,Entertainment,75.00,Movie and dinner
2024-01-20,Transportation,320.00,Car insurance
2024-01-22,Healthcare,85.00,Doctor visit copay
2024-01-25,Shopping,245.00,Clothing purchase
2024-01-28,Food,95.20,Grocery shopping
2024-01-30,Utilities,95.50,Internet bill
EOF
    echo -e "${GREEN}${CHECK} Created expenses.csv${RESET}"
    echo ""
    echo -e "${YELLOW}Edit these files with your actual budget and expense data, then run:${RESET}"
    echo -e "  ./budget-variance-analyzer.sh -b budget.csv -e expenses.csv"
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -b|--budget)
                BUDGET_FILE="$2"
                shift 2
                ;;
            -e|--expenses)
                EXPENSES_FILE="$2"
                shift 2
                ;;
            -m|--month)
                MONTH="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -w|--warning)
                THRESHOLD_WARNING="$2"
                shift 2
                ;;
            -c|--critical)
                THRESHOLD_CRITICAL="$2"
                shift 2
                ;;
            -i|--init)
                init_sample_files
                exit 0
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# Validate input files
validate_inputs() {
    local errors=0
    
    if [[ ! -f "$BUDGET_FILE" ]]; then
        echo -e "${RED}${ALERT} Error: Budget file not found: $BUDGET_FILE${RESET}"
        errors=$((errors + 1))
    fi
    
    if [[ ! -f "$EXPENSES_FILE" ]]; then
        echo -e "${RED}${ALERT} Error: Expenses file not found: $EXPENSES_FILE${RESET}"
        errors=$((errors + 1))
    fi
    
    if [[ $errors -gt 0 ]]; then
        echo ""
        echo -e "${YELLOW}Run with --init to create sample files${RESET}"
        exit 1
    fi
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
}

# Read budget data into associative array
read_budget() {
    declare -gA BUDGET
    declare -gA ACTUAL
    declare -gA VARIANCE
    declare -gA VARIANCE_PCT
    declare -gA STATUS
    
    local total_budget=0
    
    while IFS=',' read -r category amount; do
        # Skip comments and header
        [[ "$category" =~ ^#.*$ ]] && continue
        [[ "$category" == "category" ]] && continue
        [[ -z "$category" ]] && continue
        
        # Clean up values
        category=$(echo "$category" | xargs)
        amount=$(echo "$amount" | tr -d '[:space:]')
        
        BUDGET["$category"]=$(printf "%.2f" "$amount")
        ACTUAL["$category"]="0.00"
        total_budget=$(echo "$total_budget + $amount" | bc -l 2>/dev/null || echo "0")
    done < "$BUDGET_FILE"
    
    echo "$total_budget"
}

# Read expense data and aggregate by category
read_expenses() {
    local month_pattern="^${MONTH}"
    local total_expenses=0
    local transaction_count=0
    
    while IFS=',' read -r date category amount description; do
        # Skip comments and header
        [[ "$date" =~ ^#.*$ ]] && continue
        [[ "$date" == "date" ]] && continue
        [[ -z "$date" ]] && continue
        
        # Check if expense is in target month
        [[ ! "$date" =~ $month_pattern ]] && continue
        
        # Clean up values
        category=$(echo "$category" | xargs)
        amount=$(echo "$amount" | tr -d '[:space:]')
        
        # Update actual spending
        if [[ -n "${ACTUAL[$category]+isset}" ]]; then
            ACTUAL["$category"]=$(echo "${ACTUAL[$category]} + $amount" | bc -l)
        else
            # New category not in budget
            ACTUAL["$category"]=$amount
            BUDGET["$category"]="0.00"
        fi
        
        total_expenses=$(echo "$total_expenses + $amount" | bc -l)
        transaction_count=$((transaction_count + 1))
    done < "$EXPENSES_FILE"
    
    echo "$total_expenses $transaction_count"
}

# Calculate variances
calculate_variances() {
    for category in "${!BUDGET[@]}"; do
        local budgeted=${BUDGET[$category]:-0}
        local actual=${ACTUAL[$category]:-0}
        
        # Calculate variance (negative = under budget, positive = over budget)
        local variance=$(echo "$actual - $budgeted" | bc -l)
        VARIANCE["$category"]=$variance
        
        # Calculate variance percentage
        if (( $(echo "$budgeted > 0" | bc -l) )); then
            local variance_pct=$(echo "($variance / $budgeted) * 100" | bc -l)
            VARIANCE_PCT["$category"]=$(printf "%.1f" "$variance_pct")
        else
            VARIANCE_PCT["$category"]="0.0"
        fi
        
        # Determine status
        local abs_variance=$(echo "${variance#-}" | bc -l)
        local abs_pct=$(echo "${VARIANCE_PCT[$category]#-}" | bc -l)
        
        if (( $(echo "$abs_pct >= $THRESHOLD_CRITICAL" | bc -l) )); then
            STATUS["$category"]="CRITICAL"
        elif (( $(echo "$abs_pct >= $THRESHOLD_WARNING" | bc -l) )); then
            STATUS["$category"]="WARNING"
        else
            STATUS["$category"]="OK"
        fi
    done
}

# Generate ASCII bar chart
bar_chart() {
    local value=$1
    local max=$2
    local width=${3:-20}
    
    if (( $(echo "$max <= 0" | bc -l) )); then
        printf "%${width}s" ""
        return
    fi
    
    local filled=$(echo "($value / $max) * $width" | bc -l | cut -d. -f1)
    filled=${filled:-0}
    
    if [[ $filled -gt $width ]]; then
        filled=$width
    fi
    
    local empty=$((width - filled))
    
    printf "%s%${empty}s" "$(printf "%${filled}s" | tr ' ' "$BAR_FULL")" "" | tr ' ' "$BAR_LIGHT"
}

# Get status color
status_color() {
    case $1 in
        CRITICAL) echo "$RED" ;;
        WARNING)  echo "$YELLOW" ;;
        OK)       echo "$GREEN" ;;
        *)        echo "$RESET" ;;
    esac
}

# Get variance indicator
variance_indicator() {
    local variance=$1
    local abs_var=${variance#-}
    
    if (( $(echo "$variance > 0" | bc -l) )); then
        echo -e "${RED}${UP_ARROW} +${abs_var}${RESET}"
    elif (( $(echo "$variance < 0" | bc -l) )); then
        echo -e "${GREEN}${DOWN_ARROW} -${abs_var}${RESET}"
    else
        echo -e "${GREEN}=${RESET}"
    fi
}

# Print header
print_header() {
    clear 2>/dev/null || true
    echo ""
    echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${BOLD}${CYAN}║${RESET}              ${BOLD}${MONEY} BUDGET VARIANCE ANALYSIS REPORT ${MONEY}${RESET}                   ${BOLD}${CYAN}║${RESET}"
    echo -e "${BOLD}${CYAN}║${RESET}                      Month: ${YELLOW}${MONTH}${RESET}                                   ${BOLD}${CYAN}║${RESET}"
    echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
}

# Print category table
print_category_table() {
    echo -e "${BOLD}${CHART} EXPENSE BREAKDOWN BY CATEGORY${RESET}"
    echo ""
    
    printf "${BOLD}%-18s %12s %12s %10s %8s %s${RESET}\n" \
        "Category" "Budgeted" "Actual" "Variance" "Status" ""
    printf "${BOLD}%s${RESET}\n" "────────────────────────────────────────────────────────────────────────────"
    
    # Find max for chart scaling
    local max_val=0
    for cat in "${!ACTUAL[@]}"; do
        local val=${ACTUAL[$cat]:-0}
        if (( $(echo "$val > $max_val" | bc -l) )); then
            max_val=$val
        fi
    done
    
    # Sort categories by variance percentage (descending)
    for cat in "${!BUDGET[@]}"; do
        local budgeted=$(printf "%.2f" "${BUDGET[$cat]:-0}")
        local actual=$(printf "%.2f" "${ACTUAL[$cat]:-0}")
        local variance=$(printf "%.2f" "${VARIANCE[$cat]:-0}")
        local var_pct="${VARIANCE_PCT[$cat]:-0}"
        local status="${STATUS[$cat]:-OK}"
        
        local color=$(status_color "$status")
        local indicator=$(variance_indicator "$variance")
        local bar=$(bar_chart "$actual" "$max_val" 15)
        
        printf "%-18s %12s %12s %10s %b%s%b  %s\n" \
            "$(echo "$cat" | cut -c1-18)" \
            "\$${budgeted}" \
            "\$${actual}" \
            "${var_pct}%" \
            "$color" "$status" "$RESET" \
            "$bar"
    done | sort -t'%' -k1 -nr
    
    echo ""
}

# Print summary statistics
print_summary() {
    local total_budget=$1
    local total_expenses=$2
    local transaction_count=$3
    
    local net_variance=$(echo "$total_expenses - $total_budget" | bc -l)
    local variance_pct=$(echo "($net_variance / $total_budget) * 100" | bc -l 2>/dev/null || echo "0")
    variance_pct=$(printf "%.1f" "$variance_pct")
    
    local remaining=$(echo "$total_budget - $total_expenses" | bc -l)
    
    echo -e "${BOLD}${MONEY} FINANCIAL SUMMARY${RESET}"
    echo ""
    
    echo -e "  Total Budgeted:      ${BLUE}\$$(printf "%.2f" "$total_budget")${RESET}"
    echo -e "  Total Spent:         ${CYAN}\$$(printf "%.2f" "$total_expenses")${RESET}"
    echo -e "  Transactions:        ${YELLOW}$transaction_count${RESET}"
    echo ""
    
    if (( $(echo "$net_variance > 0" | bc -l) )); then
        echo -e "  Net Variance:        ${RED}\$$(printf "%.2f" "$net_variance") (${variance_pct}% over budget)${RESET}"
        echo -e "  Remaining:           ${RED}\$$(printf "%.2f" "$remaining")${RESET}"
    elif (( $(echo "$net_variance < 0" | bc -l) )); then
        echo -e "  Net Variance:        ${GREEN}\$$(printf "%.2f" "${net_variance#-}") (${variance_pct#-}% under budget)${RESET} ${CHECK}"
        echo -e "  Remaining:           ${GREEN}\$$(printf "%.2f" "$remaining")${RESET} ${CHECK}"
    else
        echo -e "  Net Variance:        ${GREEN}\$0.00 (exactly on budget)${RESET} ${CHECK}"
    fi
    
    echo ""
}

# Identify anomalies
identify_anomalies() {
    local anomalies=()
    
    # Find categories over critical threshold
    for cat in "${!STATUS[@]}"; do
        if [[ "${STATUS[$cat]}" == "CRITICAL" ]]; then
            local var_pct="${VARIANCE_PCT[$cat]}"
            if (( $(echo "$var_pct > 0" | bc -l) )); then
                anomalies+=("CRITICAL: $cat is ${var_pct}% over budget")
            fi
        fi
    done
    
    # Find categories significantly under budget (>50%)
    for cat in "${!VARIANCE_PCT[@]}"; do
        local var_pct="${VARIANCE_PCT[$cat]}"
        if (( $(echo "$var_pct < -50" | bc -l) )); then
            if [[ "${STATUS[$cat]}" != "CRITICAL" ]]; then
                anomalies+=("NOTICE: $cat is ${var_pct#-}% under budget")
            fi
        fi
    done
    
    # Find unbudgeted categories
    for cat in "${!ACTUAL[@]}"; do
        if [[ -z "${BUDGET[$cat]+isset}" ]] || [[ "${BUDGET[$cat]}" == "0.00" ]]; then
            local actual=$(printf "%.2f" "${ACTUAL[$cat]}")
            anomalies+=("WARNING: Unbudgeted spending in '$cat': \$$actual")
        fi
    done
    
    if [[ ${#anomalies[@]} -gt 0 ]]; then
        echo -e "${BOLD}${ALERT} ANOMALIES & FLAGS${RESET}"
        echo ""
        for anomaly in "${anomalies[@]}"; do
            if [[ "$anomaly" == CRITICAL* ]]; then
                echo -e "  ${RED}${ALERT} $anomaly${RESET}"
            elif [[ "$anomaly" == WARNING* ]]; then
                echo -e "  ${YELLOW}${WARNING} $anomaly${RESET}"
            else
                echo -e "  ${CYAN}ℹ $anomaly${RESET}"
            fi
        done
        echo ""
    fi
}

# Generate recommendations
generate_recommendations() {
    local recommendations=()
    
    # Analyze overspending
    local overspent=0
    for cat in "${!STATUS[@]}"; do
        if [[ "${STATUS[$cat]}" == "CRITICAL" ]]; then
            local var_pct="${VARIANCE_PCT[$cat]}"
            if (( $(echo "$var_pct > 0" | bc -l) )); then
                overspent=$((overspent + 1))
                recommendations+=("Reduce $cat spending by ${var_pct}% to meet budget")
            fi
        fi
    done
    
    # Analyze underspending in savings
    if [[ -n "${BUDGET[Savings]+isset}" ]]; then
        local savings_var="${VARIANCE_PCT[Savings]:-0}"
        if (( $(echo "$savings_var < 0" | bc -l) )); then
            recommendations+=("Consider increasing Savings contributions (currently ${savings_var#-}% under target)")
        fi
    fi
    
    # General recommendations based on overall performance
    local net_var=$1
    if (( $(echo "$net_var > $THRESHOLD_CRITICAL" | bc -l) )); then
        recommendations+=("URGENT: Overall spending is critically over budget. Review all discretionary categories.")
        recommendations+=("Consider implementing a weekly spending review to catch overspending earlier.")
    elif (( $(echo "$net_var > $THRESHOLD_WARNING" | bc -l) )); then
        recommendations+=("Monitor discretionary spending closely to avoid further overruns.")
    elif (( $(echo "$net_var < 0" | bc -l) )); then
        recommendations+=("Great job staying under budget! Consider transferring surplus to emergency fund or investments.")
    fi
    
    if [[ ${#recommendations[@]} -gt 0 ]]; then
        echo -e "${BOLD}${CYAN}💡 RECOMMENDATIONS${RESET}"
        echo ""
        local i=1
        for rec in "${recommendations[@]}"; do
            echo -e "  $i. $rec"
            i=$((i + 1))
        done
        echo ""
    fi
}

# Save report to file
save_report() {
    local report_file="$OUTPUT_DIR/budget-variance-${MONTH}.txt"
    
    {
        echo "BUDGET VARIANCE ANALYSIS REPORT"
        echo "================================"
        echo "Month: $MONTH"
        echo "Generated: $(date)"
        echo ""
        echo "SUMMARY"
        echo "-------"
        echo "Total Budgeted: \$$(printf "%.2f" "$1")"
        echo "Total Spent: \$$(printf "%.2f" "$2")"
        echo "Net Variance: \$$(printf "%.2f" "$3")"
        echo ""
        echo "CATEGORY BREAKDOWN"
        echo "------------------"
        printf "%-20s %12s %12s %12s %s\n" "Category" "Budgeted" "Actual" "Variance" "Status"
        for cat in "${!BUDGET[@]}"; do
            printf "%-20s %12.2f %12.2f %12.2f %s\n" \
                "$cat" \
                "${BUDGET[$cat]:-0}" \
                "${ACTUAL[$cat]:-0}" \
                "${VARIANCE[$cat]:-0}" \
                "${STATUS[$cat]:-OK}"
        done
    } > "$report_file"
    
    echo -e "${GREEN}${CHECK} Report saved to: $report_file${RESET}"
}

# Save CSV export
save_csv_export() {
    local csv_file="$OUTPUT_DIR/budget-variance-${MONTH}.csv"
    
    {
        echo "category,budgeted,actual,variance,variance_pct,status"
        for cat in "${!BUDGET[@]}"; do
            local budgeted="${BUDGET[$cat]:-0}"
            local actual="${ACTUAL[$cat]:-0}"
            local variance="${VARIANCE[$cat]:-0}"
            local var_pct="${VARIANCE_PCT[$cat]:-0}"
            local status="${STATUS[$cat]:-OK}"
            echo "$cat,$budgeted,$actual,$variance,$var_pct,$status"
        done
    } > "$csv_file"
    
    echo -e "${GREEN}${CHECK} CSV export saved to: $csv_file${RESET}"
}

# Save JSON export
save_json_export() {
    local json_file="$OUTPUT_DIR/budget-variance-${MONTH}.json"
    
    {
        echo "{"
        echo "  \"month\": \"$MONTH\","
        echo "  \"generated\": \"$(date -Iseconds)\","
        echo "  \"summary\": {"
        echo "    \"total_budgeted\": $(printf "%.2f" "$1"),"
        echo "    \"total_actual\": $(printf "%.2f" "$2"),"
        echo "    \"net_variance\": $(printf "%.2f" "$3"),"
        echo "    \"transaction_count\": $4"
        echo "  },"
        echo "  \"categories\": ["
        
        local first=true
        for cat in "${!BUDGET[@]}"; do
            if [[ "$first" == "true" ]]; then
                first=false
            else
                echo ","
            fi
            echo -n "    {"
            echo -n "\"category\": \"$cat\", "
            echo -n "\"budgeted\": ${BUDGET[$cat]:-0}, "
            echo -n "\"actual\": ${ACTUAL[$cat]:-0}, "
            echo -n "\"variance\": ${VARIANCE[$cat]:-0}, "
            echo -n "\"variance_pct\": ${VARIANCE_PCT[$cat]:-0}, "
            echo -n "\"status\": \"${STATUS[$cat]:-OK}\""
            echo -n "}"
        done
        echo ""
        echo "  ]"
        echo "}"
    } > "$json_file"
    
    echo -e "${GREEN}${CHECK} JSON export saved to: $json_file${RESET}"
}

# Main function
main() {
    parse_args "$@"
    validate_inputs
    
    # Read and process data
    local total_budget=$(read_budget)
    read -r total_expenses transaction_count <<< "$(read_expenses)"
    calculate_variances
    
    local net_variance=$(echo "$total_expenses - $total_budget" | bc -l)
    
    # Print report
    print_header
    print_summary "$total_budget" "$total_expenses" "$transaction_count"
    print_category_table
    identify_anomalies
    generate_recommendations "$net_variance"
    
    # Save exports
    echo -e "${BOLD}${CYAN}📁 EXPORTED FILES${RESET}"
    echo ""
    save_report "$total_budget" "$total_expenses" "$net_variance"
    save_csv_export
    save_json_export "$total_budget" "$total_expenses" "$net_variance" "$transaction_count"
    
    echo ""
    echo -e "${BOLD}${GREEN}✓ Analysis complete!${RESET}"
}

# Run main function
main "$@"

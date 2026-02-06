#!/bin/bash
#
# 💎 Diamond Hands - Crypto Tax Reporter
# Automated DeFi transaction tracking and tax reporting system
# Generates CSV reports suitable for tax filing with cost basis and gain/loss calculations
#

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================
VERSION="1.0.0"
DATA_DIR="${CRYPTO_TAX_DATA:-$HOME/.crypto-tax-data}"
TRANSACTIONS_FILE="$DATA_DIR/transactions.csv"
PRICES_FILE="$DATA_DIR/price-history.csv"
REPORTS_DIR="$DATA_DIR/reports"
FIFO_LOTS_FILE="$DATA_DIR/fifo-lots.json"

# Tax year (default to current year)
TAX_YEAR="${TAX_YEAR:-$(date +%Y)}"

# Cost basis method: FIFO, LIFO, or HIFO
COST_BASIS_METHOD="${COST_BASIS_METHOD:-FIFO}"

# Fiat currency for reporting
FIAT_CURRENCY="${FIAT_CURRENCY:-USD}"

# ============================================================================
# COLORS AND OUTPUT
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_diamond() { echo -e "${CYAN}💎 $1${NC}"; }

# ============================================================================
# INITIALIZATION
# ============================================================================
init() {
    log_diamond "Initializing Crypto Tax Reporter v$VERSION"
    
    mkdir -p "$DATA_DIR" "$REPORTS_DIR"
    
    # Create transactions file with headers if it doesn't exist
    if [[ ! -f "$TRANSACTIONS_FILE" ]]; then
        cat > "$TRANSACTIONS_FILE" << 'EOF'
# Crypto Transaction Log
# Format: timestamp,tx_hash,tx_type,wallet,token_in,amount_in,token_out,amount_out,fiat_value,fees,protocol,notes
# tx_type: BUY,SELL,SWAP,STAKE_REWARD,YIELD,FORK,AIRDROP,TRANSFER_IN,TRANSFER_OUT,GIFT_SENT,GIFT_RECEIVED
EOF
        log_info "Created transactions file: $TRANSACTIONS_FILE"
    fi
    
    # Create FIFO lots tracking file if it doesn't exist
    if [[ ! -f "$FIFO_LOTS_FILE" ]]; then
        echo '{"lots": {}, "sales": []}' > "$FIFO_LOTS_FILE"
        log_info "Created FIFO lots tracking file"
    fi
    
    log_success "Initialization complete"
}

# ============================================================================
# TRANSACTION MANAGEMENT
# ============================================================================
add_transaction() {
    local timestamp="${1:-$(date -u +"%Y-%m-%d %H:%M:%S")}"
    local tx_hash="${2:-}"
    local tx_type="${3:-}"
    local wallet="${4:-}"
    local token_in="${5:-}"
    local amount_in="${6:-0}"
    local token_out="${7:-}"
    local amount_out="${8:-0}"
    local fiat_value="${9:-}"
    local fees="${10:-0}"
    local protocol="${11:-}"
    local notes="${12:-}"
    
    # Validate required fields
    if [[ -z "$tx_type" ]]; then
        log_error "Transaction type is required"
        return 1
    fi
    
    # Auto-calculate fiat value if not provided
    if [[ -z "$fiat_value" || "$fiat_value" == "auto" ]]; then
        fiat_value=$(get_fiat_value "$token_out" "$amount_out" "$timestamp")
    fi
    
    # Escape notes for CSV
    notes="${notes//,/;}"
    
    echo "$timestamp,$tx_hash,$tx_type,$wallet,$token_in,$amount_in,$token_out,$amount_out,$fiat_value,$fees,$protocol,$notes" >> "$TRANSACTIONS_FILE"
    log_success "Added $tx_type transaction: $amount_out $token_out"
    
    # Update FIFO lots
    update_fifo_lots "$tx_type" "$token_in" "$amount_in" "$token_out" "$amount_out" "$fiat_value" "$timestamp"
}

get_fiat_value() {
    local token="$1"
    local amount="$2"
    local timestamp="$3"
    
    # Try to get historical price from price file
    local price=$(grep -i "$token,$timestamp" "$PRICES_FILE" 2>/dev/null | cut -d',' -f3 | tail -1)
    
    if [[ -n "$price" && "$price" != "0" ]]; then
        echo "$(echo "$amount * $price" | bc -l 2>/dev/null || echo "0")"
    else
        # Fallback: use current price approximation
        echo "0"
    fi
}

# ============================================================================
# FIFO LOTS MANAGEMENT
# ============================================================================
update_fifo_lots() {
    local tx_type="$1"
    local token_in="$2"
    local amount_in="$3"
    local token_out="$4"
    local amount_out="$5"
    local fiat_value="$6"
    local timestamp="$7"
    
    # Load current lots
    local lots_json=$(cat "$FIFO_LOTS_FILE")
    
    case "$tx_type" in
        BUY|STAKE_REWARD|YIELD|FORK|AIRDROP|GIFT_RECEIVED)
            # Add to lots (acquisition)
            if [[ -n "$token_out" && "$amount_out" != "0" ]]; then
                local cost_basis_per_unit="0"
                if [[ -n "$fiat_value" && "$fiat_value" != "0" && "$amount_out" != "0" ]]; then
                    cost_basis_per_unit=$(echo "scale=8; $fiat_value / $amount_out" | bc 2>/dev/null || echo "0")
                fi
                
                local new_lot="{\"timestamp\":\"$timestamp\",\"amount\":$amount_out,\"cost_basis\":$cost_basis_per_unit,\"remaining\":$amount_out}"
                lots_json=$(echo "$lots_json" | jq --arg token "$token_out" --argjson lot "$new_lot" '.lots[$token] += [$lot]')
            fi
            ;;
        SELL|SWAP|TRANSFER_OUT|GIFT_SENT)
            # Remove from lots (disposition) - calculate gain/loss
            if [[ -n "$token_in" && "$amount_in" != "0" ]]; then
                local sale_lot=$(calculate_sale_lots "$token_in" "$amount_in" "$fiat_value" "$timestamp")
                lots_json=$(echo "$lots_json" | jq --argjson sale "$sale_lot" '.sales += [$sale]')
                
                # Update remaining amounts in lots
                lots_json=$(update_remaining_lots "$lots_json" "$token_in" "$amount_in")
            fi
            ;;
    esac
    
    echo "$lots_json" > "$FIFO_LOTS_FILE"
}

calculate_sale_lots() {
    local token="$1"
    local amount_to_sell="$2"
    local sale_proceeds="$3"
    local timestamp="$4"
    
    local lots=$(cat "$FIFO_LOTS_FILE" | jq -r --arg token "$token" '.lots[$token] // []')
    local remaining_to_sell="$amount_to_sell"
    local total_cost_basis="0"
    local lots_used="[]"
    
    # Process lots based on cost basis method
    local sorted_lots="$lots"
    case "$COST_BASIS_METHOD" in
        FIFO)
            # Already in chronological order (FIFO)
            ;;
        LIFO)
            sorted_lots=$(echo "$lots" | jq 'reverse')
            ;;
        HIFO)
            sorted_lots=$(echo "$lots" | jq 'sort_by(.cost_basis) | reverse')
            ;;
    esac
    
    # Calculate cost basis from lots
    local lot_count=$(echo "$sorted_lots" | jq 'length')
    for ((i=0; i<lot_count; i++)); do
        if [[ $(echo "$remaining_to_sell > 0" | bc -l) -eq 0 ]]; then
            break
        fi
        
        local lot=$(echo "$sorted_lots" | jq -r ".[$i]")
        local lot_remaining=$(echo "$lot" | jq -r '.remaining')
        local lot_cost_basis=$(echo "$lot" | jq -r '.cost_basis')
        local lot_timestamp=$(echo "$lot" | jq -r '.timestamp')
        
        local amount_from_lot="$lot_remaining"
        if (( $(echo "$remaining_to_sell < $lot_remaining" | bc -l) )); then
            amount_from_lot="$remaining_to_sell"
        fi
        
        local lot_cost=$(echo "scale=8; $amount_from_lot * $lot_cost_basis" | bc)
        total_cost_basis=$(echo "scale=8; $total_cost_basis + $lot_cost" | bc)
        
        lots_used=$(echo "$lots_used" | jq --arg amount "$amount_from_lot" --arg cost_basis "$lot_cost_basis" --arg ts "$lot_timestamp" '. += [{"amount": $amount, "cost_basis": $cost_basis, "timestamp": $ts}]')
        
        remaining_to_sell=$(echo "scale=8; $remaining_to_sell - $amount_from_lot" | bc)
    done
    
    local gain_loss=$(echo "scale=8; $sale_proceeds - $total_cost_basis" | bc)
    
    # Return sale record
    echo "{\"timestamp\":\"$timestamp\",\"token\":\"$token\",\"amount_sold\":$amount_to_sell,\"proceeds\":$sale_proceeds,\"cost_basis\":$total_cost_basis,\"gain_loss\":$gain_loss,\"lots_used\":$lots_used}"
}

update_remaining_lots() {
    local json="$1"
    local token="$2"
    local amount_sold="$3"
    
    echo "$json" | jq --arg token "$token" --arg amount "$amount_sold" '
        .lots[$token] as $token_lots |
        $token_lots // [] | to_entries |
        reduce .[] as $item ( {remaining: ($amount | tonumber), lots: []};
            if .remaining > 0 then
                $item.value as $lot |
                ($lot.remaining | tonumber) as $lot_remaining |
                if .remaining >= $lot_remaining then
                    {remaining: (.remaining - $lot_remaining), lots: (.lots + [$item.key])}
                else
                    {remaining: 0, lots: .lots}
                end
            else
                .
            end
        ) |
        reduce .lots[] as $idx ($token_lots; .[$idx | tonumber].remaining = 0) |
        . as $updated_lots |
        $json | .lots[$token] = ($updated_lots | map(select(.remaining > 0)))
    '
}

# ============================================================================
# CSV GENERATION
# ============================================================================
generate_tax_report() {
    local output_file="${1:-$REPORTS_DIR/crypto-tax-report-$TAX_YEAR.csv}"
    
    log_diamond "Generating tax report for $TAX_YEAR"
    
    # Generate summary report
    cat > "$output_file" << EOF
# Crypto Tax Report - $TAX_YEAR
# Generated by 💎 Diamond Hands Crypto Tax Reporter v$VERSION
# Cost Basis Method: $COST_BASIS_METHOD
# Fiat Currency: $FIAT_CURRENCY
# Report Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
#
EOF

    # Section 1: Capital Gains/Losses
    echo -e "\n# CAPITAL GAINS AND LOSSES (Form 8949)\n" >> "$output_file"
    echo "Date Acquired,Date Sold,Asset,Amount Sold,Sale Proceeds,Cost Basis,Gain/Loss,Term,Tx Hash" >> "$output_file"
    
    local sales=$(cat "$FIFO_LOTS_FILE" | jq -r '.sales[]')
    local total_short_gains="0"
    local total_long_gains="0"
    local total_short_losses="0"
    local total_long_losses="0"
    
    while IFS= read -r sale; do
        [[ -z "$sale" ]] && continue
        
        local timestamp=$(echo "$sale" | jq -r '.timestamp')
        local token=$(echo "$sale" | jq -r '.token')
        local amount=$(echo "$sale" | jq -r '.amount_sold')
        local proceeds=$(echo "$sale" | jq -r '.proceeds')
        local cost_basis=$(echo "$sale" | jq -r '.cost_basis')
        local gain_loss=$(echo "$sale" | jq -r '.gain_loss')
        
        # Calculate term (short vs long term)
        local acquisition_dates=$(echo "$sale" | jq -r '.lots_used[].timestamp')
        local earliest_acquisition=""
        for acq_date in $acquisition_dates; do
            if [[ -z "$earliest_acquisition" || "$acq_date" < "$earliest_acquisition" ]]; then
                earliest_acquisition="$acq_date"
            fi
        done
        
        local term="Short"
        if [[ -n "$earliest_acquisition" ]]; then
            local acq_epoch=$(date -d "$earliest_acquisition" +%s 2>/dev/null || echo "0")
            local sale_epoch=$(date -d "$timestamp" +%s 2>/dev/null || echo "0")
            local days_diff=$(( (sale_epoch - acq_epoch) / 86400 ))
            if [[ $days_diff -gt 365 ]]; then
                term="Long"
            fi
        fi
        
        echo "$earliest_acquisition,$timestamp,$token,$amount,$proceeds,$cost_basis,$gain_loss,$term," >> "$output_file"
        
        # Categorize gains/losses
        if (( $(echo "$gain_loss >= 0" | bc -l) )); then
            if [[ "$term" == "Long" ]]; then
                total_long_gains=$(echo "scale=8; $total_long_gains + $gain_loss" | bc)
            else
                total_short_gains=$(echo "scale=8; $total_short_gains + $gain_loss" | bc)
            fi
        else
            if [[ "$term" == "Long" ]]; then
                total_long_losses=$(echo "scale=8; $total_long_losses + $gain_loss" | bc)
            else
                total_short_losses=$(echo "scale=8; $total_short_losses + $gain_loss" | bc)
            fi
        fi
    done <<< "$sales"
    
    # Section 2: Ordinary Income
    echo -e "\n# ORDINARY INCOME (Schedule 1)\n" >> "$output_file"
    echo "Date,Type,Asset,Amount,Fair Market Value,Source,Notes" >> "$output_file"
    
    local total_income="0"
    while IFS=',' read -r timestamp tx_hash tx_type wallet token_in amount_in token_out amount_out fiat_value fees protocol notes; do
        [[ "$timestamp" =~ ^# ]] && continue
        [[ -z "$timestamp" ]] && continue
        [[ -z "$tx_type" ]] && continue
        
        case "$tx_type" in
            STAKE_REWARD|YIELD|AIRDROP|FORK)
                echo "$timestamp,$tx_type,$token_out,$amount_out,$fiat_value,$protocol,$notes" >> "$output_file"
                total_income=$(echo "scale=8; $total_income + ${fiat_value:-0}" | bc)
                ;;
        esac
    done < "$TRANSACTIONS_FILE"
    
    # Section 3: Summary
    local net_short=$(echo "scale=8; $total_short_gains + $total_short_losses" | bc)
    local net_long=$(echo "scale=8; $total_long_gains + $total_long_losses" | bc)
    local total_capital_gains=$(echo "scale=8; $net_short + $net_long" | bc)
    
    cat >> "$output_file" << EOF

# SUMMARY
# Total Short-Term Gains: $total_short_gains
# Total Short-Term Losses: $total_short_losses
# Net Short-Term: $net_short
# Total Long-Term Gains: $total_long_gains
# Total Long-Term Losses: $total_long_losses
# Net Long-Term: $net_long
# Total Capital Gains/Losses: $total_capital_gains
# Total Ordinary Income: $total_income
EOF

    log_success "Tax report generated: $output_file"
    
    # Display summary
    echo ""
    log_diamond "Tax Summary for $TAX_YEAR"
    echo "  Short-Term Gains:  \$$(printf "%.2f" $total_short_gains 2>/dev/null || echo "0.00")"
    echo "  Short-Term Losses: \$$(printf "%.2f" $total_short_losses 2>/dev/null || echo "0.00")"
    echo "  Long-Term Gains:   \$$(printf "%.2f" $total_long_gains 2>/dev/null || echo "0.00")"
    echo "  Long-Term Losses:  \$$(printf "%.2f" $total_long_losses 2>/dev/null || echo "0.00")"
    echo "  Ordinary Income:   \$$(printf "%.2f" $total_income 2>/dev/null || echo "0.00")"
    echo ""
    echo "  Net Capital Gains: \$$(printf "%.2f" $total_capital_gains 2>/dev/null || echo "0.00")"
}

# ============================================================================
# TRANSACTION IMPORT
# ============================================================================
import_csv() {
    local file="$1"
    local source="${2:-generic}"
    
    log_info "Importing transactions from $source: $file"
    
    local count=0
    while IFS=',' read -r line; do
        [[ "$line" =~ ^# ]] && continue
        [[ -z "$line" ]] && continue
        
        # Parse based on source format
        case "$source" in
            etherscan|bscscan)
                # Standard blockchain explorer format
                local tx_hash=$(echo "$line" | cut -d',' -f1)
                local timestamp=$(echo "$line" | cut -d',' -f2)
                local from=$(echo "$line" | cut -d',' -f3)
                local to=$(echo "$line" | cut -d',' -f4)
                local value=$(echo "$line" | cut -d',' -f5)
                local token=$(echo "$line" | cut -d',' -f6)
                local tx_type="TRANSFER"
                [[ -n "$to" ]] && tx_type="TRANSFER_IN"
                [[ -n "$from" ]] && tx_type="TRANSFER_OUT"
                
                add_transaction "$timestamp" "$tx_hash" "$tx_type" "" "" 0 "$token" "$value" "" 0 "" ""
                ((count++))
                ;;
            coinbase|binance|kraken)
                # Exchange export format
                local timestamp=$(echo "$line" | cut -d',' -f1)
                local tx_type=$(echo "$line" | cut -d',' -f2 | tr '[:lower:]' '[:upper:]')
                local asset=$(echo "$line" | cut -d',' -f3)
                local amount=$(echo "$line" | cut -d',' -f4)
                local fiat_value=$(echo "$line" | cut -d',' -f5)
                local fees=$(echo "$line" | cut -d',' -f6)
                
                add_transaction "$timestamp" "" "$tx_type" "" "" 0 "$asset" "$amount" "$fiat_value" "$fees" "$source" ""
                ((count++))
                ;;
            generic)
                # Default format: timestamp,tx_type,token,amount,fiat_value
                local timestamp=$(echo "$line" | cut -d',' -f1)
                local tx_type=$(echo "$line" | cut -d',' -f2 | tr '[:lower:]' '[:upper:]')
                local token=$(echo "$line" | cut -d',' -f3)
                local amount=$(echo "$line" | cut -d',' -f4)
                local fiat_value=$(echo "$line" | cut -d',' -f5)
                
                add_transaction "$timestamp" "" "$tx_type" "" "" 0 "$token" "$amount" "$fiat_value" 0 "" ""
                ((count++))
                ;;
        esac
    done < "$file"
    
    log_success "Imported $count transactions"
}

# ============================================================================
# PORTFOLIO TRACKING
# ============================================================================
show_portfolio() {
    log_diamond "Current Portfolio Holdings"
    echo ""
    
    printf "%-15s %15s %20s %20s\n" "Asset" "Amount" "Avg Cost Basis" "Current Value"
    printf "%-15s %15s %20s %20s\n" "-----" "------" "--------------" "-------------"
    
    local lots=$(cat "$FIFO_LOTS_FILE" | jq -r '.lots')
    local tokens=$(echo "$lots" | jq -r 'keys[]')
    
    local total_value="0"
    local total_cost="0"
    
    for token in $tokens; do
        local token_lots=$(echo "$lots" | jq -r --arg t "$token" '.[$t] // []')
        local total_amount="0"
        local weighted_cost="0"
        
        while IFS= read -r lot; do
            [[ -z "$lot" ]] && continue
            local remaining=$(echo "$lot" | jq -r '.remaining')
            local cost_basis=$(echo "$lot" | jq -r '.cost_basis')
            total_amount=$(echo "scale=8; $total_amount + $remaining" | bc)
            weighted_cost=$(echo "scale=8; $weighted_cost + ($remaining * $cost_basis)" | bc)
        done <<< "$(echo "$token_lots" | jq -c '.[]')"
        
        if (( $(echo "$total_amount > 0" | bc -l) )); then
            local avg_cost="0"
            if (( $(echo "$total_amount > 0" | bc -l) )); then
                avg_cost=$(echo "scale=8; $weighted_cost / $total_amount" | bc)
            fi
            local current_value="$weighted_cost" # Use cost basis as fallback
            
            printf "%-15s %15.8f %20.2f %20.2f\n" "$token" "$total_amount" "$avg_cost" "$current_value"
            
            total_value=$(echo "scale=8; $total_value + $current_value" | bc)
            total_cost=$(echo "scale=8; $total_cost + $weighted_cost" | bc)
        fi
    done
    
    echo ""
    printf "%-15s %35s %20.2f\n" "TOTAL" "" "$total_value"
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================
export_turbotax() {
    local output_file="${1:-$REPORTS_DIR/turbotax-$TAX_YEAR.csv}"
    
    log_diamond "Generating TurboTax-compatible export"
    
    cat > "$output_file" << 'EOF'
Date,Type,Amount,Asset,Fiat Value,Fiat Currency,Description
EOF

    while IFS=',' read -r timestamp tx_hash tx_type wallet token_in amount_in token_out amount_out fiat_value fees protocol notes; do
        [[ "$timestamp" =~ ^# ]] && continue
        [[ -z "$timestamp" ]] && continue
        
        local date=$(date -d "$timestamp" +"%m/%d/%Y" 2>/dev/null || echo "$timestamp")
        local tt_type=""
        
        case "$tx_type" in
            BUY) tt_type="Buy" ;;
            SELL) tt_type="Sell" ;;
            STAKE_REWARD|YIELD|AIRDROP|FORK) tt_type="Income" ;;
            *) continue ;;
        esac
        
        local asset="${token_out:-$token_in}"
        local amount="${amount_out:-$amount_in}"
        
        echo "$date,$tt_type,$amount,$asset,$fiat_value,$FIAT_CURRENCY,$notes" >> "$output_file"
    done < "$TRANSACTIONS_FILE"
    
    log_success "TurboTax export generated: $output_file"
}

export_cointracker() {
    local output_file="${1:-$REPORTS_DIR/cointracker-$TAX_YEAR.csv}"
    
    log_diamond "Generating CoinTracker-compatible export"
    
    cat > "$output_file" << 'EOF'
Date,Received Quantity,Received Currency,Sent Quantity,Sent Currency,Fee Amount,Fee Currency,Tag
EOF

    while IFS=',' read -r timestamp tx_hash tx_type wallet token_in amount_in token_out amount_out fiat_value fees protocol notes; do
        [[ "$timestamp" =~ ^# ]] && continue
        [[ -z "$timestamp" ]] && continue
        
        local date=$(date -d "$timestamp" +"%m/%d/%Y %H:%M:%S" 2>/dev/null || echo "$timestamp")
        local tag=""
        
        case "$tx_type" in
            STAKE_REWARD|YIELD) tag="staking" ;;
            AIRDROP) tag="airdrop" ;;
            FORK) tag="fork" ;;
            GIFT_RECEIVED) tag="gift" ;;
        esac
        
        local received_qty=""
        local received_curr=""
        local sent_qty=""
        local sent_curr=""
        
        case "$tx_type" in
            BUY|STAKE_REWARD|YIELD|AIRDROP|FORK|GIFT_RECEIVED|TRANSFER_IN)
                received_qty="$amount_out"
                received_curr="$token_out"
                ;;
            SELL|TRANSFER_OUT|GIFT_SENT)
                sent_qty="$amount_in"
                sent_curr="$token_in"
                ;;
            SWAP)
                received_qty="$amount_out"
                received_curr="$token_out"
                sent_qty="$amount_in"
                sent_curr="$token_in"
                ;;
        esac
        
        echo "$date,$received_qty,$received_curr,$sent_qty,$sent_curr,$fees,$FIAT_CURRENCY,$tag" >> "$output_file"
    done < "$TRANSACTIONS_FILE"
    
    log_success "CoinTracker export generated: $output_file"
}

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================
show_help() {
    cat << 'EOF'
💎 Diamond Hands - Crypto Tax Reporter

USAGE:
    crypto-tax-reporter.sh [COMMAND] [OPTIONS]

COMMANDS:
    init                        Initialize the tax reporting system
    add [ARGS]                  Add a transaction manually
    import FILE [SOURCE]        Import transactions from CSV
                                Sources: etherscan, bscscan, coinbase, binance, kraken, generic
    report [OUTPUT_FILE]        Generate tax report for current year
    portfolio                   Show current portfolio holdings
    export-turbotax [FILE]      Export to TurboTax format
    export-cointracker [FILE]   Export to CoinTracker format
    help                        Show this help message

ADD TRANSACTION FORMAT:
    add "TIMESTAMP" "TX_HASH" "TYPE" "WALLET" "TOKEN_IN" "AMOUNT_IN" "TOKEN_OUT" "AMOUNT_OUT" "FIAT_VALUE" "FEES" "PROTOCOL" "NOTES"
    
    Transaction Types: BUY, SELL, SWAP, STAKE_REWARD, YIELD, FORK, AIRDROP, 
                       TRANSFER_IN, TRANSFER_OUT, GIFT_SENT, GIFT_RECEIVED

EXAMPLES:
    # Initialize the system
    ./crypto-tax-reporter.sh init
    
    # Add a buy transaction
    ./crypto-tax-reporter.sh add "2024-01-15 10:30:00" "" "BUY" "" "" 0 "BTC" 0.5 21000 15 "Coinbase" "First BTC purchase"
    
    # Add staking rewards
    ./crypto-tax-reporter.sh add "2024-02-01 00:00:00" "" "STAKE_REWARD" "" "" 0 "ETH" 0.05 150 0 "Lido" "Monthly staking reward"
    
    # Import from exchange export
    ./crypto-tax-reporter.sh import coinbase-export.csv coinbase
    
    # Generate tax report
    ./crypto-tax-reporter.sh report

ENVIRONMENT VARIABLES:
    CRYPTO_TAX_DATA      Data directory (default: ~/.crypto-tax-data)
    TAX_YEAR             Tax year to report (default: current year)
    COST_BASIS_METHOD    FIFO, LIFO, or HIFO (default: FIFO)
    FIAT_CURRENCY        Reporting currency (default: USD)

EOF
}

# ============================================================================
# MAIN
# ============================================================================
main() {
    local command="${1:-help}"
    shift || true
    
    case "$command" in
        init)
            init
            ;;
        add)
            init 2>/dev/null || true
            add_transaction "$@"
            ;;
        import)
            init 2>/dev/null || true
            if [[ -z "${1:-}" ]]; then
                log_error "Please specify a file to import"
                exit 1
            fi
            import_csv "$1" "${2:-generic}"
            ;;
        report)
            init 2>/dev/null || true
            generate_tax_report "${1:-}"
            ;;
        portfolio)
            init 2>/dev/null || true
            show_portfolio
            ;;
        export-turbotax|turbotax)
            init 2>/dev/null || true
            export_turbotax "${1:-}"
            ;;
        export-cointracker|cointracker)
            init 2>/dev/null || true
            export_cointracker "${1:-}"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"

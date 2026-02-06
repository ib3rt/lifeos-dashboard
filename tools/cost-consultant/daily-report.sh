#!/bin/bash
#
# LLM Cost Consultant - Daily Report Script
#
# Generates daily cost reports and distributes them to configured channels.
# Designed to run via cron for automated daily reporting.
#
# Usage:
#   ./daily-report.sh                    # Generate today's report
#   ./daily-report.sh --date 2024-01-15  # Generate report for specific date
#   ./daily-report.sh --channel discord  # Send to Discord only
#   ./daily-report.sh --test            # Test mode (no alerts)
#

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"
REPORTS_DIR="${SCRIPT_DIR}/../reports"
LOG_FILE="${SCRIPT_DIR}/logs/daily-report.log"
PYTHON_PATH="${PYTHON_PATH:-python3}"

# Default settings
DATE_FORMAT="%Y-%m-%d"
TODAY=$(date +${DATE_FORMAT})
REPORT_TYPE="daily"
OUTPUT_FORMAT="markdown"
CHANNELS=()
SAVE_REPORT=true
TEST_MODE=false
VERBOSE=false

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[${timestamp}] [${level}] ${message}" | tee -a "${LOG_FILE}"
}

log_info() {
    log "INFO" "$*"
}

log_warn() {
    log "${YELLOW}WARN${NC}" "$*"
}

log_error() {
    log "${RED}ERROR${NC}" "$*"
}

log_success() {
    log "${GREEN}SUCCESS${NC}" "$*"
}

# Ensure log directory exists
mkdir -p "$(dirname "${LOG_FILE}")"

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --date)
                TODAY="$2"
                shift 2
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            --channel)
                CHANNELS+=("$2")
                shift 2
                ;;
            --save)
                SAVE_REPORT=true
                shift
                ;;
            --no-save)
                SAVE_REPORT=false
                shift
                ;;
            --test)
                TEST_MODE=true
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << EOF
LLM Cost Consultant - Daily Report Script

Usage: $(basename "$0") [OPTIONS]

Options:
  --date DATE        Generate report for specific date (YYYY-MM-DD)
  --format FORMAT    Output format: markdown, json, csv (default: markdown)
  --channel CHANNEL  Send to specific channel: discord, telegram, email
  --save             Save report to file (default)
  --no-save          Don't save report to file
  --test             Test mode (no alerts or notifications)
  --verbose, -v     Verbose output
  --help, -h        Show this help message

Examples:
  $(basename "$0")                                    # Today's report
  $(basename "$0") --date 2024-01-15                  # Specific date
  $(basename "$0") --format json --channel discord    # JSON to Discord
  $(basename "$0") --test                             # Test run

Cron Examples:
  # Daily morning report at 8 AM
  0 8 * * * /path/to/daily-report.sh

  # Evening summary at 8 PM
  0 20 * * * /path/to/daily-report.sh --channel discord
EOF
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    local missing=()
    
    # Check Python
    if ! command -v "${PYTHON_PATH}" &> /dev/null; then
        missing+=("python3")
    fi
    
    # Check required Python modules
    if ! "${PYTHON_PATH}" -c "import yaml" 2>/dev/null; then
        missing+=("pyyaml")
    fi
    
    # Check reporter module
    if [[ ! -f "${SCRIPT_DIR}/reporter.py" ]]; then
        missing+=("reporter.py")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing dependencies: ${missing[*]}"
        exit 1
    fi
    
    log_success "All dependencies available"
}

# Create required directories
setup_directories() {
    log_info "Setting up directories..."
    
    mkdir -p "${REPORTS_DIR}"
    mkdir -p "${SCRIPT_DIR}/logs"
    mkdir -p "${SCRIPT_DIR}/data"
    
    log_success "Directories ready"
}

# Generate report using Python
generate_report() {
    log_info "Generating ${REPORT_TYPE} report for ${TODAY}..."
    
    local report_content
    
    # Call Python reporter module
    report_content=$("${PYTHON_PATH}" -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from reporter import CostReporter
import json

reporter = CostReporter(
    tracker_db='${SCRIPT_DIR}/data/costs.db',
    output_dir='${REPORTS_DIR}'
)

if '${REPORT_TYPE}' == 'daily':
    content = reporter.generate_daily_report(
        date='${TODAY}',
        format='${OUTPUT_FORMAT}'
    )
elif '${REPORT_TYPE}' == 'weekly':
    content = reporter.generate_weekly_report(week_end='${TODAY}')
elif '${REPORT_TYPE}' == 'monthly':
    content = reporter.generate_monthly_report(month='${TODAY}')
else:
    content = reporter.generate_daily_report(date='${TODAY}')

print(content)
" 2>&1)
    
    local exit_code=$?
    
    if [[ ${exit_code} -ne 0 ]]; then
        log_error "Failed to generate report: ${report_content}"
        exit 1
    fi
    
    REPORT_CONTENT="${report_content}"
    log_success "Report generated (${#REPORT_CONTENT} bytes)"
}

# Save report to file
save_report() {
    if [[ "${SAVE_REPORT}" == "false" ]]; then
        log_info "Skipping report save (--no-save specified)"
        return 0
    fi
    
    log_info "Saving report to ${REPORTS_DIR}..."
    
    local extension="${OUTPUT_FORMAT}"
    if [[ "${extension}" == "markdown" ]]; then
        extension="md"
    fi
    
    local filename="${TODAY}_${REPORT_TYPE}_report.${extension}"
    local filepath="${REPORTS_DIR}/${filename}"
    
    echo "${REPORT_CONTENT}" > "${filepath}"
    
    log_success "Report saved: ${filepath}"
}

# Send to Discord
send_discord() {
    log_info "Sending report to Discord..."
    
    # Get Discord webhook from config or environment
    local webhook_url="${DISCORD_WEBHOOK:-}"
    
    if [[ -z "${webhook_url}" ]]; then
        # Try to get from config
        webhook_url=$("${PYTHON_PATH}" -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
import yaml
try:
    with open('${CONFIG_FILE}') as f:
        config = yaml.safe_load(f)
    print(config.get('discord', {}).get('webhook', ''))
except:
    print('')
" 2>/dev/null || echo "")
    fi
    
    if [[ -z "${webhook_url}" ]]; then
        log_warn "Discord webhook not configured (set DISCORD_WEBHOOK env var or config)"
        return 0
    fi
    
    # Prepare payload
    local payload=$("${PYTHON_PATH}" -c "
import json
import sys

report = '''${REPORT_CONTENT}'''
# Truncate if too long for Discord (max 2000 chars)
if len(report) > 1900:
    report = report[:1900] + '\n\n_(truncated)_'

payload = {
    'content': report,
    'username': 'Cost Consultant',
    'avatar_url': 'https://example.com/icon.png'
}

print(json.dumps(payload))
" 2>/dev/null || echo '{"content": "Report generation failed"}')
    
    # Send to Discord
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Content-Type: application/json" \
        -X POST \
        -d "${payload}" \
        "${webhook_url}" 2>/dev/null || echo "000")
    
    if [[ "${response}" == "204" ]] || [[ "${response}" == "200" ]]; then
        log_success "Discord notification sent"
    else
        log_warn "Failed to send Discord notification (HTTP ${response})"
    fi
}

# Send to Telegram
send_telegram() {
    log_info "Sending report to Telegram..."
    
    local bot_token="${TELEGRAM_BOT_TOKEN:-}"
    local chat_id="${TELEGRAM_CHAT_ID:-}"
    
    if [[ -z "${bot_token}" ]] || [[ -z "${chat_id}" ]]; then
        log_warn "Telegram credentials not configured (set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)"
        return 0
    fi
    
    # Prepare message (Telegram max 4096 chars)
    local message=$("${PYTHON_PATH}" -c "
import sys
report = '''${REPORT_CONTENT}'''
# Escape special characters
report = report.replace('*', '\\*')
report = report.replace('_', '\\_')
report = report.replace('`', '\\`')
# Truncate if too long
if len(report) > 4000:
    report = report[:4000] + '\n\n_(truncated)_'
print(report)
" 2>/dev/null || echo "Report generation failed")
    
    # Send to Telegram
    local url="https://api.telegram.org/bot${bot_token}/sendMessage"
    local payload="{\"chat_id\": \"${chat_id}\", \"text\": \"${message}\", \"parse_mode\": \"Markdown\"}"
    
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Content-Type: application/json" \
        -X POST \
        -d "${payload}" \
        "${url}" 2>/dev/null || echo "000")
    
    if [[ "${response}" == "200" ]]; then
        log_success "Telegram notification sent"
    else
        log_warn "Failed to send Telegram notification (HTTP ${response})"
    fi
}

# Check budget alerts
check_alerts() {
    if [[ "${TEST_MODE}" == "true" ]]; then
        log_info "Skipping alerts (test mode)"
        return 0
    fi
    
    log_info "Checking budget alerts..."
    
    local alerts=$("${PYTHON_PATH}" -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
from tracker import CostTracker

tracker = CostTracker(db_path='${SCRIPT_DIR}/data/costs.db')
today = '${TODAY}'
daily_cost = tracker.get_daily_cost(today)

# Load budget config
import yaml
try:
    with open('${CONFIG_FILE}') as f:
        config = yaml.safe_load(f)
    budget = config.get('budgets', {}).get('daily', {}).get('soft_limit', 50)
except:
    budget = 50

warning = budget * 0.8
critical = budget * 0.95

alerts = []
if daily_cost >= critical:
    alerts.append(f'CRITICAL: Daily cost \${daily_cost:.2f} exceeds 95% of budget \${budget:.2f}')
elif daily_cost >= warning:
    alerts.append(f'WARNING: Daily cost \${daily_cost:.2f} exceeds 80% of budget \${budget:.2f}')

for alert in alerts:
    print(alert)
" 2>/dev/null)
    
    if [[ -n "${alerts}" ]]; then
        log_warn "Budget alerts: ${alerts}"
        
        # Send alerts to channels
        for channel in "${CHANNELS[@]:-}"; do
            case "${channel}" in
                discord) send_discord ;;
                telegram) send_telegram ;;
            esac
        done
    else
        log_success "No budget alerts"
    fi
}

# Main function
main() {
    parse_args "$@"
    
    echo ""
    log_info "=========================================="
    log_info "LLM Cost Consultant - Daily Report"
    log_info "=========================================="
    log_info "Date: ${TODAY}"
    log_info "Report Type: ${REPORT_TYPE}"
    log_info "Output Format: ${OUTPUT_FORMAT}"
    log_info "Channels: ${CHANNELS[*]:-none}"
    log_info "Test Mode: ${TEST_MODE}"
    echo ""
    
    check_dependencies
    setup_directories
    generate_report
    save_report
    
    # Send to specified channels
    if [[ ${#CHANNELS[@]} -gt 0 ]]; then
        for channel in "${CHANNELS[@]}"; do
            case "${channel}" in
                discord) send_discord ;;
                telegram) send_telegram ;;
                *)
                    log_warn "Unknown channel: ${channel}"
                    ;;
            esac
        done
    fi
    
    check_alerts
    
    echo ""
    log_success "Daily report completed!"
    echo ""
}

# Run main
main "$@"

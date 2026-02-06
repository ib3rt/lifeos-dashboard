#!/bin/bash
#
# Life OS Health Monitor
# Comprehensive system health checks for infrastructure monitoring
# Outputs: JSON (for dashboards) and human-readable (for logs)
#
# Author: The Mechanic ⚙️
# Created: $(date +%Y-%m-%d)

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
LOG_DIR="${WORKSPACE_DIR}/logs"
REPORT_FILE="${LOG_DIR}/health-report-$(date +%Y%m%d-%H%M%S).json"
HUMAN_LOG="${LOG_DIR}/health-check-$(date +%Y%m%d-%H%M%S).log"

# Thresholds
DISK_WARNING=80
DISK_CRITICAL=90
MEMORY_WARNING=80
MEMORY_CRITICAL=90
CPU_WARNING=70
CPU_CRITICAL=90
LOAD_WARNING=4.0
LOAD_CRITICAL=8.0

# Colors for terminal output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Health check results
declare -A CHECKS
declare -A MESSAGES
declare -A VALUES

# Initialize JSON structure
json_output='{
  "timestamp": "'$(date -Iseconds)'",
  "hostname": "'$(hostname)'",
  "checks": {},
  "summary": {
    "total": 0,
    "healthy": 0,
    "warning": 0,
    "critical": 0
  },
  "overall_status": "unknown"
}'

#######################################
# Utility Functions
#######################################

log() {
    local level="$1"
    local message="$2"
    local color="$NC"
    
    case "$level" in
        "ERROR") color="$RED" ;;
        "WARN") color="$YELLOW" ;;
        "OK") color="$GREEN" ;;
        "INFO") color="$BLUE" ;;
    esac
    
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message${NC}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$HUMAN_LOG"
}

json_set() {
    local key="$1"
    local value="$2"
    json_output=$(echo "$json_output" | jq --arg key "$key" --arg value "$value" '.checks[$key] = ($value | fromjson)')
}

update_summary() {
    local status="$1"
    json_output=$(echo "$json_output" | jq --arg status "$status" '
        .summary.total += 1 |
        if $status == "healthy" then .summary.healthy += 1
        elif $status == "warning" then .summary.warning += 1
        elif $status == "critical" then .summary.critical += 1
        else . end
    ')
}

determine_overall_status() {
    local critical=$(echo "$json_output" | jq -r '.summary.critical')
    local warning=$(echo "$json_output" | jq -r '.summary.warning')
    
    if [ "$critical" -gt 0 ]; then
        json_output=$(echo "$json_output" | jq '.overall_status = "critical"')
    elif [ "$warning" -gt 0 ]; then
        json_output=$(echo "$json_output" | jq '.overall_status = "warning"')
    else
        json_output=$(echo "$json_output" | jq '.overall_status = "healthy"')
    fi
}

#######################################
# Health Check Functions
#######################################

check_disk_space() {
    log "INFO" "Checking disk space..."
    
    local status="healthy"
    local message="All filesystems healthy"
    local details="[]"
    local max_usage=0
    
    # Get disk usage for all mounted filesystems
    while read -r filesystem size used avail percent mount; do
        [[ "$filesystem" == "Filesystem" ]] && continue
        
        local usage_num=$(echo "$percent" | tr -d '%')
        local fs_status="healthy"
        
        if [ "$usage_num" -ge "$DISK_CRITICAL" ]; then
            fs_status="critical"
            status="critical"
            message="CRITICAL: $mount is ${percent} full"
        elif [ "$usage_num" -ge "$DISK_WARNING" ]; then
            fs_status="warning"
            [ "$status" == "healthy" ] && status="warning"
            [ "$status" != "critical" ] && message="WARNING: $mount is ${percent} full"
        fi
        
        [ "$usage_num" -gt "$max_usage" ] && max_usage=$usage_num
        
        details=$(echo "$details" | jq --arg fs "$filesystem" --arg mount "$mount" --arg size "$size" \
            --arg used "$used" --arg avail "$avail" --arg percent "$percent" --arg st "$fs_status" \
            '. += [{"filesystem": $fs, "mount": $mount, "size": $size, "used": $used, "available": $avail, "percent": $percent, "status": $st}]')
    done < <(df -h | grep -E '^/dev/')
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"max_usage_percent\": $max_usage, \"filesystems\": $details}"
    json_set "disk_space" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "Disk space: All filesystems below ${DISK_WARNING}% usage" ;;
        "warning") log "WARN" "$message" ;;
        "critical") log "ERROR" "$message" ;;
    esac
}

check_memory() {
    log "INFO" "Checking memory..."
    
    local status="healthy"
    local message="Memory usage normal"
    
    # Get memory info
    local mem_total=$(free | grep Mem | awk '{print $2}')
    local mem_used=$(free | grep Mem | awk '{print $3}')
    local mem_available=$(free | grep Mem | awk '{print $7}')
    local mem_percent=$(awk "BEGIN {printf \"%.1f\", ($mem_used / $mem_total) * 100}")
    
    if (( $(echo "$mem_percent >= $MEMORY_CRITICAL" | bc -l) )); then
        status="critical"
        message="CRITICAL: Memory usage at ${mem_percent}%"
    elif (( $(echo "$mem_percent >= $MEMORY_WARNING" | bc -l) )); then
        status="warning"
        message="WARNING: Memory usage at ${mem_percent}%"
    fi
    
    # Get swap info
    local swap_total=$(free | grep Swap | awk '{print $2}')
    local swap_used=$(free | grep Swap | awk '{print $3}')
    local swap_percent=0
    [ "$swap_total" -gt 0 ] && swap_percent=$(awk "BEGIN {printf \"%.1f\", ($swap_used / $swap_total) * 100}")
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"total_mb\": $((mem_total/1024)), \"used_mb\": $((mem_used/1024)), \"available_mb\": $((mem_available/1024)), \"usage_percent\": $mem_percent, \"swap_total_mb\": $((swap_total/1024)), \"swap_used_mb\": $((swap_used/1024)), \"swap_percent\": $swap_percent}"
    json_set "memory" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "Memory: ${mem_percent}% used ($((mem_used/1024))MB / $((mem_total/1024))MB)" ;;
        "warning") log "WARN" "$message" ;;
        "critical") log "ERROR" "$message" ;;
    esac
}

check_cpu() {
    log "INFO" "Checking CPU..."
    
    local status="healthy"
    local message="CPU usage normal"
    
    # Get CPU usage (average over 1 second)
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    [ -z "$cpu_usage" ] && cpu_usage=$(awk '{u=$2+$4; t=$2+$4+$5; if (t==0) print 0; else print 100*u/t}' <(grep 'cpu ' /proc/stat) <(sleep 1; grep 'cpu ' /proc/stat))
    
    local cpu_percent=$(echo "$cpu_usage" | awk '{printf "%.1f", $1}')
    
    # Get load average
    local load_1min=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ',')
    local cpu_cores=$(nproc)
    local load_percent=$(awk "BEGIN {printf \"%.1f\", ($load_1min / $cpu_cores) * 100}")
    
    if (( $(echo "$cpu_percent >= $CPU_CRITICAL" | bc -l) )) || (( $(echo "$load_percent >= 100" | bc -l) )); then
        status="critical"
        message="CRITICAL: CPU usage at ${cpu_percent}% (load: $load_1min)"
    elif (( $(echo "$cpu_percent >= $CPU_WARNING" | bc -l) )) || (( $(echo "$load_percent >= 80" | bc -l) )); then
        status="warning"
        message="WARNING: CPU usage at ${cpu_percent}% (load: $load_1min)"
    fi
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"usage_percent\": $cpu_percent, \"load_1min\": $load_1min, \"load_5min\": $(uptime | awk -F'load average:' '{print $2}' | awk '{print $2}' | tr -d ','), \"load_15min\": $(uptime | awk -F'load average:' '{print $2}' | awk '{print $3}' | tr -d ','), \"cores\": $cpu_cores}"
    json_set "cpu" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "CPU: ${cpu_percent}% usage, load: $load_1min ($cpu_cores cores)" ;;
        "warning") log "WARN" "$message" ;;
        "critical") log "ERROR" "$message" ;;
    esac
}

check_service() {
    local service_name="$1"
    local check_pattern="$2"
    local log_label="${3:-$service_name}"
    
    log "INFO" "Checking $log_label..."
    
    local status="healthy"
    local message="$log_label is running"
    local details="{}"
    
    if pgrep -f "$check_pattern" > /dev/null 2>&1; then
        status="healthy"
    else
        status="critical"
        message="CRITICAL: $log_label is not running"
    fi
    
    # Get process details if running
    if [ "$status" == "healthy" ]; then
        case "$service_name" in
            "docker")
                local pid=$(pgrep -x 'dockerd' | head -1)
                local version="unknown"
                local containers=0
                if command -v docker &> /dev/null; then
                    version=$(docker --version 2>/dev/null | awk '{print $3}' | tr -d ',')
                    containers=$(docker ps -q 2>/dev/null | wc -l)
                fi
                details="{\"pid\": \"$pid\", \"version\": \"$version\", \"running_containers\": $containers}"
                message="$log_label is running (PID: $pid, $containers containers)"
                ;;
            "n8n")
                local port=$(netstat -tlnp 2>/dev/null | grep ":5678" | head -1 | awk '{print $4}' | cut -d: -f2)
                local pid=$(pgrep -f "n8n" | head -1)
                [ -n "$pid" ] && local mem=$(ps -p "$pid" -o rss= 2>/dev/null | awk '{print int($1/1024)}') || local mem=0
                details="{\"port\": ${port:-5678}, \"pid\": \"${pid:-null}\", \"memory_mb\": $mem}"
                ;;
            "discord_bot")
                local count=$(pgrep -f "discord.*bridge" | wc -l)
                details="{\"instances\": $count}"
                message="$log_label is running ($count instances)"
                ;;
        esac
    fi
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"details\": $details}"
    json_set "${service_name}" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "$message" ;;
        "critical") log "ERROR" "$message" ;;
    esac
}

check_docker() {
    check_service "docker" "pgrep -x 'dockerd' > /dev/null" "Docker daemon"
}

check_n8n() {
    check_service "n8n" "pgrep -f 'n8n' > /dev/null" "n8n workflow engine"
}

check_discord_bot() {
    check_service "discord_bot" "pgrep -f 'discord.*bridge' > /dev/null" "Discord bridge bot"
}

check_network() {
    log "INFO" "Checking network connectivity..."
    
    local status="healthy"
    local message="Network connectivity OK"
    local failed=0
    local total=0
    local details="[]"
    
    # Test connectivity to key endpoints
    local endpoints=(
        "8.8.8.8:Google_DNS"
        "1.1.1.1:Cloudflare_DNS"
        "google.com:Google_HTTP"
        "github.com:GitHub"
        "api.telegram.org:Telegram_API"
        "discord.com:Discord_API"
    )
    
    for endpoint in "${endpoints[@]}"; do
        IFS=':' read -r host name <<< "$endpoint"
        total=$((total + 1))
        
        local latency="null"
        local reachable=false
        
        if ping -c 1 -W 3 "$host" > /dev/null 2>&1; then
            reachable=true
            latency=$(ping -c 1 -W 3 "$host" 2>/dev/null | grep 'time=' | awk -F'time=' '{print $2}' | awk '{print $1}')
        else
            failed=$((failed + 1))
        fi
        
        details=$(echo "$details" | jq --arg name "$name" --arg host "$host" --argjson reachable "$reachable" --argjson latency "$latency" \
            '. += [{"name": $name, "host": $host, "reachable": $reachable, "latency_ms": $latency}]')
    done
    
    # Check if critical endpoints are down
    local critical_down=$(echo "$details" | jq '[.[] | select(.name == "Google_DNS" or .name == "Cloudflare_DNS") | select(.reachable == false)] | length')
    
    if [ "$critical_down" -ge 2 ]; then
        status="critical"
        message="CRITICAL: No internet connectivity"
    elif [ "$failed" -ge 3 ]; then
        status="warning"
        message="WARNING: $failed/$total network endpoints unreachable"
    elif [ "$failed" -gt 0 ]; then
        status="warning"
        message="WARNING: $failed/$total network endpoints unreachable"
    fi
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"total_tested\": $total, \"failed\": $failed, \"endpoints\": $details}"
    json_set "network" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "Network: All $total endpoints reachable" ;;
        "warning") log "WARN" "$message" ;;
        "critical") log "ERROR" "$message" ;;
    esac
}

check_git_status() {
    log "INFO" "Checking Git repository status..."
    
    local status="healthy"
    local message="Git repository clean"
    local details="{}"
    
    cd "$WORKSPACE_DIR" || return
    
    # Check if it's a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        status="critical"
        message="CRITICAL: Not a git repository"
        details="{\"is_git_repo\": false}"
    else
        # Fetch latest to check if behind
        git fetch origin --quiet 2>/dev/null || true
        
        local branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        local commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
        local uncommitted=$(git status --porcelain 2>/dev/null | wc -l)
        local ahead=$(git rev-list --count HEAD..@{upstream} 2>/dev/null || echo 0)
        local behind=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo 0)
        local last_commit_date=$(git log -1 --format=%ci 2>/dev/null || echo "unknown")
        
        details="{\"branch\": \"$branch\", \"commit\": \"$commit\", \"uncommitted_changes\": $uncommitted, \"commits_ahead\": $ahead, \"commits_behind\": $behind, \"last_commit\": \"$last_commit_date\"}"
        
        if [ "$uncommitted" -gt 0 ]; then
            status="warning"
            message="WARNING: $uncommitted uncommitted changes"
        fi
        
        if [ "$behind" -gt 0 ]; then
            [ "$status" == "healthy" ] && status="warning"
            message="WARNING: $behind commits behind origin/$branch"
        fi
        
        if [ "$ahead" -gt 0 ]; then
            [ "$status" == "healthy" ] && status="warning"
            message="${message}, $ahead commits ahead"
        fi
    fi
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"details\": $details}"
    json_set "git" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "Git: On $branch, clean working tree" ;;
        "warning") log "WARN" "$message" ;;
        "critical") log "ERROR" "$message" ;;
    esac
}

check_openclaw_gateway() {
    log "INFO" "Checking OpenClaw Gateway..."
    
    local status="healthy"
    local message="OpenClaw Gateway is running"
    local details="{}"
    
    # Check if gateway process is running
    if pgrep -f "openclaw.*gateway" > /dev/null 2>&1 || curl -s http://localhost:18789/status > /dev/null 2>&1; then
        local response=$(curl -s http://localhost:18789/status 2>/dev/null || echo '{}')
        local version=$(echo "$response" | jq -r '.version // "unknown"' 2>/dev/null || echo "unknown")
        details="{\"endpoint\": \"localhost:18789\", \"version\": \"$version\"}"
    else
        status="warning"
        message="WARNING: OpenClaw Gateway not detected on localhost:18789"
        details="{\"endpoint\": \"localhost:18789\", \"reachable\": false}"
    fi
    
    local json="{\"status\": \"$status\", \"message\": \"$message\", \"details\": $details}"
    json_set "openclaw_gateway" "$json"
    update_summary "$status"
    
    case "$status" in
        "healthy") log "OK" "$message" ;;
        "warning") log "WARN" "$message" ;;
    esac
}

#######################################
# Main Execution
#######################################

main() {
    # Ensure log directory exists
    mkdir -p "$LOG_DIR"
    
    # Header
    log "INFO" "=========================================="
    log "INFO" "Life OS Health Check Started"
    log "INFO" "Host: $(hostname)"
    log "INFO" "Time: $(date -Iseconds)"
    log "INFO" "=========================================="
    
    # Run all checks
    check_disk_space
    check_memory
    check_cpu
    check_docker
    check_n8n
    check_discord_bot
    check_network
    check_git_status
    check_openclaw_gateway
    
    # Determine overall status
    determine_overall_status
    
    # Save JSON report
    echo "$json_output" | jq '.' > "$REPORT_FILE"
    
    # Also save latest symlink
    ln -sf "$REPORT_FILE" "${LOG_DIR}/health-report-latest.json"
    ln -sf "$HUMAN_LOG" "${LOG_DIR}/health-check-latest.log"
    
    # Final summary
    local overall=$(echo "$json_output" | jq -r '.overall_status')
    local total=$(echo "$json_output" | jq -r '.summary.total')
    local healthy=$(echo "$json_output" | jq -r '.summary.healthy')
    local warning=$(echo "$json_output" | jq -r '.summary.warning')
    local critical=$(echo "$json_output" | jq -r '.summary.critical')
    
    log "INFO" "=========================================="
    log "INFO" "Health Check Complete"
    log "INFO" "Overall Status: $overall"
    log "INFO" "Total: $total | Healthy: $healthy | Warning: $warning | Critical: $critical"
    log "INFO" "JSON Report: $REPORT_FILE"
    log "INFO" "Human Log: $HUMAN_LOG"
    log "INFO" "=========================================="
    
    # Output final status for scripts
    echo "$json_output"
    
    # Return exit code based on status
    case "$overall" in
        "critical") exit 2 ;;
        "warning") exit 1 ;;
        *) exit 0 ;;
    esac
}

# Handle command line arguments
case "${1:-}" in
    --json|-j)
        main > /dev/null 2>&1
        cat "$REPORT_FILE"
        ;;
    --quiet|-q)
        main > /dev/null 2>&1
        ;;
    --help|-h)
        cat << 'EOF'
Life OS Health Monitor

Usage: $0 [OPTIONS]

Options:
    --json, -j      Output JSON only to stdout
    --quiet, -q     Run silently, only save to files
    --help, -h      Show this help message

Exit Codes:
    0   All checks passed (healthy)
    1   Some warnings detected
    2   Critical issues found

Reports are saved to:
    ${LOG_DIR}/health-report-YYYYMMDD-HHMMSS.json
    ${LOG_DIR}/health-check-YYYYMMDD-HHMMSS.log

Latest reports are symlinked:
    ${LOG_DIR}/health-report-latest.json
    ${LOG_DIR}/health-check-latest.log
EOF
        ;;
    *)
        main
        ;;
esac

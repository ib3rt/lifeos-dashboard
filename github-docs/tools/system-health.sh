#!/bin/bash
#
# System Health Monitor - Monitor OpenClaw Infrastructure
# Check disk, memory, gateway, and cron health
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Configuration
WORKSPACE="${OPENCLAW_WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
DISK_WARN_THRESHOLD=80
DISK_CRIT_THRESHOLD=90
MEM_WARN_THRESHOLD=80
MEM_CRIT_THRESHOLD=95

# Print helpers
print_header() {
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  $1"
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
}

print_section() {
    echo ""
    echo -e "${MAGENTA}${BOLD}▸ $1${NC}"
    echo -e "${MAGENTA}$(printf '%*s' "${#1}" '' | tr ' ' '-')${NC}"
}

print_ok() { echo -e "${GREEN}✓${NC} $1"; }
print_warn() { echo -e "${YELLOW}⚠ WARNING:${NC} $1"; }
print_crit() { echo -e "${RED}✗ CRITICAL:${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_metric() {
    local label="$1"
    local value="$2"
    local status="${3:-ok}"
    local icon=""
    
    case "$status" in
        ok) icon="${GREEN}●${NC}" ;;
        warn) icon="${YELLOW}●${NC}" ;;
        crit) icon="${RED}●${NC}" ;;
        *) icon="${BLUE}●${NC}" ;;
    esac
    
    printf "  %-25s %s %s\n" "$label:" "$icon" "$value"
}

# Show help
show_help() {
    cat << EOF
${BOLD}System Health Monitor${NC} - Check OpenClaw Infrastructure

${BOLD}USAGE:${NC}
    system-health.sh [options]

${BOLD}OPTIONS:${NC}
    -h, --help          Show this help message
    -q, --quick         Quick check (skip detailed info)
    -w, --watch         Continuous monitoring (30s interval)

${BOLD}CHECKS:${NC}
    ✓ Disk usage check      - Filesystem utilization
    ✓ Memory usage          - RAM and swap usage
    ✓ Gateway process       - OpenClaw gateway status
    ✓ Cron execution        - Last cron job run time

${BOLD}THRESHOLDS:${NC}
    Disk:  ${YELLOW}$DISK_WARN_THRESHOLD%${NC} warning, ${RED}$DISK_CRIT_THRESHOLD%${NC} critical
    Memory: ${YELLOW}$MEM_WARN_THRESHOLD%${NC} warning, ${RED}$MEM_CRIT_THRESHOLD%${NC} critical

${BOLD}EXAMPLES:${NC}
    ./system-health.sh
    ./system-health.sh --quick
    ./system-health.sh --watch

EOF
}

# Disk usage check
check_disk() {
    print_section "Disk Usage"
    
    local has_issue=0
    
    # Get filesystem info (exclude tmpfs, devtmpfs, etc)
    df -h -x tmpfs -x devtmpfs -x overlay 2>/dev/null | tail -n +2 | while read fs size used avail percent mount; do
        # Extract numeric percentage
        local pct=$(echo "$percent" | tr -d '%')
        local status="ok"
        
        if [[ $pct -ge $DISK_CRIT_THRESHOLD ]]; then
            status="crit"
            has_issue=1
        elif [[ $pct -ge $DISK_WARN_THRESHOLD ]]; then
            status="warn"
            has_issue=1
        fi
        
        print_metric "$mount" "$used / $size ($percent)" "$status"
        
        # Additional info for critical
        if [[ $status == "crit" ]]; then
            print_crit "Low disk space on $mount ($percent used)"
        elif [[ $status == "warn" ]]; then
            print_warn "Disk usage high on $mount ($percent used)"
        fi
    done
    
    # Check workspace specifically
    if [[ -d "$WORKSPACE" ]]; then
        local ws_usage=$(du -sh "$WORKSPACE" 2>/dev/null | cut -f1)
        print_info "Workspace size: $ws_usage"
    fi
    
    return $has_issue
}

# Memory usage check
check_memory() {
    print_section "Memory Usage"
    
    # Get memory info from /proc/meminfo
    if [[ -f /proc/meminfo ]]; then
        local total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        local available=$(grep MemAvailable /proc/meminfo 2>/dev/null | awk '{print $2}')
        local free=$(grep MemFree /proc/meminfo | awk '{print $2}')
        local buffers=$(grep Buffers /proc/meminfo | awk '{print $2}')
        local cached=$(grep "^Cached:" /proc/meminfo | awk '{print $2}')
        
        # If MemAvailable not present, estimate
        if [[ -z "$available" ]]; then
            available=$((free + buffers + cached))
        fi
        
        local used=$((total - available))
        local pct=$((used * 100 / total))
        
        local status="ok"
        if [[ $pct -ge $MEM_CRIT_THRESHOLD ]]; then
            status="crit"
        elif [[ $pct -ge $MEM_WARN_THRESHOLD ]]; then
            status="warn"
        fi
        
        # Convert to human-readable
        local total_gb=$((total / 1024 / 1024))
        local used_gb=$((used / 1024 / 1024))
        local avail_gb=$((available / 1024 / 1024))
        
        print_metric "RAM Used" "${used_gb}GB / ${total_gb}GB (${pct}%)" "$status"
        print_metric "RAM Available" "${avail_gb}GB" "ok"
        
        if [[ $status == "crit" ]]; then
            print_crit "Memory usage critical (${pct}%)"
        elif [[ $status == "warn" ]]; then
            print_warn "Memory usage high (${pct}%)"
        fi
    fi
    
    # Swap info
    local swap_total=$(grep SwapTotal /proc/meminfo | awk '{print $2}')
    if [[ $swap_total -gt 0 ]]; then
        local swap_free=$(grep SwapFree /proc/meminfo | awk '{print $2}')
        local swap_used=$((swap_total - swap_free))
        local swap_pct=$((swap_used * 100 / swap_total))
        
        local swap_status="ok"
        [[ $swap_pct -gt 50 ]] && swap_status="warn"
        [[ $swap_pct -gt 80 ]] && swap_status="crit"
        
        local swap_used_mb=$((swap_used / 1024))
        local swap_total_mb=$((swap_total / 1024))
        
        print_metric "Swap Used" "${swap_used_mb}MB / ${swap_total_mb}MB (${swap_pct}%)" "$swap_status"
    else
        print_info "Swap: Disabled"
    fi
    
    # Top memory consumers
    if command -v ps &> /dev/null; then
        echo ""
        print_info "Top memory consumers:"
        ps aux --sort=-%mem 2>/dev/null | head -4 | tail -3 | while read user pid cpu mem vsz rss tty stat start time cmd; do
            printf "  %-20s %s%%\n" "$(echo "$cmd" | cut -c1-20)" "$mem"
        done || true
    fi
}

# Gateway process check
check_gateway() {
    print_section "OpenClaw Gateway"
    
    local gateway_ok=1
    
    # Check if gateway process is running
    if pgrep -f "openclaw.*gateway" > /dev/null 2>&1; then
        local pid=$(pgrep -f "openclaw.*gateway" | head -1)
        print_ok "Gateway process running (PID: $pid)"
        
        # Get process info
        if [[ -f "/proc/$pid/status" ]]; then
            local threads=$(grep Threads /proc/$pid/status | awk '{print $2}')
            print_metric "Threads" "$threads" "ok"
        fi
        
        # Check CPU/memory usage
        if command -v ps &> /dev/null; then
            local cpu_mem=$(ps -p $pid -o %cpu,%mem --no-headers 2>/dev/null || echo "N/A")
            print_metric "CPU/Memory" "$cpu_mem" "ok"
        fi
        
        # Check uptime
        if [[ -f "/proc/$pid/stat" ]]; then
            local start_time=$(awk '{print $22}' /proc/$pid/stat)
            local uptime=$(awk '{print $1}' /proc/uptime)
            local clk_tck=$(getconf CLK_TCK)
            local proc_uptime=$(echo "scale=2; ($uptime - ($start_time / $clk_tck)) / 3600" | bc 2>/dev/null || echo "?")
            print_metric "Uptime" "${proc_uptime} hours" "ok"
        fi
        
        gateway_ok=0
    else
        print_crit "Gateway process NOT RUNNING"
    fi
    
    # Check port
    local port_status="crit"
    if netstat -tuln 2>/dev/null | grep -q ":18789"; then
        port_status="ok"
    elif ss -tuln 2>/dev/null | grep -q ":18789"; then
        port_status="ok"
    fi
    
    if [[ $port_status == "ok" ]]; then
        print_ok "Port 18789: LISTENING"
    else
        print_crit "Port 18789: NOT LISTENING"
    fi
    
    # Check openclaw command
    if command -v openclaw &> /dev/null; then
        print_ok "openclaw CLI: Available"
    else
        print_warn "openclaw CLI: Not in PATH"
    fi
    
    return $gateway_ok
}

# Cron execution check
check_cron() {
    print_section "Cron / Scheduled Tasks"
    
    # Check for cron daemon
    if pgrep -x "cron" > /dev/null 2>&1 || pgrep -x "crond" > /dev/null 2>&1; then
        print_ok "Cron daemon: Running"
    else
        print_warn "Cron daemon: Not detected"
    fi
    
    # Check for OpenClaw cron jobs
    local has_cron=0
    
    if command -v crontab &> /dev/null; then
        if crontab -l 2>/dev/null | grep -q "openclaw\|$WORKSPACE"; then
            has_cron=1
            print_ok "OpenClaw cron jobs: Found"
            crontab -l 2>/dev/null | grep "openclaw\|$WORKSPACE" | while read line; do
                echo "  ${BLUE}|${NC} $line"
            done
        fi
    fi
    
    # Check for systemd timers
    if command -v systemctl &> /dev/null; then
        if systemctl list-timers --all 2>/dev/null | grep -q "openclaw"; then
            has_cron=1
            print_ok "OpenClaw systemd timers: Found"
        fi
    fi
    
    if [[ $has_cron -eq 0 ]]; then
        print_info "No OpenClaw cron jobs found"
    fi
    
    # Check last execution markers
    local marker_dir="$WORKSPACE/.cron"
    if [[ -d "$marker_dir" ]]; then
        echo ""
        print_info "Last cron executions:"
        for marker in "$marker_dir"/*; do
            [[ -f "$marker" ]] || continue
            local name=$(basename "$marker")
            local last_run=$(stat -c "%y" "$marker" 2>/dev/null | cut -d'.' -f1)
            local age_hours=$(( ($(date +%s) - $(stat -c %Y "$marker")) / 3600 ))
            
            local status="ok"
            [[ $age_hours -gt 24 ]] && status="warn"
            [[ $age_hours -gt 48 ]] && status="crit"
            
            print_metric "$name" "$last_run (${age_hours}h ago)" "$status"
        done
    else
        print_info "No cron execution markers found"
    fi
    
    # Recent cron logs (if accessible)
    if [[ -f /var/log/syslog ]]; then
        local recent_cron=$(grep -i "cron" /var/log/syslog 2>/dev/null | tail -3 || true)
        if [[ -n "$recent_cron" ]]; then
            echo ""
            print_info "Recent cron activity:"
            echo "$recent_cron" | while read line; do
                echo "  ${BLUE}|${NC} $(echo "$line" | cut -d' ' -f1-5)"
            done
        fi
    fi
}

# Additional checks
check_extra() {
    print_section "Additional Checks"
    
    # Workspace permissions
    if [[ -d "$WORKSPACE" ]]; then
        if [[ -r "$WORKSPACE" && -w "$WORKSPACE" ]]; then
            print_ok "Workspace permissions: OK"
        else
            print_warn "Workspace permissions: Limited"
        fi
    fi
    
    # Disk IO (if iostat available)
    if command -v iostat &> /dev/null; then
        local io=$(iostat -x 1 1 2>/dev/null | tail -n +4 | head -1 || true)
        [[ -n "$io" ]] && print_info "Disk IO: $(echo "$io" | awk '{print $NF}')% util"
    fi
    
    # Load average
    local load=$(uptime 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -3 || true)
    if [[ -n "$load" ]]; then
        local load1=$(echo "$load" | head -1)
        local cpus=$(nproc 2>/dev/null || echo 1)
        local load_pct=$(echo "scale=0; ($load1 / $cpus) * 100" | bc 2>/dev/null || echo "0")
        
        local status="ok"
        [[ $load_pct -gt 70 ]] && status="warn"
        [[ $load_pct -gt 90 ]] && status="crit"
        
        print_metric "Load Average" "$load" "$status"
    fi
    
    # Network connectivity
    if ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
        print_ok "Network: Connected"
    else
        print_warn "Network: No external connectivity"
    fi
}

# Run all checks
run_checks() {
    local quick_mode="${1:-}"
    
    print_header "OpenClaw System Health Report"
    print_info "Host: $(hostname)"
    print_info "Time: $(date)"
    print_info "Workspace: $WORKSPACE"
    
    local exit_code=0
    
    check_disk || exit_code=1
    check_memory || exit_code=1
    check_gateway || exit_code=1
    check_cron
    
    if [[ "$quick_mode" != "true" ]]; then
        check_extra
    fi
    
    echo ""
    print_header "Health Check Complete"
    
    if [[ $exit_code -eq 0 ]]; then
        print_ok "All critical checks passed"
    else
        print_crit "Some checks failed - review above"
    fi
    
    return $exit_code
}

# Main dispatcher
main() {
    local mode="normal"
    
    case "${1:-}" in
        -h|--help|help)
            show_help
            exit 0
            ;;
        -q|--quick)
            mode="quick"
            run_checks "true"
            exit $?
            ;;
        -w|--watch)
            print_info "Starting continuous monitoring (Ctrl+C to stop)"
            while true; do
                clear
                run_checks "true"
                echo ""
                print_info "Refreshing in 30 seconds..."
                sleep 30
            done
            ;;
        "")
            run_checks
            exit $?
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"

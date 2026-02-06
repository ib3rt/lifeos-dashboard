#!/bin/bash
# Life OS System Monitor
# Proactive health checks and alerts

LOG_FILE="$HOME/.openclaw/workspace/logs/system-monitor.log"
ALERT_FILE="$HOME/.openclaw/workspace/logs/alerts.log"
mkdir -p "$(dirname $LOG_FILE)"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

alert() {
    local level=$1
    local message=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$ALERT_FILE"
    
    # Could integrate with Telegram bot here
    # curl -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" ...
}

# Check disk usage
check_disk() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$usage" -gt 90 ]; then
        alert "CRITICAL" "Disk usage at ${usage}%"
    elif [ "$usage" -gt 80 ]; then
        alert "WARNING" "Disk usage at ${usage}%"
    else
        log "Disk: ${usage}% OK"
    fi
}

# Check memory
check_memory() {
    local mem_info=$(free | grep Mem)
    local total=$(echo $mem_info | awk '{print $2}')
    local used=$(echo $mem_info | awk '{print $3}')
    local usage=$((used * 100 / total))
    
    if [ "$usage" -gt 90 ]; then
        alert "CRITICAL" "Memory usage at ${usage}%"
    elif [ "$usage" -gt 80 ]; then
        alert "WARNING" "Memory usage at ${usage}%"
    else
        log "Memory: ${usage}% OK"
    fi
}

# Check OpenClaw processes
check_openclaw() {
    local count=$(pgrep -c openclaw 2>/dev/null || echo 0)
    if [ "$count" -eq 0 ]; then
        alert "CRITICAL" "OpenClaw not running!"
    else
        log "OpenClaw: $count processes OK"
    fi
}

# Check bot status
check_bots() {
    if [ -f "$HOME/.openclaw/workspace/bot-tokens.txt" ]; then
        while IFS='=' read -r name token; do
            local response=$(curl -s "https://api.telegram.org/bot$token/getMe" 2>/dev/null)
            if echo "$response" | grep -q '"ok":true'; then
                log "Bot $name: OK"
            else
                alert "WARNING" "Bot $name not responding"
            fi
        done < "$HOME/.openclaw/workspace/bot-tokens.txt"
    fi
}

# Check for stuck operations
check_stuck_ops() {
    local stuck=$(find ~/.openclaw/workspace -name "*.tmp" -mmin +60 2>/dev/null | wc -l)
    if [ "$stuck" -gt 0 ]; then
        alert "WARNING" "$stuck stuck temporary files detected"
    fi
}

# Check git sync status
check_git() {
    cd "$HOME/.openclaw/workspace" 2>/dev/null || return
    
    if [ -d .git ]; then
        local unpushed=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l)
        if [ "$unpushed" -gt 5 ]; then
            alert "INFO" "$unpushed unpushed commits"
        fi
    fi
}

# Main
log "=== System Monitor Check ==="
check_disk
check_memory
check_openclaw
check_bots
check_stuck_ops
check_git
log "=== Check Complete ==="

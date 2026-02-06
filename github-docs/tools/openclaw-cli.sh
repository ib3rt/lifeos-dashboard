#!/bin/bash
#
# OpenClaw CLI Toolkit - Main Entry Script
# Your command center for managing OpenClaw
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
WORKSPACE="${OPENCLAW_WORKSPACE:-/home/ubuntu/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
AGENTS_DIR="$WORKSPACE/agents"
GATEWAY_LOG="${OPENCLAW_LOG:-/var/log/openclaw/gateway.log}"

# Helper functions
print_header() {
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  $1"
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Show help
show_help() {
    cat << EOF
${BOLD}OpenClaw CLI Toolkit${NC} - Manage your Life OS

${BOLD}USAGE:${NC}
    openclaw-cli.sh <command> [options]

${BOLD}COMMANDS:${NC}
    status              Show OpenClaw gateway status, session count, recent errors
    logs [lines]        Tail gateway logs (default: 50 lines)
    restart             Restart the gateway service
    agents              List all agents with their status
    memory search <q>   Search MEMORY.md for specific content
    session list        Show recent sessions

${BOLD}OPTIONS:${NC}
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output

${BOLD}EXAMPLES:${NC}
    ./openclaw-cli.sh status
    ./openclaw-cli.sh logs 100
    ./openclaw-cli.sh memory search "backup"
    ./openclaw-cli.sh agents

${BOLD}ENVIRONMENT:${NC}
    OPENCLAW_WORKSPACE  Path to workspace (default: /home/ubuntu/.openclaw/workspace)
    OPENCLAW_LOG        Path to gateway log file

EOF
}

# Get gateway status
cmd_status() {
    print_header "OpenClaw Gateway Status"
    
    # Check if gateway is running
    if pgrep -f "openclaw.*gateway" > /dev/null 2>&1; then
        print_success "Gateway process: RUNNING"
        local pid=$(pgrep -f "openclaw.*gateway" | head -1)
        print_info "PID: $pid"
    else
        print_error "Gateway process: NOT RUNNING"
    fi
    
    # Check port
    if netstat -tuln 2>/dev/null | grep -q ":18789"; then
        print_success "Gateway port (18789): LISTENING"
    elif ss -tuln 2>/dev/null | grep -q ":18789"; then
        print_success "Gateway port (18789): LISTENING"
    else
        print_warning "Gateway port (18789): NOT LISTENING"
    fi
    
    # Session count (approximate from processes)
    local session_count=$(pgrep -c "openclaw" 2>/dev/null || echo "0")
    print_info "Active processes: $session_count"
    
    # Recent errors from log
    if [[ -f "$GATEWAY_LOG" ]]; then
        local errors=$(grep -i "error\|fatal\|panic" "$GATEWAY_LOG" 2>/dev/null | tail -5 || true)
        if [[ -n "$errors" ]]; then
            echo ""
            print_warning "Recent errors:"
            echo "$errors" | while read line; do
                echo -e "  ${RED}$line${NC}"
            done
        else
            print_success "No recent errors in log"
        fi
    else
        print_warning "Gateway log not found: $GATEWAY_LOG"
    fi
    
    # Config status
    if [[ -f "$WORKSPACE/../openclaw.json" ]]; then
        print_success "Configuration: FOUND"
    else
        print_warning "Configuration: NOT FOUND"
    fi
}

# Tail gateway logs
cmd_logs() {
    local lines="${1:-50}"
    print_header "Gateway Logs (last $lines lines)"
    
    if [[ -f "$GATEWAY_LOG" ]]; then
        tail -n "$lines" "$GATEWAY_LOG" 2>/dev/null || {
            print_error "Cannot read log file: $GATEWAY_LOG"
            return 1
        }
    else
        # Try to find log file
        local alt_log="$WORKSPACE/../gateway.log"
        if [[ -f "$alt_log" ]]; then
            tail -n "$lines" "$alt_log" 2>/dev/null
        else
            print_error "Log file not found. Tried:"
            print_info "  $GATEWAY_LOG"
            print_info "  $alt_log"
            print_info "Set OPENCLAW_LOG environment variable to specify log location"
        fi
    fi
}

# Restart gateway
cmd_restart() {
    print_header "Restarting Gateway"
    
    if ! command -v openclaw &> /dev/null; then
        print_error "openclaw command not found in PATH"
        return 1
    fi
    
    print_info "Stopping gateway..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
    
    print_info "Starting gateway..."
    if openclaw gateway start; then
        sleep 1
        if pgrep -f "openclaw.*gateway" > /dev/null; then
            print_success "Gateway restarted successfully"
        else
            print_error "Gateway failed to start"
            return 1
        fi
    else
        print_error "Failed to restart gateway"
        return 1
    fi
}

# List agents
cmd_agents() {
    print_header "OpenClaw Agents"
    
    if [[ ! -d "$AGENTS_DIR" ]]; then
        print_error "Agents directory not found: $AGENTS_DIR"
        return 1
    fi
    
    local agent_count=0
    
    for agent_dir in "$AGENTS_DIR"/*/; do
        [[ -d "$agent_dir" ]] || continue
        
        local agent_name=$(basename "$agent_dir")
        local readme="$agent_dir/README.md"
        local status_file="$agent_dir/.status"
        local last_output=$(find "$agent_dir" -type f -mtime -1 2>/dev/null | wc -l)
        
        agent_count=$((agent_count + 1))
        
        echo ""
        echo -e "${BOLD}${CYAN}▸ $agent_name${NC}"
        
        # Check for README
        if [[ -f "$readme" ]]; then
            local desc=$(grep -m1 "^# " "$readme" 2>/dev/null | sed 's/^# //' || echo "No description")
            print_info "$desc"
        fi
        
        # Status
        if [[ -f "$status_file" ]]; then
            local status=$(cat "$status_file" 2>/dev/null)
            print_success "Status: $status"
        elif [[ $last_output -gt 0 ]]; then
            print_success "Status: ACTIVE (recent output)"
        else
            print_warning "Status: IDLE"
        fi
        
        # Files
        local file_count=$(find "$agent_dir" -type f 2>/dev/null | wc -l)
        print_info "Files: $file_count"
    done
    
    if [[ $agent_count -eq 0 ]]; then
        print_warning "No agents found in $AGENTS_DIR"
        print_info "Use agent-manager.sh create <name> to create a new agent"
    else
        echo ""
        print_info "Total agents: $agent_count"
    fi
}

# Search memory
cmd_memory_search() {
    local query="$1"
    
    if [[ -z "$query" ]]; then
        print_error "Search query required"
        echo "Usage: memory search <query>"
        return 1
    fi
    
    print_header "Memory Search: '$query'"
    
    if [[ ! -f "$MEMORY_FILE" ]]; then
        print_error "MEMORY.md not found: $MEMORY_FILE"
        return 1
    fi
    
    # Try ripgrep first, fall back to grep
    local results
    if command -v rg &> /dev/null; then
        results=$(rg -i -n -C 2 "$query" "$MEMORY_FILE" 2>/dev/null || true)
    else
        results=$(grep -i -n -C 2 "$query" "$MEMORY_FILE" 2>/dev/null || true)
    fi
    
    if [[ -z "$results" ]]; then
        print_warning "No matches found for '$query'"
    else
        echo "$results" | while read line; do
            # Highlight matches
            if echo "$line" | grep -qi "$query"; then
                echo -e "${YELLOW}$line${NC}"
            else
                echo "$line"
            fi
        done
        print_success "Search complete"
    fi
}

# List sessions
cmd_session_list() {
    print_header "Recent Sessions"
    
    # Look for session logs in workspace
    local session_dir="$WORKSPACE/sessions"
    local memory_dir="$WORKSPACE/memory"
    
    # Check memory directory for daily files
    if [[ -d "$memory_dir" ]]; then
        print_info "Recent daily logs:"
        ls -lt "$memory_dir"/*.md 2>/dev/null | head -5 | while read line; do
            local file=$(echo "$line" | awk '{print $NF}')
            local date=$(basename "$file" .md)
            local size=$(stat -c%s "$file" 2>/dev/null || echo "0")
            echo -e "  ${CYAN}$date${NC} (${size} bytes)"
        done || print_warning "No daily logs found"
    fi
    
    # Check for active session markers
    echo ""
    print_info "Active components:"
    
    if pgrep -f "openclaw.*gateway" > /dev/null; then
        print_success "Gateway: Running"
    else
        print_warning "Gateway: Stopped"
    fi
    
    local agent_procs=$(pgrep -c "openclaw.*agent" 2>/dev/null || echo "0")
    if [[ $agent_procs -gt 0 ]]; then
        print_success "Agent processes: $agent_procs"
    else
        print_info "Agent processes: 0"
    fi
    
    # Recent activity
    echo ""
    print_info "Recent workspace activity:"
    find "$WORKSPACE" -type f -mtime -1 2>/dev/null | head -10 | while read file; do
        local name=$(basename "$file")
        local mtime=$(stat -c "%y" "$file" 2>/dev/null | cut -d'.' -f1)
        echo -e "  ${BLUE}$name${NC} - $mtime"
    done || print_warning "No recent activity"
}

# Main command dispatcher
main() {
    local command="${1:-}"
    
    case "$command" in
        -h|--help|help)
            show_help
            exit 0
            ;;
        status)
            cmd_status
            ;;
        logs)
            cmd_logs "${2:-50}"
            ;;
        restart)
            cmd_restart
            ;;
        agents)
            cmd_agents
            ;;
        memory)
            shift
            local subcmd="${1:-}"
            case "$subcmd" in
                search)
                    cmd_memory_search "${2:-}"
                    ;;
                *)
                    print_error "Unknown memory subcommand: $subcmd"
                    echo "Usage: memory search <query>"
                    exit 1
                    ;;
            esac
            ;;
        session)
            shift
            local subcmd="${1:-}"
            case "$subcmd" in
                list)
                    cmd_session_list
                    ;;
                *)
                    print_error "Unknown session subcommand: $subcmd"
                    echo "Usage: session list"
                    exit 1
                    ;;
            esac
            ;;
        "")
            print_error "No command specified"
            show_help
            exit 1
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"

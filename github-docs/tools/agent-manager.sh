#!/bin/bash
#
# Agent Manager - Manage OpenClaw Agent Lifecycle
# Create, deploy, and monitor your agents
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
AGENTS_DIR="$WORKSPACE/agents"
ROSTER_FILE="$WORKSPACE/AGENTS_ROSTER_V2.md"

# Print helpers
print_header() {
    echo -e "${MAGENTA}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}${BOLD}║${NC}  $1"
    echo -e "${MAGENTA}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
}

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1" >&2; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_agent() { echo -e "${CYAN}🤖${NC} $1"; }

# Show help
show_help() {
    cat << EOF
${BOLD}Agent Manager${NC} - Manage OpenClaw Agents

${BOLD}USAGE:${NC}
    agent-manager.sh <command> [arguments]

${BOLD}COMMANDS:${NC}
    list                Show all agents in agents/ directory
    create <name>       Scaffold new agent folder with README.md template
    deploy <name>       Mark agent as active/deployed
    status              Check which agents have recent output

${BOLD}OPTIONS:${NC}
    -h, --help          Show this help message

${BOLD}EXAMPLES:${NC}
    ./agent-manager.sh list
    ./agent-manager.sh create MyNewAgent
    ./agent-manager.sh deploy MyNewAgent
    ./agent-manager.sh status

${BOLD}AGENT STRUCTURE:${NC}
    agents/
    └── <agent-name>/
        ├── README.md        # Agent description and docs
        ├── .status          # Current status (ACTIVE/IDLE/etc)
        ├── src/             # Source files (optional)
        └── output/          # Agent output (optional)

EOF
}

# Convert name to valid directory name
sanitize_name() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-'
}

# Get personality from roster
get_personality_hint() {
    if [[ -f "$ROSTER_FILE" ]]; then
        # Try to extract a random personality archetype
        local archetypes=$(grep -E "^- \*\*" "$ROSTER_FILE" 2>/dev/null | sed 's/- \*\*//;s/\*\*.*//' || true)
        if [[ -n "$archetypes" ]]; then
            echo "$archetypes" | shuf -n 1 2>/dev/null || echo "$archetypes" | head -1
        else
            echo "Specialist"
        fi
    else
        echo "Specialist"
    fi
}

# List all agents
cmd_list() {
    print_header "Registered Agents"
    
    if [[ ! -d "$AGENTS_DIR" ]]; then
        print_error "Agents directory not found: $AGENTS_DIR"
        print_info "Creating directory..."
        mkdir -p "$AGENTS_DIR"
    fi
    
    local count=0
    
    for agent_dir in "$AGENTS_DIR"/*/; do
        [[ -d "$agent_dir" ]] || continue
        
        local name=$(basename "$agent_dir")
        local readme="$agent_dir/README.md"
        local status_file="$agent_dir/.status"
        local created=$(stat -c "%y" "$agent_dir" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        
        count=$((count + 1))
        
        # Get status
        local status="IDLE"
        local status_color="${YELLOW}"
        if [[ -f "$status_file" ]]; then
            status=$(cat "$status_file" 2>/dev/null | tr '[:lower:]' '[:upper:]')
            if [[ "$status" == "ACTIVE" ]]; then
                status_color="${GREEN}"
            elif [[ "$status" == "DEPLOYED" ]]; then
                status_color="${CYAN}"
            fi
        fi
        
        # Get description from README
        local desc=""
        if [[ -f "$readme" ]]; then
            desc=$(grep -m1 "^## Purpose" "$readme" 2>/dev/null | sed 's/## Purpose//' | xargs || echo "")
            [[ -z "$desc" ]] && desc=$(grep -m1 "^- " "$readme" 2>/dev/null | sed 's/^- //' | xargs || echo "")
        fi
        
        echo ""
        print_agent "${BOLD}$name${NC}"
        echo -e "  Status: ${status_color}${status}${NC}"
        echo -e "  Created: $created"
        [[ -n "$desc" ]] && echo -e "  ${BLUE}$desc${NC}"
    done
    
    if [[ $count -eq 0 ]]; then
        print_warning "No agents found"
        print_info "Create your first agent with: ./agent-manager.sh create <name>"
    else
        echo ""
        print_info "Total agents: $count"
    fi
}

# Create new agent
cmd_create() {
    local raw_name="$1"
    
    if [[ -z "$raw_name" ]]; then
        print_error "Agent name required"
        echo "Usage: create <name>"
        exit 1
    fi
    
    local name=$(sanitize_name "$raw_name")
    local agent_dir="$AGENTS_DIR/$name"
    local personality=$(get_personality_hint)
    
    if [[ -d "$agent_dir" ]]; then
        print_error "Agent '$name' already exists"
        exit 1
    fi
    
    print_header "Creating Agent: $name"
    
    # Create directory structure
    mkdir -p "$agent_dir/src" "$agent_dir/output" "$agent_dir/memory"
    print_success "Created directory structure"
    
    # Create README.md template
    cat > "$agent_dir/README.md" << EOF
# $raw_name

## Purpose

<!-- Describe what this agent does -->
$raw_name is a $personality agent for OpenClaw.

## Responsibilities

- <!-- Add responsibility 1 -->
- <!-- Add responsibility 2 -->
- <!-- Add responsibility 3 -->

## Inputs

- <!-- What does this agent receive? -->

## Outputs

- <!-- What does this agent produce? -->

## Schedule

- <!-- When does this agent run? (cron, heartbeat, manual) -->

## Dependencies

- <!-- Other agents or services this depends on -->

## Notes

<!-- Additional context -->

---
Created: $(date +%Y-%m-%d)
Status: IDLE
EOF
    
    print_success "Created README.md"
    
    # Create initial status file
    echo "IDLE" > "$agent_dir/.status"
    print_success "Initialized status"
    
    # Create placeholder script
    cat > "$agent_dir/src/run.sh" << 'EOF'
#!/bin/bash
# Main execution script for agent

set -e

# Source environment if needed
# source ../../.env

echo "[$0] Agent execution started at $(date)"

# TODO: Add agent logic here

echo "[$0] Agent execution completed at $(date)"
EOF
    chmod +x "$agent_dir/src/run.sh"
    print_success "Created run.sh template"
    
    # Create .gitkeep for empty directories
    touch "$agent_dir/output/.gitkeep"
    touch "$agent_dir/memory/.gitkeep"
    
    echo ""
    print_success "Agent '$name' created successfully!"
    print_info "Location: $agent_dir"
    print_info "Edit $agent_dir/README.md to customize"
}

# Deploy agent
cmd_deploy() {
    local name="$1"
    
    if [[ -z "$name" ]]; then
        print_error "Agent name required"
        echo "Usage: deploy <name>"
        exit 1
    fi
    
    local agent_dir="$AGENTS_DIR/$name"
    
    if [[ ! -d "$agent_dir" ]]; then
        # Try sanitized name
        local sanitized=$(sanitize_name "$name")
        if [[ "$sanitized" != "$name" && -d "$AGENTS_DIR/$sanitized" ]]; then
            agent_dir="$AGENTS_DIR/$sanitized"
        else
            print_error "Agent '$name' not found"
            print_info "Available agents:"
            cmd_list
            exit 1
        fi
    fi
    
    print_header "Deploying Agent: $(basename "$agent_dir")"
    
    # Update status
    echo "DEPLOYED" > "$agent_dir/.status"
    print_success "Status updated to DEPLOYED"
    
    # Update README
    local readme="$agent_dir/README.md"
    if [[ -f "$readme" ]]; then
        sed -i "s/^Status: .*/Status: DEPLOYED (as of $(date +%Y-%m-%d))/" "$readme" 2>/dev/null || true
    fi
    
    # Create deployment marker
    echo "$(date): Deployed" >> "$agent_dir/.deployments"
    
    # Check if run.sh exists and is executable
    if [[ -f "$agent_dir/src/run.sh" ]]; then
        if [[ -x "$agent_dir/src/run.sh" ]]; then
            print_success "Run script is executable"
        else
            chmod +x "$agent_dir/src/run.sh"
            print_warning "Made run.sh executable"
        fi
    fi
    
    echo ""
    print_success "Agent deployed successfully!"
    print_info "To activate: update status to ACTIVE"
    print_info "To run manually: $agent_dir/src/run.sh"
}

# Check agent status
cmd_status() {
    print_header "Agent Health Status"
    
    if [[ ! -d "$AGENTS_DIR" ]]; then
        print_error "Agents directory not found"
        exit 1
    fi
    
    local active_count=0
    local idle_count=0
    local stale_count=0
    
    for agent_dir in "$AGENTS_DIR"/*/; do
        [[ -d "$agent_dir" ]] || continue
        
        local name=$(basename "$agent_dir")
        local status_file="$agent_dir/.status"
        local last_output="$agent_dir/output"
        local recent_files
        
        # Check for recent output (within 24 hours)
        recent_files=$(find "$last_output" -type f -mtime -1 2>/dev/null | wc -l)
        
        # Get declared status
        local declared_status="IDLE"
        [[ -f "$status_file" ]] && declared_status=$(cat "$status_file" 2>/dev/null | tr '[:lower:]' '[:upper:]')
        
        echo ""
        print_agent "$name"
        
        # Determine actual status
        if [[ $recent_files -gt 0 ]]; then
            print_success "Recent output: YES ($recent_files files in last 24h)"
            active_count=$((active_count + 1))
        else
            print_info "Recent output: No activity in last 24h"
            
            # Check if it should have output
            if [[ "$declared_status" == "ACTIVE" ]]; then
                print_warning "Declared ACTIVE but no recent output!"
                stale_count=$((stale_count + 1))
            else
                idle_count=$((idle_count + 1))
            fi
        fi
        
        # Show declared status
        if [[ "$declared_status" == "ACTIVE" ]]; then
            echo -e "  Declared status: ${GREEN}$declared_status${NC}"
        elif [[ "$declared_status" == "DEPLOYED" ]]; then
            echo -e "  Declared status: ${CYAN}$declared_status${NC}"
        else
            echo -e "  Declared status: ${YELLOW}$declared_status${NC}"
        fi
        
        # Show last modified file
        local last_file=$(find "$agent_dir" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
        if [[ -n "$last_file" ]]; then
            local last_time=$(stat -c "%y" "$last_file" 2>/dev/null | cut -d'.' -f1)
            print_info "Last activity: $(basename "$last_file") at $last_time"
        fi
    done
    
    echo ""
    print_header "Summary"
    print_success "Active agents: $active_count"
    print_info "Idle agents: $idle_count"
    [[ $stale_count -gt 0 ]] && print_warning "Stale agents: $stale_count"
}

# Main dispatcher
main() {
    local cmd="${1:-}"
    
    case "$cmd" in
        -h|--help|help)
            show_help
            exit 0
            ;;
        list)
            cmd_list
            ;;
        create)
            cmd_create "$2"
            ;;
        deploy)
            cmd_deploy "$2"
            ;;
        status)
            cmd_status
            ;;
        "")
            print_error "No command specified"
            show_help
            exit 1
            ;;
        *)
            print_error "Unknown command: $cmd"
            show_help
            exit 1
            ;;
    esac
}

main "$@"

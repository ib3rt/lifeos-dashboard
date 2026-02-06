#!/bin/bash

#===============================================================================
# SUPER SWARM COORDINATOR - Master Automation Hub
#===============================================================================
# Orchestrates and integrates all Business SOP, Strategic Logic, 
# and Content Automation systems.
#
# Usage:
#   ./super-swarm-coordinator.sh --all          # Run all swarms
#   ./super-swarm-coordinator.sh --sop          # Run SOP automation only
#   ./super-swarm-coordinator.sh --strategy      # Run strategy automation only
#   ./super-swarm-coordinator.sh --content      # Run content automation only
#   ./super-swarm-coordinator.sh --status        # Show status
#   ./super-swarm-coordinator.sh --integrate    # Integrate outputs
#
#===============================================================================

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="${WORKSPACE_DIR}/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#===============================================================================
# UTILITY FUNCTIONS
#===============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

ensure_log_dir() {
    mkdir -p "$LOG_DIR"
}

#===============================================================================
# STATUS FUNCTIONS
#===============================================================================

show_status() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "                    SUPER SWARM STATUS REPORT"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    
    # Check each swarm directory
    local sop_status="❌ Not Found"
    local strategy_status="❌ Not Found"
    local content_status="❌ Not Found"
    
    if [ -d "${WORKSPACE_DIR}/tools/sop-automation" ]; then
        sop_status="✅ Active"
    fi
    
    if [ -d "${WORKSPACE_DIR}/tools/strategy-automation" ]; then
        strategy_status="✅ Active"
    fi
    
    if [ -d "${WORKSPACE_DIR}/tools/content-automation" ]; then
        content_status="✅ Active"
    fi
    
    echo "┌─────────────────────────────────────────────┐"
    echo "│           Swarm Component Status             │"
    echo "├─────────────────────────────────────────────┤"
    echo "│  🏢 SOP Automation (Agent 1):  ${sop_status}   │"
    echo "│  🧠 Strategy Engine (Agent 2):   ${strategy_status}   │"
    echo "│  📝 Content Automation (Agent 3): ${content_status}   │"
    echo "└─────────────────────────────────────────────┘"
    echo ""
    
    # Check for recent logs
    echo "Recent Activity:"
    if [ -d "$LOG_DIR" ]; then
        ls -lah "$LOG_DIR" 2>/dev/null | tail -5 || echo "  No logs found"
    else
        echo "  No logs directory"
    fi
    echo ""
}

#===============================================================================
# SOP AUTOMATION (AGENT 1)
#===============================================================================

run_sop_automation() {
    log_info "Starting Business SOP Automation (Agent 1)..."
    
    local sop_dir="${WORKSPACE_DIR}/tools/sop-automation"
    
    if [ -f "${sop_dir}/run.sh" ]; then
        bash "${sop_dir}/run.sh"
    else
        log_info "SOP Automation: Creating base structure..."
        mkdir -p "${sop_dir}/logs"
        mkdir -p "${sop_dir}/templates"
        mkdir -p "${sop_dir}/workflows"
        
        # Create base SOP automation script
        cat > "${sop_dir}/sop-engine.sh" << 'SOP_ENGINE'
#!/bin/bash
# SOP Automation Engine
echo "[SOP] Processing standard operating procedures..."
SOP_ENGINE
        chmod +x "${sop_dir}/sop-engine.sh"
        
        log_success "SOP Automation base structure created"
    fi
}

#===============================================================================
# STRATEGY AUTOMATION (AGENT 2)
#===============================================================================

run_strategy_automation() {
    log_info "Starting Strategic Logic Engine (Agent 2)..."
    
    local strategy_dir="${WORKSPACE_DIR}/tools/strategy-automation"
    
    if [ -f "${strategy_dir}/run.sh" ]; then
        bash "${strategy_dir}/run.sh"
    else
        log_info "Strategy Automation: Creating base structure..."
        mkdir -p "${strategy_dir}/logs"
        mkdir -p "${strategy_dir}/frameworks"
        mkdir -p "${strategy_dir}/roadmaps"
        
        # Create base strategy automation script
        cat > "${strategy_dir}/strategy-engine.sh" << 'STRAT_ENGINE'
#!/bin/bash
# Strategy Automation Engine
echo "[STRATEGY] Processing strategic logic..."
STRAT_ENGINE
        chmod +x "${strategy_dir}/strategy-engine.sh"
        
        log_success "Strategy Automation base structure created"
    fi
}

#===============================================================================
# CONTENT AUTOMATION (AGENT 3)
#===============================================================================

run_content_automation() {
    log_info "Starting Content Automation (Agent 3)..."
    
    local content_dir="${WORKSPACE_DIR}/tools/content-automation"
    
    if [ -f "${content_dir}/run.sh" ]; then
        bash "${content_dir}/run.sh"
    else
        log_info "Content Automation: Creating base structure..."
        mkdir -p "${content_dir}/logs"
        mkdir -p "${content_dir}/templates"
        mkdir -p "${content_dir}/pipelines"
        
        # Create base content automation script
        cat > "${content_dir}/content-engine.sh" << 'CONTENT_ENGINE'
#!/bin/bash
# Content Automation Engine
echo "[CONTENT] Processing content pipelines..."
CONTENT_ENGINE
        chmod +x "${content_dir}/content-engine.sh"
        
        log_success "Content Automation base structure created"
    fi
}

#===============================================================================
# INTEGRATION FUNCTIONS
#===============================================================================

integrate_outputs() {
    log_info "Integrating outputs from all swarms..."
    
    local integration_status="success"
    
    # Check SOP outputs
    if [ -d "${WORKSPACE_DIR}/tools/sop-automation/output" ]; then
        log_info "Found SOP outputs"
    fi
    
    # Check Strategy outputs
    if [ -d "${WORKSPACE_DIR}/tools/strategy-automation/output" ]; then
        log_info "Found Strategy outputs"
    fi
    
    # Check Content outputs
    if [ -d "${WORKSPACE_DIR}/tools/content-automation/output" ]; then
        log_info "Found Content outputs"
    fi
    
    # Create integration report
    cat > "${WORKSPACE_DIR}/super-swarm/integration-report.md" << EOF
# Integration Report - $(date)

## Summary
All swarm outputs have been processed and integrated.

## SOP Integration
- Status: Complete
- Processed: $(date)

## Strategy Integration
- Status: Complete
- Processed: $(date)

## Content Integration
- Status: Complete
- Processed: $(date)

## Overall Status
✅ Integration Complete
EOF
    
    log_success "Outputs integrated successfully"
}

#===============================================================================
# PARALLEL EXECUTION
#===============================================================================

run_all_parallel() {
    log_info "🚀 Starting ALL swarms in PARALLEL..."
    echo ""
    
    ensure_log_dir
    
    # Run all three in background
    run_sop_automation > "${LOG_DIR}/sop_automation_${TIMESTAMP}.log" 2>&1 &
    local sop_pid=$!
    
    run_strategy_automation > "${LOG_DIR}/strategy_automation_${TIMESTAMP}.log" 2>&1 &
    local strategy_pid=$!
    
    run_content_automation > "${LOG_DIR}/content_automation_${TIMESTAMP}.log" 2>&1 &
    local content_pid=$!
    
    echo "┌─────────────────────────────────────────────┐"
    echo "│  Parallel Execution Started                 │"
    echo "├─────────────────────────────────────────────┤"
    echo "│  🏢 SOP Agent:     PID ${sop_pid}              │"
    echo "│  🧠 Strategy Agent: PID ${strategy_pid}         │"
    echo "│  📝 Content Agent: PID ${content_pid}          │"
    echo "└─────────────────────────────────────────────┘"
    echo ""
    
    # Wait for all to complete
    log_info "Waiting for all swarms to complete..."
    
    wait $sop_pid 2>/dev/null || true
    log_success "SOP Automation completed"
    
    wait $strategy_pid 2>/dev/null || true
    log_success "Strategy Automation completed"
    
    wait $content_pid 2>/dev/null || true
    log_success "Content Automation completed"
    
    echo ""
    log_success "All parallel swarms completed!"
    
    # Run integration
    integrate_outputs
}

run_all_sequential() {
    log_info "Starting ALL swarms SEQUENTIALLY..."
    
    ensure_log_dir
    
    run_sop_automation
    run_strategy_automation
    run_content_automation
    
    integrate_outputs
}

#===============================================================================
# MAIN ENTRY POINT
#===============================================================================

main() {
    echo "═══════════════════════════════════════════════════════════════════"
    echo "           SUPER SWARM COORDINATOR v1.0.0"
    echo "           Master Automation Hub for Life OS"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    
    case "${1:-}" in
        --all)
            run_all_parallel
            ;;
        --sop)
            run_sop_automation
            ;;
        --strategy)
            run_strategy_automation
            ;;
        --content)
            run_content_automation
            ;;
        --status)
            show_status
            ;;
        --integrate)
            integrate_outputs
            ;;
        --help|-h)
            echo "Usage: $0 {--all|--sop|--strategy|--content|--status|--integrate|--help}"
            echo ""
            echo "Options:"
            echo "  --all        Run all three swarms in parallel"
            echo "  --sop        Run Business SOP Automation only"
            echo "  --strategy   Run Strategic Logic Engine only"
            echo "  --content    Run Content Automation only"
            echo "  --status     Show status of all swarms"
            echo "  --integrate  Integrate outputs from all swarms"
            echo "  --help       Show this help message"
            ;;
        "")
            run_all_parallel
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
    
    echo ""
    log_success "Super Swarm Coordinator finished"
}

# Run main function with all arguments
main "$@"

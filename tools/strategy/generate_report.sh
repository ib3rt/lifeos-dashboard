#!/bin/bash
# Strategy Report Generator
# Usage: ./generate_report.sh [report_type] [output_format]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/../reports"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)

mkdir -p "$OUTPUT_DIR"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Generate KPI Report
generate_kpi_report() {
    log_info "Generating KPI Report..."
    
    python3 "${SCRIPT_DIR}/kpi_collector.py" --report > "${OUTPUT_DIR}/kpi_report_${DATE}.md"
    
    # Also generate JSON version
    python3 "${SCRIPT_DIR}/kpi_collector.py" --json > "${OUTPUT_DIR}/kpi_report_${DATE}.json"
    
    log_info "KPI Report saved to ${OUTPUT_DIR}/kpi_report_${DATE}.md"
}

# Generate SWOT Analysis Report
generate_swot_report() {
    log_info "Generating SWOT Analysis..."
    
    python3 "${SCRIPT_DIR}/swot_analyzer.py" > "${OUTPUT_DIR}/swot_report_${DATE}.md"
    
    log_info "SWOT Report saved to ${OUTPUT_DIR}/swot_report_${DATE}.md"
}

# Generate Revenue Projection
generate_revenue_projection() {
    local months=${1:-36}
    log_info "Generating ${months}-month revenue projection..."
    
    python3 "${SCRIPT_DIR}/revenue_projector.py" --months "$months" > "${OUTPUT_DIR}/revenue_projection_${DATE}.md"
    
    log_info "Revenue Projection saved to ${OUTPUT_DIR}/revenue_projection_${DATE}.md"
}

# Generate Risk Report
generate_risk_report() {
    log_info "Generating Risk Assessment Report..."
    
    python3 "${SCRIPT_DIR}/risk_matrix.py" > "${OUTPUT_DIR}/risk_report_${DATE}.md"
    
    log_info "Risk Report saved to ${OUTPUT_DIR}/risk_report_${DATE}.md"
}

# Generate Full Strategic Report
generate_full_report() {
    log_info "Generating Full Strategic Report..."
    
    {
        echo "# Strategic Report - ${DATE}"
        echo ""
        echo "## Executive Summary"
        echo "Generated: ${TIMESTAMP}"
        echo ""
        echo "---"
        echo ""
        
        echo "## KPI Status"
        echo ""
        python3 "${SCRIPT_DIR}/kpi_collector.py" --report 2>/dev/null || echo "No KPI data available"
        echo ""
        
        echo "---"
        echo ""
        
        echo "## Risk Assessment"
        echo ""
        python3 "${SCRIPT_DIR}/risk_matrix.py" 2>/dev/null || echo "No risk data available"
        echo ""
        
        echo "---"
        echo ""
        
        echo "## SWOT Analysis"
        echo ""
        python3 "${SCRIPT_DIR}/swot_analyzer.py" 2>/dev/null || echo "No SWOT data available"
        echo ""
        
        echo "---"
        echo ""
        echo "*Report generated automatically*"
        
    } > "${OUTPUT_DIR}/strategic_report_${DATE}.md"
    
    log_info "Full Strategic Report saved to ${OUTPUT_DIR}/strategic_report_${DATE}.md"
}

# Send notification (placeholder)
send_notification() {
    local message="$1"
    # Add webhook/API call here
    log_info "Notification: ${message}"
}

# Main
case "${1:-help}" in
    kpi)
        generate_kpi_report
        ;;
    swot)
        generate_swot_report
        ;;
    revenue)
        generate_revenue_projection "${2:-36}"
        ;;
    risk)
        generate_risk_report
        ;;
    full)
        generate_full_report
        ;;
    all)
        generate_kpi_report
        generate_swot_report
        generate_risk_report
        generate_revenue_projection
        generate_full_report
        log_info "All reports generated"
        ;;
    help|*)
        echo "Strategy Report Generator"
        echo ""
        echo "Usage: $0 [command] [options]"
        echo ""
        echo "Commands:"
        echo "  kpi         Generate KPI report"
        echo "  swot        Generate SWOT analysis"
        echo "  revenue [months]  Generate revenue projection (default: 36)"
        echo "  risk        Generate risk assessment"
        echo "  full        Generate comprehensive strategic report"
        echo "  all         Generate all reports"
        echo ""
        ;;
esac

#!/bin/bash
#===============================================================================
# SOP Generator Script
# Purpose: Auto-generate SOP documents from templates
# Usage: ./generate_sop.sh [template_name] [output_path]
#===============================================================================

set -e

# Configuration
TEMPLATES_DIR="${TEMPLATES_DIR:-./business/templates}"
OUTPUT_DIR="${OUTPUT_DIR:-./business/sops}"
SOP_INDEX="${OUTPUT_DIR}/index.md"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S %Z")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
SOP Generator - Auto-generate SOP documents from templates

Usage: $(basename "$0") [OPTIONS]

OPTIONS:
    -t, --template TEMPLATE    Template name to use (required)
    -o, --output OUTPUT        Output directory (default: ./business/sops)
    -n, --name SOP_NAME        Name for the SOP (default: from template)
    --list-templates           List available templates
    --init-templates           Initialize default templates
    -h, --help                Show this help message

EXAMPLES:
    $(basename "$0") -t sales-pipeline -n "My Sales SOP"
    $(basename "$0") --template client-onboarding --output ./custom-sops
    $(basename "$0") --list-templates

EOF
}

list_templates() {
    log_info "Available templates:"
    if [ -d "$TEMPLATES_DIR" ]; then
        find "$TEMPLATES_DIR" -name "*.md" -o -name "*.yaml" -o -name "*.json" | while read -r template; do
            local name=$(basename "$template" .md | basename "$template" .yaml | basename "$template" .json)
            echo "  - $name"
        done
    else
        log_warn "Templates directory not found: $TEMPLATES_DIR"
    fi
}

init_templates() {
    log_info "Initializing default templates..."
    
    mkdir -p "$TEMPLATES_DIR"
    
    # Create base SOP template
    cat > "$TEMPLATES_DIR/sop-base.md" << 'EOF'
# SOP_TITLE

## Document Information
- **SOP ID**: SOP-XXX
- **Version**: 1.0.0
- **Effective Date**: YYYY-MM-DD
- **Owner**: ROLE
- **Last Review**: YYYY-MM-DD

## Purpose
Brief description of the SOP purpose.

## Scope
Description of what this SOP covers.

## Process Overview

```mermaid
graph TD
    A[Step 1] --> B[Step 2]
    B --> C[Step 3]
```

## Detailed Procedures

### 1. Section Name

#### 1.1 Subsection
Description of procedures...

## Automation Triggers

| Trigger | Action | Owner |
|---------|--------|-------|
| Event | Action | System |

## Metrics & KPIs

| Metric | Target | Measurement Frequency |
|--------|--------|----------------------|
| KPI 1 | Target | Frequency |

## Roles & Responsibilities

| Role | Responsibilities |
|------|------------------|
| Role | Resp |

## Compliance Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## References
- Reference link 1
- Reference link 2

---

*Document Version: 1.0.0*
*Last Updated: YYYY-MM-DD*
*Next Review: YYYY-MM-DD*
EOF

    log_success "Default templates initialized in $TEMPLATES_DIR"
}

generate_sop() {
    local template="$1"
    local output_name="$2"
    
    # Find template file
    local template_file=""
    for ext in .md .yaml .json; do
        if [ -f "$TEMPLATES_DIR/${template}${ext}" ]; then
            template_file="$TEMPLATES_DIR/${template}${ext}"
            break
        fi
    done
    
    if [ -z "$template_file" ]; then
        log_error "Template not found: $template"
        log_info "Available templates:"
        list_templates
        exit 1
    fi
    
    log_info "Using template: $template_file"
    
    # Generate output filename
    if [ -z "$output_name" ]; then
        output_name="$template"
    fi
    
    local output_file="${OUTPUT_DIR}/${output_name}.md"
    
    # Create output directory if needed
    mkdir -p "$(dirname "$output_file")"
    
    # Read template and replace placeholders
    local content=$(cat "$template_file")
    
    # Replace placeholders
    content=$(echo "$content" | sed "s/SOP_TITLE/$(echo "$output_name" | sed 's/-/ /g' | sed 's/\b./\U&/g')/g")
    content=$(echo "$content" | sed "s/SOP-XXX/SOP-$(echo "$output_name" | tr '[:lower:]' '[:upper:]' | tr '-' '_' | head -c 8)-001/g")
    content=$(echo "$content" | sed "s/YYYY-MM-DD/$DATE/g")
    
    # Write output file
    echo "$content" > "$output_file"
    
    log_success "SOP generated: $output_file"
    
    # Update index if it exists
    if [ -f "$SOP_INDEX" ]; then
        update_index "$output_name" "$output_file"
    fi
    
    # Log generation
    log_generation "$output_name" "$template" "$output_file"
}

update_index() {
    local name="$1"
    local file="$2"
    
    log_info "Updating SOP index..."
    
    # Add entry to index if not exists
    if ! grep -q "\[$name\]" "$SOP_INDEX" 2>/dev/null; then
        # Find insertion point (alphabetically)
        local temp_file=$(mktemp)
        local inserted=false
        
        while IFS= read -r line; do
            if [ "$inserted" = false ] && echo "$line" | grep -q "^\- \*\*\[.*\]\("; then
                local entry_title=$(echo "$line" | sed 's/.*\[\([^]]*\)\].*/\1/' | tr '[:upper:]' '[:lower:]')
                local new_title=$(echo "$name" | tr '[:upper:]' '[:lower:]')
                
                if [ "$new_title" \< "$entry_title" ]; then
                    echo "- **[${name}](${file})** - Description" >> "$temp_file"
                    inserted=true
                fi
            fi
            echo "$line"
        done < "$SOP_INDEX"
        
        if [ "$inserted" = false ]; then
            echo "- **[${name}](${file})** - Description" >> "$temp_file"
        fi
        
        mv "$temp_file" "$SOP_INDEX"
        log_success "Index updated"
    fi
}

log_generation() {
    local log_file="${OUTPUT_DIR}/.sop_generation_log"
    echo "[$TIMESTAMP] Generated: $1 from template: $2 -> $3" >> "$log_file"
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--template)
                TEMPLATE="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -n|--name)
                SOP_NAME="$2"
                shift 2
                ;;
            --list-templates)
                list_templates
                exit 0
                ;;
            --init-templates)
                init_templates
                exit 0
                ;;
            -h|--help)
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
    
    # Check required parameters
    if [ -z "$TEMPLATE" ]; then
        log_error "Template name is required"
        show_help
        exit 1
    fi
    
    # Generate SOP
    generate_sop "$TEMPLATE" "$SOP_NAME"
}

# Run main
main "$@"

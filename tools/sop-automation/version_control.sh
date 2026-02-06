#!/bin/bash
#===============================================================================
# SOP Version Control Script
# Purpose: Manage SOP versions, track changes, and maintain history
# Usage: ./version_control.sh [command] [options]
#===============================================================================

set -e

# Configuration
SOPS_DIR="${SOPS_DIR:-./business/sops}"
VERSION_FILE="${SOPS_DIR}/.versions"
ARCHIVE_DIR="${SOPS_DIR}/.archive"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S %Z")

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_help() {
    cat << EOF
SOP Version Control - Manage SOP document versions

Usage: $(basename "$0") <command> [options]

COMMANDS:
    init              Initialize version tracking for SOPs
    commit <file>     Commit changes to an SOP
    status <file>     Show version status of an SOP
    history <file>    Show version history of an SOP
    diff <file>       Show changes from last version
    rollback <file>   Rollback to previous version
    tag <file> <tag>  Create a named tag for a version
    list              List all tracked SOPs
    sync              Sync versions across all SOPs

OPTIONS:
    -m, --message MSG     Commit message
    -v, --version VER     Version number (default: patch bump)
    -b, --branch NAME     Branch name (for future use)
    -h, --help            Show this help

VERSION SCHEME:
    MAJOR.MINOR.PATCH (e.g., 1.0.0 -> 1.1.0)
    - MAJOR: Breaking changes
    - MINOR: New features, non-breaking changes
    - PATCH: Bug fixes, minor updates

EXAMPLES:
    $(basename "$0") init
    $(basename "$0") commit sales-pipeline.md -m "Updated approval workflow"
    $(basename "$0") status client-onboarding.md
    $(basename "$0") history content-workflow.md
    $(basename "$0") rollback financial-tracking.md -v 1.2.0
    $(basename "$0") tag project-management.md v1.0.0

EOF
}

init_version_tracking() {
    log_info "Initializing version tracking..."
    
    # Create directories
    mkdir -p "$ARCHIVE_DIR"
    
    # Create version tracking file if not exists
    if [ ! -f "$VERSION_FILE" ]; then
        cat > "$VERSION_FILE" << EOF
# SOP Version Tracking
# Auto-generated - DO NOT EDIT MANUALLY
# Format: JSON

{
  "initialized": "$DATE",
  "last_updated": "$DATE",
  "sops": {}
}
EOF
    fi
    
    # Initialize tracking for existing SOPs
    for sop in "$SOPS_DIR"/*.md; do
        if [ -f "$sop" ]; then
            local filename=$(basename "$sop")
            local version=$(extract_version "$sop")
            add_to_tracking "$filename" "$version" "Initial version"
        fi
    done
    
    log_success "Version tracking initialized"
}

extract_version() {
    local file="$1"
    grep -oP 'Version: \K[0-9]+\.[0-9]+\.[0-9]+' "$file" 2>/dev/null || echo "1.0.0"
}

extract_sop_id() {
    local file="$1"
    grep -oP 'SOP ID: \K[A-Z\-]+' "$file" 2>/dev/null || echo "UNKNOWN"
}

add_to_tracking() {
    local filename="$1"
    local version="$2"
    local message="$3"
    
    python3 << PYEOF
import json

version_file = "$VERSION_FILE"
filename = "$filename"
version = "$version"
message = """$message""".strip()

with open(version_file, 'r') as f:
    data = json.load(f)

if filename not in data['sops']:
    data['sops'][filename] = {
        "current_version": version,
        "versions": []
    }

data['sops'][filename]['versions'].append({
    "version": version,
    "date": "$DATE",
    "message": message,
    "timestamp": "$TIMESTAMP"
})
data['sops'][filename]['current_version'] = version
data['last_updated'] = "$DATE"

with open(version_file, 'w') as f:
    json.dump(data, f, indent=2)

print("OK")
PYEOF
}

commit_sop() {
    local file="$1"
    local message="${2:-Update}"
    local version_type="${3:-patch}"
    
    # Find the file
    local filepath=""
    if [ -f "$file" ]; then
        filepath="$file"
    elif [ -f "${SOPS_DIR}/${file}" ]; then
        filepath="${SOPS_DIR}/${file}"
    elif [ -f "${SOPS_DIR}/${file}.md" ]; then
        filepath="${SOPS_DIR}/${file}.md"
    else
        log_error "SOP file not found: $file"
        exit 1
    fi
    
    local filename=$(basename "$filepath")
    
    log_info "Committing changes to: $filename"
    
    # Archive current version
    local current_version=$(extract_version "$filepath")
    local archive_file="${ARCHIVE_DIR}/${filename%.md}_v${current_version}.md"
    cp "$filepath" "$archive_file"
    
    # Bump version
    local new_version=$(bump_version "$current_version" "$version_type")
    
    # Update version in file
    sed -i "s/Version: $current_version/Version: $new_version/g" "$filepath"
    
    # Update last review date
    sed -i "s/Last Review:.*/Last Review: $DATE/g" "$filepath"
    
    # Update tracking
    add_to_tracking "$filename" "$new_version" "$message"
    
    # Create diff if git available
    if command -v git &> /dev/null; then
        git add "$filepath" 2>/dev/null || true
        git commit -m "SOP: $filename v$new_version - $message" 2>/dev/null || true
    fi
    
    log_success "Committed $filename: $current_version -> $new_version"
    log_info "Message: $message"
}

bump_version() {
    local current="$1"
    local type="$2"
    
    IFS='.' read -ra parts <<< "$current"
    
    case "$type" in
        major)
            echo "$((parts[0] + 1)).0.0"
            ;;
        minor)
            echo "${parts[0]}.$((parts[1] + 1)).0"
            ;;
        patch|*)
            echo "${parts[0]}.${parts[1]}.$((parts[2] + 1))"
            ;;
    esac
}

show_status() {
    local file="$1"
    
    # Find file
    local filepath=""
    if [ -f "$file" ]; then
        filepath="$file"
    elif [ -f "${SOPS_DIR}/${file}" ]; then
        filepath="${SOPS_DIR}/${file}"
    elif [ -f "${SOPS_DIR}/${file}.md" ]; then
        filepath="${SOPS_DIR}/${file}.md"
    else
        log_error "SOP file not found: $file"
        exit 1
    fi
    
    local filename=$(basename "$filepath")
    local version=$(extract_version "$filepath")
    local sop_id=$(extract_sop_id "$filepath")
    
    echo -e "${CYAN}=== $filename ===${NC}"
    echo -e "SOP ID: $sop_id"
    echo -e "Current Version: $version"
    echo -e "Last Updated: $(grep -oP 'Last Updated: \K[0-9\-]+' "$filepath" 2>/dev/null || echo 'N/A')"
    
    # Check version file
    if [ -f "$VERSION_FILE" ]; then
        python3 << PYEOF
import json

with open("$VERSION_FILE", 'r') as f:
    data = json.load(f)

if "$filename" in data.get('sops', {}):
    sop = data['sops']["$filename"]
    print(f"Tracked Version: {sop['current_version']}")
    print(f"Total Versions: {len(sop['versions'])}")
else:
    print("Status: NOT TRACKED")
PYEOF
    fi
}

show_history() {
    local file="$1"
    
    # Find file
    local filepath=""
    if [ -f "$file" ]; then
        filepath="$file"
    elif [ -f "${SOPS_DIR}/${file}" ]; then
        filepath="${SOPS_DIR}/${file}"
    elif [ -f "${SOPS_DIR}/${file}.md" ]; then
        filepath="${SOPS_DIR}/${file}.md"
    else
        log_error "SOP file not found: $file"
        exit 1
    fi
    
    local filename=$(basename "$filepath")
    
    echo -e "${CYAN}=== Version History: $filename ===${NC}"
    
    python3 << PYEOF
import json

version_file = "$VERSION_FILE"
filename = "$filename"

with open(version_file, 'r') as f:
    data = json.load(f)

if filename in data.get('sops', {}):
    sop = data['sops'][filename]
    versions = sorted(sop['versions'], key=lambda v: v['version'], reverse=True)
    
    print(f"{'Version':<12} {'Date':<12} {'Message'}")
    print("-" * 60)
    for v in versions:
        msg = v['message'][:40] + ('...' if len(v['message']) > 40 else '')
        print(f"{v['version']:<12} {v['date']:<12} {msg}")
else:
    print("No history found")
PYEOF
}

show_diff() {
    local file="$1"
    local version="${2:-previous}"
    
    # Find file
    local filepath=""
    if [ -f "$file" ]; then
        filepath="$file"
    elif [ -f "${SOPS_DIR}/${file}" ]; then
        filepath="${SOPS_DIR}/${file}"
    elif [ -f "${SOPS_DIR}/${file}.md" ]; then
        filepath="${SOPS_DIR}/${file}.md"
    else
        log_error "SOP file not found: $file"
        exit 1
    fi
    
    local filename=$(basename "$filepath")
    
    if command -v git &> /dev/null && git rev-parse &> /dev/null; then
        git log --oneline -5 -- "$filepath" 2>/dev/null || echo "Git history available"
    else
        log_info "Git not available, showing archive diffs"
        
        current_version=$(extract_version "$filepath")
        compare_version=$(bump_version "$current_version" "patch")
        
        archive_file="${ARCHIVE_DIR}/${filename%.md}_v${compare_version}.md"
        
        if [ -f "$archive_file" ]; then
            diff -u "$archive_file" "$filepath" | head -100 || echo "No significant changes detected"
        else
            log_warn "No previous version found to compare"
        fi
    fi
}

rollback_sop() {
    local file="$1"
    local target_version="${2:-}"
    
    # Find file
    local filepath=""
    if [ -f "$file" ]; then
        filepath="$file"
    elif [ -f "${SOPS_DIR}/${file}" ]; then
        filepath="${SOPS_DIR}/${file}"
    elif [ -f "${SOPS_DIR}/${file}.md" ]; then
        filepath="${SOPS_DIR}/${file}.md"
    else
        log_error "SOP file not found: $file"
        exit 1
    fi
    
    local filename=$(basename "$filepath")
    
    log_info "Rolling back: $filename"
    
    if [ -z "$target_version" ]; then
        log_error "Target version required. Use -v flag."
        exit 1
    fi
    
    # Find archive file
    local archive_file="${ARCHIVE_DIR}/${filename%.md}_v${target_version}.md"
    
    if [ ! -f "$archive_file" ]; then
        log_error "Version $target_version not found in archives"
        log_info "Available versions:"
        ls -la "${ARCHIVE_DIR}/${filename%.md}_"*.md 2>/dev/null || echo "No archives found"
        exit 1
    fi
    
    # Backup current
    local current_version=$(extract_version "$filepath")
    cp "$filepath" "${ARCHIVE_DIR}/${filename%.md}_v${current_version}_backup.md"
    
    # Restore from archive
    cp "$archive_file" "$filepath"
    
    # Update version
    sed -i "s/Version: $target_version/Version: $(bump_version "$target_version" "patch")/g" "$filepath"
    sed -i "s/Last Updated:.*/Last Updated: $DATE/g" "$filepath"
    
    log_success "Rolled back $filename to version $target_version"
}

create_tag() {
    local file="$1"
    local tag="$2"
    
    # Find file
    local filepath=""
    if [ -f "$file" ]; then
        filepath="$file"
    elif [ -f "${SOPS_DIR}/${file}" ]; then
        filepath="${SOPS_DIR}/${file}"
    elif [ -f "${SOPS_DIR}/${file}.md" ]; then
        filepath="${SOPS_DIR}/${file}.md"
    else
        log_error "SOP file not found: $file"
        exit 1
    fi
    
    local filename=$(basename "$filepath")
    local version=$(extract_version "$filepath")
    
    log_info "Creating tag '$tag' for $filename v$version"
    
    # Copy to tagged version
    local tag_file="${ARCHIVE_DIR}/${tag}_${filename}"
    cp "$filepath" "$tag_file"
    
    python3 << PYEOF
import json

version_file = "$VERSION_FILE"
filename = "$filename"
tag = "$tag"
version = "$version"

with open(version_file, 'r') as f:
    data = json.load(f)

if 'tags' not in data:
    data['tags'] = {}

data['tags'][tag] = {
    "filename": filename,
    "version": version,
    "date": "$DATE",
    "timestamp": "$TIMESTAMP"
}

with open(version_file, 'w') as f:
    json.dump(data, f, indent=2)

print("OK")
PYEOF

    log_success "Tag created: $tag -> $version"
}

list_sops() {
    echo -e "${CYAN}=== Tracked SOPs ===${NC}"
    
    if [ -f "$VERSION_FILE" ]; then
        python3 << PYEOF
import json

with open("$VERSION_FILE", 'r') as f:
    data = json.load(f)

print(f"{'SOP Name':<35} {'Version':<12} {'Updated':<12}")
print("-" * 60)
for name, sop in data.get('sops', {}).items():
    print(f"{name:<35} {sop['current_version']:<12} {data.get('last_updated', 'N/A'):<12}")
PYEOF
    else
        log_warn "No SOPs tracked. Run '$(basename "$0") init' first."
    fi
}

sync_versions() {
    log_info "Syncing versions across all SOPs..."
    
    for sop in "$SOPS_DIR"/*.md; do
        if [ -f "$sop" ]; then
            local filename=$(basename "$sop")
            local current_version=$(extract_version "$sop")
            
            python3 << PYEOF
import json

version_file = "$VERSION_FILE"
filename = "$filename"
current_version = "$current_version"

with open(version_file, 'r') as f:
    data = json.load(f)

if filename in data.get('sops', {}):
    tracked_version = data['sops'][filename]['current_version']
    if tracked_version != current_version:
        print(f"Mismatch: $filename (file: $current_version, tracked: $tracked_version)")
else:
    print(f"Not tracked: $filename")
PYEOF
        fi
    done
    
    log_success "Sync complete"
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    local command="$1"
    shift
    
    local file=""
    local message=""
    local version_type="patch"
    local target_version=""
    local tag=""
    
    # Parse remaining arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -m|--message)
                message="$2"
                shift 2
                ;;
            -v|--version)
                target_version="$2"
                shift 2
                ;;
            -b|--branch)
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$file" ]; then
                    file="$1"
                else
                    log_error "Unexpected argument: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Execute command
    case "$command" in
        init)
            init_version_tracking
            ;;
        commit)
            if [ -z "$file" ]; then
                log_error "File required for commit"
                exit 1
            fi
            # Determine version type from message
            if echo "$message" | grep -qi "breaking\|major"; then
                version_type="major"
            elif echo "$message" | grep -qi "feature\|minor"; then
                version_type="minor"
            fi
            commit_sop "$file" "$message" "$version_type"
            ;;
        status)
            if [ -z "$file" ]; then
                log_error "File required for status"
                exit 1
            fi
            show_status "$file"
            ;;
        history)
            if [ -z "$file" ]; then
                log_error "File required for history"
                exit 1
            fi
            show_history "$file"
            ;;
        diff)
            if [ -z "$file" ]; then
                log_error "File required for diff"
                exit 1
            fi
            show_diff "$file" "$target_version"
            ;;
        rollback)
            if [ -z "$file" ]; then
                log_error "File required for rollback"
                exit 1
            fi
            rollback_sop "$file" "$target_version"
            ;;
        tag)
            if [ -z "$file" ] || [ -z "$tag" ]; then
                log_error "File and tag required"
                exit 1
            fi
            create_tag "$file" "$tag"
            ;;
        list)
            list_sops
            ;;
        sync)
            sync_versions
            ;;
        -h|--help)
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

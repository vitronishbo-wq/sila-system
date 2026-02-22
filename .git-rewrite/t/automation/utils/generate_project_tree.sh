#!/bin/bash
################################################################################
# SILA System - Project Tree Generation Script
# ==============================================================================
# Generates clean and focused project tree snapshots for three scopes:
# 1. Root - complete project structure
# 2. Backend - backend application structure
# 3. Frontend - frontend application structure
#
# Purpose: Provide automated, up-to-date project structure documentation
# suitable for audits, CI/CD pipelines, and development reference.
#
# Generated files are placed in the project root for easy access.
#
# Usage:
#   ./scripts/generate_project_tree.sh [max_depth]
#
# Arguments:
#   max_depth (optional): Maximum directory depth to traverse (default: 4)
#
# Example:
#   ./scripts/generate_project_tree.sh
#   ./scripts/generate_project_tree.sh 5
################################################################################

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'  # No Color

# Configuration
MAX_DEPTH="${1:-4}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"

# Output directory - in project root for easy access
OUTPUT_DIR="${PROJECT_ROOT}"

# Exclusion patterns for find command
# These patterns represent directories/files to skip
EXCLUDE_PATTERNS=(
    -not -path "*node_modules*"
    -not -path "*venv*"
    -not -path "*\.venv*"
    -not -path "*.git*"
    -not -path "*__pycache__*"
    -not -path "*.pytest_cache*"
    -not -path "*\.mypy_cache*"
    -not -path "*\.ruff_cache*"
    -not -path "*.egg-info*"
    -not -path "*htmlcov*"
    -not -path "*dist*"
    -not -path "*build*"
    -not -path "*\.coverage*"
    -not -path "*\.backups*"
    -not -path "*backups*"
    -not -path "*archive*"
    -not -path "*\.temp*"
    -not -path "*\.cache*"
    -not -path "*logs*"
    -not -path "*\.logs*"
    -not -path "*\.vscode*"
    -not -path "*\.github*"
    -not -path "*\.husky*"
    -not -path "*uploads*"
    -not -path "*\.tar.gz*"
    -not -path "*\.zip*"
)

# File extension filters for inclusion
# Only show these types of files in the tree
INCLUDE_EXTENSIONS=(
    "\.py$"
    "\.sh$"
    "\.md$"
    "\.json$"
    "\.yaml$"
    "\.yml$"
    "Dockerfile"
    "Makefile"
    "\.txt$"
    "\.env"
    "\.conf$"
    "\.sql$"
    "\.ts$"
    "\.tsx$"
    "\.jsx$"
    "\.js$"
)

# ============================================================================
# Helper Functions
# ============================================================================

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_section() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

# Check if a file should be included based on extension
should_include_file() {
    local file="$1"
    local filename=$(basename "$file")

    # Always include directories
    if [[ -d "$file" ]]; then
        return 0
    fi

    # Check against extension list
    for ext in "${INCLUDE_EXTENSIONS[@]}"; do
        if [[ "$filename" =~ $ext ]] || [[ "$filename" == *"$ext" ]]; then
            return 0
        fi
    done

    return 1
}

# Generate tree using find command with proper formatting
generate_tree() {
    local target_dir="$1"
    local output_file="$2"
    local scope_name="$3"

    if [[ ! -d "$target_dir" ]]; then
        log_error "Directory not found: $target_dir"
        return 1
    fi

    log_info "Generating tree for ${scope_name}..."

    {
        echo "# SILA System - Project Structure"
        echo "# Scope: ${scope_name}"
        echo "# Generated: ${TIMESTAMP}"
        echo "# Max Depth: ${MAX_DEPTH}"
        echo ""
        echo "\`\`\`"

        # Use find to generate tree-like output
        cd "$target_dir"
        find . -maxdepth "$MAX_DEPTH" -type f "${EXCLUDE_PATTERNS[@]}" 2>/dev/null | \
            while IFS= read -r file; do
                if should_include_file "$file"; then
                    # Calculate indentation based on directory depth
                    depth=$(echo "$file" | tr -cd '/' | wc -c)
                    indent=$(printf '%*s' "$((depth * 2))" | tr ' ' '·')

                    # Clean up path display
                    display_path="${file#./}"

                    if [[ -d "$file" ]]; then
                        echo "${indent}📁 ${display_path}/"
                    else
                        # Show file extension icon
                        case "$display_path" in
                            *.py)    echo "${indent}🐍 ${display_path}" ;;
                            *.sh)    echo "${indent}⚙️  ${display_path}" ;;
                            *.md)    echo "${indent}📄 ${display_path}" ;;
                            *.json)  echo "${indent}⚙️  ${display_path}" ;;
                            *.yaml|*.yml) echo "${indent}⚙️  ${display_path}" ;;
                            Dockerfile*) echo "${indent}🐳 ${display_path}" ;;
                            Makefile) echo "${indent}🛠️  ${display_path}" ;;
                            *)       echo "${indent}📄 ${display_path}" ;;
                        esac
                    fi
                fi
            done | sort

        echo "\`\`\`"
        echo ""
        echo "**Generated at:** $(date)"
        echo "**Location:** ${target_dir}"

    } > "$output_file"

    log_success "Tree generated: $output_file"
}

# Alternative tree generation using the 'tree' command if available
generate_tree_with_tree_cmd() {
    local target_dir="$1"
    local output_file="$2"
    local scope_name="$3"

    if ! command -v tree &>/dev/null; then
        return 1
    fi

    log_info "Using 'tree' command for ${scope_name}..."

    {
        echo "# SILA System - Project Structure"
        echo "# Scope: ${scope_name}"
        echo "# Generated: ${TIMESTAMP}"
        echo ""

        tree "$target_dir" \
            -L "$MAX_DEPTH" \
            -I "node_modules|venv|.git|__pycache__|.pytest_cache|.mypy_cache|.ruff_cache|*.egg-info|htmlcov|dist|build|.coverage|.backups|backups|archive|.temp|.cache|logs" \
            --dirsfirst \
            2>/dev/null || true

        echo ""
        echo "**Generated at:** $(date)"
        echo "**Location:** ${target_dir}"

    } > "$output_file"

    log_success "Tree generated (using tree command): $output_file"
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    log_section "SILA System - Project Tree Generator"

    log_info "Project Root: ${PROJECT_ROOT}"
    log_info "Max Depth: ${MAX_DEPTH}"
    log_info "Output Directory: ${OUTPUT_DIR}"

    # Check prerequisites (new domain-oriented layout under apps/)
    if [[ ! -d "$PROJECT_ROOT/apps/backend" ]] || [[ ! -d "$PROJECT_ROOT/apps/frontend" ]]; then
        log_error "Backend or Frontend directory not found under apps/!"
        log_info "This script must be run from the SILA project root with apps/backend and apps/frontend present"
        return 1
    fi

    log_section "Generating Trees"

    # Generate root project tree
    generate_tree \
        "$PROJECT_ROOT" \
        "${OUTPUT_DIR}/.tree-root.md" \
        "Project Root" || log_warning "Failed to generate root tree"

    # Generate backend tree
    generate_tree \
        "$PROJECT_ROOT/apps/backend" \
        "${OUTPUT_DIR}/.tree-backend.md" \
        "Backend Application (apps/backend)" || log_warning "Failed to generate backend tree"

    # Generate frontend tree
    generate_tree \
        "$PROJECT_ROOT/apps/frontend" \
        "${OUTPUT_DIR}/.tree-frontend.md" \
        "Frontend Application (apps/frontend)" || log_warning "Failed to generate frontend tree"

    log_section "Summary"

    log_success "All trees generated successfully!"
    echo ""
    echo "📁 Generated Files:"
    ls -lh "${OUTPUT_DIR}"/.tree-*.md 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'

    echo ""
    log_info "These files are hidden (prefixed with .) and automatically excluded from git."
    log_info "To view them: cat ${OUTPUT_DIR}/.tree-root.md"
    echo ""
}

# Run main function
main "$@"

#!/bin/bash
# QUICK REFERENCE - Project Tree Generation System
# ================================================

# 🌳 GENERATE TREES
# ────────────────────────────────────────────────

# Generate with default settings (depth 4)
./scripts/generate_project_tree.sh

# Generate with custom depth
./scripts/generate_project_tree.sh 2    # Shallow view
./scripts/generate_project_tree.sh 3    # Recommended
./scripts/generate_project_tree.sh 5    # Deep view


# 📋 VIEW GENERATED TREES
# ────────────────────────────────────────────────

# View all three trees
cat .tree-root.md      # Complete project
cat .tree-backend.md   # Backend only
cat .tree-frontend.md  # Frontend only

# Quick search in trees
grep -i "models" .tree-backend.md


# 🔍 VERIFY GENERATION
# ────────────────────────────────────────────────

# Check file sizes
ls -lh .tree-*.md

# Check modification times
stat .tree-root.md | grep Modify

# Validate trees exist
[[ -f .tree-root.md ]] && echo "✅ Root tree OK"
[[ -f .tree-backend.md ]] && echo "✅ Backend tree OK"
[[ -f .tree-frontend.md ]] && echo "✅ Frontend tree OK"


# 🚀 AUTOMATION EXAMPLES
# ────────────────────────────────────────────────

# Add to your bash profile for daily generation
# alias generate-trees="./scripts/generate_project_tree.sh"

# Add to development startup scripts
# eval "$(./scripts/generate_project_tree.sh)"

# Add to pre-commit hook (.pre-commit-config.yaml)
# - repo: local
#   hooks:
#     - id: update-project-tree
#       name: Update Project Tree
#       entry: bash scripts/generate_project_tree.sh 3
#       language: script
#       pass_filenames: false


# 📖 DOCUMENTATION
# ────────────────────────────────────────────────

# Read full documentation
cat scripts/TREE_GENERATION.md

# View script source
cat scripts/generate_project_tree.sh


# ⚙️  TROUBLESHOOTING
# ────────────────────────────────────────────────

# Make script executable
chmod +x scripts/generate_project_tree.sh

# Run with debug output
bash -x scripts/generate_project_tree.sh 2

# Check for errors
bash scripts/generate_project_tree.sh 2>&1 | grep -i error


# 📊 STATISTICS
# ────────────────────────────────────────────────

# Count files in each tree
wc -l .tree-*.md

# File size comparison
du -h .tree-*.md | sort -h

# Show directory depth in trees
head -20 .tree-root.md


# 🎯 COMMON TASKS
# ────────────────────────────────────────────────

# Generate and show root tree (all in one)
./scripts/generate_project_tree.sh 3 && cat .tree-root.md

# Generate and verify
./scripts/generate_project_tree.sh && [[ -f .tree-root.md ]] && echo "✅ Done"

# Compare old vs new structure
# diff .tree-root.md.bak .tree-root.md

# Archive for historical tracking
# cp .tree-*.md .tree-*.md."$(date +%Y%m%d)"


# ✨ ADVANCED USAGE
# ────────────────────────────────────────────────

# Export trees to a report
{
  echo "# Project Structure Report"
  echo "Generated: $(date)"
  echo ""
  echo "## Root Structure"
  cat .tree-root.md
  echo ""
  echo "## Backend Structure"
  cat .tree-backend.md
  echo ""
  echo "## Frontend Structure"
  cat .tree-frontend.md
} > project_structure_report.md

# Search for specific patterns
grep -r "modules" .tree-backend.md | head -10

# Generate with all depths and compare
for depth in 2 3 4 5; do
  ./scripts/generate_project_tree.sh $depth
  echo "Depth $depth: $(wc -l < .tree-root.md) lines"
done

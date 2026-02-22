#!/bin/bash
# Master Index Generator - Wrapper for easy WSL access
# Usage: ./master-index.sh [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/master_index_generator.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: master_index_generator.py not found in $SCRIPT_DIR"
    exit 1
fi

# Display help
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    cat <<EOF
🎯 Master Index Generator - Quick Usage

USAGE:
  ./master-index.sh [COMMAND] [OPTIONS]

COMMANDS:
  py              Index Python files (--ext py)
  js              Index JavaScript files (--ext js ts vue)
  full            Full index (all files, respects .gitignore)
  quick           Quick scan (Python, exclude venv, size sorted)

OPTIONS:
  --dry           Dry-run mode (no file write)
  --debug         Verbose output
  --json          Export JSON
  --csv           Export CSV
  --sort NAME     Sort by name/size/date (default: name)

EXAMPLES:
  ./master-index.sh py                    # Python files, basic index
  ./master-index.sh quick --json          # Python with JSON export
  ./master-index.sh full --csv            # All files to CSV
  ./master-index.sh py --dry --debug      # Test mode with logging

EOF
    exit 0
fi

# Default command
COMMAND="${1:-quick}"
shift

# Build command arguments
ARGS="."

case "$COMMAND" in
    py)
        ARGS="$ARGS --ext py"
        ;;
    js)
        ARGS="$ARGS --ext js ts vue"
        ;;
    full)
        ARGS="$ARGS --require-gitignore --sort size --json --csv"
        ;;
    quick)
        ARGS="$ARGS --ext py --exclude venv node_modules __pycache__ --sort size --json --csv"
        ;;
    *)
        # Treat as raw args to pass through
        ARGS="$ARGS $COMMAND"
        ;;
esac

# Add any additional arguments
ARGS="$ARGS $@"

# Execute
echo "🚀 Running: python3 $PYTHON_SCRIPT $ARGS"
echo ""
python3 "$PYTHON_SCRIPT" $ARGS

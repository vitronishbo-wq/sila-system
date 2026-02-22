#!/bin/bash
# Helper script to run commands with correct PYTHONPATH
# Usage: ./run_with_pythonpath.sh <command>

export PYTHONPATH="$(pwd)/backend:$PYTHONPATH"

echo "🔧 PYTHONPATH configurado: $PYTHONPATH"
echo "📍 Executando: $@"
echo ""

exec "$@"

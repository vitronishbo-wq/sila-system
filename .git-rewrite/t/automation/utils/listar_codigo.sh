#!/bin/bash

# Root directory of the project
ROOT_DIR="/opt/sila-system"

# Output file
OUTPUT_FILE="$ROOT_DIR/scripts/lista_codigo_gerado.csv"

# File extensions considered as pure code
EXTENSIONS="*.py *.js *.ts *.java *.go *.c *.cpp *.rb *.php *.rs *.sh *.html *.css"

# Header for CSV
echo "Path,Size (bytes),Last Modified" > "$OUTPUT_FILE"

# Find and list files with metadata
find "$ROOT_DIR" \( -name node_modules -o -name .git -o -name dist -o -name build \) -prune -false -o \
    \( $(printf -- '-name %s -o ' $EXTENSIONS | sed 's/ -o $//') \) \
    -type f -exec stat --format '%n,%s,%y' {} \; | \
    sort -t',' -k3,3r -k2,2nr >> "$OUTPUT_FILE"

# Final message
echo "✅ CSV file generated at: $OUTPUT_FILE"

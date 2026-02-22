#!/usr/bin/env bash
set -euo pipefail

MODULES_DIR="apps/backend/modules"
OUT_DIR="reports"
mkdir -p "$OUT_DIR"

echo "Audit: modules structure and models"
echo "Modules dir: $MODULES_DIR"

# 1) list modules
ls -1 "$MODULES_DIR" > "$OUT_DIR/modules_list.txt"

# 2) all __tablename__ lines
grep -R "__tablename__" --include="*.py" "$MODULES_DIR" | sort > "$OUT_DIR/tablenames_raw.txt"

# 3) summarize by table name (count)
awk -F: '{print $2}' "$OUT_DIR/tablenames_raw.txt" | sed 's/__tablename__\s*=\s*//g' | sed "s/['\"]//g" | sed 's/^[ \t]*//;s/[ \t]*$//' | sort | uniq -c | sort -nr > "$OUT_DIR/tablenames_summary.txt"

# 4) locations of Payment-related models/schemas
grep -R "class Payment" --include="*.py" "$MODULES_DIR" > "$OUT_DIR/payment_class_locs.txt" || true
grep -R "class PaymentTransaction" --include="*.py" "$MODULES_DIR" > "$OUT_DIR/payment_txn_class_locs.txt" || true
grep -R "class Refund" --include="*.py" "$MODULES_DIR" > "$OUT_DIR/payment_refund_class_locs.txt" || true

# 5) files with 'from .* import *'
grep -R "import \*" --include="*.py" "$MODULES_DIR" > "$OUT_DIR/import_star.txt" || true

# 6) files with model_validate usage
grep -R "model_validate" --include="*.py" "$MODULES_DIR" > "$OUT_DIR/model_validate_usage.txt" || true

# 7) files with .value usage
grep -R "\.value" --include="*.py" "$MODULES_DIR" > "$OUT_DIR/value_usage.txt" || true

# 8) summary JSON
python3 - <<PY
import json, pathlib, sys
out = {
 "modules": [l.strip() for l in pathlib.Path("$OUT_DIR/modules_list.txt").read_text().splitlines()],
 "tablenames_raw": [l.strip() for l in pathlib.Path("$OUT_DIR/tablenames_raw.txt").read_text().splitlines()],
 "tablenames_summary": [l.strip() for l in pathlib.Path("$OUT_DIR/tablenames_summary.txt").read_text().splitlines()],
 "payment_files": [l.strip() for l in pathlib.Path("$OUT_DIR/payment_class_locs.txt").read_text().splitlines() if pathlib.Path("$OUT_DIR/payment_class_locs.txt").exists()],
 "import_star": [l.strip() for l in pathlib.Path("$OUT_DIR/import_star.txt").read_text().splitlines() if pathlib.Path("$OUT_DIR/import_star.txt").exists()],
 "model_validate_usage": [l.strip() for l in pathlib.Path("$OUT_DIR/model_validate_usage.txt").read_text().splitlines() if pathlib.Path("$OUT_DIR/model_validate_usage.txt").exists()],
 "value_usage": [l.strip() for l in pathlib.Path("$OUT_DIR/value_usage.txt").read_text().splitlines() if pathlib.Path("$OUT_DIR/value_usage.txt").exists()]
}
path = pathlib.Path("$OUT_DIR/audit_modules_detailed.json")
path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
print("Wrote", path)
PY

echo "Audit completed. Reports in $OUT_DIR/"

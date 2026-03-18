#!/bin/bash
cd /home/truman/dev/sila-system
python3 automation/tools/mass_fix_prototype_v2.py --dry-run --report reports/mass_fix_v2
echo "Exit code: $?"

#!/bin/bash
# ROUTES AUDIT - VERIFICATION CHECKLIST
# Execute this script to verify all audit artifacts are in place

echo "========================================"
echo "🔍 ROUTES HEALTH AUDIT VERIFICATION"
echo "========================================"
echo ""

artifacts=(
    "ROUTES_HEALTH_SUMMARY.md:Executive summary (2-minute read)"
    "ROUTES_HEALTH_AUDIT.md:Comprehensive analysis with deep dive"
    "ROUTES_DETAILED_INVENTORY.md:Complete catalog of 561 endpoints"
    "ROUTES_ACTION_PLAN.md:4-week implementation roadmap"
    "scripts/routes_health_monitor.py:Runtime health monitoring tool"
)

total=${#artifacts[@]}
found=0

for artifact in "${artifacts[@]}"; do
    file="${artifact%%:*}"
    description="${artifact##*:}"
    
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        lines=$(wc -l < "$file")
        echo "✅ $file"
        echo "   Size: $(numfmt --to=iec-i --suffix=B $size 2>/dev/null || echo '~'$((size/1024))'KB')"
        echo "   Description: $description"
        ((found++))
    else
        echo "❌ $file"
        echo "   Status: MISSING"
    fi
    echo ""
done

echo "========================================"
echo "📊 SUMMARY"
echo "========================================"
echo "Artifacts Found: $found/$total"

if [ $found -eq $total ]; then
    echo "Status: ✅ ALL ARTIFACTS PRESENT"
    echo ""
    echo "📋 QUICK START:"
    echo "  1. Read:   cat ROUTES_HEALTH_SUMMARY.md"
    echo "  2. Review: cat ROUTES_HEALTH_AUDIT.md"
    echo "  3. Plan:   cat ROUTES_ACTION_PLAN.md"
    echo "  4. Monitor: python scripts/routes_health_monitor.py"
else
    echo "Status: 🔴 MISSING FILES"
    exit 1
fi

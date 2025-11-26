#!/bin/bash
# Monitor Module 4 (CUDA Water Structure Analysis) Progress
# Run this script to check status: bash check_module4_progress.sh

echo "=========================================="
echo "MODULE 4 PROGRESS CHECK"
echo "=========================================="
echo ""

# Check if process is running
echo "1. Process Status:"
ps_out=$(ps aux | grep "04_comprehensive_water_structure" | grep -v grep)
if [ -n "$ps_out" ]; then
    echo "✓ Module 4 is RUNNING"
    echo "$ps_out" | awk '{print "  CPU: "$3"% | Memory: "$6/1024" MB | Runtime: "$10}'
else
    echo "✗ Module 4 is NOT running (completed or crashed)"
fi
echo ""

# Check output files
echo "2. Output Files Created:"
PLOTS_DIR="/store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/plots"

json_count=$(ls "$PLOTS_DIR"/water_structure_*.json 2>/dev/null | wc -l)
csv_count=$(ls "$PLOTS_DIR"/water_structure_*.csv 2>/dev/null | wc -l)

echo "  JSON files: $json_count / 6"
echo "  CSV files: $csv_count / 6"

if [ $json_count -gt 0 ]; then
    echo ""
    echo "  File sizes:"
    ls -lh "$PLOTS_DIR"/water_structure_*.json 2>/dev/null | awk '{print "    "$9": "$5}'
fi
echo ""

# Estimate progress
if [ $json_count -eq 0 ]; then
    progress="0%"
elif [ $json_count -eq 6 ] && [ $csv_count -eq 6 ]; then
    progress="100% - COMPLETE!"
else
    progress=$(( json_count * 100 / 6 ))"% (epsilon $json_count of 6)"
fi

echo "3. Estimated Progress: $progress"
echo ""

# Check file integrity (JSON should be >1KB when complete)
if [ $json_count -gt 0 ]; then
    echo "4. File Integrity Check:"
    for f in "$PLOTS_DIR"/water_structure_*.json; do
        size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null)
        if [ "$size" -lt 1000 ]; then
            echo "  ⏳ $(basename $f): $size bytes (still writing...)"
        else
            size_kb=$(( size / 1024 ))
            echo "  ✓ $(basename $f): ${size_kb} KB (complete)"
        fi
    done
    echo ""
fi

# Recommendations
echo "=========================================="
echo "NEXT STEPS:"
echo "=========================================="

if [ $json_count -eq 6 ] && [ $csv_count -eq 6 ]; then
    echo "✓ Module 4 COMPLETE!"
    echo ""
    echo "  Run Module 5 to create visualizations:"
    echo "    cd /store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/codes"
    echo "    python 05_plot_water_structure.py"
elif [ -n "$ps_out" ]; then
    echo "⏳ Module 4 still running..."
    echo ""
    echo "  Estimated time remaining: ~$(( 15 - json_count * 2 )) minutes"
    echo "  Check again in 5 minutes: bash check_module4_progress.sh"
else
    echo "⚠ Module 4 not running but incomplete output"
    echo ""
    echo "  This might indicate an error. Check for errors:"
    echo "    Check terminal output where Module 4 was started"
    echo "  Or restart Module 4:"
    echo "    cd /store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/codes"
    echo "    python 04_comprehensive_water_structure_CUDA.py"
fi

echo ""
echo "=========================================="

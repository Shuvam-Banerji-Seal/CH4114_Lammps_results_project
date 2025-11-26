#!/usr/bin/env python3
"""
Fix epsilon_values_list definition in modules 04-07 that are missing it
"""

import re
from pathlib import Path

BASE_DIR = Path("/store/shuvam/learning_solvent_effects/analysis/codes")

# Modules that need epsilon_values_list defined
MODULES_TO_FIX = [
    '04_comprehensive_water_structure_CUDA.py',
    '05_plot_water_structure.py',
    '06_msd_validation.py',
    '07_high_priority_additional_analysis.py'
]

# The epsilon list definition to add
EPSILON_DEF = """
# Setup epsilon directories (handle epsilon_0.0 and format differences)
epsilon_values_list = [
    0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
    0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0, 1.05, 1.10
]
"""

def add_epsilon_list_if_missing(filepath):
    """Add epsilon_values_list definition if missing"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if epsilon_values_list is already defined
    if re.search(r'^epsilon_values_list\s*=', content, re.MULTILINE):
        print(f"  Already has epsilon_values_list definition")
        return False
    
    # Find the BASE_DIR definition
    base_dir_match = re.search(r'(BASE_DIR\s*=\s*Path.*?\n)', content)
    if not base_dir_match:
        print(f"  ERROR: Could not find BASE_DIR definition")
        return False
    
    # Insert epsilon_values_list after BASE_DIR
    insert_pos = base_dir_match.end()
    new_content = content[:insert_pos] + EPSILON_DEF + content[insert_pos:]
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    print("="*70)
    print("FIXING MISSING epsilon_values_list DEFINITIONS")
    print("="*70)
    print()
    
    for module in MODULES_TO_FIX:
        filepath = BASE_DIR / module
        if not filepath.exists():
            print(f"❌ {module} - not found")
            continue
            
        print(f"Processing {module}...")
        if add_epsilon_list_if_missing(filepath):
            print(f"✅ {module} - added epsilon_values_list")
        else:
            print(f"⏭️  {module} - skipped")
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)

if __name__ == "__main__":
    main()

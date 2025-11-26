#!/usr/bin/env python3
"""
Script to update all analysis modules to handle all 23 epsilon values
"""

import re
from pathlib import Path

BASE_DIR = Path("/store/shuvam/learning_solvent_effects/analysis/codes")

# Modules to update
MODULES = [
    '04_comprehensive_water_structure_CUDA.py',
    '05_plot_water_structure.py',
    '06_msd_validation.py',
    '07_high_priority_additional_analysis.py',
    '09_equilibration_pathway_analysis.py',
    '10_structural_data_analysis.py',
    '12_equilibration_convergence_analysis.py',
    '13_log_file_performance_analysis.py',
    '14_system_validation.py',
    '15_thermal_trajectory_analysis.py',
    '16_advanced_cuda_trajectory_analysis.py'
]

# New epsilon values (23 total)
NEW_EPSILON_LIST = """epsilon_values_list = [
    0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
    0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0, 1.05, 1.10
]"""

# New directory setup with solvent_effects path
NEW_DIR_SETUP = """EPSILON_DIRS = []
for eps in epsilon_values_list:
    if eps == 0.0:
        EPSILON_DIRS.append(BASE_DIR / "solvent_effects" / "epsilon_0.0")
    elif eps == 1.0:
        EPSILON_DIRS.append(BASE_DIR / "solvent_effects" / "epsilon_1.0")
    else:
        EPSILON_DIRS.append(BASE_DIR / "solvent_effects" / f"epsilon_{eps:.2f}")"""

def update_module(filepath):
    """Update a single module file"""
    if not filepath.exists():
        print(f"  Skipping {filepath.name} - not found")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: Update epsilon_values_list definition
    pattern1 = r'epsilon_values_list\s*=\s*\[0\.0,\s*0\.05[^\]]+\]'
    if re.search(pattern1, content):
        content = re.sub(pattern1, NEW_EPSILON_LIST, content)
    
    # Pattern 2: Update directory paths from "epsilon_0.0" to "solvent_effects" / "epsilon_0.0"
    pattern2 = r'EPSILON_DIRS\.append\(BASE_DIR\s*/\s*"epsilon_0\.0"\)'
    content = re.sub(pattern2, 'EPSILON_DIRS.append(BASE_DIR / "solvent_effects" / "epsilon_0.0")', content)
    
    pattern3 = r'EPSILON_DIRS\.append\(BASE_DIR\s*/\s*f"epsilon_\{eps:.2f\}"\)'
    content = re.sub(pattern3, 'EPSILON_DIRS.append(BASE_DIR / "solvent_effects" / f"epsilon_{eps:.2f}")', content)
    
    # Pattern 4: Add epsilon_1.0 handling if not present
    if 'elif eps == 1.0:' not in content and 'if eps == 0.0:' in content:
        # Insert after the epsilon_0.0 block
        content = re.sub(
            r'(if eps == 0\.0:.*?EPSILON_DIRS\.append\(BASE_DIR.*?\))\n(\s+else:)',
            r'\1\n    elif eps == 1.0:\n        EPSILON_DIRS.append(BASE_DIR / "solvent_effects" / "epsilon_1.0")\n\2',
            content,
            flags=re.DOTALL
        )
    
    # Pattern 5: Update inline epsilon_values assignments in main()
    pattern5 = r'epsilon_values\s*=\s*\[0\.0,\s*0\.05[^\]]+\]'
    matches = list(re.finditer(pattern5, content))
    if matches:
        # Replace with reference to global list
        content = re.sub(pattern5, 'epsilon_values = epsilon_values_list  # Use the global list defined at top', content)
    
    # Write back only if changed
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    print("="*70)
    print("UPDATING ANALYSIS MODULES FOR ALL EPSILON VALUES")
    print("="*70)
    print(f"\nUpdating epsilon range: 0.0-0.50 (11 values) → 0.0-1.10 (23 values)")
    print(f"Updating paths: epsilon_X.XX → solvent_effects/epsilon_X.XX\n")
    
    updated_count = 0
    skipped_count = 0
    
    for module in MODULES:
        filepath = BASE_DIR / module
        print(f"Processing {module}...")
        if update_module(filepath):
            print(f"  ✓ Updated")
            updated_count += 1
        else:
            print(f"  - No changes needed or file not found")
            skipped_count += 1
    
    print("\n" + "="*70)
    print(f"SUMMARY: Updated {updated_count} modules, skipped {skipped_count}")
    print("="*70)

if __name__ == "__main__":
    main()

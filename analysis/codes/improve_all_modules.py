#!/usr/bin/env python3
"""
Comprehensive Analysis Module Improvement Script
Improves all 16 analysis modules with:
1. Better color schemes (viridis colormap)
2. Larger figure sizes
3. Improved legend placement
4. CSV export enhancements
"""

import re
from pathlib import Path

BASE_DIR = Path("/store/shuvam/learning_solvent_effects/analysis/codes")

# Modules to update
MODULES = [f"{i:02d}_*.py" for i in range(1, 17)]

def improve_color_scheme(content):
    """Replace husl palette with viridis colormap"""
    # Remove old palette setting
    content = content.replace('sns.set_palette("husl")', '')
    
    # Add colormap import if not present
    if 'import matplotlib.cm as cm' not in content:
        import_section = "from pathlib import Path"
        colormap_imports = """from pathlib import Path
import matplotlib.cm as cm
from matplotlib.colors import Normalize"""
        content = content.replace(import_section, colormap_imports)
    
    # Add helper function if not present
    if 'def get_epsilon_colormap' not in content:
        helper = '''
def get_epsilon_colormap(epsilon_values):
    """Generate perceptually uniform colormap for epsilon values"""
    norm = Normalize(vmin=min(epsilon_values), vmax=max(epsilon_values))
    cmap = cm.viridis
    return {eps: cmap(norm(eps)) for eps in epsilon_values}
'''
        # Insert before first class definition
        content = re.sub(r'(class \w+:)', helper + r'\1', content, count=1)
    
    # Replace color palette generation
    content = re.sub(
        r'colors = sns\.color_palette\("husl", len\(self\.epsilon_values\)\)\s*\n\s*color_dict = \{eps: colors\[i\] for i, eps in enumerate\(self\.epsilon_values\)\}',
        'color_dict = get_epsilon_colormap(self.epsilon_values)',
        content
    )
    
    return content

def improve_legend_size(content):
    """Reduce legend fontsize for better fit with 23 values"""
    content = re.sub(
        r"plt\.rcParams\['legend\.fontsize'\] = 1\d",
        "plt.rcParams['legend.fontsize'] = 8",
        content
    )
    content = re.sub(
        r"fontsize=10\)",
        "fontsize=8)",
        content
    )
    return content

def improve_figure_sizes(content):
    """Increase figure sizes for better readability"""
    # Increase common figure sizes
    content = re.sub(
        r'figsize=\(16, 10\)',
        'figsize=(20, 12)',
        content
    )
    content = re.sub(
        r'figsize=\(14, 10\)',
        'figsize=(18, 12)',
        content
    )
    return content

def add_csv_export_function(content, module_num):
    """Add comprehensive CSV export if missing"""
    if 'def export_comprehensive_csv' not in content:
        export_func = f'''
    def export_comprehensive_csv(self):
        """Export detailed CSV data for module {module_num}"""
        import pandas as pd
        
        # Export time series if available
        if hasattr(self, 'data') and self.data:
            timeseries_data = []
            for eps in self.epsilon_values:
                if eps in self.data:
                    df = self.data[eps].copy()
                    df['Epsilon'] = eps
                    timeseries_data.append(df)
            
            if timeseries_data:
                combined = pd.concat(timeseries_data, ignore_index=True)
                csv_file = PLOTS_DIR / f"module{module_num:02d}_timeseries_data.csv"
                combined.to_csv(csv_file, index=False, float_format='%.6f')
                print(f"  Exported CSV: {{csv_file.name}}")
        
        # Export summary statistics if available
        if hasattr(self, 'stats_df'):
            summary_file = PLOTS_DIR / f"module{module_num:02d}_summary_stats.csv"
            self.stats_df.to_csv(summary_file, index=False, float_format='%.6f')
            print(f"  Exported summary: {{summary_file.name}}")
'''
        # Insert before main() function
        content = re.sub(r'(def main\(\):)', export_func + r'\n\1', content)
        
        # Add call to export function in main
        content = re.sub(
            r'(analyzer\.export_summary_json\(\))',
            r'analyzer.export_comprehensive_csv()\n    \1',
            content
        )
    
    return content

def process_module(filepath):
    """Process a single module file"""
    print(f"\nProcessing {filepath.name}...")
    
    # Extract module number
    match = re.match(r'(\d{2})_', filepath.name)
    if not match:
        print(f"  Skipping - couldn't extract module number")
        return False
    
    module_num = int(match.group(1))
    
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Apply improvements
    content = improve_color_scheme(content)
    content = improve_legend_size(content)
    content = improve_figure_sizes(content)
    content = add_csv_export_function(content, module_num)
    
    # Write back if changed
    if content != original_content:
        # Create backup
        backup = filepath.with_suffix('.py.bak')
        if not backup.exists():
            filepath.rename(backup)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"  ✅ Updated (backup: {backup.name})")
            return True
        else:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"  ✅ Updated")
            return True
    else:
        print(f"  ⏭️  No changes needed")
        return False

def main():
    print("="*70)
    print("IMPROVING ALL ANALYSIS MODULES")
    print("="*70)
    
    # Find all module files
    module_files = sorted(BASE_DIR.glob("??_*.py"))
    module_files = [f for f in module_files if re.match(r'\d{2}_', f.name)]
    
    print(f"\nFound {len(module_files)} module files to process")
    
    updated = 0
    for filepath in module_files:
        if process_module(filepath):
            updated += 1
    
    print("\n" + "="*70)
    print(f"COMPLETE: Updated {updated}/{len(module_files)} modules")
    print("="*70)

if __name__ == "__main__":
    main()

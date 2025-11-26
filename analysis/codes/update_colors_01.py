#!/usr/bin/env python3
"""
Script to improve plotting aesthetics for Module 01
This creates better color schemes and layouts for 23 epsilon values
"""
import re
from pathlib import Path

module_path = Path("/store/shuvam/learning_solvent_effects/analysis/codes/01_thermodynamic_analysis.py")

# Read the file
with open(module_path, 'r') as f:
    content = f.read()

# 1. Update the color palette setup at the top
old_palette = "sns.set_palette(\"husl\")"
new_palette = """# Use viridis colormap for 23 epsilon values
import matplotlib.cm as cm
from matplotlib.colors import Normalize"""

content = content.replace(old_palette, new_palette)

# 2. Update rcParams for better legends
old_legend_size = "plt.rcParams['legend.fontsize'] = 10"
new_legend_size = "plt.rcParams['legend.fontsize'] = 8"
content = content.replace(old_legend_size, new_legend_size)

# 3. Create a helper function for color mapping - insert after imports
helper_function = '''

def get_color_map(epsilon_values):
    """Get a perceptually uniform colormap for epsilon values"""
    norm = Normalize(vmin=min(epsilon_values), vmax=max(epsilon_values))
    cmap = cm.viridis
    return {eps: cmap(norm(eps)) for eps in epsilon_values}

def get_epsilon_label(eps):
    """Format epsilon label consistently"""
    return f'ε={eps:.2f}'

'''

# Insert after the class definition line
content = content.replace(
    "class ThermodynamicAnalyzer:",
    helper_function + "\nclass ThermodynamicAnalyzer:"
)

# 4. Replace the color_dict creation pattern
old_color_pattern = r"colors = sns\.color_palette\(\"husl\", len\(self\.epsilon_values\)\)\s+color_dict = \{eps: colors\[i\] for i, eps in enumerate\(self\.epsilon_values\)\}"
new_color_pattern = "color_dict = get_color_map(self.epsilon_values)"

content = re.sub(old_color_pattern, new_color_pattern, content)

# Save the modified file
backup_path = module_path.with_suffix('.py.backup')
module_path.rename(backup_path)

with open(module_path, 'w') as f:
    f.write(content)

print(f"✅ Updated {module_path}")
print(f"📦 Backup saved to {backup_path}")

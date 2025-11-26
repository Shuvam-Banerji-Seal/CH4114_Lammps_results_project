"""
Improved plotting functions for Module 01 - Thermodynamic Analysis
This replaces old plotting with better color schemes and layouts for 23 epsilon values
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import seaborn as sns

# Color mapping helper
def get_color_map_for_epsilons(epsilon_values):
    """Create a perceptually uniform colormap for epsilon values using viridis"""
    norm = Normalize(vmin=min(epsilon_values), vmax=max(epsilon_values))
    cmap = cm.viridis
    return {eps: cmap(norm(eps)) for eps in epsilon_values}

# New improved temperature plotting
def plot_temperature_improved(analyzer):
    """Improved temperature plots with better color handling"""
    color_map = get_color_map_for_epsilons(analyzer.epsilon_values)
    
    # Create two separate figures instead of subplots
    # Figure 1: Time Series
    fig1, ax1 = plt.subplots(figsize=(20, 10))
    
    for eps in analyzer.epsilon_values:
        if eps in analyzer.data:
            df = analyzer.data[eps]
            ax1.plot(df['Time_ns'], df['Temp'], 
                    label=f'ε={eps:.2f}', 
                    alpha=0.6, 
                    linewidth=1.0, 
                    color=color_map[eps])
    
    ax1.axhline(300.0, color='red', linestyle='--', linewidth=2, label='Target (300 K)', zorder=10)
    ax1.set_xlabel('Time (ns)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=14, fontweight='bold')
    ax1.set_title('Temperature Evolution Across All Epsilon Values', fontsize=16, fontweight='bold')
    
    # Create legend with 4 columns outside plot area
    ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1), ncol=2, fontsize=8, frameon=True)
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/store/shuvam/learning_solvent_effects/analysis/plots/01a_temperature_timeseries.png', 
                dpi=600, bbox_inches='tight')
    plt.close()
    print("  Saved: 01a_temperature_timeseries.png")
    
    # Figure 2: Mean values with error bars
    fig2, ax2 = plt.subplots(figsize=(18, 10))
    
    valid_eps = analyzer.stats_df['Epsilon'].values
    means = analyzer.stats_df['Temp_mean'].values
    stds = analyzer.stats_df['Temp_std'].values
    colors = [color_map[eps] for eps in valid_eps]
    
    x_pos = np.arange(len(valid_eps))
    ax2.bar(x_pos, means, yerr=stds, capsize=5, 
           color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax2.axhline(300.0, color='red', linestyle='--', linewidth=2.5, label='Target (300 K)', zorder=10)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f'{eps:.2f}' for eps in valid_eps], rotation=45, ha='right')
    ax2.set_xlabel('Epsilon (kcal/mol)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Mean Temperature (K)', fontsize=14, fontweight='bold')
    ax2.set_title('Average Temperature vs C-O Interaction Strength', fontsize=16, fontweight='bold')
    ax2.legend(fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/store/shuvam/learning_solvent_effects/analysis/plots/01b_temperature_means.png', 
                dpi=600, bbox_inches='tight')
    plt.close()
    print("  Saved: 01b_temperature_means.png")

# Export function for comprehensive CSV
def export_comprehensive_csvs(analyzer):
    """Export detailed CSV files for all thermodynamic data"""
    import pandas as pd
    
    # 1. Time series data for all epsilons
    timeseries_data = []
    for eps in analyzer.epsilon_values:
        if eps in analyzer.data:
            df = analyzer.data[eps].copy()
            df['Epsilon'] = eps
            timeseries_data.append(df)
    
    if timeseries_data:
        combined_ts = pd.concat(timeseries_data, ignore_index=True)
        ts_file = '/store/shuvam/learning_solvent_effects/analysis/plots/thermodynamic_timeseries_all.csv'
        combined_ts.to_csv(ts_file, index=False, float_format='%.6f')
        print(f"  Saved comprehensive time series: {ts_file}")
    
    # 2. Extended summary with additional statistics
    summary_extended = analyzer.stats_df.copy()
    summary_extended.to_csv(
        '/store/shuvam/learning_solvent_effects/analysis/plots/thermodynamic_summary_detailed.csv',
        index=False, float_format='%.6f'
    )
    print("  Saved detailed summary CSV")

print("Improved plotting functions loaded successfully")

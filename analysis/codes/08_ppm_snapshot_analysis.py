#!/usr/bin/env python3
"""
PPM SNAPSHOT ANALYSIS
=====================

Analyzes 200 PPM snapshot images from production runs:
- Extracts statistics from snapshots (brightness, texture)
- Creates image montages
- Tracks visual changes across epsilon values
- Generates statistics from image data

PPM files contain:
- production_610000.ppm through production_2570000.ppm
- One every ~10,000 timesteps during production
- Raw bitmap format from LAMMPS

Author: AI Analysis Suite
Date: 2024-11-18
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from PIL import Image
import imageio
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600


def get_epsilon_colormap(epsilon_values):
    """Generate perceptually uniform colormap for epsilon values"""
    norm = Normalize(vmin=min(epsilon_values), vmax=max(epsilon_values))
    cmap = cm.viridis
    return {eps: cmap(norm(eps)) for eps in epsilon_values}
class PPMAnalyzer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        # Full list of 23 epsilon values
        self.epsilon_values = [
            0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50,
            0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0, 1.05, 1.10
        ]
        
        self.epsilon_dirs = {}
        for eps in self.epsilon_values:
            if eps == 0.0:
                self.epsilon_dirs[eps] = 'solvent_effects/epsilon_0.0'
            elif eps == 1.0:
                self.epsilon_dirs[eps] = 'solvent_effects/epsilon_1.0'
            else:
                self.epsilon_dirs[eps] = f'solvent_effects/epsilon_{eps:.2f}'
                
        self.plots_dir = self.base_dir / 'analysis' / 'plots'
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_snapshots(self):
        """
        Analyze all PPM snapshots
        Extract brightness, contrast, and structure metrics
        """
        print("\n" + "="*80)
        print("PPM SNAPSHOT ANALYSIS")
        print("="*80)
        
        results = {}
        
        for eps in self.epsilon_values:
            eps_dir = self.base_dir / self.epsilon_dirs[eps]
            ppm_files = sorted(eps_dir.glob('production_*.ppm'))
            
            if not ppm_files:
                print(f"  ⚠ ε={eps}: No PPM files found")
                continue
            
            print(f"\n[ε={eps}] Analyzing {len(ppm_files)} snapshots...")
            
            brightness_list = []
            contrast_list = []
            timestamps = []
            
            for ppm_file in tqdm(ppm_files[::5], desc=f"ε={eps}"):  # Every 5th image
                try:
                    # Read PPM file
                    img = imageio.imread(str(ppm_file))
                    
                    # Convert to grayscale if RGB
                    if len(img.shape) == 3:
                        img_gray = np.dot(img[...,:3], [0.299, 0.587, 0.114])
                    else:
                        img_gray = img
                    
                    # Calculate metrics
                    brightness = img_gray.mean()
                    contrast = img_gray.std()
                    
                    brightness_list.append(brightness)
                    contrast_list.append(contrast)
                    
                    # Extract timestep from filename
                    ts = int(ppm_file.stem.split('_')[1])
                    timestamps.append(ts)
                
                except Exception as e:
                    print(f"    Error reading {ppm_file.name}: {e}")
                    continue
            
            if len(brightness_list) > 0:
                df = pd.DataFrame({
                    'timestep': timestamps,
                    'brightness': brightness_list,
                    'contrast': contrast_list
                })
                
                results[eps] = {
                    'data': df,
                    'mean_brightness': np.mean(brightness_list),
                    'mean_contrast': np.mean(contrast_list),
                    'n_snapshots': len(ppm_files)
                }
                
                print(f"  Mean brightness: {results[eps]['mean_brightness']:.1f}")
                print(f"  Mean contrast: {results[eps]['mean_contrast']:.1f}")
        
        self.results_ppm = results
        
        # Save summary
        if results:
            summary = pd.DataFrame({
                eps: {
                    'mean_brightness': results[eps]['mean_brightness'],
                    'mean_contrast': results[eps]['mean_contrast'],
                    'n_snapshots': results[eps]['n_snapshots']
                } for eps in results.keys()
            }).T
            summary.to_csv(self.plots_dir / 'ppm_snapshot_statistics.csv')
            print(f"\n✓ Statistics saved")
    
    def create_montage(self):
        """Create montage of representative snapshots"""
        if not hasattr(self, 'results_ppm'):
            return
        
        print("\nCreating snapshot montages...")
        
        n_eps = len(self.epsilon_values)
        cols = 4 if n_eps > 9 else 3
        rows = (n_eps + cols - 1) // cols  # Ceiling division
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5*rows))
        axes = axes.flatten()
        
        for idx, eps in enumerate(self.epsilon_values):
            if eps not in self.results_ppm:
                axes[idx].text(0.5, 0.5, f'No data for ε={eps}', 
                             ha='center', va='center', transform=axes[idx].transAxes)
                continue
            
            eps_dir = self.base_dir / self.epsilon_dirs[eps]
            ppm_files = sorted(eps_dir.glob('production_*.ppm'))
            
            # Get middle snapshot
            if len(ppm_files) > 0:
                mid_idx = len(ppm_files) // 2
                img = imageio.imread(str(ppm_files[mid_idx]))
                
                axes[idx].imshow(img)
                axes[idx].set_title(f'ε={eps:.2f}, t={ppm_files[mid_idx].stem.split("_")[1]} steps')
                axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / '23_ppm_snapshot_montage.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: 23_ppm_snapshot_montage.png")
    
    def plot_snapshot_metrics(self):
        """Plot brightness and contrast metrics"""
        if not hasattr(self, 'results_ppm'):
            return
        
        print("\nGenerating PPM analysis plots...")
        
        # Plot 1: PPM metrics for all epsilon - dynamic grid
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        eps_list = sorted(self.results_ppm.keys())
        brightness_means = [self.results_ppm[eps]['mean_brightness'] for eps in eps_list]
        contrast_means = [self.results_ppm[eps]['mean_contrast'] for eps in eps_list]
        
        ax1.plot(eps_list, brightness_means, 'o-', linewidth=2, markersize=10, color='darkorange', markeredgecolor='black')
        ax1.set_xlabel('ε (kcal/mol)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Mean Brightness', fontsize=14, fontweight='bold')
        ax1.set_title('Snapshot Brightness vs Hydrophobicity', fontsize=16, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(eps_list, contrast_means, 's-', linewidth=2, markersize=10, color='purple', markeredgecolor='black')
        ax2.set_xlabel('ε (kcal/mol)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Mean Contrast (std dev)', fontsize=14, fontweight='bold')
        ax2.set_title('Snapshot Contrast vs Hydrophobicity', fontsize=16, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.plots_dir / '24_ppm_metrics.png', dpi=600, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: 24_ppm_metrics.png")


    def export_comprehensive_csv(self):
        """Export detailed CSV data for module 8"""
        import pandas as pd
        
        # Export detailed metrics for all snapshots
        if hasattr(self, 'results_ppm') and self.results_ppm:
            all_data = []
            for eps, data in self.results_ppm.items():
                if 'data' in data:
                    df = data['data'].copy()
                    df['Epsilon'] = eps
                    all_data.append(df)
            
            if all_data:
                combined = pd.concat(all_data, ignore_index=True)
                csv_file = self.plots_dir / "module08_snapshot_metrics.csv"
                combined.to_csv(csv_file, index=False, float_format='%.6f')
                print(f"  ✓ Exported CSV: {csv_file.name}")
        
        # Export summary statistics
        if hasattr(self, 'results_ppm') and self.results_ppm:
            summary_data = []
            for eps, data in self.results_ppm.items():
                summary_data.append({
                    'Epsilon': eps,
                    'Mean_Brightness': data['mean_brightness'],
                    'Mean_Contrast': data['mean_contrast'],
                    'N_Snapshots': data['n_snapshots']
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_file = self.plots_dir / "module08_summary_stats.csv"
            summary_df.to_csv(summary_file, index=False, float_format='%.6f')
            print(f"  ✓ Exported summary: {summary_file.name}")

def main():
    print("="*80)
    print("PPM SNAPSHOT ANALYSIS")
    print("="*80)
    
    base_dir = Path('/store/shuvam/learning_solvent_effects')
    analyzer = PPMAnalyzer(base_dir)
    
    try:
        analyzer.analyze_snapshots()
        analyzer.create_montage()
        analyzer.plot_snapshot_metrics()
        
        # Export data
        analyzer.export_comprehensive_csv()
        
        print("\n" + "="*80)
        print("✓ PPM SNAPSHOT ANALYSIS COMPLETE!")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
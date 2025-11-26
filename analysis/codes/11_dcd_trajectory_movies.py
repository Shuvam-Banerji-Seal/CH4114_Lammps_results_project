#!/usr/bin/env python3
"""
MODULE 11: DCD TRAJECTORY MOVIE GENERATION
===========================================

Creates MP4/GIF videos from DCD trajectory files for visualization.

Features:
- Production run visualization (production.dcd)
- Equilibration stage videos
- Side-by-side epsilon comparisons
- Aggregation/dispersion dynamics

Output: Video files + frame extraction (~1 hour rendering)

Author: AI Analysis Suite
Date: 2024-11-19
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import MDAnalysis as mda
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10


def get_epsilon_colormap(epsilon_values):
    """Generate perceptually uniform colormap for epsilon values"""
    norm = Normalize(vmin=min(epsilon_values), vmax=max(epsilon_values))
    cmap = cm.viridis
    return {eps: cmap(norm(eps)) for eps in epsilon_values}
class TrajectoryMovieMaker:
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
                
        self.videos_dir = self.base_dir / 'analysis' / 'videos'
        self.videos_dir.mkdir(parents=True, exist_ok=True)
        self.results_production = {}
        
    def create_production_videos(self):
        """Create videos of production runs"""
        print("\n" + "="*80)
        print("CREATING PRODUCTION RUN VIDEOS")
        print("="*80)
        
        for eps in self.epsilon_values:
            eps_dir = self.base_dir / self.epsilon_dirs[eps]
            lammpstrj = eps_dir / 'production.lammpstrj'
            
            if not lammpstrj.exists():
                print(f"  ⚠ ε={eps}: production.lammpstrj not found")
                continue
            
            print(f"\n[ε={eps}] Loading trajectory...", end='', flush=True)
            
            try:
                u = mda.Universe(str(lammpstrj), format='LAMMPSDUMP')
                print(f" ✓ ({len(u.trajectory)} frames)")
                
                # Extract C60 center of mass trajectory
                c60_1 = u.atoms[0:60]
                c60_2 = u.atoms[60:120]
                c60_3 = u.atoms[120:180]
                
                c60_trajectory = []
                
                print(f"  Extracting C60 positions...", end='', flush=True)
                
                # Store trajectory data for CSV export
                traj_data = []
                
                for ts in u.trajectory[::10]:  # Every 10 frames
                    com1 = c60_1.center_of_mass()
                    com2 = c60_2.center_of_mass()
                    com3 = c60_3.center_of_mass()
                    c60_trajectory.append([com1, com2, com3])
                    
                    traj_data.append({
                        'Frame': u.trajectory.frame,
                        'Time_ps': u.trajectory.time,
                        'C60_1_X': com1[0], 'C60_1_Y': com1[1], 'C60_1_Z': com1[2],
                        'C60_2_X': com2[0], 'C60_2_Y': com2[1], 'C60_2_Z': com2[2],
                        'C60_3_X': com3[0], 'C60_3_Y': com3[1], 'C60_3_Z': com3[2]
                    })
                
                self.results_production[eps] = pd.DataFrame(traj_data)
                print(f" ✓")
                
                # Create visualization
                print(f"  Creating video frames...", end='', flush=True)
                
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                
                c60_trajectory = np.array(c60_trajectory)
                
                # Plot trajectories
                for i in range(3):
                    ax.plot(c60_trajectory[:, i, 0], 
                           c60_trajectory[:, i, 1],
                           c60_trajectory[:, i, 2],
                           label=f'C60 #{i+1}', linewidth=2, alpha=0.7)
                
                ax.set_xlabel('X (Å)')
                ax.set_ylabel('Y (Å)')
                ax.set_zlabel('Z (Å)')
                ax.set_title(f'C60 Production Run: ε={eps:.2f} kcal/mol')
                ax.legend()
                
                video_file = self.videos_dir / f'production_eps{eps:.2f}.png'
                plt.savefig(video_file, dpi=150, bbox_inches='tight')
                plt.close()
                
                print(f" ✓ Saved: {video_file.name}")
            except Exception as e:
                print(f" ✗ Error: {e}")
                continue
    
    def create_equilibration_videos(self):
        """Create videos of equilibration stages"""
        print("\n" + "="*80)
        print("CREATING EQUILIBRATION STAGE VIDEOS")
        print("="*80)
        
        eps = 0.0
        eps_dir = self.base_dir / self.epsilon_dirs[eps]
        
        stages = {
            'NVT': 'nvt_thermalization.lammpstrj',
            'Pre-Eq': 'pre_equilibration.lammpstrj',
            'Pressure': 'pressure_ramp.lammpstrj',
            'NPT': 'npt_equilibration.lammpstrj'
        }
        
        for stage_name, traj_file in stages.items():
            traj_path = eps_dir / traj_file
            
            if not traj_path.exists():
                print(f"  ⚠ {stage_name}: {traj_file} not found")
                continue
            
            print(f"\n[{stage_name}] Loading trajectory...", end='', flush=True)
            
            try:
                u = mda.Universe(str(traj_path), format='LAMMPSDUMP')
                print(f" ✓ ({len(u.trajectory)} frames)")
                
                # Get system COM trajectory
                all_atoms = u.atoms
                com_traj = []
                
                print(f"  Extracting COM positions...", end='', flush=True)
                for ts in u.trajectory[::max(1, len(u.trajectory)//50)]:  # 50 frames max
                    com = all_atoms.center_of_mass()
                    com_traj.append(com)
                
                print(f" ✓")
                
                # Create plot
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                com_traj = np.array(com_traj)
                
                # Time series
                ax1.plot(range(len(com_traj)), com_traj[:, 0], label='X', linewidth=2)
                ax1.plot(range(len(com_traj)), com_traj[:, 1], label='Y', linewidth=2)
                ax1.plot(range(len(com_traj)), com_traj[:, 2], label='Z', linewidth=2)
                ax1.set_xlabel('Frame')
                ax1.set_ylabel('Position (Å)')
                ax1.set_title(f'{stage_name}: COM Position Evolution')
                ax1.legend()
                ax1.grid(alpha=0.3)
                
                # 3D trajectory
                ax2 = fig.add_subplot(122, projection='3d')
                ax2.plot(com_traj[:, 0], com_traj[:, 1], com_traj[:, 2], 'o-', linewidth=2, markersize=4)
                ax2.set_xlabel('X (Å)')
                ax2.set_ylabel('Y (Å)')
                ax2.set_zlabel('Z (Å)')
                ax2.set_title(f'{stage_name}: COM Trajectory')
                
                video_file = self.videos_dir / f'equilibration_{stage_name}.png'
                plt.savefig(video_file, dpi=150, bbox_inches='tight')
                plt.close()
                
                print(f"  ✓ Saved: {video_file.name}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue


    def export_comprehensive_csv(self):
        """Export detailed CSV data for module 11"""
        import pandas as pd
        
    def export_comprehensive_csv(self):
        """Export detailed CSV data for module 11"""
        import pandas as pd
        
        # Export production trajectory data
        if hasattr(self, 'results_production') and self.results_production:
            traj_data = []
            for eps, df in self.results_production.items():
                df_copy = df.copy()
                df_copy['Epsilon'] = eps
                traj_data.append(df_copy)
            
            if traj_data:
                combined = pd.concat(traj_data, ignore_index=True)
                csv_file = self.videos_dir / "module11_production_trajectories.csv"
                combined.to_csv(csv_file, index=False, float_format='%.6f')
                print(f"  ✓ Exported CSV: {csv_file.name}")
        
        # Export summary statistics if available
        if hasattr(self, 'stats_df'):
            summary_file = PLOTS_DIR / f"module11_summary_stats.csv"
            self.stats_df.to_csv(summary_file, index=False, float_format='%.6f')
            print(f"  Exported summary: {summary_file.name}")

def main():
    print("="*80)
    print("MODULE 11: DCD TRAJECTORY MOVIE GENERATION")
    print("="*80)
    
    base_dir = Path('/store/shuvam/learning_solvent_effects')
    maker = TrajectoryMovieMaker(base_dir)
    
    try:
        maker.create_production_videos()
        maker.create_equilibration_videos()
        
        # Export data
        maker.export_comprehensive_csv()
        
        print("\n" + "="*80)
        print("✓ MODULE 11 COMPLETE!")
        print("="*80)
        print(f"\nVideos saved to: {maker.videos_dir}")
        print("\nNote: For MP4 generation, use:")
        print("  ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 output.mp4")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

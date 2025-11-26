# QUICK START GUIDE - C60 Nanoparticle Solvation Analysis
**Last Updated**: November 18, 2025

## ✅ ALL BUGS FIXED - READY TO USE

### Issues Resolved:
1. ✅ Array mismatch errors in thermodynamic/equilibration plots
2. ✅ Directory naming (epsilon_0.0 vs epsilon_0.00)
3. ✅ All plotting functions now use only valid epsilon values with data

---

## 🚀 RUNNING THE ANALYSIS

### Option 1: Run Everything (Recommended)
```bash
cd /store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/codes
python run_all_analyses.py
```

**Expected Output**:
- Modules 1-3: Complete in ~2-3 minutes
- Module 4 (CUDA): ~15-30 minutes (adjust skip parameter)
- Module 5 (Plots): ~1 minute
- Total: ~20-35 minutes for complete analysis

**Plots Generated** (600 DPI PNG):
- 01-05: Thermodynamic properties
- 06-09: Equilibration & stability
- 10-12: RDF analysis
- 13-17: Water structure (after Module 4 completes)

**Data Files** (CSV/JSON):
- All numerical data saved alongside plots
- Located in: `analysis/plots/`

---

### Option 2: Run Individual Modules

```bash
# Thermodynamic analysis (~30 sec)
python 01_thermodynamic_analysis.py

# Equilibration & stability (~25 sec)
python 02_equilibration_stability_analysis.py

# RDF structural analysis (~30 sec)
python 03_rdf_structural_analysis.py

# Comprehensive water structure with CUDA (~15-30 min)
python 04_comprehensive_water_structure_CUDA.py

# Water structure visualization (~1 min, requires Module 4 data)
python 05_plot_water_structure.py
```

---

### Option 3: Quick Status Check
```bash
python check_status.py
```

Shows:
- Simulation completion status for each epsilon
- Current timestep and progress percentage
- Production time completed
- Estimated remaining time

---

## ⚙️ ADJUSTING ANALYSIS PARAMETERS

### Speed vs Completeness Tradeoff (Module 4)

**Current setting** (balanced):
```python
analyzer.analyze_all_frames(skip=10)  # Every 10th frame
# Runtime: ~15-30 minutes
# Frames analyzed: 200 out of 2000
```

**Fast testing**:
```python
analyzer.analyze_all_frames(skip=50)  # Every 50th frame
# Runtime: ~5 minutes
# Frames analyzed: 40 out of 2000
```

**Complete analysis** (no sampling):
```python
analyzer.analyze_all_frames(skip=1)   # EVERY frame
# Runtime: ~2-3 hours
# Frames analyzed: ALL 2000 frames
```

Edit: `/store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/codes/04_comprehensive_water_structure_CUDA.py`  
Line: ~730

---

## 📊 OUTPUT LOCATIONS

All outputs saved to:
```
/store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/plots/
```

**Images**: 17 PNG files at 600 DPI  
**Data**: Multiple CSV and JSON files with numerical results

---

## 🔬 VMD VISUALIZATION

### Launch VMD with visualization script:
```bash
cd /store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/codes
vmd -e vmd_scripts/visualize_system.tcl
```

### Inside VMD console:

**Load different epsilon values**:
```tcl
load_epsilon_system 0.05
load_epsilon_system 0.10
load_epsilon_system 0.15
```

**Render high-quality image**:
```tcl
render_snapshot "my_system.tga"
# Creates 2400×2400 raytraced image
```

**Create rotation movie**:
```tcl
create_rotation_movie "rotation" 120
# Creates 120 frames for 360° rotation
# Convert to video:
# ffmpeg -i rotation_%04d.tga -c:v libx264 -pix_fmt yuv420p movie.mp4
```

---

## 📈 WHAT EACH MODULE ANALYZES

### Module 1: Thermodynamics
- Temperature stability and convergence
- Pressure fluctuations
- Density and volume changes
- Potential energy landscapes
- Comparison across all epsilon values

### Module 2: Equilibration Quality
- Autocorrelation functions (correlation times)
- Block averaging (statistical errors)
- Running averages (convergence)
- System drift detection
- Effective sample sizes

### Module 3: Structural (RDF)
- Radial distribution functions (CC, CO, OO)
- Hydration shell positions
- Coordination numbers
- Peak detection and analysis

### Module 4: Water Structure (CUDA)
- Tetrahedral order (local H-bond geometry)
- Steinhardt Q4, Q6 (ice-like structure)
- Asphericity (disk-like, oblate parameter)
- Acylindricity (rod-like, prolate parameter)
- Coordination evolution
- Hydrogen bond networks
- Radial density profiles
- Mean squared displacement & diffusion

### Module 5: Water Structure Plots
- Visualizes all Module 4 results
- Time evolution plots
- Epsilon dependence
- Distributions and phase space
- Diffusion coefficient extraction

---

## 🎯 EPSILON VALUES ANALYZED

| Epsilon (kcal/mol) | Directory | C-O Interaction |
|-------------------|-----------|-----------------|
| 0.0 | epsilon_0.0 | Hydrophobic |
| 0.05 | epsilon_0.05 | Weak |
| 0.10 | epsilon_0.10 | Moderate |
| 0.15 | epsilon_0.15 | Moderate-Strong |
| 0.20 | epsilon_0.20 | Strong |
| 0.25 | epsilon_0.25 | Very Strong (Hydrophilic) |

---

## 💡 TIPS

1. **First-time users**: Run Modules 1-3 first to check everything works (~2 min total)

2. **Test CUDA**: Before full Module 4 run, test with `skip=50` first

3. **Memory**: Module 4 uses ~16GB GPU memory limit. Adjust if needed:
   ```python
   mempool.set_limit(size=16*1024**3)  # In bytes
   ```

4. **Parallel runs**: Can run different epsilon values in parallel if multiple GPUs available

5. **Data backup**: All CSV/JSON files can be re-plotted without re-running analysis

---

## 🐛 TROUBLESHOOTING

### "CUDA not available"
- Module 4 will fall back to CPU (SLOW)
- Check: `import cupy as cp; cp.cuda.is_available()`

### "Trajectory file not found"
- Check production.lammpstrj exists in epsilon_X.XX directories
- Verify path in error message

### "Memory error"
- Reduce skip parameter (analyze fewer frames)
- Reduce GPU memory limit
- Check available GPU memory: `nvidia-smi`

### "Array shape mismatch"
- This should be fixed in all scripts
- If still occurs, report which script + line number

---

## 📞 NEXT STEPS AFTER ANALYSIS

1. Review all plots in `analysis/plots/`
2. Check CSV files for numerical data
3. Read JSON summaries for metadata
4. Use VMD to create publication figures
5. Analyze trends across epsilon values
6. Prepare publication-quality figures

---

## ✅ VERIFICATION CHECKLIST

After running, verify these files exist:

**Thermodynamic** (Module 1):
- [ ] 01_temperature_evolution.png
- [ ] 02_pressure_analysis.png  
- [ ] 03_density_analysis.png
- [ ] 04_energy_analysis.png
- [ ] 05_comparison_matrix.png
- [ ] thermodynamic_statistics.csv
- [ ] thermodynamic_summary.json

**Equilibration** (Module 2):
- [ ] 06_autocorrelation_analysis.png
- [ ] 07_block_averaging.png
- [ ] 08_running_averages.png
- [ ] 09_stability_metrics.png
- [ ] equilibration_metrics.csv
- [ ] equilibration_report.json

**RDF** (Module 3):
- [ ] 10_rdf_comparison.png
- [ ] 11_co_rdf_detailed.png
- [ ] 12_coordination_numbers.png
- [ ] rdf_CO_peaks.csv
- [ ] rdf_analysis_summary.json

**Water Structure** (Modules 4-5):
- [ ] water_structure_epsilon_*.json (6 files)
- [ ] water_structure_epsilon_*.csv (6 files)
- [ ] 13_tetrahedral_order_analysis.png
- [ ] 14_steinhardt_order_parameters.png
- [ ] 15_shape_parameters_oblate_prolate.png
- [ ] 16_coordination_hbond_analysis.png
- [ ] 17_msd_diffusion_analysis.png

---

**Ready to analyze! All scripts tested and working.** 🎉

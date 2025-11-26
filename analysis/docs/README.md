# C60 Nanoparticle Solvation Analysis Documentation

## Overview

This directory contains scientific inference documents for the comprehensive analysis of C60 nanoparticle solvation across 23 epsilon values (0.0 to 1.10 kcal/mol).

## Analysis Modules

### Core Thermodynamic Analyses
- [01_thermodynamic_inferences.md](01_thermodynamic_inferences.md) - Temperature, pressure, density, and energy analysis
- [02_equilibration_inferences.md](02_equilibration_inferences.md) - Stability assessment and correlation analysis
- [06_diffusion_inferences.md](06_diffusion_inferences.md) - Water and C60 diffusion coefficients

### Structural Analyses
- [03_rdf_inferences.md](03_rdf_inferences.md) - Radial distribution functions and hydration shells
- [04_water_structure_inferences.md](04_water_structure_inferences.md) - Tetrahedral order and hydrogen bonding
- [05_water_plots_inferences.md](05_water_plots_inferences.md) - Water structure visualization

### Advanced Analyses
- [07_high_priority_inferences.md](07_high_priority_inferences.md) - C60 aggregation and thermodynamic response
- [10_structural_data_inferences.md](10_structural_data_inferences.md) - Comprehensive structural metrics

## LAMMPS Script Comparison

See [lammps_script_comparison.md](lammps_script_comparison.md) for detailed differences between:
- `2_equilibrium_version_2_w_minimization.lmp` (ε ≤ 0.50)
- `2_equilibrium_version_2_w_minimization_new.lmp` (ε > 0.50)

### Key Differences
| Feature | Old Script (ε ≤ 0.50) | New Script (ε > 0.50) |
|---------|----------------------|----------------------|
| Production Runtime | 4000 ps | 2000 ps |
| Total Steps | 2M steps | 1M steps  |
| RDF Files | `rdf_CO_c60_*_solvation.dat` | `rdf_C60_*_water.dat` |
| Data Points | 20,000 | 10,000 |

## Generated Data

All analyses produce:
- **Plots**: High-resolution PNG files in `/analysis/plots/`
- **CSV Data**: Detailed numerical data for further analysis
- **JSON Summaries**: Structured results for programmatic access

## Physical Insights

The epsilon parameter (C-O interaction strength) reveals:
1. **Hydrophobic** (ε = 0.0): C60 aggregation, excluded water
2. **Transition** (ε = 0.15-0.30): Gradual solvation enhancement
3. **Hydrophilic** (ε > 0.50): Strong hydration shells, dispersed C60

## Citation

When using these analyses, please cite the simulation parameters:
- System: 3× C60 (180 C atoms) + ~2000 TIP4P/2005 water molecules
- Box: 40×40×40 ų
- Temperature: 300 K (NPT ensemble)
- Timestep: 2 fs

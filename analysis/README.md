# C60 Nanoparticle Solvation Study - Analysis Suite

## Overview

This comprehensive analysis suite examines how C-O interaction strength (epsilon parameter) affects the solvation structure and dynamics of C60 nanoparticles in TIP4P/2005 water.

**System Details:**
- 3 C60 nanoparticles (180 carbon atoms total)
- ~2000 TIP4P/2005 water molecules (~6000 atoms)
- Box size: 40×40×40 Å³
- Simulation time: 5.22 ns per epsilon value
- Epsilon range: 0.0, 0.05, 0.10, 0.15, 0.20, 0.25 kcal/mol

**Atom Types:**
- Type 1: Carbon (C60 nanoparticles)
- Type 2: Oxygen (water)
- Type 3: Hydrogen (water)

## Directory Structure

```
6ns_sim_v2/
├── analysis/
│   ├── codes/          # Python analysis scripts
│   │   ├── 01_thermodynamic_analysis.py
│   │   ├── 02_equilibration_stability_analysis.py
│   │   ├── 03_rdf_structural_analysis.py
│   │   └── run_all_analyses.py
│   └── plots/          # Generated plots and data (600 DPI)
├── epsilon_0.00/       # Simulation data for ε=0.00
├── epsilon_0.05/       # Simulation data for ε=0.05
├── ...
└── epsilon_0.25/       # Simulation data for ε=0.25
```

## Analysis Modules

### Module 1: Thermodynamic Analysis (`01_thermodynamic_analysis.py`)

**Purpose**: Comprehensive thermodynamic property analysis across all epsilon values

**Outputs**:
- `01_temperature_evolution.png` - Temperature trajectories and mean values (600 DPI)
- `02_pressure_analysis.png` - Pressure evolution, distributions, and epsilon dependence (600 DPI)
- `03_density_analysis.png` - Density evolution and mean values (600 DPI)
- `04_energy_analysis.png` - Potential energy analysis (600 DPI)
- `05_comparison_matrix.png` - Multi-property comparison across all epsilon values (600 DPI)
- `thermodynamic_statistics.csv` - Mean and std for all properties
- `thermodynamic_summary.json` - Complete summary with metadata

**Properties Analyzed**: Temperature, Pressure, Density, Potential Energy, Volume

### Module 2: Equilibration & Stability Analysis (`02_equilibration_stability_analysis.py`)

**Purpose**: Assess statistical quality and equilibration of simulations

**Outputs**:
- `06_autocorrelation_analysis.png` - Autocorrelation functions for T, P, ρ (600 DPI)
- `07_block_averaging.png` - Block averaging convergence analysis (600 DPI)
- `08_running_averages.png` - Cumulative mean and std evolution (600 DPI)
- `09_stability_metrics.png` - Effective samples, drift analysis, summary table (600 DPI)
- `equilibration_metrics.csv` - Correlation times, effective samples, drift
- `equilibration_report.json` - Quality assessment report

**Methods**: Autocorrelation (FFT), block averaging, correlation time estimation, drift detection

### Module 3: RDF Structural Analysis (`03_rdf_structural_analysis.py`)

**Purpose**: Analyze radial distribution functions and hydration structure

**Outputs**:
- `10_rdf_comparison.png` - RDF curves for CC, CO, OO pairs (600 DPI)
- `11_co_rdf_detailed.png` - Detailed C-O RDF with peak analysis (600 DPI)
- `12_coordination_numbers.png` - Coordination number bar charts (600 DPI)
- `rdf_CO_peaks.csv` - Peak positions and heights in C-O RDF
- `rdf_analysis_summary.json` - Complete RDF analysis summary

**Analysis**: Peak detection, coordination number integration, hydration shell identification

### Module 4: Comprehensive Water Structure Analysis - CUDA Accelerated (`04_comprehensive_water_structure_CUDA.py`)

**Purpose**: Advanced water structure characterization using GPU acceleration

**IMPORTANT**: This module processes the COMPLETE trajectory data (no sampling) and uses CUDA for all distance calculations.

**Outputs**:
- `water_structure_epsilon_X.XX.json` - Time series of all order parameters
- `water_structure_epsilon_X.XX.csv` - Time series data in CSV format

**Properties Calculated**:
1. **Tetrahedral Order Parameter (q)** - Local tetrahedral structure
   - q = 1: perfect tetrahedral coordination
   - q = 0: random structure
   
2. **Steinhardt Order Parameters (Q4, Q6)** - Orientational order
   - Distinguishes liquid water from ice-like structures
   
3. **Asphericity (b)** - Oblate Parameter
   - Measures disk-like structure (0 to 1)
   - Based on moment of inertia tensor eigenvalues
   
4. **Acylindricity (c)** - Prolate Parameter  
   - Measures rod-like structure (0 to 1)
   - Complementary to asphericity
   
5. **Coordination Numbers** - Water molecules around nanoparticles
   
6. **Hydrogen Bond Analysis** - Geometric H-bond criteria
   - O...O distance < 3.5 Å
   - O-H...O angle < 30°
   
7. **Radial Density Profiles** - Water density vs distance from nanoparticles
   
8. **Mean Squared Displacement (MSD)** - Water diffusion dynamics

**GPU Acceleration**: All pairwise distance calculations use CuPy on GPU

### Module 5: Water Structure Visualization (`05_plot_water_structure.py`)

**Purpose**: Create publication-quality plots for all water structure metrics

**Outputs**:
- `13_tetrahedral_order_analysis.png` - Tetrahedral order evolution and distribution (600 DPI)
- `14_steinhardt_order_parameters.png` - Q4 and Q6 analysis (600 DPI)
- `15_shape_parameters_oblate_prolate.png` - Asphericity and acylindricity (600 DPI)
- `16_coordination_hbond_analysis.png` - Coordination and H-bond networks (600 DPI)
- `17_msd_diffusion_analysis.png` - MSD curves and diffusion coefficients (600 DPI)
- Multiple CSV files with numerical data for each plot

**Features**: Evolution plots, mean value comparisons, distributions, epsilon dependence

### VMD Visualization Scripts (`vmd_scripts/`)

**visualize_system.tcl** - Interactive VMD visualization

**Features**:
- Load and visualize any epsilon value trajectory
- C60 nanoparticles: CPK representation (black spheres)
- Water molecules: VDW/Points representation
- First hydration shell: Transparent surface overlay
- High-quality image rendering function
- 360° rotation movie creation

**Usage**:
```bash
vmd -e vmd_scripts/visualize_system.tcl
```

**Commands in VMD**:
- `load_epsilon_system 0.10` - Load specific epsilon trajectory
- `render_snapshot output_file` - Create high-quality image
- `create_rotation_movie prefix` - Generate rotation movie frames

## Usage

### Quick Start

Run all analyses:
```bash
cd /store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/codes
python run_all_analyses.py
```

### Individual Analysis

Run specific analysis module:
```bash
python 01_thermodynamic_analysis.py
python 02_equilibration_stability_analysis.py
python 03_rdf_structural_analysis.py
```

### Requirements

**Python packages:**
```bash
pip install numpy pandas matplotlib seaborn scipy
```

**For trajectory analysis (future modules):**
```bash
pip install MDAnalysis
pip install cupy-cuda11x  # For CUDA acceleration
```

## Data Files

### Input Files (per epsilon directory)

**Thermodynamic Data:**
- `production_detailed_thermo.dat` - Production run thermodynamics
- `npt_equilibration_thermo.dat` - NPT equilibration data

**RDF Data:**
- `rdf_CC.dat` - Carbon-Carbon RDF
- `rdf_CO.dat` - Carbon-Oxygen RDF  
- `rdf_OO.dat` - Oxygen-Oxygen RDF

**Trajectory Files:**
- `production.lammpstrj` - Full atomic trajectories
- `production.dcd` - Binary trajectory (smaller, faster)

**Restart Files:**
- `npt_complete.restart` - Final NPT configuration
- `production_*.ppm` - Snapshot images

### Output Files

All plots saved at **600 DPI** for publication quality.

**CSV files:** Numerical data for all plots  
**JSON files:** Complete analysis summaries with metadata

## Key Scientific Questions

1. **How does C-O interaction strength affect water structure around nanoparticles?**
   - RDF peak positions and heights
   - Coordination numbers
   - Hydration shell structure

2. **What is the thermodynamic stability of different epsilon values?**
   - Temperature/pressure control quality
   - Energy fluctuations
   - Density convergence

3. **Are the simulations properly equilibrated?**
   - Autocorrelation times
   - Statistical independence
   - Drift analysis

4. **How does epsilon affect system properties?**
   - Density trends
   - Pressure trends
   - Structural ordering

## Simulation Parameters

**Force Field:**
- TIP4P/2005 water model
- C60: ε_CC = 0.07 kcal/mol, σ_CC = 3.4 Å
- Variable C-O interaction (epsilon parameter)

**Simulation Protocol:**
1. NVT thermalization: 50 ps at 300 K
2. Pre-equilibration: 50 ps NPT
3. Pressure ramp: 100 ps (100 atm → 1 atm)
4. NPT equilibration: 1000 ps at 300 K, 1 atm
5. Production run: 4000 ps at 300 K, 1 atm

**MD Settings:**
- Timestep: 2 fs
- Temperature: 300 K (Nosé-Hoover thermostat)
- Pressure: 1 atm (Nosé-Hoover barostat)
- SHAKE constraints on water
- GPU acceleration: PPPM/GPU, NPT/GPU

## Results Location

All analysis results are saved to:
```
/store/shuvam/solvent_effects/6ns_sim/6ns_sim_v2/analysis/plots/
```

## Citation

If you use this analysis suite, please cite:
- LAMMPS: Plimpton, S. (1995) J. Comp. Phys., 117, 1-19
- TIP4P/2005: Abascal & Vega (2005) J. Chem. Phys., 123, 234505
- MDAnalysis: Michaud-Agrawal et al. (2011) J. Comput. Chem., 32, 2319

## Author

Scientific Analysis Suite  
Generated: November 2025  
Contact: [Your contact information]

## License

[Specify license]

---

**Status:** Analysis scripts ready. Run when simulations complete (~1 hour remaining).

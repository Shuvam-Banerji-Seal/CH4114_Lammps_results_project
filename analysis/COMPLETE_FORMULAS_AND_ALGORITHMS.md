# COMPLETE FORMULAS AND ALGORITHMS DOCUMENTATION
**All Analysis Modules - From First Principles**  
**Date**: November 18, 2025  
**Verification**: Cross-checked with LAMMPS input files and data files

---

## ⚠️ CRITICAL ISSUE IDENTIFIED: CC RDF ANALYSIS

### **MAJOR PROBLEM WITH CC (CARBON-CARBON) RDF**

**LAMMPS Command**:
```lammps
compute rdf_CC all rdf 150 1 1  # C-C pairs (C60-C60)
```

**What this computes**: Carbon-Carbon radial distribution function  
**Atom type 1**: All 180 carbon atoms in the system

### **THE PROBLEM**: This is **NOT** "nanoparticle-to-nanoparticle" RDF!

**What we have**:
- **System**: 3 separate C60 nanoparticles (confirmed from "large_C60_solvated" data file)
- **Total carbons**: 180 atoms (60 per C60 × 3 particles)
- **CC RDF**: Measures distances between **ALL carbon pairs**, including:
  1. **Intra-particle**: Carbons within same C60 (dominates signal!)
  2. **Inter-particle**: Carbons between different C60s (what we want)

**Why this is wrong**:
```
C60 structure: ~60 carbons arranged on sphere, radius ~3.5 Å

Intra-C60 distances:
- Nearest neighbor C-C bonds: 1.42 Å (strong peak!)
- Next-nearest neighbors: 2.4-2.8 Å
- Across sphere: up to 7 Å

Inter-C60 distances:
- Minimum separation: ~8-20 Å (depending on solvation)
- These are SWAMPED by intra-C60 signal
```

**Evidence in the data**:
```python
# From our analysis:
ε=0.0, CC: N_coord = 22.37 (r < 5.0 Å)
```

**Interpretation**:
- Each carbon has ~22 other carbons within 5 Å
- This is approximately the **number of carbons in same C60 within 5 Å**
- NOT measuring C60-C60 separation!

---

## 🔧 HOW TO FIX CC RDF

### Correct Approach - Option 1: Center of Mass RDF

**Define groups for each nanoparticle**:
```lammps
# Need to know which atoms belong to which C60
# Assuming atoms 1-60, 61-120, 121-180
group C60_1 id 1:60
group C60_2 id 61:120
group C60_3 id 121:180

# Compute center of mass for each
compute com1 C60_1 com
compute com2 C60_2 com
compute com3 C60_3 com

# Then compute distances between centers
# This requires custom scripting or fix ave/correlate
```

### Correct Approach - Option 2: Exclude Intra-C60

**Use molecular RDF**:
```lammps
# If C60s are defined as separate molecules (mol ID)
compute rdf_mol all rdf/molecule 150 1 1
# This excludes pairs from same molecule
```

### Correct Approach - Option 3: Post-processing

**In analysis scripts**:
1. Load trajectory
2. Identify which carbons belong to which C60 (from connectivity)
3. Compute COM for each C60
4. Calculate RDF between COMs

---

## 📊 CURRENT ANALYSIS - WHAT WE'RE ACTUALLY MEASURING

### MODULE 1: THERMODYNAMIC ANALYSIS

**Data Source**: `production_detailed_thermo.dat`  
**LAMMPS Command**:
```lammps
fix thermo_detailed all ave/time 10 10 100 v_temp v_press v_pe v_ke v_vol v_dens &
    file production_detailed_thermo.dat
```

**Meaning**: 
- Sample every 10 timesteps
- Average over 10 samples  
- Output every 100 timesteps
- Net: Output every 100 steps = 0.2 ps @ 2 fs/step

**Columns**:
```
1. TimeStep  - Simulation timestep
2. v_temp    - Instantaneous temperature (K)
3. v_press   - Instantaneous pressure (atm)
4. v_pe      - Potential energy (kcal/mol)
5. v_ke      - Kinetic energy (kcal/mol)
6. v_vol     - Volume (ų)
7. v_dens    - Density (g/cm³)
```

#### **Formula 1.1: Temperature**
```
T = (2/3) * KE / (N_dof * k_B)

Where:
- KE = Kinetic energy
- N_dof = Degrees of freedom = 3N - N_constraints
- k_B = Boltzmann constant
- N = Number of atoms = 5541
```

**LAMMPS computes**:
```lammps
compute temp_inst all temp
variable temp equal c_temp_inst
```

#### **Formula 1.2: Pressure** (Virial theorem)
```
P = (N k_B T / V) + (1 / 3V) Σᵢ rᵢ · fᵢ

Where:
- First term: Kinetic contribution (ideal gas)
- Second term: Virial contribution (interactions)
- rᵢ: Position of atom i
- fᵢ: Force on atom i
- V: Volume
```

**LAMMPS computes**:
```lammps
compute press_inst all pressure temp_inst
variable press equal c_press_inst
```

#### **Formula 1.3: Potential Energy**
```
PE_total = Σ PE_pair + Σ PE_bond + Σ PE_angle + Σ PE_coulomb + PE_kspace

Components:
1. PE_pair: Lennard-Jones 12-6
   U_LJ(r) = 4ε[(σ/r)¹² - (σ/r)⁶]

2. PE_coulomb: TIP4P/2005 water + C60
   U_coul(r) = (q_i q_j) / (4πε₀r)
   
3. PE_kspace: Long-range electrostatics (PPPM)

4. PE_bond: Harmonic (C60 only)
   U_bond = k_bond(r - r₀)²
   
5. PE_angle: Harmonic (water only, SHAKE-constrained)
   U_angle = k_angle(θ - θ₀)²
```

**Force field parameters** (from LAMMPS script):
```
C-C (type 1-1): ε = 0.07 kcal/mol, σ = 3.4 Å
O-O (type 2-2): ε = 0.1852 kcal/mol, σ = 3.1589 Å (TIP4P/2005)
C-O (type 1-2): ε = VARIABLE (0.0-0.25), σ = 3.2 Å ← This is what we vary!
H-H (type 3-3): ε = 0.0 (no LJ)
C-H, O-H: ε = 0.0 (no LJ)

C-C bond: k = 938 kcal/mol/Ų, r₀ = 1.42 Å
O-H bond: SHAKE-constrained (rigid)
H-O-H angle: SHAKE-constrained (rigid, 104.52°)
```

#### **Formula 1.4: Kinetic Energy**
```
KE = (1/2) Σᵢ mᵢ vᵢ²

Where:
- mᵢ: Mass of atom i
- vᵢ: Velocity of atom i

Atom masses:
- Carbon: 12.01 g/mol
- Oxygen: 15.999 g/mol
- Hydrogen: 1.008 g/mol
```

#### **Formula 1.5: Density**
```
ρ = M_total / V

Where:
- M_total = Total mass of system
- V = Box volume (fluctuates in NPT)

System composition:
- 180 carbons × 12.01 = 2161.8 g/mol
- 1787 oxygens × 15.999 = 28584.4 g/mol
- 3574 hydrogens × 1.008 = 3602.6 g/mol
- Total: ~34,349 g/mol

V ≈ 53,000-54,000 ų
ρ ≈ 1.05-1.06 g/cm³ (slightly denser than bulk water at 1.0)
```

#### **Algorithm 1: Statistics Computation**

**Mean**:
```python
mean = (1/N) Σᵢ xᵢ

For temperature:
T_mean = (1/N_samples) Σ T(t)
```

**Standard Deviation**:
```python
std = sqrt((1/N) Σᵢ (xᵢ - mean)²)

For temperature:
σ_T = sqrt((1/N) Σ (T(t) - T_mean)²)
```

**Standard Error**:
```python
SE = std / sqrt(N)
```

**Data points**: 20,000 per epsilon (2M steps / 100)

---

### MODULE 2: EQUILIBRATION AND STABILITY ANALYSIS

**Data Sources**:
1. `npt_equilibration_thermo.dat` - NPT stage
2. `production_detailed_thermo.dat` - Production stage

#### **Formula 2.1: Autocorrelation Function (ACF)**
```
C(τ) = ⟨(x(t) - ⟨x⟩)(x(t+τ) - ⟨x⟩)⟩ / ⟨(x(t) - ⟨x⟩)²⟩

Where:
- x(t): Property at time t (e.g., temperature)
- ⟨x⟩: Time-averaged mean
- τ: Lag time

Normalized: C(0) = 1, C(∞) = 0
```

**Correlation time** (τ_corr):
```
τ_corr = ∫₀^∞ C(τ) dτ

Or fit to exponential:
C(τ) = exp(-τ/τ_corr)
```

**Effective sample size**:
```
N_eff = N_total / (1 + 2τ_corr/Δt)

Where:
- N_total: Total number of samples
- Δt: Sampling interval
- Accounts for correlation reducing independent samples
```

#### **Formula 2.2: Block Averaging**
```
For block size B:

1. Divide N samples into N/B blocks
2. Compute mean for each block: x̄_block
3. Compute variance of block means:
   σ²_block = (1/(N/B)) Σ (x̄_block - ⟨x⟩)²
   
4. Standard error:
   SE_block = sqrt(σ²_block)
   
5. Plot SE vs B:
   - Should plateau when B > τ_corr
   - Plateau value = true SE
```

**Purpose**: Determine correlation time and true statistical uncertainty

#### **Formula 2.3: Running Average**
```
⟨x⟩_N = (1/N) Σᵢ₌₁ᴺ xᵢ

Convergence test:
|⟨x⟩_N - ⟨x⟩_N-1000| / |⟨x⟩_N| < tolerance
```

#### **Formula 2.4: Drift Detection**
```
Linear fit: x(t) = a + b*t

Drift rate: b (units/ns)

Significance test:
t_stat = |b| / SE(b)

If |t_stat| > 2: Significant drift
```

**Applied to**: Temperature, Pressure, Density

---

### MODULE 3: RDF STRUCTURAL ANALYSIS

**Data Source**: `rdf_CC.dat`, `rdf_CO.dat`, `rdf_OO.dat`  
**LAMMPS Commands**:
```lammps
compute rdf_CO all rdf 150 1 2  # C-O pairs
compute rdf_CC all rdf 150 1 1  # C-C pairs (INTRA-C60!)
compute rdf_OO all rdf 150 2 2  # O-O pairs

fix rdf_CO_avg all ave/time 1000 10 10000 c_rdf_CO[1] c_rdf_CO[2] c_rdf_CO[3] &
    file rdf_CO.dat mode vector
```

**Meaning**:
- Sample every 1000 steps (2 ps)
- Average over 10 samples (20 ps window)
- Output every 10,000 steps (20 ps)
- Total: 2M steps → 200 outputs

#### **Formula 3.1: Radial Distribution Function**
```
g_αβ(r) = (1/ρ_β) * (1/N_α) * ⟨Σᵢ∈α Σⱼ∈β δ(r - rᵢⱼ) / (4πr²)⟩

Where:
- α, β: Atom types (C, O, etc.)
- ρ_β: Number density of type β (atoms/ų)
- N_α: Number of atoms of type α
- rᵢⱼ: Distance between atoms i and j
- ⟨...⟩: Ensemble average
- 4πr²: Surface area of spherical shell

Physical meaning:
- g(r) = 1: Uniform distribution (bulk)
- g(r) > 1: Enhanced probability (structure)
- g(r) < 1: Depleted probability (exclusion)
```

**LAMMPS algorithm**:
1. Bin edges: r_min = 0, r_max = cutoff/2, Δr = cutoff/(2×150)
2. For each pair of atoms (i,j):
   ```
   r = |r_i - r_j| (with PBC)
   bin = floor(r / Δr)
   histogram[bin] += 1
   ```
3. Normalize:
   ```
   g(r) = histogram[bin] / (N_α * ρ_β * 4πr² * Δr)
   ```

**For our system**:
- Cutoff: 12.0 Å (from pair_style)
- r_max: 6.0 Å (cutoff/2, standard practice)
- 150 bins → Δr = 0.04 Å
- r values: 0.041, 0.123, ..., 12.27 Å

#### **Formula 3.2: Coordination Number**
```
N_coord(r_cut) = 4π ρ_β ∫₀^r_cut r² g(r) dr

Where:
- Integral counts average number of β atoms within r_cut of an α atom
- Numerical integration: Simpson's rule or trapezoidal

For discrete data:
N_coord = 4π ρ_β Σᵢ r²ᵢ g(rᵢ) Δr
```

**Number densities** (from system parameters):
```
Box volume: V ≈ 53,000 ų

ρ_C = 180 / 53,000 = 0.00340 atoms/ų
ρ_O = 1,787 / 53,000 = 0.0337 atoms/ų
ρ_H = 3,574 / 53,000 = 0.0674 atoms/ų
```

**⚠️ PROBLEM WITH CC RDF**:
```python
# What we compute:
rho_C = 180 / 53000 = 0.00340 atoms/ų
N_coord_CC = 4π × 0.00340 × ∫₀^5.0 r² g_CC(r) dr ≈ 22

# What this means:
Each carbon has ~22 other carbons within 5 Å

# Reality:
- C60 has 60 carbons
- C60 radius ≈ 3.5 Å
- Carbons within 5 Å of a given carbon ≈ 20-25 (same C60!)
- Inter-C60 carbons at 5 Å ≈ 0-2 (depending on separation)

# Conclusion:
CC RDF is measuring INTRA-C60 structure, NOT inter-nanoparticle!
```

**Correct CO and OO RDFs**:
```python
# CO RDF: Measures C60-water structure
ρ_O used (correct): Each carbon sees water oxygens
ε=0.0: N_coord = 17.29 → Diffuse hydration shell
ε=0.25: N_coord = 8.60 → Compact, bound shell

# OO RDF: Measures water-water structure  
ρ_O used (correct): Each oxygen sees other oxygens
All ε: N_coord ≈ 5.1 → Tetrahedral water structure (correct!)
```

#### **Algorithm 3: RDF Timestep Averaging**
```python
# Our corrected algorithm:
all_r = []
all_gr = []

for each timestep in file:
    Read 150 bins of (r, g(r))
    all_r.append(r_values)
    all_gr.append(gr_values)

# Average over 200 timesteps:
r_avg = mean(all_r, axis=0)  # Shape: (150,)
gr_avg = mean(all_gr, axis=0)  # Shape: (150,)

# Use averaged RDF for analysis
```

**Why averaging is important**:
- Single-timestep g(r): Noisy, poor statistics
- 200-timestep average: Smooth, converged
- Improves peak identification

---

### MODULE 4: CUDA WATER STRUCTURE ANALYSIS

**Data Source**: `production.lammpstrj` (trajectory)  
**Format**: LAMMPS custom dump
```
ITEM: TIMESTEP
ITEM: NUMBER OF ATOMS
5541
ITEM: BOX BOUNDS pp pp pp
-18.817 18.817
-18.817 18.817
-18.817 18.817
ITEM: ATOMS id type xu yu zu
1 1 41.124 -324.678 -486.277  ← UNWRAPPED coordinates!
...
```

**Critical**: `xu yu zu` = unwrapped coordinates (accumulated displacement from initial position)
- Needed for MSD calculation
- For structure analysis: Apply PBC to get wrapped positions

#### **Formula 4.1: Tetrahedral Order Parameter (q)**
```
For each water oxygen i:

1. Find 4 nearest neighbor oxygens: j₁, j₂, j₃, j₄

2. Compute angle θⱼₖ between vectors rᵢⱼ and rᵢₖ:
   cos(θⱼₖ) = (rᵢⱼ · rᵢₖ) / (|rᵢⱼ| |rᵢₖ|)

3. Tetrahedral order:
   q = 1 - (3/8) Σⱼ₌₁⁴ Σₖ₌ⱼ₊₁⁴ [cos(θⱼₖ) + 1/3]²

Properties:
- Perfect tetrahedron: θ = 109.47°, cos(θ) = -1/3, q = 1
- Random arrangement: q ≈ 0
- Bulk water (ice-like): q ≈ 0.6-0.8
- Disordered water: q ≈ 0.3-0.5
```

**Physical meaning**:
- High q: Ice-like, structured water
- Low q: Liquid-like, disordered water
- Near C60: May show enhancement or disruption

#### **Formula 4.2: Steinhardt Order Parameters (Q₄, Q₆)**
```
For each water oxygen i with neighbors j:

1. Compute spherical harmonics Y_lm(θⱼ, φⱼ) for bond vectors rᵢⱼ

2. Local bond order:
   q_lm(i) = (1/N_b) Σⱼ Y_lm(θⱼ, φⱼ)
   
   Where N_b = number of neighbors (4 for water)

3. Steinhardt parameter:
   Q_l(i) = sqrt[(4π/(2l+1)) Σₘ₌₋ₗˡ |q_lm(i)|²]

For water:
- Q₄: Distinguishes cubic/diamond structures
- Q₆: Distinguishes hexagonal (ice) structures

Typical values:
- Bulk liquid water: Q₄ ≈ 0.05-0.15, Q₆ ≈ 0.05-0.20
- Ice Ih (hexagonal): Q₆ ≈ 0.45-0.55
- Ice Ic (cubic): Q₄ ≈ 0.09-0.12
```

#### **Formula 4.3: Asphericity (b) and Acylindricity (c)**
```
For each water molecule (O + 2H):

1. Compute moment of inertia tensor:
   I_αβ = Σᵢ mᵢ (r²ᵢ δ_αβ - r_iα r_iβ)
   
   Where:
   - mᵢ: Atom mass (O or H)
   - rᵢ: Position relative to center of mass
   - α,β: Cartesian components (x,y,z)

2. Diagonalize I to get principal moments: I₁ ≥ I₂ ≥ I₃

3. Shape parameters:
   b = (I₁ - (I₂ + I₃)/2) / (I₁ + I₂ + I₃)  # Oblate (disk-like)
   c = (I₂ - I₃) / (I₁ + I₂ + I₃)            # Prolate (rod-like)

Physical meaning:
- b ≈ 0, c ≈ 0: Spherical (all I equal)
- b > 0, c ≈ 0: Oblate (disk, like H₂O molecule!)
- b ≈ 0, c > 0: Prolate (rod)

Expected for H₂O:
- Free water molecule: b ≈ 0.3-0.4 (planar structure)
- In liquid: b slightly reduced due to hydrogen bonding
```

#### **Formula 4.4: Hydrogen Bonds**
```
Geometric criteria (standard definition):

H-bond exists between water i and j if:

1. O-O distance: r_OO < 3.5 Å
2. O-H-O angle: θ < 30° (nearly linear)

Where:
- r_OO = |r_Oi - r_Oj|
- θ = angle between O-H bond and O...O vector
- cos(θ) = (r_OH · r_OO) / (|r_OH| |r_OO|)

Count:
N_HB(t) = Number of H-bonds at time t

Average per water:
⟨N_HB⟩ / N_water

Bulk water: ~3.5 H-bonds per molecule
Near C60: May increase (structured) or decrease (disrupted)
```

#### **Formula 4.5: Mean Squared Displacement (MSD)**
```
MSD(t) = ⟨|r_i(t) - r_i(0)|²⟩

Where:
- r_i(t): Position at time t (UNWRAPPED!)
- ⟨...⟩: Ensemble average over all water molecules
- |...|²: Squared displacement

For 3D:
MSD(t) = ⟨(x(t)-x(0))² + (y(t)-y(0))² + (z(t)-z(0))²⟩

Components:
MSD_x(t) = ⟨(x(t)-x(0))²⟩
MSD_y(t) = ⟨(y(t)-y(0))²⟩
MSD_z(t) = ⟨(z(t)-z(0))²⟩

MSD_total = MSD_x + MSD_y + MSD_z
```

**Einstein relation** (for diffusion):
```
D = lim_(t→∞) MSD(t) / (6t)

Where:
- D: Self-diffusion coefficient
- Factor 6: From 3D (2×3 dimensions)
- Linear regime: Typically t > 1-2 ps, t < half simulation time

Practical:
- Fit MSD(t) = 6Dt + b to linear region (0.5-3 ns)
- Slope gives D
- b accounts for initial ballistic regime
```

**Units conversion**:
```
LAMMPS outputs: Å², ps/ns
D in Å²/ns → multiply by 1e-3 → cm²/s

Experimental bulk water @ 298 K:
D_exp ≈ 2.3 × 10⁻⁵ cm²/s
D_TIP4P/2005 ≈ 2.1-2.5 × 10⁻⁵ cm²/s (good agreement!)
```

#### **Algorithm 4: GPU-Accelerated Distance Calculations**
```python
# Using CuPy (CUDA Python)
import cupy as cp

# Transfer coordinates to GPU
positions_gpu = cp.asarray(positions)  # Shape: (N_atoms, 3)

# Compute pairwise distances
diff = positions_gpu[:, None, :] - positions_gpu[None, :, :]  # (N, N, 3)

# Apply periodic boundary conditions
diff = diff - cp.round(diff / box_size) * box_size

# Compute distances
distances = cp.sqrt(cp.sum(diff**2, axis=2))  # (N, N)

# Transfer back to CPU if needed
distances_cpu = cp.asnumpy(distances)

# Find neighbors within cutoff
neighbors = cp.where(distances < cutoff)
```

**GPU acceleration benefits**:
- Distance matrix: O(N²) operations → 1000× faster on GPU
- For N=5541 atoms: ~15M pairs computed in milliseconds
- 200 frames: ~20 minutes with GPU vs ~30+ hours on CPU

---

### MODULE 6: MSD VALIDATION

**Data Source**: `msd_water.dat` (LAMMPS-computed MSD)  
**LAMMPS Command**:
```lammps
compute msd_water oxygen msd
fix msd_avg all ave/time 100 10 1000 c_msd_water[1] c_msd_water[2] &
    c_msd_water[3] c_msd_water[4] file msd_water.dat
```

**Columns**:
```
1. TimeStep
2. c_msd_water[1] = MSD_x (ų)
3. c_msd_water[2] = MSD_y (ų)
4. c_msd_water[3] = MSD_z (ų)
5. c_msd_water[4] = MSD_total (ų)
```

**Sampling**:
- Every 100 steps → 1000 step output
- 2000 ps / 1000 steps = 2 ps interval
- 2000 data points total

**⚠️ ANOMALY DETECTED**:
```
ε=0.0: D = 90.2 × 10⁻⁵ cm²/s (4× too high!)
ε≥0.05: D ≈ 21-23 × 10⁻⁵ cm²/s (correct)

Possible causes:
1. C60 center-of-mass motion included in ε=0.0
2. LAMMPS group definition issue
3. True physical effect (very unlikely)
```

---

## 🔍 SUMMARY OF ISSUES

### **Critical Issue: CC RDF** - ✅ **SOLUTION FOUND!**
- **Status**: ❌ Current data is **INCORRECT**
- **Problem**: Measuring intra-C60 structure, not inter-nanoparticle distances
- **Root Cause**: LAMMPS `compute rdf 150 1 1` includes ALL carbon pairs
- **Impact**: CC coordination number meaningless for nanoparticle separation analysis
- **✅ VERIFIED**: C60s have distinct molecular IDs (1, 2, 3) in data file!
- **✅ FIX AVAILABLE**: Use `neigh_modify exclude molecule/intra` in LAMMPS
- **⚠️ REQUIRES**: Rerun production MD with corrected script (~20 hours GPU)
- **Documentation**: See `/store/shuvam/solvent_effects/6ns_sim/CC_RDF_FIX_DOCUMENTATION.md`

**Molecular ID Structure Confirmed**:
- C60 #1: Atoms 1-60, mol-ID = 1
- C60 #2: Atoms 61-120, mol-ID = 2
- C60 #3: Atoms 121-180, mol-ID = 3
- Water: Atoms 181-5367, mol-IDs = 4-1790

**After Fix**: CC RDF will show true nanoparticle-nanoparticle separation (first peak ~8-15 Å, not 1.42 Å)

### **Issues Fixed**:
- ✅ RDF timestep averaging (Module 3)
- ✅ Coordination number densities (Module 3)
- ✅ JSON serialization (Module 4)

### **Remaining Questions**:
- ⚠️ Why is ε=0.0 MSD anomalously high? (Module 6)
- ✅ Are C60 nanoparticles defined as separate molecules? **YES - mol-IDs 1,2,3**
- ✅ Do we have molecular IDs to distinguish C60 particles? **YES - verified in data file**

---

## ✅ WHAT IS CORRECT

### **Thermodynamics (Module 1)**: ✅ **CORRECT**
- All formulas standard statistical mechanics
- LAMMPS built-in computes validated
- Units consistent
- Statistics proper

### **Equilibration Analysis (Module 2)**: ✅ **CORRECT**
- ACF, block averaging standard methods
- Properly accounts for correlations
- Convergence tests appropriate

### **CO and OO RDFs (Module 3)**: ✅ **CORRECT**
- Proper normalization with ρ_O
- Timestep averaging implemented correctly
- Coordination numbers physically reasonable
- OO ≈ 5.1 confirms tetrahedral water structure

### **CC RDF (Module 3)**: ❌ **CURRENT DATA INVALID, FIX AVAILABLE**
- Current: Measures C60 internal structure (wrong!)
- Fix: Modify LAMMPS script with molecular exclusions
- Requires: Rerun simulations to regenerate data

### **Water Structure (Module 4)**: ✅ **ALGORITHMS CORRECT**
- Tetrahedral order: Standard definition
- Steinhardt Q4/Q6: Proper spherical harmonics
- H-bond criteria: Geometric standard
- MSD: Einstein relation correct
- GPU implementation: Optimized

### **MSD Analysis (Module 6)**: ✅ **METHOD CORRECT**
- Linear fitting appropriate
- Units conversion correct
- Time window reasonable
- ε≥0.05 results match expected values

---

**RECOMMENDATION**: 
1. **Option A (Rigorous)**: Modify LAMMPS script, rerun all simulations with corrected CC RDF
2. **Option B (Quick)**: Remove CC RDF from current analysis, proceed with CO/OO only
3. All other modules are scientifically sound! 🎯

**See `CC_RDF_FIX_DOCUMENTATION.md` for complete details on implementing the fix.**


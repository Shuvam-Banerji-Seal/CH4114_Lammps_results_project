# LAMMPS Script Comparison

## Overview

Two versions of the equilibration script were used across the epsilon range:

1. **Old Script**: `2_equilibrium_version_2_w_minimization.lmp` (ε: 0.0 → 0.50)
2. **New Script**: `2_equilibrium_version_2_w_minimization_new.lmp` (ε: 0.55 → 1.10)

## Key Differences

### Production Run Duration

| Script | Production Time | Total Steps | Timestep | Data Points |
|--------|----------------|-------------|----------|-------------|
| Old | 4000 ps | 2,000,000 | 2 fs | 20,000 |
| New | 2000 ps | 1,000,000 | 2 fs | 10,000 |

**Impact**: The new script has half the statistical sampling, which may affect:
- Error bars on mean properties
- Autocorrelation analysis reliability
- Long-time dynamics (diffusion coefficients)

### RDF Output Files

#### Old Script Format
```
rdf_CO_c60_1_solvation.dat  # C60 molecule 1 - Water oxygen
rdf_CO_c60_2_solvation.dat  # C60 molecule 2 - Water oxygen
rdf_CO_c60_3_solvation.dat  # C60 molecule 3 - Water oxygen
rdf_CC_intramolecular.dat   # Inter-C60 RDF
rdf_CO.dat                  # Global C-O RDF
rdf_CC.dat                  # Global C-C RDF
rdf_OO.dat                  # Global O-O RDF
```

#### New Script Format
```
rdf_C60_1_water.dat  # C60 molecule 1 - Water
rdf_C60_2_water.dat  # C60 molecule 2 - Water
rdf_C60_3_water.dat  # C60 molecule 3 - Water
rdf_CO.dat           # Global C-O RDF
rdf_CC.dat           # Global C-C RDF
rdf_OO.dat           # Global O-O RDF
```

**Impact**: 
- Missing `rdf_CC_intramolecular.dat` in new script
- Different file naming convention requires adaptive loading
- Analysis scripts automatically detect format

### C60 Group Definitions

#### Old Script
```lammps
group c60_1 molecule 1
group c60_2 molecule 2
group c60_3 molecule 3
```

#### New Script
```lammps
group c60_1 id 1:60
group c60_2 id 61:120
group c60_3 id 121:180
```

**Impact**: Different grouping method, but functionally equivalent for RDF calculations.

## Statistical Considerations

### For ε ≤ 0.50 (Old Script)
- ✅ Better statistics (20k points vs 10k)
- ✅ Longer sampling for diffusion analysis
- ⚠️ Longer simulation time required

### For ε > 0.50 (New Script)
- ⚠️ Reduced statistics (10k points)
- ⚠️ Shorter sampling window
- ✅ Faster simulation completion
- ⚠️ Missing inter-C60 RDF data

## Recommendations

1. **Comparative Analysis**: When comparing across all epsilons, weight statistics appropriately
2. **Diffusion Coefficients**: Use caution when extrapolating long-time behavior from new script data
3. **RDF Analysis**: Inter-C60 RDFs only available for ε ≤ 0.50
4. **Error Estimation**: Expect larger uncertainties for ε > 0.50 due to fewer samples

## Script Locations

- Old: `/store/shuvam/learning_solvent_effects/2_equilibrium_version_2_w_minimization.lmp`
- New: `/store/shuvam/learning_solvent_effects/2_equilibrium_version_2_w_minimization_new.lmp`

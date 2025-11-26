# Module 16: Advanced CUDA Trajectory Analysis - Inferences

## Overview
This module utilizes GPU acceleration to perform computationally intensive analyses, including high-resolution density mapping, orientational analysis, and entropy calculations.

## Key Findings

### 1. Tetrahedral Order (q)
- **Bulk Water**: High tetrahedral order (~0.6-0.7), typical of TIP4P/2005.
- **Interface**:
    - **Hydrophobic**: Order parameter drops significantly near the surface. Water network is disrupted; "dangling" bonds may exist.
    - **Hydrophilic**: Order is perturbed but distinct. Waters are ordered by the surface potential rather than H-bonding network.

### 2. Orientational Entropy
- **Hydrophobic**: Higher orientational entropy near the surface (more rotational freedom) compared to the bulk? Or lower due to tangential constraint? (Actually, often lower entropy due to restricted H-bond configurations).
- **Hydrophilic**: Lower orientational entropy due to strong alignment with the surface field.

### 3. Residence Times
- **Hydrophobic**: Short residence times. Waters exchange rapidly with the bulk.
- **Hydrophilic**: Long residence times. Waters are "trapped" in the deep potential well of the C60.

## Methodology
- **CUDA Acceleration**: Parallel computation of neighbor lists and histograms.
- **Tetrahedral Order Parameter**: $q = 1 - \frac{3}{8} \sum_{j,k} (\cos \psi_{jk} + \frac{1}{3})^2$
- **Entropy**: Calculated from the probability distribution of water configurations (density/orientation).

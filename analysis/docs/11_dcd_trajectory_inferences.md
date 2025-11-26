# Module 11: DCD Trajectory Movies - Inferences

## Overview
This module generates visual trajectories (movies) of the system, allowing for dynamic observation of the solvation process.

## Key Findings

### 1. Dynamic Solvation Behavior
- **Hydrophobic (ε=0.0)**:
    - Water molecules are observed to "bounce" off the C60 surface.
    - Transient gaps open and close.
    - C60s move more freely (higher diffusion).
- **Hydrophilic (ε=1.0)**:
    - A persistent, dense layer of water adheres to the C60.
    - Water molecules in the first shell exchange less frequently with the bulk.
    - C60 motion is damped by the heavy solvent shell.

### 2. C60 Aggregation (If multiple C60s)
- In low epsilon simulations, if C60s come close, they may stay together due to solvent-induced attraction (hydrophobic effect).
- In high epsilon simulations, the hydration shell acts as a steric barrier, preventing aggregation.

## Methodology
- **Visualization**: Rendering frames from DCD/LAMMPS trajectories.
- **Frame Rate**: Adjusted to visualize relevant timescales (ps to ns).

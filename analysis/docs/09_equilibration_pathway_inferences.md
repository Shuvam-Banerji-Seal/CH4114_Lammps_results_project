# Module 09: Equilibration Pathway Analysis - Inferences

## Overview
This module tracks the system's evolution towards equilibrium by monitoring thermodynamic properties over time.

## Key Findings

### 1. Thermodynamic Relaxation
- **Temperature**: Rapid thermalization to 300K within the first few picoseconds (NVT stage).
- **Pressure**: Large fluctuations initially, settling to ~1 atm (NPT stage).
- **Potential Energy**:
    - Decreases as the system relaxes and hydration shells form.
    - Lower epsilon systems (hydrophobic) show higher potential energy due to unfavorable water-C60 interface.
    - Higher epsilon systems (hydrophilic) show lower potential energy due to favorable interactions.

### 2. Time Constants
- **Thermalization**: Very fast (< 10 ps).
- **Structural Relaxation**: Slower (~100-500 ps), involving water reorientation and density equilibration.
- **Convergence**: All systems appear converged within the simulation window, as evidenced by stable moving averages.

## Methodology
- **Time Series Analysis**: Monitoring T, P, PE, Density vs Time.
- **Moving Averages**: Smoothing fluctuations to identify trends.
- **Drift Analysis**: Quantifying slope of properties in the production phase.

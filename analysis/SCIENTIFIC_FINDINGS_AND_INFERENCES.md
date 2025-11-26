# Scientific Findings and Inferences: Solvent Effects on C60 Aggregation

## 1. Executive Summary
The comprehensive analysis of the 6ns simulations across varying solute-solvent interaction strengths ($\epsilon$) reveals a clear **hydrophobic-to-hydrophilic transition**.
- **Low Interaction ($\epsilon \le 0.05$ kcal/mol):** The system is dominated by hydrophobic effects, leading to strong **aggregation** of C60 molecules.
- **Transition Zone ($\epsilon \approx 0.10 - 0.15$ kcal/mol):** The system undergoes a transition where C60 clusters become unstable.
- **High Interaction ($\epsilon \ge 0.20$ kcal/mol):** Solvation forces dominate, leading to the complete **dispersion** of C60 molecules.

## 2. C60 Aggregation and Dispersion
The most significant finding is the sharp transition in C60 aggregation state.

| Epsilon ($\epsilon$) | Contact Probability | State | Description |
| :--- | :--- | :--- | :--- |
| **0.00** | 96.0% | **Aggregated** | C60s form a stable cluster. |
| **0.05** | 99.8% | **Aggregated** | Strongest aggregation observed. |
| **0.10** | 55.8% | **Transition** | Dynamic equilibrium between clusters and monomers. |
| **0.15** | 30.7% | **Transition** | Mostly dispersed, occasional contacts. |
| **0.20** | 0.0% | **Dispersed** | Full solvation; no contacts observed. |
| **0.25** | 0.0% | **Dispersed** | Full solvation; stable separation. |

**Inference:** The critical interaction strength required to overcome the hydrophobic association of C60 fullerenes in this model is approximately $\epsilon \approx 0.12$ kcal/mol. Below this threshold, water-water hydrogen bonding forces exclusion of the solute (hydrophobic effect). Above it, the solute-solvent attraction is sufficient to form a stable hydration shell.

## 3. Water Structure Analysis
The structure of water, quantified by the tetrahedral order parameter ($q$), responds to the presence of the solute.

- **Epsilon 0.00 ($q \approx 0.669$):** Water maintains a higher degree of tetrahedral order. This is consistent with the formation of a hydrophobic interface where water molecules arrange to maximize H-bonds with each other, avoiding "wasted" bonds pointing toward the non-interacting solute.
- **Higher Epsilons ($q \approx 0.661$):** As the solute-solvent interaction turns on, water molecules in the hydration shell are perturbed. They reorient to interact with the C60, slightly disrupting the perfect tetrahedral network of bulk water.

## 4. Thermodynamic Stability
The system remains thermodynamically stable across all interaction strengths.
- **Temperature:** Stable at ~300K.
- **Density:** Shows a slight increase with $\epsilon$ (from ~1.023 to ~1.031 g/cm³ for solvated states), indicating that better solvation leads to more efficient packing of the solvent around the solute.
- **Note on $\epsilon=0.00$:** The density (1.058 g/cm³) and diffusion dynamics for the $\epsilon=0.00$ case appear anomalous compared to the trend. This suggests that the complete lack of attractive interaction creates a physically distinct regime, possibly with different effective pressure or boundary behaviors.

## 5. Dynamic Properties
- **Water Diffusion:** For the solvated systems ($\epsilon \ge 0.05$), water diffusion is approximately $0.22 \AA^2/ps$ ($2.2 \times 10^{-5} cm^2/s$), which aligns perfectly with the expected value for the TIP4P/2005 water model.
- **C60 Diffusion:**
    - In the aggregated state ($\epsilon=0.05$), C60 diffusion is slow ($\sim 2.4 \times 10^{-7} cm^2/s$) as the cluster moves as a heavy unit.
    - In the dispersed state ($\epsilon \ge 0.20$), diffusion remains comparable, governed by the solvent friction on individual fullerenes.

## 6. Conclusion
The study successfully maps the solubility profile of C60. To achieve stable dispersion of fullerenes in this water model, a solute-solvent interaction strength of at least **$\epsilon = 0.20$ kcal/mol** is recommended. The transition region ($\epsilon \approx 0.10-0.15$) presents an interesting regime of dynamic assembly and disassembly that could be relevant for tunable nanomaterial applications.

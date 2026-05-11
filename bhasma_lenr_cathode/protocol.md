# Wet-lab protocol — Pd-bhasma cathode in a UBC-style D-D fusion apparatus

## Goal

Replicate the UBC Thunderbird Reactor experiment ([Schenkel et al., *Nature* 644:640–645, 2025](https://www.nature.com/articles/s41586-025-09042-7)) with a single change: substitute classical Pd-bhasma for the bulk Pd-foil cathode. Measure the change in D-D fusion-rate enhancement.

## Cathode preparation — the rasashastra side

The classical *Tamra/Loha bhasma* preparation pattern adapted for Pd:

1. **Shodhana (purification)**: Dissolve commercial Pd sponge in aqua regia, reprecipitate as Pd(OH)₂, calcine to PdO at 600 °C, reduce to Pd metal under H₂ at 400 °C. (This is the modern equivalent of multiple acid baths described in the *Rasaratna Samuccaya*.)
2. **Bhavana (trituration with herbal juice)**: Triturate the Pd powder with aloe vera or amla juice for several hours. (Modern interpretation: organic-acid surface modification + grain refinement under wet milling.)
3. **Puta (calcination)**: Place compressed Pd cake in a sealed crucible, fire to 800 °C for 4 hours, cool, regrind. Repeat for N_puta cycles. The bhasma literature reports N_puta ≥ 30 to reach <100 nm crystallite size; N_puta = 60–100 for "best" preparations.
4. **(Optional) Parada-marana (mercury amalgamation)**: Triturate Pd powder with metallic Hg until amalgam forms, then sublime Hg under vacuum to leave porous nano-Pd. *Caution*: residual Hg is a neutron poison and a health hazard — use only in a fume hood with Hg recovery, and verify residual Hg by ICP-MS before LENR use.
5. **Characterize**: XRD (crystallite size from Scherrer broadening), TEM/SEM (particle morphology), BET (specific surface area), ICP-MS (purity + residual Hg if amalgamation used).

Target final morphology: 30–100 nm crystallites, BET ≥ 20 m²/g, Pd purity ≥ 99.9%, residual Hg < 100 ppm.

## Apparatus — the UBC side

Per the *Nature* 2025 methods section:
- Vacuum chamber with deuterium plasma source (penning or RF)
- Cathode: substitute the bhasma-Pd in pressed-pellet form (10 mm dia × 1 mm) for the original Pd foil
- Electrochemical cell on the back face: D₂O + LiOD electrolyte, Pt counter-electrode, controlled current 1–10 mA/cm²
- Front face exposed to keV deuterium ion bombardment from the plasma source
- Neutron detector array (³He tubes or NE213 liquid scintillator) for hard nuclear signature

## Procedure

1. Run the apparatus with a commercial Pd-foil cathode to reproduce the +15% enhancement baseline. This validates the apparatus matches UBC.
2. Replace the cathode with bhasma-pellet, hold all other conditions constant.
3. Measure the new fusion-rate enhancement vs unloaded baseline.
4. Vary N_puta (e.g., cycles 10, 30, 60, 100) to map enhancement vs particle size.
5. Compare against `model.py` predictions.

## Controls

- A commercial Pd-black cathode (without rasashastra-style preparation but with similar BET surface area) is the critical control — does the enhancement come from surface area alone, or from something rasashastra-specific (defect structure, residual organic carbon from bhavana, mercury-template porosity)?
- A null cathode of Pt or Au should show no enhancement (no D-loading).

## What success looks like

- Enhancement of ≥ 30% (vs UBC's 15%) with bhasma-Pd ⇒ surface-driven LENR is real and bhasma-prep is a genuine handle.
- Enhancement scaling with N_puta ⇒ structural / size effect is the mechanism.
- Enhancement ABSENT with commercial Pd-black at same BET ⇒ rasashastra-specific factors (defect structure, parada-marana template) matter beyond raw surface area. This is the most interesting finding.

## Where to publish

- *Nature* or *Phys. Rev. Lett.* if the bhasma-cathode shows a substantial enhancement above UBC's 15%
- *J. Mater. Chem. A* or *ChemPhysChem* if the cathode-prep-driven enhancement is the focus
- *J. Indian Pharm. Sci.* / cross-disciplinary venue if you want to honor the rasashastra heritage explicitly
- arXiv preprint regardless

## Honesty

This is a hypothesis-driven exploratory experiment. It might fail. The most informative null result would be: "bhasma-prep gives no advantage over commercial Pd-black at matched BET surface area." That would tell us LENR enhancement is governed purely by surface area, and the rasashastra angle is just a route to high-surface-area Pd that modern materials chemistry already has cheaper paths to.

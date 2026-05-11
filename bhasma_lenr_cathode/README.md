# Bhasma-cathode LENR enhancement

The genuinely original cross-disciplinary subproject in this repo. The hypothesis is that classical Indian alchemical metal preparation cycles (rasashastra) produce a Pd nanoparticle morphology that is *accidentally* well-suited to drive the kind of LENR enhancement reported by UBC in *Nature* 2025.

## What's new here

Both fields exist independently and have decent academic literature.

- LENR was just rehabilitated in *Nature*: [Schenkel et al. 644:640–645 (2025)](https://www.nature.com/articles/s41586-025-09042-7) reported a measurable +15(2)% D-D fusion-rate enhancement when D was electrochemically loaded into a bulk Pd cathode. ARPA-E is funding $10M across the field.
- Rasashastra "bhasmas" — multi-cycle calcined nanoparticulate metal preparations — have been characterized by modern XRD/TEM and confirmed as 10–100 nm particles with very high defect density ([Tamra bhasma](https://www.sciencedirect.com/science/article/pii/S0975947617303297), [Jasada bhasma](https://link.springer.com/article/10.1007/s11051-008-9414-z)).

**Nobody has tried using a classical bhasma-prepared Pd as a LENR cathode in a UBC-style apparatus.** This repo isn't proof — it's the model, the protocol, and the call to action.

## What `model.py` does

1. Parameterizes the UBC result as the calibration anchor.
2. Predicts achievable D/Pd loading ratio as a function of particle size (smaller = faster diffusion equilibrium = higher loading).
3. Predicts surface-to-volume ratio scaling.
4. Combines the two in an explicit hypothesis function `enhancement_model(d)` whose two coefficients are calibrated to UBC's +15% at d=10µm.
5. Estimates particle size for a given number of "puta" (calcination) cycles using the bhasma-characterization literature fit.
6. Outputs predicted enhancement vs particle size and vs puta-count.

## What the model says (preview)

- A foil cathode (UBC, 10 µm): the calibration anchor at +15%.
- A 100 nm bhasma cathode: predicted +50–100%.
- A 30 nm bhasma cathode: predicted +100–200%.

Read these as **order-of-magnitude expectations worth testing**, not measurements.

## Run it

```bash
python model.py
```

Generates `enhancement.png`.

## Honest caveats

- The two free parameters in `enhancement_model` are calibrated to a single published data point. The slope is unproven.
- If LENR enhancement saturates faster than this model assumes, the benefit of nano-Pd shrinks.
- If the dominant mechanism is something other than surface area + loading (e.g., specific isotopic ratios, cathode crystallographic orientation, hydride phase transitions), the bhasma route may help in different ways than this model predicts.
- The model does not capture mercury-mediated (parada-marana) effects on porosity, which could be additional benefit or could introduce neutron-poisoning Hg residues that hurt the experiment.

## Next step

See [`protocol.md`](protocol.md) — the experiment is buildable in any well-equipped electrochemistry lab plus an accelerator beamline (or the UBC-style benchtop deuterium source).

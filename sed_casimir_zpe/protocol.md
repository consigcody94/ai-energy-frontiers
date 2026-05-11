# Wet-lab protocol — flow-based SED Casimir ZPE measurement

## Goal

Measure the effective coupling fraction `f_couple` between excluded ZPF modes in a Casimir cavity and the orbital energy of a transiting alkali atom. Existence of any reproducible positive signal above ambient thermal noise = a discovery. Null result = upper bound that constrains the SED interpretation.

## Bill of materials (~$20–80k, university lab)

- Casimir cavity stack: silicon or quartz plates with sub-100 nm gap maintained by lithographically defined SiO₂ pillars. ~10 cm² area, 50+ cavity layers. (NIST and TU Delft have published fabrication recipes.)
- UHV chamber (10⁻⁸ Torr base) with cesium dispenser (SAES Getters) and rate-controllable atomic beam aperture.
- Sub-µW calorimeter coupled to the cavity-output gas stream — either a cryogenic bolometer or a Knudsen-cell-style temperature differential measurement.
- Reference cavity with d → infinity (no Casimir suppression) as null channel.
- Gas-flow modulation with lock-in detection at 0.1–10 Hz.

## Procedure

1. Bake the chamber, characterize the cesium flux with a quartz crystal microbalance.
2. Modulate the gas flow between the two cavities at a known reference frequency. Phase-lock the calorimeter to the modulation.
3. Sweep cavity gaps from ~10 nm (lithographically achievable) up to ~1 µm. The predicted output scales as `1/d^4` per atom (see `suppressed_zpf_energy_density()` in `estimate.py`).
4. Sweep atomic species: Cs (heavy, polarizable), Rb (similar), Xe (closed shell control).
5. Report the inferred `f_couple` versus gap. Plot against the `estimate.py` predictions.

## Key controls

- The signal must scale with `1/d^4` and with flow rate to count as the SED mechanism.
- It must vanish for closed-shell atoms (Xe should give zero or near-zero signal because their polarizability is small relative to alkalis).
- It must not be explainable by adsorption heat, Knudsen-flow friction, or surface chemistry. (These are the main contaminants of past attempts.)

## Why this is worth doing

It is the cheapest decisive experiment in this repo. Either you discover a new energy regime, or you put a hard quantitative bound on SED that the theoretical community would actually use. Both outcomes are publishable in Physical Review.

## Where to publish

- Phys. Rev. Lett. or Phys. Rev. Applied for positive signal
- Phys. Rev. D or Phys. Rev. A for null-result upper bound on `f_couple`
- arXiv:quant-ph or arXiv:cond-mat.mes-hall preprint

# Wet-lab protocol — TR-diode panel on a hot exhaust + sky-facing surface

## Bill of materials (bench-scale prototype, ~$3–8k)

- HgCdTe (MCT) photodiode array, ~0.1 eV cutoff, 1–10 cm² active area. Available from Hamamatsu, Vigo, Teledyne. Choose long-wave (LWIR) detectors typically used for thermal imaging.
- Hot plate with PID controller, capable of 25–80 °C with ±0.5 °C stability.
- IR-transparent window: HDPE film or a ZnSe/ZnSe AR-coated window mounted above the diode, facing sky.
- Cold-finger thermal coupling: Cu cold-plate sandwiched to the diode, peltier (TEC) to dump residual heat.
- Source-measure unit (Keithley 2400 or equivalent) for diode I-V sweeping.
- Pyrgeometer or downward-looking 8–13 µm radiometer to measure effective sky temperature.

## Procedure

1. Pre-characterize the diode at room temperature in the dark to obtain dark current and series resistance. Fit to a single-diode model.
2. Mount the diode emitter side facing the sky through the IR window. Hot side coupled to PID-controlled hot plate at 50 °C.
3. Wait for clear night. Record T_sky from pyrgeometer (typically 240–260 K under clear dry conditions; 270–290 K under clouds).
4. Sweep V from 0 to V_oc; record I; compute P = V·I; find P_max.
5. Repeat at hot-plate temperatures from 25 to 70 °C.
6. Compare measured P_max(T_hot, T_sky) against `simulate.py` predictions. Discrepancy → identify whether parasitic loss, non-radiative recombination, or window absorption is dominant.

## Scale-up question to answer

What is the largest patch of MCT-array-based TR diode that can be made cost-effective when amortized over 10 years of nightly operation, given a marginal cost of $X/W of installed capacity? The simulator's `data_center_roof_yield()` gives the upper-bound annual MWh; multiply by your local off-peak electricity price to get an annual revenue ceiling.

## Where to publish

- IEEE J. Photovoltaics or Nature Photonics for the device-level result
- Energy & Buildings or Applied Energy for the data-center system-level result
- arXiv:cond-mat.mtrl-sci or arXiv:physics.app-ph for preprint

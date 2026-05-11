# Thermoradiative diodes on AI data-center roofs

A solid-state device that pumps electrons by emitting thermal photons toward the cold night sky. Same physics as a photovoltaic cell run in reverse. Sees ~250 K when the atmosphere is clear; the data center's hot exhaust is ~325 K. That ΔT⁴ drives current.

## Why this is the most defensible of the three

- The physics is identical to standard radiative cooling + a known semiconductor diode response.
- A 350 mW/m² nighttime electricity record was published in 2024 ([arXiv 2407.17751](https://arxiv.org/abs/2407.17751)).
- The theoretical radiative-limit ceiling is ~6 W/m² ([Sci. Reports 2025](https://www.nature.com/articles/s41598-025-91800-8)).
- Data centers have huge flat warm roofs. Nobody has published on this specific marriage.

## What the simulator does

1. Builds Planck spectra for the emitter and the effective sky temperature.
2. Convolves with a coarse atmospheric-window transmission model (8–13 µm).
3. Applies a step-cutoff diode quantum efficiency above bandgap.
4. Integrates net spectral flux to get W/m².
5. Calibrates: with T_h=300 K, T_sky=248 K, Eg=0.10 eV the model lands close to the published 350 mW/m² record.
6. Estimates yield on a 100,000 m² (~10 ha) hyperscale roof at hot-aisle exhaust temperature.

## Run it

```bash
python simulate.py
```

You'll get a numerical breakdown plus `spectra.png` showing the Planck curves, atmospheric window, and net usable flux.

## Honest caveats

- Model assumes radiative limit + 85% internal quantum efficiency. Real devices have series resistance, non-radiative recombination, surface reflection. Expect 30–60% derating in a real prototype.
- Atmospheric transmittance varies enormously with humidity and clouds. The model uses a smooth approximation, not MODTRAN.
- Hot-aisle exhaust temperature varies by data-center cooling architecture; we picked 325 K as a representative warm exhaust.
- Yield ≈ 0.1–1% of facility load is small but additive. It is not "powering the AI" — it is *contributing* alongside Rankine, district heating, immersion-cooling heat reuse, and so on.

## Next step

See [`protocol.md`](protocol.md) for what a wet-lab person would actually build.

# AI Energy Frontiers

Three computational experiments probing under-explored physics that *could* address the AI-driven electricity gap (data centers projected to grow from ~485 TWh in 2025 to ~950 TWh by 2030, per IEA).

This repo holds **simulations and experimental protocols**, not lab results. The goal is to make the unexplored intersections concrete enough that someone with a wet lab can act on them.

## What's here

| Subproject | Status | What it does |
|---|---|---|
| [`tr_diode_data_center/`](tr_diode_data_center/) | most defensible | Simulates thermoradiative diodes pointed at the night sky from a hot data-center surface. Calibrated against the 350 mW/m² record from [arXiv 2407.17751](https://arxiv.org/abs/2407.17751). Estimates yield on a 5 MW data-center roof. |
| [`sed_casimir_zpe/`](sed_casimir_zpe/) | speculative-but-principled | Estimates per-atom energy release for the gas-pumping-through-Casimir-cavity ZPE method ([Schrieber 2019](https://www.mdpi.com/2218-2004/7/2/51)) — the only ZPE extraction class that doesn't violate thermodynamics. Almost zero follow-up since 2019. |
| [`bhasma_lenr_cathode/`](bhasma_lenr_cathode/) | exploratory cross-disciplinary | Models D-D fusion enhancement vs cathode nanoparticle size, calibrated to the [UBC *Nature* 2025 paper](https://www.nature.com/articles/s41586-025-09042-7). Hypothesizes that classical rasashastra bhasma metal-preparation cycles produce defect-rich nano-Pd that should outperform commercial Pd black as a LENR cathode. |

## Honesty section

- **None of these have been physically tested by this repo.** Every prediction is a calculation, not a measurement.
- Tier 1 (TR diode) is solid published physics applied to a new geometry — the math should hold.
- Tier 2 (SED Casimir) is one of three ZPE classes; the other two violate the 2nd law. This one *doesn't appear to* but has never been cleanly verified.
- Tier 3 (bhasma-LENR) is a hypothesis bridging Sanskrit metallurgical scholarship and modern cold fusion research. The cross-reference is original to this repo. It could be wrong. It could also be the unlock.
- LENR itself is a contested field. As of [Nature 644:640–645 (2025)](https://www.nature.com/articles/s41586-025-09042-7), peer-reviewed evidence of D-D fusion enhancement via electrochemical loading does exist. It is still net-energy-negative.

## How to run

```bash
pip install -r requirements.txt
python tr_diode_data_center/simulate.py
python sed_casimir_zpe/estimate.py
python bhasma_lenr_cathode/model.py
```

## Virtual testing

Each subproject ships a `validate.py` with physics-consistency checks,
multi-reference benchmarks, and Monte Carlo uncertainty quantification.
See [`TESTING.md`](TESTING.md) for the methodology.

```bash
python validate_all.py
```

Current status: **42/42 tests passing** across the three subprojects.
A "pass" means the model is internally consistent and matches its
calibration anchors — not that the underlying speculative physics is
correct. Read each subproject's `validate.py` to see exactly what is
tested.

## Citations

See [`LITERATURE.md`](LITERATURE.md) for the source papers.

## License

MIT — fork it, fix it, prove it wrong.

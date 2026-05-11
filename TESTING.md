# Testing methodology

Each subproject ships a `validate.py` that virtually tests the model
against the physics, against published reference points, and via
Monte Carlo uncertainty quantification.

Why this matters: the three subprojects are speculative-to-realistic
ranging widely. A model that fits one number is not the same as a
model that *works*. Virtual testing keeps us honest.

## What each subproject tests

### `tr_diode_data_center/validate.py`
- **Physics consistency**: zero output at thermal equilibrium, sign reversal when sky is hotter, monotonicity in T_hot and T_sky, Planck integral reproduces Stefan-Boltzmann, Wien displacement law for the peak.
- **Bandgap limits**: low-bandgap plateau (admits whole window), high-bandgap suppression.
- **Multi-reference benchmarks**: realistic device matches the 350 mW/m² record from arXiv:2407.17751; radiative-limit prediction lies in the published-permissive range; data-center recovery sub-1% of facility load.
- **Monte Carlo**: propagates ±8 K sky-temp uncertainty, ±5 K exhaust uncertainty, 0.3–1% device-efficiency uncertainty into annual MWh prediction.

### `sed_casimir_zpe/validate.py`
- **Casimir formula consistency**: closed-form energy per area at d=1µm matches Casimir's 1948 result; force per area matches the well-known 1.3e-3 N/m² value; 1/d³ scaling holds.
- **ZPF mode-cutoff consistency**: cutoff frequency scales as 1/d and lands in UV range at 100 nm; suppressed energy density scales as 1/d⁴; closed form matches direct integration.
- **Per-atom and flow scaling**: linear in `f_couple`; linear in atoms/s.
- **Schrieber experimental constraints**: at typical lab Cs flow (1 mg/s) and `f_couple ≤ 1e-4`, predicted output is sub-µW — consistent with the experimental null Schrieber reported.
- **Data-center sanity**: 5 MW from 100 nm cavities requires absurd Cs flow regardless of `f_couple` — protects against optimism.
- **Monte Carlo**: samples (gap, `f_couple`) jointly across the unknown parameter space, reports the fraction with detectable signal at cryogenic-bolometer sensitivity.

### `bhasma_lenr_cathode/validate.py`
- **Auxiliary functions**: S/V = 6/d for spheres; `fraction_atoms_within` bounded in [0, 1]; D/Pd ratio bounded in [0.70, 0.95]; D/Pd monotonically non-increasing in d.
- **Calibration anchor**: model exactly reproduces UBC's +15% at d=10µm; foil-scale enhancement insensitive to alpha values (anchor preserved).
- **Composite model behavior**: enhancement monotonically non-increasing in d across 10 nm – 10 µm; significant boost (>2× foil) at 30–100 nm; finite and bounded at 1 nm extreme.
- **Sensitivity to free parameters**: ±50% Monte Carlo variation in `alpha_surface` and `alpha_loading` gives the honest uncertainty band on the 100-nm prediction.
- **Cross-claim consistency**: 50 nm bhasma factor lands in the 2–10× range that Storms / Iwamura / Mizuno LENR claims have asserted for nano-Pd.
- **Rasashastra mapping**: more puta cycles → smaller particles; size range matches the bhasma characterization literature.

## Running the suite

```bash
# Each subproject independently:
python tr_diode_data_center/validate.py
python sed_casimir_zpe/validate.py
python bhasma_lenr_cathode/validate.py

# Or all at once (exits non-zero on any failure):
python validate_all.py
```

## What "PASS" means and doesn't mean

A pass means the model is **internally consistent** and **agrees with the published reference points it was calibrated against**. It does *not* mean the underlying physics is correct, that the experiment will work, or that the bhasma-LENR or SED-ZPE hypotheses are true.

If you fork this and the tests still pass after you change a parameter, the model still satisfies physics — but the predictions may have moved. Always re-read `[INFO]` lines from the Monte Carlo runs after changes.

## Adding tests

When you add a new physics function to any subproject's main module, add a test in the matching `validate.py`. The format is:

```python
def test_my_thing():
    result = M.my_function(...)
    check("description of what's being tested",
          result_is_ok,
          f"detail with actual numbers if useful")
```

Then call `test_my_thing()` from `main()` in the appropriate section.

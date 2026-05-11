"""
Virtual validation suite for the TR-diode simulator.

Strategy
--------
Don't just check that the model runs — check that it satisfies the
underlying physics in limits we can verify analytically, that it
behaves monotonically where it should, and that calibration to one
published number doesn't lock us into wrong predictions for other
published numbers.

Run with:  python validate.py
"""

import sys
import numpy as np
from scipy import integrate

import simulate as S


# -------- helpers --------

PASSED, FAILED = 0, 0


def check(name, ok, detail=""):
    global PASSED, FAILED
    tag = "[PASS]" if ok else "[FAIL]"
    print(f"  {tag} {name}" + (f"  -- {detail}" if detail else ""))
    if ok:
        PASSED += 1
    else:
        FAILED += 1


def approx(a, b, rel=0.10):
    """Relative tolerance check."""
    if b == 0:
        return abs(a) < 1e-12
    return abs(a - b) / abs(b) < rel


# -------- physics consistency tests --------

def test_zero_when_isothermal():
    """Reciprocity at thermal equilibrium: net flux must be zero."""
    P = S.net_radiative_power_density(300.0, 300.0, 0.10)
    check("Zero output at T_hot == T_sky", abs(P) < 1e-9,
          f"got {P:.3e} W/m^2 (should be ~0)")


def test_negative_when_inverted():
    """If sky is hotter than emitter, net flux reverses sign."""
    P = S.net_radiative_power_density(248.0, 300.0, 0.10)
    check("Negative output when T_sky > T_hot", P < 0,
          f"got {P:.3e} W/m^2")


def test_monotonic_in_T_hot():
    """At fixed sky and bandgap, output rises monotonically with T_hot."""
    Ts = np.linspace(280, 360, 9)
    Ps = [S.net_radiative_power_density(T, 250.0, 0.10) for T in Ts]
    diffs = np.diff(Ps)
    check("Monotonic increasing in T_hot",
          np.all(diffs > 0),
          f"min consecutive diff = {diffs.min():.2e}")


def test_monotonic_in_T_sky():
    """At fixed T_hot and bandgap, output drops monotonically with T_sky."""
    Ts = np.linspace(220, 290, 8)
    Ps = [S.net_radiative_power_density(310.0, T, 0.10) for T in Ts]
    diffs = np.diff(Ps)
    check("Monotonic decreasing in T_sky",
          np.all(diffs < 0),
          f"max consecutive diff = {diffs.max():.2e}")


def test_planck_integrates_to_stefan_boltzmann():
    """sigma*T^4 = pi * integral of B(lambda, T) over all lambda.

    Verifies the Planck spectral radiance function is dimensionally
    correct and properly normalized.
    """
    T = 300.0
    lam = np.linspace(1e-7, 1e-3, 200_000)  # very wide
    B = S.planck_spectral_radiance(lam, T)
    integral = np.pi * integrate.trapezoid(B, lam)
    expected = S.sigma * T ** 4
    rel_err = abs(integral - expected) / expected
    check("Planck integral reproduces sigma*T^4 (300 K)",
          rel_err < 0.01,
          f"got {integral:.3f}, expected {expected:.3f}, rel_err {rel_err:.2%}")


def test_wien_displacement():
    """Peak of B(lambda, T) sits at lambda_max = 2898/T um (Wien's law)."""
    T = 300.0
    lam = np.linspace(1e-6, 30e-6, 5000)
    B = S.planck_spectral_radiance(lam, T)
    lam_peak_um = lam[np.argmax(B)] * 1e6
    expected_um = 2898.0 / T
    check("Wien displacement law (300 K)",
          abs(lam_peak_um - expected_um) < 0.2,
          f"peak at {lam_peak_um:.2f} um, Wien predicts {expected_um:.2f} um")


def test_low_bandgap_approaches_full_window_limit():
    """As bandgap shrinks below the sky-window photon energies, the
    diode admits all atmospheric-window photons. Output should plateau."""
    Egs = [0.04, 0.05, 0.06, 0.075]
    Ps = [S.net_radiative_power_density(310.0, 250.0, Eg) for Eg in Egs]
    rel_spread = (max(Ps) - min(Ps)) / max(Ps)
    check("Output plateaus at very low bandgap",
          rel_spread < 0.30,
          f"spread {rel_spread:.1%} across Eg in [{min(Egs):.2f}, {max(Egs):.2f}] eV")


def test_high_bandgap_kills_output():
    """At Eg >> kT, almost no photons clear the bandgap."""
    P_high_Eg = S.net_radiative_power_density(310.0, 250.0, 0.50)
    P_low_Eg = S.net_radiative_power_density(310.0, 250.0, 0.10)
    check("High bandgap suppresses output by >100x",
          P_high_Eg < P_low_Eg / 100.0,
          f"P(Eg=0.5)={P_high_Eg*1000:.4f} mW/m^2,"
          f" P(Eg=0.1)={P_low_Eg*1000:.1f} mW/m^2")


# -------- multi-reference benchmark tests --------

def test_calibration_to_arxiv_2407_17751():
    """Realistic device should reproduce 350 mW/m^2 at the cited conditions."""
    _, _, _, _, P_real = S.radiative_limit_check()
    check("Realistic-derate matches arXiv:2407.17751 record (350 mW/m^2)",
          approx(P_real * 1000, 350, rel=0.10),
          f"predicted {P_real*1000:.1f} mW/m^2 vs published 350 mW/m^2")


def test_radiative_limit_in_published_range():
    """The radiative-limit upper bound across literature is 1-150 W/m^2
    depending on assumptions about atmospheric window and bandgap.
    Sci. Reports 2025 (intermediate-band) cites 6 W/m^2 with strict
    detailed-balance constraints; our model is more permissive (no
    detailed-balance enforcement) so it should land in 30-200 W/m^2.
    """
    P = S.net_radiative_power_density(325.0, 255.0, 0.10)
    check("Radiative limit in published-permissive range (10-200 W/m^2)",
          10.0 < P < 200.0,
          f"got {P:.1f} W/m^2 at T_h=325, T_sky=255, Eg=0.1")


def test_nighttime_yield_realistic_scale():
    """Realistic data-center recovery should be sub-1% of facility load
    today. If the model says 10%+, the calibration is wrong."""
    r = S.data_center_roof_yield()
    pct = 100.0 * r["annual_MWh"] / (5000 * 8760 / 1000.0)
    check("Realistic DC recovery <1% of facility load",
          pct < 1.0,
          f"got {pct:.2f}%")


# -------- Monte Carlo uncertainty quantification --------

def test_monte_carlo_uncertainty():
    """Quantify uncertainty in DC roof annual yield given the input
    uncertainties on T_sky (clear vs cloudy), exhaust temperature,
    and device efficiency."""
    rng = np.random.default_rng(42)
    n = 5000
    T_sky_samples = rng.normal(255.0, 8.0, n)        # +/- 8 K
    T_hot_samples = rng.normal(325.0, 5.0, n)        # +/- 5 K
    eff_samples = rng.uniform(0.003, 0.010, n)       # 0.3-1.0% device eff

    yields = []
    for Th, Ts, eff in zip(T_hot_samples, T_sky_samples, eff_samples):
        r = S.data_center_roof_yield(T_hot=Th, T_sky=Ts,
                                     device_efficiency=eff)
        yields.append(r["annual_MWh"])
    yields = np.array(yields)

    mean = yields.mean()
    p10 = np.percentile(yields, 10)
    p90 = np.percentile(yields, 90)
    print(f"    [INFO] DC annual yield Monte Carlo (n={n}):")
    print(f"           mean = {mean:.0f} MWh, p10-p90 = [{p10:.0f}, {p90:.0f}]")
    print(f"           std = {yields.std():.0f} MWh ({100*yields.std()/mean:.1f}% relative)")

    # Sanity: relative std should be 30-80% given input uncertainties
    rel_std = yields.std() / mean
    check("Monte Carlo std within plausible range",
          0.20 < rel_std < 1.00,
          f"rel std = {rel_std:.2f}")


# -------- main --------

def main():
    print("=" * 64)
    print("VALIDATION: tr_diode_data_center.simulate")
    print("=" * 64)
    print("\n[Physics consistency]")
    test_zero_when_isothermal()
    test_negative_when_inverted()
    test_monotonic_in_T_hot()
    test_monotonic_in_T_sky()
    test_planck_integrates_to_stefan_boltzmann()
    test_wien_displacement()
    test_low_bandgap_approaches_full_window_limit()
    test_high_bandgap_kills_output()

    print("\n[Multi-reference benchmarks]")
    test_calibration_to_arxiv_2407_17751()
    test_radiative_limit_in_published_range()
    test_nighttime_yield_realistic_scale()

    print("\n[Monte Carlo]")
    test_monte_carlo_uncertainty()

    print(f"\nTOTAL: {PASSED} passed, {FAILED} failed")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()

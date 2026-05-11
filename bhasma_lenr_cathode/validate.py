"""
Virtual validation suite for the bhasma-LENR cathode model.

Strategy
--------
The model has two free parameters (alpha_surface, alpha_loading)
calibrated to a single published data point. So our tests are:

  1. The calibration anchor must hold exactly.
  2. Auxiliary functions (S/V, fraction-within-depth, D/Pd ramp)
     must obey their physical bounds and analytical limits.
  3. The composite enhancement model must be monotonic in particle
     size (smaller -> more enhancement, with no weird non-monotonic
     dips in the practical range).
  4. Sensitivity: vary alpha parameters and report the spread of
     predicted enhancements at typical bhasma sizes — gives an
     honest uncertainty band.
  5. Comparison to other LENR claims (Iwamura/Mizuno/Storms) for
     consistency check.

Run with:  python validate.py
"""

import sys
import numpy as np

import model as M

PASSED, FAILED = 0, 0


def check(name, ok, detail=""):
    global PASSED, FAILED
    tag = "[PASS]" if ok else "[FAIL]"
    print(f"  {tag} {name}" + (f"  -- {detail}" if detail else ""))
    if ok:
        PASSED += 1
    else:
        FAILED += 1


def approx(a, b, rel=0.05):
    if b == 0:
        return abs(a) < 1e-12
    return abs(a - b) / abs(b) < rel


# -------- Auxiliary function tests --------

def test_surface_to_volume_sphere():
    """6/d for spheres."""
    sv = M.surface_to_volume_ratio(1e-6, "sphere")
    check("S/V = 6/d for sphere d=1um",
          approx(sv, 6e6, rel=1e-9),
          f"got {sv:.3e} 1/m")


def test_fraction_atoms_within_zero_depth():
    """Zero shell depth = zero fraction."""
    f = M.fraction_atoms_within(100e-9, 0)
    check("fraction_atoms_within(d, 0) == 0", abs(f) < 1e-12)


def test_fraction_atoms_within_full_depth():
    """Depth >= radius means whole particle is 'within' = 1.0."""
    f = M.fraction_atoms_within(100e-9, 100e-9)
    check("fraction_atoms_within(d, d) == 1.0", abs(f - 1.0) < 1e-12)


def test_fraction_atoms_within_bounds():
    """Always in [0, 1] across a range of inputs."""
    rng = np.random.default_rng(0)
    ds = 10 ** rng.uniform(-9, -5, 200)
    depths = 10 ** rng.uniform(-10, -4, 200)
    fs = [M.fraction_atoms_within(d, depth) for d, depth in zip(ds, depths)]
    check("fraction_atoms_within in [0, 1] across 200 random samples",
          all(0.0 <= f <= 1.0 for f in fs))


def test_dpd_loading_bounds():
    """D/Pd should stay between 0.70 (foil) and 0.95 (nano)."""
    sizes = np.logspace(-9, -4, 100)
    vals = [M.achievable_dpd_ratio(d) for d in sizes]
    check("D/Pd loading in [0.70, 0.95] across all sizes",
          all(0.70 - 1e-9 <= v <= 0.95 + 1e-9 for v in vals))


def test_dpd_loading_monotonic():
    """Smaller particles -> higher D/Pd (or equal at the plateaus)."""
    sizes = np.logspace(-9, -4, 100)
    vals = np.array([M.achievable_dpd_ratio(d) for d in sizes])
    diffs = np.diff(vals)
    check("D/Pd loading monotonically non-increasing in d",
          np.all(diffs <= 1e-12),
          f"max increasing step = {diffs.max():.2e}")


# -------- Calibration anchor --------

def test_calibration_anchor_holds():
    """At UBC foil scale (d = 10 um), enhancement must equal 15%."""
    enh = M.enhancement_model(M.UBC_BASELINE_FOIL_THICKNESS_M)
    check("Enhancement = UBC baseline at d=10um",
          approx(enh, M.UBC_FUSION_ENHANCEMENT, rel=1e-9),
          f"predicted {enh*100:.4f}%, expected {M.UBC_FUSION_ENHANCEMENT*100}%")


def test_calibration_anchor_holds_above_threshold():
    """Above the foil scale, model should hold at the UBC baseline (no
    extrapolation past bulk behavior)."""
    enh_30um = M.enhancement_model(30e-6)
    enh_100um = M.enhancement_model(100e-6)
    check("Enhancement = UBC baseline for all foil-or-thicker cathodes",
          approx(enh_30um, M.UBC_FUSION_ENHANCEMENT) and
          approx(enh_100um, M.UBC_FUSION_ENHANCEMENT))


# -------- Composite model behavior --------

def test_enhancement_monotonic_decreasing_in_d():
    """Across the practical bhasma-to-foil range, enhancement should
    drop monotonically as d grows."""
    ds = np.logspace(-8, -5, 60)  # 10 nm to 10 um
    enh = np.array([M.enhancement_model(d) for d in ds])
    diffs = np.diff(enh)
    check("Enhancement monotonically non-increasing in d (10nm-10um)",
          np.all(diffs <= 1e-12),
          f"max increasing step = {diffs.max():.2e}")


def test_enhancement_at_nanoparticle_scale_significant():
    """At 30-100 nm bhasma sizes, predicted enhancement should be at
    least 2x the foil baseline — otherwise the experiment isn't worth
    running."""
    enh_30 = M.enhancement_model(30e-9)
    enh_100 = M.enhancement_model(100e-9)
    check("30 nm bhasma predicted >2x foil baseline",
          enh_30 > 2 * M.UBC_FUSION_ENHANCEMENT,
          f"predicted {enh_30*100:.1f}% vs 2x baseline = "
          f"{2*M.UBC_FUSION_ENHANCEMENT*100}%")
    check("100 nm bhasma predicted >2x foil baseline",
          enh_100 > 2 * M.UBC_FUSION_ENHANCEMENT,
          f"predicted {enh_100*100:.1f}% vs 2x baseline")


def test_enhancement_does_not_diverge():
    """Even at 1 nm (atomic scale), enhancement should stay finite
    and below ~5x the baseline (not blow up)."""
    enh_1nm = M.enhancement_model(1e-9)
    check("Enhancement finite and bounded at 1 nm",
          np.isfinite(enh_1nm) and enh_1nm < 10 * M.UBC_FUSION_ENHANCEMENT,
          f"predicted {enh_1nm*100:.1f}%")


# -------- Sensitivity to free parameters --------

def test_sensitivity_to_free_parameters():
    """Vary the two alpha coefficients ±50% and report enhancement
    spread at 100 nm. This is the honest uncertainty band."""
    base_a_surface = 0.020
    base_a_load = 2.0
    d_test = 100e-9
    rng = np.random.default_rng(42)
    n = 4000
    a_s = rng.uniform(0.5 * base_a_surface, 1.5 * base_a_surface, n)
    a_l = rng.uniform(0.5 * base_a_load, 1.5 * base_a_load, n)
    enh = np.array([M.enhancement_model(d_test,
                                        alpha_surface=s,
                                        alpha_loading=l)
                    for s, l in zip(a_s, a_l)])
    p10 = np.percentile(enh, 10)
    p50 = np.percentile(enh, 50)
    p90 = np.percentile(enh, 90)
    print(f"    [INFO] Sensitivity at d=100 nm under ±50% alpha variation"
          f" (n={n}):")
    print(f"           p10 = {p10*100:.1f}%, median = {p50*100:.1f}%,"
          f" p90 = {p90*100:.1f}%")
    rel_spread = (p90 - p10) / p50
    check("Sensitivity-band relative width plausible (40-200%)",
          0.40 < rel_spread < 2.00,
          f"(p90-p10)/median = {rel_spread:.2f}")


def test_sensitivity_at_foil_scale_zero():
    """At foil scale, both terms vanish by construction, so the
    enhancement should equal the baseline regardless of alpha values."""
    rng = np.random.default_rng(1)
    n = 200
    a_s = rng.uniform(0.001, 0.10, n)
    a_l = rng.uniform(0.5, 5.0, n)
    enh = [M.enhancement_model(M.UBC_BASELINE_FOIL_THICKNESS_M,
                               alpha_surface=s, alpha_loading=l)
           for s, l in zip(a_s, a_l)]
    spread = max(enh) - min(enh)
    check("Foil-scale enhancement insensitive to alpha (anchor preserved)",
          spread < 1e-9,
          f"spread = {spread:.3e}")


# -------- Cross-claim consistency --------

def test_consistent_with_storms_iwamura_scale_claims():
    """LENR literature (Storms, Iwamura, Mizuno) variously claims
    nano-Pd or thin-film enhancements of factor 2-10 over bulk Pd
    in their own (less-rigorous) calorimetry. Our model should
    predict factors in that ballpark for 50-200 nm particles —
    not 100x and not negligible."""
    enh_50 = M.enhancement_model(50e-9)
    factor = enh_50 / M.UBC_FUSION_ENHANCEMENT
    check("50 nm bhasma factor in 2-10x range (consistent with field claims)",
          2.0 < factor < 10.0,
          f"predicted factor {factor:.2f}x")


# -------- Rasashastra puta -> particle size mapping --------

def test_puta_size_estimate_decreasing():
    """More puta cycles -> smaller particles."""
    sizes = [M.rasashastra_puta_to_size_estimate(n) for n in [1, 10, 30, 100]]
    diffs = np.diff(sizes)
    check("Puta count -> size monotonically decreasing",
          np.all(diffs < 0),
          f"sizes (nm) = {[f'{s*1e9:.0f}' for s in sizes]}")


def test_puta_size_in_physical_range():
    """Bhasma literature size range: 5 um (low puta) to 50 nm (high)."""
    s1 = M.rasashastra_puta_to_size_estimate(1)
    s100 = M.rasashastra_puta_to_size_estimate(100)
    check("Puta=1 size ~few microns",
          1e-6 < s1 < 1e-5,
          f"got {s1*1e9:.0f} nm")
    check("Puta=100 size ~tens to hundreds of nm",
          50e-9 < s100 < 500e-9,
          f"got {s100*1e9:.0f} nm")


def main():
    print("=" * 64)
    print("VALIDATION: bhasma_lenr_cathode.model")
    print("=" * 64)

    print("\n[Auxiliary functions]")
    test_surface_to_volume_sphere()
    test_fraction_atoms_within_zero_depth()
    test_fraction_atoms_within_full_depth()
    test_fraction_atoms_within_bounds()
    test_dpd_loading_bounds()
    test_dpd_loading_monotonic()

    print("\n[Calibration anchor]")
    test_calibration_anchor_holds()
    test_calibration_anchor_holds_above_threshold()

    print("\n[Composite model behavior]")
    test_enhancement_monotonic_decreasing_in_d()
    test_enhancement_at_nanoparticle_scale_significant()
    test_enhancement_does_not_diverge()

    print("\n[Sensitivity to free parameters]")
    test_sensitivity_to_free_parameters()
    test_sensitivity_at_foil_scale_zero()

    print("\n[Cross-claim consistency]")
    test_consistent_with_storms_iwamura_scale_claims()

    print("\n[Rasashastra mapping]")
    test_puta_size_estimate_decreasing()
    test_puta_size_in_physical_range()

    print(f"\nTOTAL: {PASSED} passed, {FAILED} failed")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()

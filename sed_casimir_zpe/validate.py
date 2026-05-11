"""
Virtual validation suite for the SED Casimir ZPE estimator.

Strategy
--------
The headline number depends on an unmeasured coupling fraction
(f_couple), but the underlying vacuum energy formulas have
exact closed forms we can verify, the scaling with cavity gap
follows known power laws, and the experimental upper bound
(Schrieber 2019) gives us a calibration anchor for f_couple.

Run with:  python validate.py
"""

import sys
import numpy as np
from scipy import integrate

import estimate as E

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
        return abs(a) < 1e-30
    return abs(a - b) / abs(b) < rel


# -------- Casimir formula consistency --------

def test_casimir_formula_at_1um():
    """Casimir's classic 1948 result for parallel plates:
        E/A = -pi^2 hbar c / (720 d^3)
    For d = 1 um, this evaluates to about -4.33e-10 J/m^2
    (equivalently, attractive force per area is 1.30e-3 N/m^2).
    """
    d = 1e-6
    E_pred = E.casimir_energy_per_area(d)
    expected = -np.pi**2 * 1.054571817e-34 * 2.99792458e8 / (720.0 * d**3)
    check("Casimir energy per area, d=1um, matches closed form",
          approx(E_pred, expected, rel=1e-9),
          f"got {E_pred:.4e} J/m^2, expected {expected:.4e}")


def test_casimir_force_known_value():
    """Force per area at d=1um is roughly 1.3e-3 N/m^2.
    Force = -dE/dd, so |F/A| = 3 * |E/A| / d in this scaling.
    """
    d = 1e-6
    E_per_A = E.casimir_energy_per_area(d)
    force_per_area = 3.0 * abs(E_per_A) / d
    expected = 1.30e-3  # N/m^2 at d=1um
    check("Casimir force per area at d=1um in expected range",
          approx(force_per_area, expected, rel=0.02),
          f"got {force_per_area:.3e} N/m^2")


def test_casimir_d_cube_scaling():
    """Casimir energy per area scales as 1/d^3."""
    d1, d2 = 100e-9, 1000e-9
    E1 = abs(E.casimir_energy_per_area(d1))
    E2 = abs(E.casimir_energy_per_area(d2))
    ratio = E1 / E2
    expected = (d2 / d1) ** 3  # 1000
    check("Casimir energy follows 1/d^3",
          approx(ratio, expected, rel=1e-9),
          f"ratio E(100nm)/E(1um) = {ratio:.1f}, expected {expected:.1f}")


# -------- ZPF mode-cutoff consistency --------

def test_cutoff_frequency_dimensions():
    """omega_cut = pi*c/d should be in rad/s and scale as 1/d."""
    omega_100 = E.cavity_mode_cutoff_freq(100e-9)
    omega_300 = E.cavity_mode_cutoff_freq(300e-9)
    check("Cutoff freq scales as 1/d",
          approx(omega_100 / omega_300, 3.0, rel=1e-9),
          f"ratio = {omega_100/omega_300:.4f}")
    # Sanity: 100 nm cavity cutoff should be ~9.4e15 rad/s (UV)
    check("Cutoff freq at 100 nm in UV range",
          5e15 < omega_100 < 2e16,
          f"got {omega_100:.2e} rad/s")


def test_suppressed_energy_density_d4_scaling():
    """Delta_u = hbar pi^2 c / (8 d^4) — scales as 1/d^4."""
    d1, d2 = 50e-9, 500e-9
    u1 = E.suppressed_zpf_energy_density(d1)
    u2 = E.suppressed_zpf_energy_density(d2)
    check("Suppressed-mode energy density scales as 1/d^4",
          approx(u1 / u2, (d2 / d1) ** 4, rel=1e-9),
          f"ratio = {u1/u2:.0f}, expected {(d2/d1)**4:.0f}")


def test_suppressed_energy_density_by_integration():
    """
    Delta_u should equal the integral from omega=0 to omega_cut of the
    free-space ZPF spectral energy density:
        u(omega) = hbar omega^3 / (2 pi^2 c^3)
    This is a direct sanity check of the closed form.
    """
    d = 100e-9
    omega_cut = np.pi * 2.99792458e8 / d
    omega = np.linspace(0, omega_cut, 50000)
    spectral = 1.054571817e-34 * omega ** 3 / (2 * np.pi**2 * (2.99792458e8) ** 3)
    integrated = integrate.trapezoid(spectral, omega)
    closed_form = E.suppressed_zpf_energy_density(d)
    check("Suppressed energy density by direct integration",
          approx(integrated, closed_form, rel=0.005),
          f"integrated {integrated:.3e}, closed form {closed_form:.3e}")


# -------- Per-atom and flow scaling --------

def test_per_atom_dE_linear_in_f_couple():
    """dE_atom should be exactly linear in f_couple."""
    d = 100e-9
    Vat = E.ATOM_VOL_HEAVY
    dE_1 = E.per_atom_orbital_shift_J(d, Vat, 1.0)
    dE_2 = E.per_atom_orbital_shift_J(d, Vat, 2.0)
    check("dE_atom linear in f_couple",
          approx(dE_2 / dE_1, 2.0, rel=1e-9))


def test_flow_power_linear_in_atoms():
    """Steady-state power should be exactly linear in atoms/s."""
    P1 = E.cavity_flow_power_W(100e-9, E.ATOM_VOL_HEAVY, 1e20, 1.0)
    P2 = E.cavity_flow_power_W(100e-9, E.ATOM_VOL_HEAVY, 5e20, 1.0)
    check("Flow power linear in atoms/s",
          approx(P2 / P1, 5.0, rel=1e-9))


# -------- Schrieber 2019 experimental upper bound --------

def test_schrieber_experimental_upper_bound():
    """
    Schrieber's cited experiments saw 'lower-than-expected output,'
    consistent with f_couple <= ~1e-4. At lab-scale Cs vapor flow
    (e.g., 1 mg/s) and 100 nm gap, predicted output at f=1e-4
    should be sub-microwatt, matching experimental null at typical
    calorimeter sensitivity ~uW.
    """
    flow_atoms = E.gas_flow_atoms_per_second(1e-3, 132.9)  # 1 mg/s
    P = E.cavity_flow_power_W(100e-9, E.ATOM_VOL_HEAVY, flow_atoms, 1e-4)
    check("Schrieber 1 mg/s @ f=1e-4 gives sub-uW (consistent with null)",
          P < 1e-6,
          f"predicted {P:.3e} W")


def test_data_center_target_unreachable():
    """Sanity: at any plausible f_couple, 5 MW from 100 nm cavities
    requires absurd Cs flow (~Mt/s). This protects against optimism."""
    d = 100e-9
    target = 5e6
    dE = E.per_atom_orbital_shift_J(d, E.ATOM_VOL_HEAVY, 1.0)
    atoms_needed = target / dE
    mass_g_s = atoms_needed * 132.9 / 6.02214076e23
    check("5 MW target needs >>1e9 g/s of Cs (absurd)",
          mass_g_s > 1e9,
          f"requires {mass_g_s:.2e} g/s")


# -------- Monte Carlo sweep over (d, f_couple) --------

def test_monte_carlo_envelope():
    """Sample (gap, f_couple) jointly and report the distribution
    of predicted lab-bench power output. We want to know what fraction
    of the parameter space gives a 'detectable' (>1 fW) signal."""
    rng = np.random.default_rng(7)
    n = 10000
    # gap log-uniform in [10 nm, 1 um]
    log_d = rng.uniform(np.log10(10e-9), np.log10(1e-6), n)
    d = 10 ** log_d
    # f_couple log-uniform in [1e-8, 1] (the unknown range)
    log_f = rng.uniform(-8, 0, n)
    f = 10 ** log_f
    # Lab-bench Cs flow ~ 1 mg/s
    flow = E.gas_flow_atoms_per_second(1e-3, 132.9)
    powers = np.array([E.cavity_flow_power_W(di, E.ATOM_VOL_HEAVY, flow, fi)
                       for di, fi in zip(d, f)])

    detect_threshold_W = 1e-15  # 1 fW (cryogenic bolometer)
    above = (powers > detect_threshold_W).mean()
    print(f"    [INFO] Monte Carlo (n={n}): fraction of (d, f_couple) parameter")
    print(f"           space producing >{detect_threshold_W:.0e} W at 1 mg/s Cs flow:")
    print(f"           {above*100:.1f}%")

    # Sanity: should be a substantial chunk if model is right
    check("Monte Carlo: detection-feasible region exists",
          above > 0.10,
          f"got {above*100:.1f}% above detection threshold")


def main():
    print("=" * 64)
    print("VALIDATION: sed_casimir_zpe.estimate")
    print("=" * 64)

    print("\n[Casimir formula consistency]")
    test_casimir_formula_at_1um()
    test_casimir_force_known_value()
    test_casimir_d_cube_scaling()

    print("\n[ZPF mode cutoff]")
    test_cutoff_frequency_dimensions()
    test_suppressed_energy_density_d4_scaling()
    test_suppressed_energy_density_by_integration()

    print("\n[Per-atom and flow scaling]")
    test_per_atom_dE_linear_in_f_couple()
    test_flow_power_linear_in_atoms()

    print("\n[Schrieber experimental constraints]")
    test_schrieber_experimental_upper_bound()
    test_data_center_target_unreachable()

    print("\n[Monte Carlo]")
    test_monte_carlo_envelope()

    print(f"\nTOTAL: {PASSED} passed, {FAILED} failed")
    sys.exit(0 if FAILED == 0 else 1)


if __name__ == "__main__":
    main()

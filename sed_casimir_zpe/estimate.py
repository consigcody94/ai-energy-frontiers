"""
Stochastic-Electrodynamics Casimir-cavity zero-point energy estimator.

Based on:
  Schrieber, G. "Extraction of Zero-Point Energy from the Vacuum:
  Assessment of Stochastic Electrodynamics-Based Approach as Compared
  to Other Methods." Atoms 7(2):51 (2019).
  https://www.mdpi.com/2218-2004/7/2/51   (arXiv:0910.5893)

The premise (and the only ZPE class that does not appear to violate
the second law)
---------------------------------------------------------------
In stochastic electrodynamics (SED), the ground state of an atomic
electron is the equilibrium between random absorption from the
zero-point field (ZPF) and Larmor radiation. Inside a Casimir cavity
of plate separation d, electromagnetic modes with wavelength longer
than ~2d are excluded. SED therefore predicts the atomic ground state
in the cavity sits LOWER than in free space — by an amount equal to
the integrated suppressed mode coupling.

If gas atoms are pumped continuously through such a cavity, each
atom releases a small dE on entry (orbital relaxation) and absorbs
the same dE on exit (orbital rebuild from the full ZPF). The trick
is to extract the dE on entry as heat or photons before the atom
exits, so the cycle is non-conservative.

The two fundamental knobs
-------------------------
  d          : cavity gap         (smaller = more suppressed modes)
  flow_rate  : atoms / second     (linear scaling of total power)

The "honest answer" knob
------------------------
  f_couple   : the fraction of cavity ZPF-energy-density-difference
               that actually couples into atomic orbital energy.
               Schrieber's framework leaves this as a phenomenological
               number to be measured. We sweep it.

Calibration
-----------
We bound the per-area extractable energy by the Casimir attraction
energy itself:  E_Casimir / A = - pi^2 hbar c / (720 d^3).
Anything we propose to extract has to live inside that envelope per
"refresh" of the cavity contents.
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
hbar = 1.054571817e-34
c = 2.99792458e8
e_charge = 1.602176634e-19
N_A = 6.02214076e23


# ----------------------------------------------------------------------
# Vacuum / Casimir quantities
# ----------------------------------------------------------------------

def casimir_energy_per_area(d_m):
    """Casimir energy per unit area between parallel plates (J/m^2).

    E_Casimir / A = - pi^2 hbar c / (720 d^3)

    This is the fundamental energy bound on the "vacuum gap" — anything
    you propose to extract from the cavity per refresh has to be
    smaller than (or comparable to) this magnitude per unit area.
    """
    return -np.pi**2 * hbar * c / (720.0 * d_m**3)


def cavity_mode_cutoff_freq(d_m):
    """Lowest mode supported in the cavity, omega_cut = pi*c/d."""
    return np.pi * c / d_m


def suppressed_zpf_energy_density(d_m):
    """
    Energy density of ZPF modes excluded by the cavity (J/m^3).

    For modes with omega < omega_cut, the spectral energy density is
    u(omega) = hbar * omega^3 / (2 pi^2 c^3). Integrate from 0 to
    omega_cut to get the missing energy density:

      Delta_u = hbar * omega_cut^4 / (8 pi^2 c^3)
              = hbar * (pi*c/d)^4 / (8 pi^2 c^3)
              = hbar * pi^2 * c / (8 d^4)
    """
    return hbar * np.pi**2 * c / (8.0 * d_m**4)


# ----------------------------------------------------------------------
# SED prediction for atomic energy release per cavity transit
# ----------------------------------------------------------------------

def per_atom_orbital_shift_J(d_m, atom_volume_m3, f_couple):
    """
    Predicted SED orbital energy release per atom on entry to cavity.

    dE_atom = f_couple * Delta_u(d) * atom_volume

    f_couple is an effective coupling fraction. Strict SED arguments
    suggest atoms with orbital sizes comparable to the missing mode
    wavelengths can have f_couple approaching unity for those modes.
    Atoms much smaller than the missing wavelengths see a strongly
    reduced effective coupling. Schrieber's experiments suggest the
    effective f_couple is small (sub-percent), but the mechanism does
    not specify it from first principles — it must be measured.
    """
    return f_couple * suppressed_zpf_energy_density(d_m) * atom_volume_m3


def cavity_flow_power_W(d_m, atom_volume_m3, atoms_per_second, f_couple):
    """Steady-state power output assuming continuous gas pump-through."""
    dE = per_atom_orbital_shift_J(d_m, atom_volume_m3, f_couple)
    return dE * atoms_per_second


# ----------------------------------------------------------------------
# Reasonable parameter pickers
# ----------------------------------------------------------------------

# Bohr radius cubed scale for "atomic volume"
ATOM_VOL_BOHR = (4.0 / 3.0) * np.pi * (5.29e-11) ** 3   # m^3

# A larger "effective coupling volume" picks up van-der-Waals-range
# polarizability. Cesium / heavy alkali atoms have ~1e-30 m^3
# polarizability volume.
ATOM_VOL_HEAVY = 1.0e-30  # m^3

def gas_flow_atoms_per_second(mass_flow_g_s, atomic_mass_amu):
    """Convert a mass flow rate (g/s) of monatomic gas into atoms/s."""
    moles_per_s = mass_flow_g_s / atomic_mass_amu
    return moles_per_s * N_A


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------

def main():
    print("=" * 64)
    print("SED CASIMIR-CAVITY ZPE FLOW EXTRACTOR — feasibility envelope")
    print("=" * 64)

    print("\n[1] Vacuum/Casimir bounds vs cavity gap")
    print(f"    {'gap d (nm)':>12s}  {'Casimir E/A (J/m^2)':>22s}"
          f"  {'omega_cut (rad/s)':>20s}  {'Delta_u (J/m^3)':>18s}")
    for d_nm in [10, 30, 100, 300, 1000]:
        d = d_nm * 1e-9
        print(f"    {d_nm:12d}  {casimir_energy_per_area(d):22.3e}"
              f"  {cavity_mode_cutoff_freq(d):20.3e}"
              f"  {suppressed_zpf_energy_density(d):18.3e}")

    print("\n[2] Per-atom orbital shift (heavy-alkali polarizability volume)")
    print(f"    Atom volume = {ATOM_VOL_HEAVY:.2e} m^3 (Cs-like)")
    print(f"    {'gap (nm)':>10s}  {'f_couple':>10s}"
          f"  {'dE per atom (J)':>20s}  {'dE (eV)':>14s}")
    for d_nm in [30, 100, 300]:
        d = d_nm * 1e-9
        for f in [1e-6, 1e-4, 1e-2, 1.0]:
            dE = per_atom_orbital_shift_J(d, ATOM_VOL_HEAVY, f)
            print(f"    {d_nm:10d}  {f:10.0e}"
                  f"  {dE:20.3e}  {dE/e_charge:14.3e}")

    print("\n[3] Steady-state flow power (cesium gas through Casimir stack)")
    print("    Assumptions: continuous Cs vapor pumped through 100-nm-gap")
    print("    parallel-plate Casimir stack at given mass flow rate.")
    d = 100e-9
    print(f"    {'flow (g/s)':>10s}  {'atoms/s':>14s}"
          f"  {'f=1e-6 (W)':>14s}  {'f=1e-4 (W)':>14s}"
          f"  {'f=1e-2 (W)':>14s}  {'f=1 (W)':>14s}")
    for mass_flow in [1e-6, 1e-3, 1.0, 1e3]:
        atoms = gas_flow_atoms_per_second(mass_flow, 132.9)  # Cs amu
        powers = [cavity_flow_power_W(d, ATOM_VOL_HEAVY, atoms, f)
                  for f in [1e-6, 1e-4, 1e-2, 1.0]]
        print(f"    {mass_flow:10.0e}  {atoms:14.3e}"
              f"  {powers[0]:14.3e}  {powers[1]:14.3e}"
              f"  {powers[2]:14.3e}  {powers[3]:14.3e}")

    print("\n[4] What needs to be true for this to power a 5 MW data center?")
    target_W = 5e6
    d = 100e-9
    print(f"    Target = {target_W:.0e} W continuous from a 100 nm cavity stack")
    for f in [1.0, 1e-2, 1e-4]:
        dE = per_atom_orbital_shift_J(d, ATOM_VOL_HEAVY, f)
        atoms_needed = target_W / dE
        mass_flow = atoms_needed * 132.9 / N_A   # g/s of Cs
        print(f"    f_couple = {f:>5.0e} -> need {atoms_needed:.2e} atoms/s "
              f"= {mass_flow:.2e} g/s of Cs")

    print()
    print("    Honest read:")
    print("    - The per-atom orbital shift is TINY at any practical")
    print("      cavity gap. At 100 nm gap and f_couple=1 (theoretical")
    print("      max), each atom releases ~2e-9 eV. Even 1 g/s of cesium")
    print("      throughput yields only microwatts.")
    print("    - The output scales as 1/d^4. Going from 100 nm to 1 nm")
    print("      gaps would boost by 1e8 — but stable 1 nm Casimir")
    print("      cavities are themselves an unsolved fabrication problem.")
    print("    - For data-center-scale power, this physics is essentially")
    print("      not viable with any current technology.")
    print("    - HOWEVER: a microwatt signal is MEASURABLE with cryogenic")
    print("      bolometers. The decisive experiment is not 'power a data")
    print("      center' but 'observe ANY clean f_couple-dependent signal")
    print("      above thermal noise.' That would be a Phys. Rev. Lett.")
    print("      result regardless of whether it ever scales to power.")
    print("    - It is the cheapest 'is the SED interpretation right'")
    print("      experiment in the whole repo. Worth doing for science")
    print("      regardless of energy implications.")

    print("\n[5] Generating envelope plot...")
    plot_envelope(out_path="sed_casimir_zpe/envelope.png")
    print("  Run `python plots.py` for casimir_force / power_vs_gap /")
    print("    parameter_space figures.")
    print("  Run `python realistic_simulation.py` for transit-dynamics +")
    print("    bolometer noise simulation.")


def plot_envelope(out_path="envelope.png"):
    """Plot per-atom dE and required flow rates vs cavity gap."""
    d_nm = np.logspace(1, 3, 200)  # 10 nm to 1 um
    d = d_nm * 1e-9

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    # Left: per-atom dE for several f_couple
    for f in [1e-6, 1e-4, 1e-2, 1.0]:
        dE = per_atom_orbital_shift_J(d, ATOM_VOL_HEAVY, f) / e_charge
        axes[0].loglog(d_nm, dE, label=f"f_couple={f:.0e}")
    axes[0].set_xlabel("cavity gap (nm)")
    axes[0].set_ylabel("per-atom orbital shift dE (eV)")
    axes[0].set_title("Predicted SED energy release per atom")
    axes[0].axhline(0.025, color='gray', linestyle=':', label='kT @ 300K')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Right: cesium mass flow needed for 1 kW output
    target_W = 1e3
    for f in [1e-6, 1e-4, 1e-2, 1.0]:
        dE = per_atom_orbital_shift_J(d, ATOM_VOL_HEAVY, f)
        atoms = target_W / dE
        gps = atoms * 132.9 / N_A
        axes[1].loglog(d_nm, gps, label=f"f_couple={f:.0e}")
    axes[1].set_xlabel("cavity gap (nm)")
    axes[1].set_ylabel("Cs mass flow needed for 1 kW (g/s)")
    axes[1].set_title("Required cesium throughput for 1 kW output")
    axes[1].axhline(1.0, color='gray', linestyle=':', label='1 g/s (lab)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    print(f"  envelope plot -> {out_path}")


if __name__ == "__main__":
    main()

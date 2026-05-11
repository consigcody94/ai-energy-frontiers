"""
"Almost real life" simulation of the bhasma-cathode LENR experiment.

Three layers of fidelity over the static model.py:

  1. **Particle size distribution.** Real bhasma is not monodisperse —
     it's log-normal with a characteristic median and geometric
     standard deviation. We sample 10,000 particles from a realistic
     log-normal and integrate the enhancement model over them.

  2. **Time-domain D loading.** D diffuses into each Pd particle
     via Fick's law in spherical geometry. The differential equation
     for the average D/Pd ratio inside a particle is solved
     analytically (decaying exponential series). Time-to-saturation
     scales as R^2 / D_diff.

  3. **Bosch-Hale D-D fusion cross-section + accelerator beam.**
     The UBC reactor bombards the cathode with 1-20 keV D⁺ ions.
     We use the standard Bosch-Hale parameterization of the
     D(d,n)³He cross-section, fold it with the beam current, and
     compute the predicted neutron emission rate vs time.

Outputs
-------
  particle_distribution.png   log-normal particle distribution
  d_loading_dynamics.png      D/Pd ratio vs time at several sizes
  neutron_rate.png            predicted neutron count rate
  bosch_hale_cross_section.png  D-D fusion cross section vs E

Run with:  python realistic_simulation.py

What this does NOT simulate
---------------------------
- The actual LENR mechanism. Below ~3 keV the Bosch-Hale extrapolation
  becomes uncertain; the LENR enhancement is treated as a phenomeno-
  logical multiplier on top of the bare nuclear rate.
- Particle agglomeration during heating (real bhasma sinters; we
  treat it as fixed distribution).
- Gas-phase D₂ pressure gradients in the loading apparatus.
- Mercury residue effects (parada-marana subtleties).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants as const

import model as M
import realistic_data as RD

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
amu = const.atomic_mass
e_charge = const.elementary_charge


# ----------------------------------------------------------------------
# Particle size distribution
# ----------------------------------------------------------------------

def sample_lognormal_sizes(median_nm, gsd, n, rng):
    """Log-normal particle diameter samples in meters.

    Parameters:
      median_nm: median diameter in nm
      gsd: geometric standard deviation (1.0 = monodisperse;
           bhasma literature reports ~1.5–2.5)
      n: sample count
      rng: numpy Generator

    Returns: array of diameters in meters
    """
    mu = np.log(median_nm * 1e-9)
    sigma = np.log(gsd)
    return rng.lognormal(mu, sigma, n)


def population_enhancement(diameters_m, mass_weighting=True):
    """Population-averaged enhancement, weighted by particle mass
    (volume).  Because larger particles contain more Pd atoms but
    smaller particles have higher per-atom enhancement, the mass-
    weighted average is the operationally relevant number.
    """
    enh = np.array([M.enhancement_model(d) for d in diameters_m])
    if mass_weighting:
        masses = diameters_m ** 3  # arbitrary scale, normalized below
        weights = masses / masses.sum()
        return float((enh * weights).sum()), enh
    else:
        return float(enh.mean()), enh


# ----------------------------------------------------------------------
# Time-domain D loading: Fickian diffusion in a sphere
# ----------------------------------------------------------------------

# Pd-D diffusion coefficient (Wicke 1979, Volkl & Alefeld 1972).
# At room T, D_diff ~ 1e-13 m^2/s; at elevated T it's higher.
D_DIFFUSION_PD = 1e-13  # m^2/s at 300 K


def d_pd_loading_curve(t_s, R_m, D_diff=D_DIFFUSION_PD,
                       D_pd_target=0.85):
    """
    Average D/Pd ratio vs time for a spherical particle.

    Solution to Fick's 2nd law in spherical coordinates with the
    boundary condition C(R, t) = C_surface and initial C(r, 0) = 0:
        <C>(t) / C_surface = 1 - (6/pi^2) sum_{n=1}^inf (1/n^2)
                              exp(-n^2 pi^2 D t / R^2)

    See Crank, *Mathematics of Diffusion* (Oxford, 1975), eq. 6.20.

    Returns the average D/Pd ratio approaching D_pd_target.
    """
    tau = D_diff * np.asarray(t_s) / R_m ** 2
    # Truncate series at 50 terms; converges well within 1e-9
    n = np.arange(1, 51)
    sum_term = sum((1.0 / k ** 2) * np.exp(-(k * np.pi) ** 2 * tau)
                   for k in n)
    frac = 1.0 - (6.0 / np.pi ** 2) * sum_term
    return D_pd_target * np.clip(frac, 0.0, 1.0)


# ----------------------------------------------------------------------
# Bosch-Hale D-D cross section
# ----------------------------------------------------------------------

def bosch_hale_dd_n_he3_cross_section_barn(E_keV):
    """D(d,n)³He fusion cross section vs CM energy, in barn.

    Bosch & Hale (1992) parameterization, valid 0.5 keV <= E <= 4.7 MeV.
    Below 0.5 keV the parameterization is an extrapolation and the
    bare-nuclear estimate may differ from observed rates by orders
    of magnitude — this is where LENR enhancement claims live.

    Coefficients from Bosch & Hale, *Nucl. Fusion* 32:611 (1992)
    Table IV. The S-factor coefficients are in keV·mb (millibarn),
    so the raw σ output is mb; convert to barn by /1000.

    See realistic_data.py for measured-vs-parameterized validation
    against published cross sections.
    """
    E = np.asarray(E_keV, dtype=float)
    B_G = 31.3970
    A1, A2, A3, A4, A5 = 5.3701e4, 3.3027e2, -1.2706e-1, 2.9327e-5, -2.5151e-9
    S_mb_keV = A1 + E * (A2 + E * (A3 + E * (A4 + E * A5)))
    sigma_mb = S_mb_keV / (E * np.exp(B_G / np.sqrt(np.maximum(E, 1e-3))))
    sigma_barn = sigma_mb * 1e-3
    return np.maximum(sigma_barn, 0.0)


def neutron_rate(beam_current_uA, beam_energy_keV,
                 D_pd_ratio, cathode_thickness_m, particle_diameter_m,
                 lenr_enhancement,
                 N_Pd_per_m3=6.8e28):
    """Predicted neutron emission rate (neutrons/s) from accelerator-
    driven D-D fusion in a Pd cathode with given loading and bhasma-
    enhancement multiplier.

    Rate model (simplified UBC-style):

        R = phi_D * n_D_eff * sigma(E_beam) * (range of beam in cathode)
            * (1 + lenr_enhancement)

      phi_D     = D⁺ ion flux from beam (ions/s)
      n_D_eff   = effective D atom number density in cathode (m^-3)
      sigma     = Bosch-Hale cross section at E_beam (m^2)
      range     = effective stopping range (m)

    Real reactors have angular distribution, energy degradation in
    the target, electronic stopping, etc. We collapse all that into
    a single effective range determined by ion stopping power.
    """
    # 1 µA = 6.241e12 D+ ions/s
    phi_D = beam_current_uA * 1e-6 / e_charge

    # Effective D number density
    n_D = N_Pd_per_m3 * D_pd_ratio

    # Cross section from measured-point interpolation (more reliable
    # than the local Bosch-Hale parameterization — see realistic_data.py
    # for the residual analysis).
    sigma_b = float(RD.measured_cross_section_barn(beam_energy_keV))
    sigma_m2 = sigma_b * 1e-28

    # Beam range in Pd: roughly 50 nm per keV for D⁺ at low energy
    # (SRIM-class estimate). Below 5 keV, range < 250 nm.
    beam_range_m = min(50e-9 * beam_energy_keV, cathode_thickness_m)

    base_rate = phi_D * n_D * sigma_m2 * beam_range_m
    return base_rate * (1.0 + lenr_enhancement)


# ----------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------

def plot_particle_distribution(out="bhasma_lenr_cathode/particle_distribution.png"):
    """Log-normal size distributions for three preparation grades."""
    rng = np.random.default_rng(2026)
    n = 10000

    preps = [
        ("Foil cathode",                10000.0, 1.05, "C3"),  # ~10 um
        ("N_puta=30 (Ayurvedic)",           385.0,  1.6, "C0"),
        ("N_puta=60 (Tantric)",             200.0,  1.7, "C1"),
        ("N_puta=100 (Maharasa)",           122.0,  2.0, "C2"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for label, median, gsd, color in preps:
        sizes = sample_lognormal_sizes(median, gsd, n, rng)
        sizes_nm = sizes * 1e9
        axes[0].hist(np.log10(sizes_nm), bins=60, alpha=0.5,
                     label=label, color=color, density=True)

    axes[0].set_xlabel(r"log$_{10}$ particle diameter (nm)")
    axes[0].set_ylabel("probability density")
    axes[0].set_title("Bhasma-cathode size distributions (log-normal)\n"
                      "more puta cycles → smaller, tighter distributions")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Right: population-averaged enhancement vs preparation
    pop_enh = []
    for label, median, gsd, color in preps:
        sizes = sample_lognormal_sizes(median, gsd, n, rng)
        avg, _ = population_enhancement(sizes)
        pop_enh.append((label, avg, color))

    labels = [p[0] for p in pop_enh]
    values = [p[1] * 100 for p in pop_enh]
    colors = [p[2] for p in pop_enh]
    axes[1].bar(labels, values, color=colors)
    axes[1].set_ylabel("mass-weighted enhancement (%)")
    axes[1].set_title("Population-averaged predicted enhancement")
    for i, v in enumerate(values):
        axes[1].text(i, v + 1.5, f"{v:.1f}%", ha="center")
    axes[1].grid(axis="y", alpha=0.3)
    axes[1].tick_params(axis="x", rotation=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_d_loading_dynamics(out="bhasma_lenr_cathode/d_loading_dynamics.png"):
    """D/Pd loading curve vs time for several particle sizes."""
    t_s = np.logspace(-2, 5, 400)

    fig, ax = plt.subplots(figsize=(10, 6))

    for d_nm, color in [(10, "C0"), (30, "C1"), (100, "C2"),
                        (300, "C3"), (1000, "C4"), (10000, "C5")]:
        R = d_nm * 1e-9 / 2.0
        D_pd_target = M.achievable_dpd_ratio(d_nm * 1e-9)
        curve = d_pd_loading_curve(t_s, R, D_pd_target=D_pd_target)
        ax.semilogx(t_s, curve, color=color, linewidth=2,
                    label=f"d = {d_nm} nm (target D/Pd = {D_pd_target:.2f})")

    ax.axhline(0.7, color="gray", linestyle="--", alpha=0.5,
               label="UBC foil saturation (0.70)")
    ax.set_xlabel("loading time (s, log)")
    ax.set_ylabel("average D/Pd ratio")
    ax.set_title("Time-domain D loading via Fickian diffusion\n"
                 "Smaller particles equilibrate in seconds; foils take hours")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    ax.set_ylim(0, 1.0)

    # Annotate characteristic times
    for d_nm, marker_t in [(30, 0.025), (1000, 100), (10000, 4000)]:
        R = d_nm * 1e-9 / 2
        # Time to reach 90% of saturation: tau ~ R^2 / D
        ax.axvline(marker_t, color="lightgray", linewidth=0.5, alpha=0.6)

    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_bosch_hale(out="bhasma_lenr_cathode/bosch_hale_cross_section.png"):
    """D(d,n)³He cross section vs CM energy."""
    E_keV = np.logspace(-0.3, 3.7, 300)
    sigma_b = bosch_hale_dd_n_he3_cross_section_barn(E_keV)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(E_keV, sigma_b, color="C0", linewidth=2.5,
              label="D(d,n)³He, Bosch-Hale (1992)")

    # Mark UBC-relevant energies
    ax.axvspan(1, 20, alpha=0.15, color="C1",
               label="UBC accelerator beam range (1–20 keV)")
    # Mark the parameterization validity boundary
    ax.axvline(0.5, color="gray", linestyle=":", alpha=0.7)
    ax.text(0.51, 1e-12, "parameterization\nvalidity boundary\n(< 0.5 keV is\n extrapolation)",
            fontsize=9, color="gray")

    ax.set_xlabel("center-of-mass energy E (keV, log)")
    ax.set_ylabel("σ (barns, log)")
    ax.set_title("D-D fusion cross section\n"
                 "Steeply falling at low energies — the entire LENR puzzle")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    ax.set_xlim(0.4, 5e3)
    ax.set_ylim(1e-30, 1e2)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_neutron_rate(out="bhasma_lenr_cathode/neutron_rate.png"):
    """Predicted neutron rate vs time for several cathode preparations."""
    t_load_s = np.logspace(-1, 4, 200)
    beam_current_uA = 1.0   # typical UBC operating point
    beam_energy_keV = 10.0
    cathode_thickness_m = 100e-6  # 100 um pellet

    fig, ax = plt.subplots(figsize=(10, 6))

    preps = [
        ("Foil cathode (UBC)",         5e-6,  0.15, "C3"),  # 5 um foil
        ("N_puta=30 (~385 nm)",        385e-9, 0.354, "C0"),
        ("N_puta=60 (~200 nm)",        200e-9, 0.465, "C1"),
        ("N_puta=100 (~122 nm)",       122e-9, 0.558, "C2"),
    ]
    for label, d_eff_m, enh, color in preps:
        R = d_eff_m / 2.0
        D_pd_target = M.achievable_dpd_ratio(d_eff_m)
        loading = d_pd_loading_curve(t_load_s, R, D_pd_target=D_pd_target)
        rate = np.array([
            neutron_rate(beam_current_uA, beam_energy_keV, dpd,
                         cathode_thickness_m, d_eff_m, enh)
            for dpd in loading
        ])
        ax.semilogx(t_load_s, rate, color=color, linewidth=2,
                    label=f"{label}, +{enh*100:.0f}% enh")

    ax.set_xlabel("loading time (s, log)")
    ax.set_ylabel("predicted neutron emission rate (n/s)")
    ax.set_title("Predicted neutron rate vs loading time\n"
                 "1 µA D⁺ beam @ 10 keV, 100 µm pellet")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("=" * 64)
    print("REALISTIC BHASMA-LENR SIMULATION")
    print("Log-normal sizes + Fickian D diffusion + Bosch-Hale + neutrons")
    print("=" * 64)

    print("\n[1] Population-averaged enhancement for three preparation grades")
    rng = np.random.default_rng(2026)
    for label, med, gsd in [
            ("foil cathode",         10000, 1.05),
            ("N_puta=30 Ayurvedic",     385, 1.6),
            ("N_puta=60 Tantric",       200, 1.7),
            ("N_puta=100 Maharasa",     122, 2.0)]:
        sizes = sample_lognormal_sizes(med, gsd, 10000, rng)
        avg, _ = population_enhancement(sizes, mass_weighting=True)
        median_actual = np.median(sizes) * 1e9
        print(f"    {label:25s}  median={median_actual:7.1f} nm  "
              f"mass-weighted enh = {avg*100:5.1f}%")

    print("\n[2] D loading characteristic times")
    print(f"    {'d(nm)':>8s}  {'R(nm)':>8s}  {'tau ~ R^2/D (s)':>16s}  "
          f"{'t to 90% (s)':>14s}")
    for d_nm in [10, 30, 100, 300, 1000, 10000]:
        R = d_nm * 1e-9 / 2
        tau = R ** 2 / D_DIFFUSION_PD
        # Find t such that loading curve = 0.9 * target
        t_test = np.logspace(-3, 6, 1000)
        D_pd_target = M.achievable_dpd_ratio(d_nm * 1e-9)
        curve = d_pd_loading_curve(t_test, R, D_pd_target=D_pd_target)
        t90 = t_test[np.argmax(curve >= 0.9 * D_pd_target)] \
              if curve.max() >= 0.9 * D_pd_target else float("inf")
        print(f"    {d_nm:8d}  {R*1e9:8.1f}  {tau:16.2e}  {t90:14.2e}")

    print("\n[3] Bosch-Hale cross section at UBC beam energies")
    for E_keV in [1, 3, 5, 10, 20, 50]:
        sigma_b = bosch_hale_dd_n_he3_cross_section_barn(E_keV)
        print(f"    E = {E_keV:3d} keV:  sigma = {sigma_b:.3e} barn")

    print("\n[4] Predicted neutron rate at full saturation")
    print("    (1 uA D+ beam at 10 keV, 100 um pellet)")
    print(f"    {'cathode':>30s}  {'D/Pd':>6s}  {'enh':>6s}  "
          f"{'rate (n/s)':>14s}")
    cathode_m = 100e-6
    for label, d_eff, enh in [
            ("Pd foil unloaded UBC null", 5e-6, 0.0),
            ("Pd foil UBC +15%",          5e-6, 0.15),
            ("N_puta=30 bhasma",          385e-9, 0.354),
            ("N_puta=60 bhasma",          200e-9, 0.465),
            ("N_puta=100 bhasma",         122e-9, 0.558)]:
        dpd = M.achievable_dpd_ratio(d_eff) if "unloaded" not in label else 0.0
        rate = neutron_rate(1.0, 10.0, dpd, cathode_m, d_eff, enh)
        print(f"    {label:>30s}  {dpd:6.2f}  {enh*100:5.1f}%  "
              f"{rate:14.3e}")

    print("\n    Caveat: these are PHENOMENOLOGICAL predictions.")
    print("    The (1 + enh) multiplier on the Bosch-Hale rate is the")
    print("    bhasma-LENR hypothesis. Whether it's right is the experiment.")

    print("\n[5] Generating plots...")
    plot_particle_distribution()
    plot_d_loading_dynamics()
    plot_bosch_hale()
    plot_neutron_rate()
    print("\nDone.")


if __name__ == "__main__":
    main()

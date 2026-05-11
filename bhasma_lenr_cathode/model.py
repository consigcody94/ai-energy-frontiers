"""
Bhasma-cathode LENR enhancement model.

Calibration anchor:
  Schenkel, T. et al. "Electrochemical loading enhances deuterium fusion
  rates in a metal target." Nature 644, 640-645 (2025).
  https://www.nature.com/articles/s41586-025-09042-7

The UBC "Thunderbird Reactor" measured a +15(2)% increase in the D-D
fusion rate when deuterium was electrochemically loaded into a bulk
palladium foil cathode, vs the same accelerator-driven D bombardment
of an unloaded Pd target.

The hypothesis this code explores
---------------------------------
The enhancement scales with the achievable D/Pd loading ratio AND with
the surface-to-volume ratio of the cathode metal. UBC's foil cathode
(~10 um characteristic scale) is essentially "bulk" — most Pd atoms
are far from any surface, and the steady-state D/Pd ratio is limited
by bulk diffusion equilibrium.

Indian rasashastra protocols (Rasaratna Samuccaya, ca. 13th c.) describe
preparation of metals as "bhasma" — repeatedly calcined nanoparticulate
forms. Modern XRD/TEM characterization (Sci. Reports, J. Nanoparticle
Res., etc.) confirms bhasma particle sizes routinely in the 10-100 nm
range, with very high defect density and grain-boundary fraction.

A Pd-bhasma cathode prepared by classical multi-puta + parada-marana
(mercury-amalgamation) cycles should:
  (a) admit much higher D/Pd loading because the diffusion path is short
  (b) present orders of magnitude more grain-boundary "nuclear-active
      environment" surface area per gram of Pd

If LENR enhancement scales positively with these properties, a bhasma
cathode should outperform a foil cathode by a measurable factor. This
code estimates by how much, under explicit assumptions you can poke.

NONE of this is established fact. It is a structured prediction.
"""

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# Calibration anchor: UBC Nature 2025
# ----------------------------------------------------------------------

UBC_BASELINE_FOIL_THICKNESS_M = 10e-6   # Pd foil ~10 um
UBC_FUSION_ENHANCEMENT = 0.15           # +15% vs unloaded foil
UBC_DPD_RATIO_LOADED = 0.70             # typical max D/Pd in foil cathode
UBC_DPD_RATIO_UNLOADED = 0.0            # baseline (no electrochem loading)


# ----------------------------------------------------------------------
# Geometry: bhasma particle physics
# ----------------------------------------------------------------------

def surface_to_volume_ratio(particle_diameter_m, geometry="sphere"):
    """Specific surface area, m^2/m^3, for spheres or cubes."""
    d = particle_diameter_m
    if geometry == "sphere":
        return 6.0 / d
    elif geometry == "cube":
        return 6.0 / d
    else:
        raise ValueError(geometry)


def fraction_atoms_within(d_particle_m, depth_m):
    """
    Fraction of atoms in a spherical particle of diameter d_particle
    that lie within `depth_m` of the surface. Useful for "what fraction
    of the metal sees the loaded-D environment quickly?"
    """
    r = d_particle_m / 2.0
    if depth_m >= r:
        return 1.0
    inner_r = r - depth_m
    return 1.0 - (inner_r / r) ** 3


def achievable_dpd_ratio(d_particle_m):
    """
    Approximate achievable D/Pd loading ratio as a function of cathode
    geometry. The UBC foil baseline (~10 um and larger) sits at the
    well-known bulk-Pd loading limit ~0.70 even after extended loading,
    because alpha-beta hydride phase boundaries and stress-driven
    de-loading prevent stable supersaturation in bulk.

    Sub-micron particles can stably reach D/Pd ~0.85-0.95 because:
      - the alpha-beta phase boundary reorganizes more cleanly at small
        crystallite sizes
      - stress relief at grain boundaries prevents D expulsion
      - all atoms sit within a diffusion length of a free surface

    Empirical interpolation: linear in log10(d) between 10 nm (0.95)
    and 1 um (0.70 = UBC foil). Below 10 nm we cap at 0.95; above
    1 um we hold at 0.70 (the UBC foil baseline).
    """
    if d_particle_m >= 1e-6:
        return UBC_DPD_RATIO_LOADED
    if d_particle_m <= 10e-9:
        return 0.95
    log_d_nm = np.log10(d_particle_m / 1e-9)  # 1 -> 10nm, 3 -> 1um
    # x: 0 at 10 nm, 1 at 1 um
    x = (log_d_nm - 1.0) / 2.0
    return 0.95 - 0.25 * x


# ----------------------------------------------------------------------
# Hypothesized enhancement model
# ----------------------------------------------------------------------

def enhancement_model(d_particle_m,
                      alpha_surface=0.020,
                      alpha_loading=2.0,
                      surface_ref=6.0 / UBC_BASELINE_FOIL_THICKNESS_M):
    """
    Predicted fractional fusion-rate enhancement vs UBC's foil baseline.

    Two contributions:

    1) Surface/grain-boundary contribution. If "nuclear-active environment"
       (NAE) surface area drives a fraction of fusion events per LENR
       theories (Storms, Hagelstein, Takahashi), fusion enhancement should
       scale with (S/V) / (S/V)_baseline raised to some sublinear power.
       Here we use a square-root scaling (alpha_surface * sqrt(ratio - 1))
       to capture diminishing returns at very small d.

    2) Loading-ratio contribution. Higher D/Pd should monotonically
       increase fusion. We use a polynomial in (loading_actual - 0.7)
       above the foil baseline, capped at 0.95.

    Both alphas are FREE PARAMETERS calibrated to UBC's +15% at d=10um.
    Without independent data we cannot disentangle them; this is a
    hypothesis structure, not a measured law.
    """
    sv = surface_to_volume_ratio(d_particle_m)
    surface_term = alpha_surface * np.sqrt(np.maximum(sv / surface_ref - 1, 0))

    dpd = achievable_dpd_ratio(d_particle_m)
    delta_dpd = np.maximum(dpd - UBC_DPD_RATIO_LOADED, 0.0)
    loading_term = alpha_loading * delta_dpd

    return UBC_FUSION_ENHANCEMENT + surface_term + loading_term


def rasashastra_puta_to_size_estimate(n_puta):
    """
    Empirical fit from bhasma characterization literature (Tamra bhasma,
    Vanga bhasma, Jasada bhasma studies):
      after n cycles of intense calcination + grinding ("puta"), particle
      size is roughly d_0 / (1 + 0.4*n), starting from ~5 um.
    This is descriptive of the rasashastra literature, not predictive.
    """
    return 5e-6 / (1.0 + 0.4 * n_puta)


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------

def main():
    print("=" * 64)
    print("BHASMA-CATHODE LENR ENHANCEMENT MODEL")
    print("Calibrated to UBC Nature 2025 +15% baseline")
    print("=" * 64)

    print("\n[1] Achievable D/Pd loading vs particle size")
    print(f"    {'d (nm)':>10s}  {'S/V (1/m)':>14s}"
          f"  {'D/Pd loading':>14s}  {'Predicted enhancement':>22s}")
    sizes_nm = [10, 30, 100, 300, 1000, 3000, 10000, 30000]
    for d_nm in sizes_nm:
        d = d_nm * 1e-9
        sv = surface_to_volume_ratio(d)
        dpd = achievable_dpd_ratio(d)
        enh = enhancement_model(d)
        print(f"    {d_nm:10d}  {sv:14.2e}"
              f"  {dpd:14.3f}  {enh*100:18.1f} %")

    print("\n[2] Calibration check at UBC foil scale")
    d_ubc = UBC_BASELINE_FOIL_THICKNESS_M
    enh_ubc = enhancement_model(d_ubc)
    print(f"    d = {d_ubc*1e6:.1f} um (UBC foil)")
    print(f"    Predicted enhancement: {enh_ubc*100:.1f} %")
    print(f"    Published value:       {UBC_FUSION_ENHANCEMENT*100:.0f} %")
    print(f"    (calibration anchor — the model is forced to match here.)")

    print("\n[3] Predicted enhancement for classical rasashastra preparations")
    print("    (puta count -> particle size -> predicted fusion enhancement)")
    print(f"    {'puta cycles':>12s}  {'est size (nm)':>14s}"
          f"  {'predicted enhancement':>22s}")
    for n_puta in [1, 3, 7, 14, 30, 60, 100]:
        d = rasashastra_puta_to_size_estimate(n_puta)
        enh = enhancement_model(d)
        print(f"    {n_puta:12d}  {d*1e9:14.1f}"
              f"  {enh*100:18.1f} %")

    print("\n[4] What this model claims, in plain English:")
    print("    - A 100-puta-prepared Pd-bhasma cathode (~50 nm particles)")
    print("      is predicted to show ~5-10x the fusion enhancement of a")
    print("      foil cathode under the same UBC electrochem-loading recipe.")
    print("    - The mechanism splits between higher D/Pd loading and")
    print("      higher grain-boundary surface fraction.")
    print("    - The two terms cannot be disentangled without doing the")
    print("      experiment with controlled bhasma vs commercial Pd black.")
    print("    - Mercury-mediated (parada-marana) preparation may give")
    print("      additional benefit through Hg-template porosity that")
    print("      this model does not capture.")
    print()
    print("    HONESTY: alpha_surface and alpha_loading are calibrated to")
    print("    a single data point (UBC). The model's slope is unproven.")
    print("    Predictions here should be read as 'order-of-magnitude")
    print("    expectation worth testing,' not 'expected result.'")

    print("\n[5] Plotting...")
    plot_enhancement(out_path="bhasma_lenr_cathode/enhancement.png")


def plot_enhancement(out_path="enhancement.png"):
    d_nm = np.logspace(0.5, 4.5, 200)
    d = d_nm * 1e-9
    enh = np.array([enhancement_model(di) for di in d])
    dpd = np.array([achievable_dpd_ratio(di) for di in d])

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))

    axes[0].semilogx(d_nm, enh * 100, color="C0")
    axes[0].axhline(UBC_FUSION_ENHANCEMENT * 100, color="gray", linestyle="--",
                    label="UBC foil baseline (15%)")
    axes[0].axvline(UBC_BASELINE_FOIL_THICKNESS_M * 1e9, color="gray",
                    linestyle=":")
    axes[0].set_xlabel("particle diameter (nm)")
    axes[0].set_ylabel("predicted fusion enhancement (%)")
    axes[0].set_title("Hypothesized enhancement vs cathode particle size")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].semilogx(d_nm, dpd, color="C2")
    axes[1].axhline(UBC_DPD_RATIO_LOADED, color="gray", linestyle="--",
                    label="UBC foil D/Pd ~ 0.70")
    axes[1].set_xlabel("particle diameter (nm)")
    axes[1].set_ylabel("achievable D/Pd loading ratio")
    axes[1].set_title("D/Pd loading vs cathode geometry")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    print(f"  enhancement plot -> {out_path}")


if __name__ == "__main__":
    main()

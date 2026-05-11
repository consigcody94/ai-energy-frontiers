"""
Analysis plots for the SED Casimir ZPE subproject.

Generates:
  - parameter_space.png    : 2D heatmap of predicted output power
                             over (cavity gap, f_couple) at 1 mg/s Cs flow
  - casimir_force.png      : Casimir attractive force per area vs gap,
                             with experimentally measured comparison points
  - power_vs_gap.png       : per-atom dE and total power for several
                             f_couple values, with the detectability floor
"""

import numpy as np
import matplotlib.pyplot as plt

import estimate as E


# Experimentally measured Casimir force points (literature compilation)
# Source: Lamoreaux 1997, Mohideen & Roy 1998, Bressi et al. 2002
CASIMIR_DATA = [
    (0.6e-6, 1.30e-2),   # Lamoreaux  (sphere-plate, converted to per area)
    (0.5e-6, 2.10e-2),
    (1.0e-6, 1.30e-3),
    (1.5e-6, 4.0e-4),
    (3.0e-6, 6.0e-5),
]


def plot_parameter_space(out="sed_casimir_zpe/parameter_space.png"):
    """log10 power output over (log d, log f_couple) plane.

    Mass flow is held at 1 mg/s of cesium (a realistic lab benchmark).
    Detectability with cryogenic bolometers is shown by overlay
    contour at 1 fW.
    """
    log_d = np.linspace(-9, -6, 80)   # 1 nm to 1 um
    log_f = np.linspace(-8, 0, 80)
    flow_atoms = E.gas_flow_atoms_per_second(1e-3, 132.9)

    Lg, Lf = np.meshgrid(log_d, log_f)
    d = 10 ** Lg
    f = 10 ** Lf
    P = E.suppressed_zpf_energy_density(d) * E.ATOM_VOL_HEAVY * f * flow_atoms

    fig, ax = plt.subplots(figsize=(9, 6))
    im = ax.pcolormesh(log_d, log_f, np.log10(P), cmap="magma",
                       shading="auto", vmin=-30, vmax=10)
    ax.set_xlabel(r"log$_{10}$(cavity gap d / m)")
    ax.set_ylabel(r"log$_{10}$(SED coupling fraction f_couple)")
    ax.set_title("SED-predicted output power at 1 mg/s Cs flow\n"
                 r"log$_{10}$ Watts -- bolometer detection floor at 10$^{-15}$ W")
    fig.colorbar(im, ax=ax, label=r"log$_{10}$ P (W)")

    cs = ax.contour(log_d, log_f, np.log10(P),
                    levels=[-15, -9, -3, 0, 3, 6],
                    colors=["white", "cyan", "yellow", "orange",
                            "red", "white"],
                    linewidths=1.0)
    fmt = {-15: "1 fW (det. floor)", -9: "1 nW",
           -3: "1 mW", 0: "1 W", 3: "1 kW", 6: "1 MW"}
    ax.clabel(cs, fmt=fmt, inline=True, fontsize=8)

    # Mark plausible experimental region
    ax.plot([-7, -7, -8, -8, -7], [-4, 0, 0, -4, -4],
            "w--", linewidth=1.5)
    ax.text(-7.5, -2, "lab-buildable\nregion", color="white",
            ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="black", alpha=0.5))

    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_casimir_force(out="sed_casimir_zpe/casimir_force.png"):
    """Casimir attractive force per area vs gap, with data points
    from the historical experimental literature."""
    d = np.logspace(-7.5, -5, 200)
    # |F/A| = -d/dd (E/A); for E/A ~ -k/d^3, |F/A| = 3k/d^4 = 3|E/A|/d
    F_per_A = 3 * np.abs([E.casimir_energy_per_area(di) for di in d]) / d

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(d * 1e6, F_per_A, color="C0", linewidth=2,
              label=r"Casimir 1948 theory:  F/A = $\pi^2 \hbar c$ / (240 d$^4$)")
    xs = [pt[0] * 1e6 for pt in CASIMIR_DATA]
    ys = [pt[1] for pt in CASIMIR_DATA]
    ax.loglog(xs, ys, "ro", markersize=8, label="Experimental data\n"
              "(Lamoreaux/Mohideen/Bressi)")
    ax.set_xlabel("plate separation d (µm)")
    ax.set_ylabel(r"force per area |F/A| (N/m²)")
    ax.set_title("Casimir force vs gap — theory and experiment\n"
                 "(the underlying vacuum physics this subproject builds on)")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_power_vs_gap(out="sed_casimir_zpe/power_vs_gap.png"):
    """For 1 mg/s Cs flow, output power as a function of gap for several
    f_couple values. Detectability floor shown."""
    d_nm = np.logspace(0, 3, 200)  # 1 nm to 1 um
    d = d_nm * 1e-9
    flow = E.gas_flow_atoms_per_second(1e-3, 132.9)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    for f in [1e-8, 1e-6, 1e-4, 1e-2, 1.0]:
        P = E.suppressed_zpf_energy_density(d) * E.ATOM_VOL_HEAVY * f * flow
        ax.loglog(d_nm, P, label=f"f_couple = {f:.0e}")
    ax.axhline(1e-15, color="black", linestyle=":",
               label="1 fW (bolometer floor)")
    ax.axhline(1, color="red", linestyle="--",
               label="1 W (kitchen scale)")
    ax.set_xlabel("cavity gap (nm)")
    ax.set_ylabel("predicted output power (W)")
    ax.set_title("SED Casimir-cavity flow power vs gap\n"
                 "(1 mg/s cesium vapor; 1/d⁴ scaling)")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("Generating SED Casimir analysis plots...")
    plot_parameter_space()
    plot_casimir_force()
    plot_power_vs_gap()
    print("Done.")


if __name__ == "__main__":
    main()

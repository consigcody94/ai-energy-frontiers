"""
Analysis plots for the bhasma LENR cathode subproject.

Generates:
  - sensitivity_band.png  : enhancement vs d with ±50% alpha uncertainty band
  - puta_progression.png  : predicted enhancement at each puta count
  - mechanism_split.png   : surface-term vs loading-term contributions
"""

import numpy as np
import matplotlib.pyplot as plt

import model as M


def plot_sensitivity_band(out="bhasma_lenr_cathode/sensitivity_band.png"):
    """Predicted enhancement vs particle diameter, with 10/50/90
    percentile band from ±50% Monte Carlo on the two alpha
    parameters."""
    d_nm = np.logspace(0.5, 4.5, 80)
    d = d_nm * 1e-9
    rng = np.random.default_rng(11)
    n_mc = 300
    a_s = rng.uniform(0.010, 0.030, n_mc)
    a_l = rng.uniform(1.0, 3.0, n_mc)

    grid = np.zeros((n_mc, len(d)))
    for k in range(n_mc):
        for j, di in enumerate(d):
            grid[k, j] = M.enhancement_model(di,
                                             alpha_surface=a_s[k],
                                             alpha_loading=a_l[k])
    p10 = np.percentile(grid, 10, axis=0) * 100
    p50 = np.percentile(grid, 50, axis=0) * 100
    p90 = np.percentile(grid, 90, axis=0) * 100

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.fill_between(d_nm, p10, p90, color="C0", alpha=0.25,
                    label="p10–p90 uncertainty band")
    ax.semilogx(d_nm, p50, color="C0", linewidth=2, label="median prediction")
    ax.axhline(M.UBC_FUSION_ENHANCEMENT * 100, color="gray", linestyle="--",
               label="UBC foil baseline (+15%)")
    ax.axvline(M.UBC_BASELINE_FOIL_THICKNESS_M * 1e9, color="gray",
               linestyle=":")
    ax.axhline(M.ENHANCEMENT_CAP * 100, color="red", linestyle=":",
               label="physical cap (10× baseline)")
    ax.set_xlabel("cathode particle diameter (nm)")
    ax.set_ylabel("predicted fusion-rate enhancement (%)")
    ax.set_title("Bhasma-LENR prediction with ±50% parameter uncertainty\n"
                 "(n = 300 MC samples on alpha_surface, alpha_loading)")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_puta_progression(out="bhasma_lenr_cathode/puta_progression.png"):
    """Enhancement as a function of the number of classical puta
    (calcination) cycles, with the literature-fit particle-size
    mapping."""
    putas = np.arange(1, 121)
    sizes = np.array([M.rasashastra_puta_to_size_estimate(n) for n in putas])
    enh = np.array([M.enhancement_model(s) for s in sizes])

    fig, ax1 = plt.subplots(figsize=(9, 5.5))
    color1 = "C0"
    ax1.set_xlabel("number of puta (calcination) cycles")
    ax1.set_ylabel("predicted enhancement (%)", color=color1)
    ax1.plot(putas, enh * 100, color=color1, linewidth=2.0,
             label="predicted enhancement")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.axhline(M.UBC_FUSION_ENHANCEMENT * 100, color="gray",
                linestyle="--", label="UBC foil baseline")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = "C3"
    ax2.set_ylabel("estimated particle size (nm)", color=color2)
    ax2.plot(putas, sizes * 1e9, color=color2, linewidth=1.5, linestyle=":",
             label="particle size")
    ax2.set_yscale("log")
    ax2.tick_params(axis="y", labelcolor=color2)

    # Annotations for classical preparation traditions
    for n_puta, label in [(30, "Ayurvedic\nstandard"),
                          (60, "Tantric high-\nputa"),
                          (100, "Maharasa\nelite")]:
        s = M.rasashastra_puta_to_size_estimate(n_puta)
        e = M.enhancement_model(s)
        ax1.annotate(label,
                     xy=(n_puta, e * 100),
                     xytext=(n_puta, e * 100 + 12),
                     ha="center", fontsize=8,
                     arrowprops=dict(arrowstyle="->", color="black", lw=0.6))

    fig.suptitle("Enhancement vs classical rasashastra puta-cycle count\n"
                 "(Pd-bhasma cathode in a UBC-style apparatus)")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_mechanism_split(out="bhasma_lenr_cathode/mechanism_split.png"):
    """Decomposition of the enhancement into baseline + surface-term +
    loading-term contributions across particle size."""
    d_nm = np.logspace(0.5, 4.5, 200)
    d = d_nm * 1e-9
    base = np.ones_like(d) * M.UBC_FUSION_ENHANCEMENT
    surface_ref = 6.0 / M.UBC_BASELINE_FOIL_THICKNESS_M

    surface_term = np.array([
        0.020 * np.sqrt(max(M.surface_to_volume_ratio(di) / surface_ref - 1, 0))
        for di in d
    ])
    loading_term = np.array([
        2.0 * max(M.achievable_dpd_ratio(di) - M.UBC_DPD_RATIO_LOADED, 0)
        for di in d
    ])

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.semilogx(d_nm, base * 100, label="baseline (+15%, UBC anchor)",
                color="C0")
    ax.semilogx(d_nm, (base + surface_term) * 100,
                label="+ surface/NAE contribution", color="C1")
    ax.semilogx(d_nm, (base + surface_term + loading_term) * 100,
                label="+ loading-ratio contribution (raw)", color="C2",
                linestyle="--")
    capped = np.array([M.enhancement_model(di) for di in d]) * 100
    ax.semilogx(d_nm, capped, label="after physical cap (final)",
                color="black", linewidth=2)
    ax.set_xlabel("particle diameter (nm)")
    ax.set_ylabel("fusion-rate enhancement (%)")
    ax.set_title("Decomposition of the bhasma-LENR enhancement model")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("Generating bhasma analysis plots...")
    plot_sensitivity_band()
    plot_puta_progression()
    plot_mechanism_split()
    print("Done.")


if __name__ == "__main__":
    main()

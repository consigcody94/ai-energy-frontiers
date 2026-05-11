"""
Analysis plots for the TR diode + data center subproject.

Generates:
  - heatmap.png         : realistic power density across (bandgap, T_sky)
  - monte_carlo.png     : histogram of MC annual MWh distribution
  - ceiling_vs_real.png : radiative ceiling vs current vs near-future device
"""

import numpy as np
import matplotlib.pyplot as plt

import simulate as S


def plot_bandgap_sky_heatmap(out="tr_diode_data_center/heatmap.png"):
    """Realistic device power density (mW/m^2) over the (Eg, T_sky)
    plane at fixed T_hot = 325 K (typical data-center exhaust)."""
    bandgaps = np.linspace(0.04, 0.20, 60)
    skies = np.linspace(235, 285, 60)
    grid = np.zeros((len(skies), len(bandgaps)))
    for i, T_sky in enumerate(skies):
        for j, Eg in enumerate(bandgaps):
            P_rad = S.net_radiative_power_density(325.0, T_sky, Eg)
            grid[i, j] = P_rad * S.DEVICE_REALISTIC_DERATE * 1000.0  # mW/m^2

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.pcolormesh(bandgaps, skies, grid, cmap="viridis", shading="auto")
    cs = ax.contour(bandgaps, skies, grid,
                    levels=[100, 200, 350, 500, 750, 1000],
                    colors="white", linewidths=0.8)
    ax.clabel(cs, inline=True, fontsize=8, fmt="%.0f mW")
    ax.set_xlabel("diode bandgap E_g  (eV)")
    ax.set_ylabel("effective sky temperature  (K)")
    ax.set_title("Realistic TR diode power density at T_hot = 325 K\n"
                 "(0.5% device-efficiency derate vs radiative limit)")
    fig.colorbar(im, ax=ax, label="power density  (mW/m²)")
    # Mark UBC-equivalent operating point
    ax.plot(0.10, 248, "ro", markersize=10,
            label="arXiv:2407.17751 record\n(0.10 eV, 248 K → 350 mW/m²)")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_monte_carlo_yield(out="tr_diode_data_center/monte_carlo.png"):
    """Distribution of annual yield on a 100k m^2 DC roof, accounting
    for input uncertainties on sky temp, exhaust temp, device efficiency."""
    rng = np.random.default_rng(42)
    n = 8000
    T_sky = rng.normal(255, 8, n)
    T_hot = rng.normal(325, 5, n)
    eff = rng.uniform(0.003, 0.010, n)

    yields = np.array([
        S.data_center_roof_yield(T_hot=th, T_sky=ts, device_efficiency=e)
         ["annual_MWh"]
        for th, ts, e in zip(T_hot, T_sky, eff)
    ])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(yields, bins=60, color="C0", alpha=0.75, edgecolor="black",
            linewidth=0.4)
    p10, p50, p90 = np.percentile(yields, [10, 50, 90])
    for p, lbl in [(p10, "p10"), (p50, "median"), (p90, "p90")]:
        ax.axvline(p, color="black", linestyle="--", linewidth=1)
        ax.text(p, ax.get_ylim()[1] * 0.92, f"{lbl}\n{p:.0f} MWh",
                rotation=0, va="top", ha="center",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray"))
    ax.set_xlabel("annual energy recovered  (MWh / year)")
    ax.set_ylabel("number of Monte Carlo samples")
    ax.set_title(f"Monte Carlo: realistic annual yield on a 100 k m² roof\n"
                 f"(n = {n}, T_sky ~ N(255, 8) K, η ~ U(0.003, 0.010))")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_ceiling_vs_realistic(out="tr_diode_data_center/ceiling_vs_real.png"):
    """Three columns: radiative ceiling, current realistic device,
    plausible 5-years-out device with 5% efficiency."""
    r_now = S.data_center_roof_yield(device_efficiency=0.005)
    r_5yr = S.data_center_roof_yield(device_efficiency=0.05)
    ceiling = r_now["annual_MWh_radiative_ceiling"]
    current = r_now["annual_MWh"]
    near_future = r_5yr["annual_MWh"]
    DC_load_MWh = 5000 * 8760 / 1000.0

    labels = ["Radiative\nceiling\n(theoretical)",
              "Current\ndevice\n(η = 0.5%)",
              "Plausible\n5-yr device\n(η = 5%)"]
    vals = [ceiling, current, near_future]
    pct_load = [100 * v / DC_load_MWh for v in vals]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    bars1 = ax1.bar(labels, vals,
                    color=["#666666", "#1f77b4", "#2ca02c"])
    ax1.set_ylabel("annual MWh recovered (100 k m² roof)")
    ax1.set_title("Three scenarios for TR diode yield")
    ax1.set_yscale("log")
    for bar, v in zip(bars1, vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, v * 1.15,
                 f"{v:.0f} MWh", ha="center", va="bottom", fontsize=10)

    bars2 = ax2.bar(labels, pct_load,
                    color=["#666666", "#1f77b4", "#2ca02c"])
    ax2.set_ylabel("% of 5 MW data-center load")
    ax2.set_title("Recovery as fraction of facility load")
    for bar, v in zip(bars2, pct_load):
        ax2.text(bar.get_x() + bar.get_width() / 2, v + 1.5,
                 f"{v:.2f}%", ha="center", va="bottom", fontsize=10)

    fig.suptitle("Realistic device captures ~0.5% of the radiative ceiling.\n"
                 "Closing that gap is the device-engineering challenge.")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("Generating TR diode analysis plots...")
    plot_bandgap_sky_heatmap()
    plot_monte_carlo_yield()
    plot_ceiling_vs_realistic()
    print("Done.")


if __name__ == "__main__":
    main()

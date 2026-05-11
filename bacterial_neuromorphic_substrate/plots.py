"""
Analysis plots for the bacterial neuromorphic substrate subproject.

Generates:
  - substrate_comparison.png : per-token energy across all 4 substrates
  - neuron_scaling.png       : scale from current demos to AI-substrate size
  - global_demand.png        : 2030 global AI inference TWh by substrate

Run with:  python plots.py
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import estimate as E


SUBSTRATE_ORDER = [
    ("h100_silicon",                "#cc3333", "dense"),
    ("loihi2_silicon_neuromorphic", "#666666", "sparse_snn"),
    ("geobacter_demo",              "#cc9933", "sparse_snn"),
    ("geobacter_target",            "#33aa33", "sparse_snn"),
    ("biological_brain_floor",      "#1166aa", "sparse_snn"),
]


def plot_substrate_comparison(out="bacterial_neuromorphic_substrate/substrate_comparison.png"):
    """Per-token energy for each substrate, LLaMA-70B reference."""
    fig, ax = plt.subplots(figsize=(11, 6))

    labels = []
    energies = []
    colors = []
    for s, c, arch in SUBSTRATE_ORDER:
        E_J = E.energy_per_token(s, "llama70b", arch)
        labels.append(E.SUBSTRATE[s]["name"])
        energies.append(E_J)
        colors.append(c)

    bars = ax.bar(range(len(labels)), energies, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("energy per token (J, log scale)")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels([l[:35] for l in labels], rotation=15, fontsize=9)

    # Reference lines
    ax.axhline(1.0, color="black", linestyle=":", alpha=0.5)
    ax.text(len(labels) - 0.5, 1.2, "1 J", fontsize=9, color="black",
            ha="right")
    ax.axhline(0.001, color="black", linestyle=":", alpha=0.5)
    ax.text(len(labels) - 0.5, 0.0012, "1 mJ", fontsize=9, color="black",
            ha="right")
    ax.axhline(1e-6, color="black", linestyle=":", alpha=0.5)
    ax.text(len(labels) - 0.5, 1.2e-6, "1 µJ", fontsize=9, color="black",
            ha="right")

    for bar, e in zip(bars, energies):
        if e > 1:
            txt = f"{e:.1f} J"
        elif e > 1e-3:
            txt = f"{e*1e3:.0f} mJ"
        elif e > 1e-6:
            txt = f"{e*1e6:.0f} µJ"
        else:
            txt = f"{e*1e9:.0f} nJ"
        ax.text(bar.get_x() + bar.get_width()/2, e * 1.5,
                txt, ha="center", fontsize=9)

    ax.set_title("Energy per token across compute substrates\n"
                 "(LLaMA-3 70B reference, 140 GFLOPs per token)")
    ax.grid(axis="y", which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_neuron_scaling(out="bacterial_neuromorphic_substrate/neuron_scaling.png"):
    """The scale challenge: from current demos to transformer-equivalent."""
    fig, ax = plt.subplots(figsize=(11, 6))

    milestones = [
        # (name,                            neurons,   year_achieved, color, status)
        ("Fu 2020 demo",                       5,      2020, "#cc9933", "demonstrated"),
        ("BrainScaleS-2",                    512,      2022, "#666666", "demonstrated"),
        ("Tianjic / mid-scale",         40_000,        2019, "#666666", "demonstrated"),
        ("Loihi 2 chip",             1_000_000,        2021, "#666666", "demonstrated"),
        ("SpiNNaker 2",            152_000_000,        2024, "#666666", "demonstrated"),
        ("transformer block (1 head)", 100_000_000,    None, "#cc9933", "near-term target"),
        ("full LLaMA-70B",          1_000_000_000_000, None, "#33aa33", "long-term target"),
        ("Biological brain",        86_000_000_000,    None, "#1166aa", "reference"),
    ]

    for name, n, yr, color, status in milestones:
        # Use 0-9 for x position; pack manually
        pass

    names = [m[0] for m in milestones]
    neurons = [m[1] for m in milestones]
    colors = [m[3] for m in milestones]
    statuses = [m[4] for m in milestones]

    x = np.arange(len(names))
    bars = ax.bar(x, neurons, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("neuron count (log)")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=20, fontsize=9, ha="right")

    # Annotate status
    for bar, n, s in zip(bars, neurons, statuses):
        ax.text(bar.get_x() + bar.get_width()/2, n * 1.5,
                f"{n:,}\n({s})",
                ha="center", fontsize=8)

    ax.set_title("Path from current Geobacter demos to AI-scale\n"
                 "Demonstrated → near-term target → long-term target")
    ax.grid(axis="y", which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def plot_global_demand(out="bacterial_neuromorphic_substrate/global_demand.png"):
    """2030 global inference electricity demand by substrate."""
    fig, ax = plt.subplots(figsize=(11, 6))

    substrates = list(E.SUBSTRATE.keys())
    labels = [E.SUBSTRATE[s]["name"] for s in substrates]
    arches = ["dense" if s == "h100_silicon" else "sparse_snn"
              for s in substrates]
    values = [E.annual_TWh(s, "gpt4_class", a,
                            daily_inferences_billion=1000,
                            tokens_per_inference=500)
              for s, a in zip(substrates, arches)]

    colors = ["#cc3333", "#666666", "#cc9933", "#33aa33", "#1166aa"]
    bars = ax.bar(range(len(values)), values, color=colors)
    ax.set_yscale("log")
    ax.set_ylabel("annual TWh (log)")
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels([f"{l[:25]}\n({a})" for l, a in zip(labels, arches)],
                       rotation=15, fontsize=9)

    ax.axhline(950, color="red", linestyle="--", linewidth=2,
               label="IEA 2030 forecast (950 TWh, all data centers)")
    ax.text(-0.4, 1100, "IEA 950 TWh", color="red", fontsize=9)

    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, v * 1.4,
                f"{v:.1f} TWh", ha="center", fontsize=9)

    ax.set_title("Projected 2030 global AI inference electricity demand\n"
                 "(1 trillion daily inferences, GPT-4-class, 500 tokens each)")
    ax.legend()
    ax.grid(axis="y", which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"  -> {out}")


def main():
    print("Generating bacterial-neuromorphic analysis plots...")
    plot_substrate_comparison()
    plot_neuron_scaling()
    plot_global_demand()
    print("Done.")


if __name__ == "__main__":
    main()

"""
Generate physical-design diagrams for the SED Casimir-cavity ZPE
experiment: apparatus layout and a close-up of one Casimir cavity layer.

Run with:  python schematic.py
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_apparatus_layout(out="sed_casimir_zpe/apparatus_layout.png"):
    """Top-down (bench) view of the full apparatus."""
    fig, ax = plt.subplots(figsize=(13, 7))

    boxes = [
        # (x, y, w, h, color, label)
        (0.5, 4.0, 1.8, 1.6, "#ffd699",
         "Cs vapor source\nSAES dispenser\nT ~ 380 K"),
        (3.0, 4.0, 1.8, 1.6, "#cce6ff",
         "Beam-defining\naperture\n0.5 mm pinhole"),
        (5.5, 4.0, 1.8, 1.6, "#ffb3b3",
         "PEEK diverter\nf_lock = 1 Hz\nmodulates flow"),
        (8.0, 5.5, 1.8, 1.4, "#888888",
         "CASIMIR STACK\n50 layers × 30 nm gap\n10 cm² area"),
        (8.0, 3.0, 1.8, 1.4, "#cccccc",
         "REFERENCE cell\nno plates\n(d → ∞)"),
        (10.7, 4.0, 1.7, 1.6, "#0066cc",
         "SQUID-TES\nT_op = 50 mK\nNEP 1e-19 W/√Hz"),
    ]
    for x, y, w, h, color, label in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h,
                                       boxstyle="round,pad=0.05",
                                       facecolor=color, edgecolor="black",
                                       linewidth=1.2)
        ax.add_patch(rect)
        text_color = "white" if color == "#0066cc" else "black"
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=9, color=text_color)

    # Cryostat surrounding the bolometer
    cryostat = patches.FancyBboxPatch((10.4, 3.6), 2.3, 2.4,
                                       boxstyle="round,pad=0.15",
                                       fill=False, edgecolor="#003366",
                                       linewidth=2, linestyle="--")
    ax.add_patch(cryostat)
    ax.text(11.55, 3.4, "dilution fridge", ha="center", fontsize=9,
            color="#003366", style="italic")

    # UHV chamber wrapping everything except cryostat
    chamber = patches.FancyBboxPatch((0.2, 3.5), 11.0, 3.0,
                                      boxstyle="round,pad=0.2",
                                      fill=False, edgecolor="#444444",
                                      linewidth=1.5, linestyle=":")
    ax.add_patch(chamber)
    ax.text(5.5, 3.3, "UHV chamber  ─  5×10⁻⁹ Torr base pressure",
            ha="center", fontsize=10, color="#444444", style="italic")

    # Flow arrows
    arrow = dict(arrowstyle="->", color="#cc3300", lw=1.8)
    ax.annotate("", xy=(3.0, 4.8), xytext=(2.3, 4.8), arrowprops=arrow)
    ax.annotate("", xy=(5.5, 4.8), xytext=(4.8, 4.8), arrowprops=arrow)
    ax.annotate("", xy=(8.0, 6.0), xytext=(7.3, 5.2), arrowprops=arrow)
    ax.annotate("", xy=(8.0, 3.6), xytext=(7.3, 4.4), arrowprops=arrow)
    ax.annotate("", xy=(10.7, 4.8), xytext=(9.8, 5.8), arrowprops=arrow)
    ax.annotate("", xy=(10.7, 4.8), xytext=(9.8, 3.8), arrowprops=arrow)

    # Lock-in below
    li = patches.FancyBboxPatch((4.5, 1.3), 4.0, 1.0,
                                 boxstyle="round,pad=0.05",
                                 facecolor="#e6ffe6", edgecolor="black")
    ax.add_patch(li)
    ax.text(6.5, 1.8, "Lock-in amplifier  (SR830 / MFLI)\nreference = beam chopper",
            ha="center", va="center", fontsize=9)

    # SQUID -> lock-in
    ax.annotate("", xy=(7.0, 2.3), xytext=(11.0, 3.9),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
    ax.text(9.5, 3.2, "SQUID\nreadout", ha="center", fontsize=8,
            color="#444")

    ax.set_xlim(0, 13.5)
    ax.set_ylim(0.5, 7.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("SED Casimir-cavity ZPE experiment — apparatus layout\n"
                 "Tabletop bench, ~2 m² footprint",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def plot_cavity_layer(out="sed_casimir_zpe/cavity_layer_zoom.png"):
    """Cross-section of one Si-Si Casimir layer with SiO2 pillars."""
    fig, ax = plt.subplots(figsize=(11, 5.5))

    # Lower Si wafer
    lower = patches.Rectangle((0, 0), 30, 2.0, facecolor="#aaaaaa",
                               edgecolor="black", linewidth=1.2)
    ax.add_patch(lower)
    ax.text(15, 1, "lower Si wafer  (200 µm thick)", ha="center",
            va="center", fontsize=10, fontweight="bold")

    # Upper Si wafer
    upper = patches.Rectangle((0, 2.7), 30, 2.0, facecolor="#aaaaaa",
                               edgecolor="black", linewidth=1.2)
    ax.add_patch(upper)
    ax.text(15, 3.7, "upper Si wafer  (200 µm thick)", ha="center",
            va="center", fontsize=10, fontweight="bold")

    # SiO2 pillars (5 of them across the 30 mm span)
    for x in [3, 9, 15, 21, 27]:
        pillar = patches.Rectangle((x - 0.5, 2.0), 1.0, 0.7,
                                    facecolor="#3366cc", edgecolor="black",
                                    linewidth=0.5)
        ax.add_patch(pillar)
    ax.text(15, 2.35, "SiO₂ pillars  100 µm × 100 µm × 30 nm tall  (pitch 5 mm)",
            ha="center", va="center", fontsize=9, color="white",
            fontweight="bold")

    # Gas-flow arrows through the gap
    for x_start in [0.2, 6.0, 12.0, 18.0, 24.0]:
        ax.annotate("", xy=(x_start + 2.5, 2.35),
                    xytext=(x_start, 2.35),
                    arrowprops=dict(arrowstyle="->", color="#ff6600", lw=1.8))
    ax.text(15, 5.0, "Cs vapor flow through cavity gap →",
            ha="center", fontsize=10, color="#cc3300", fontweight="bold")

    # Dimension labels
    ax.annotate("", xy=(31.2, 2.0), xytext=(31.2, 2.7),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.0))
    ax.text(31.5, 2.35, "30 nm\n(cavity gap d)", ha="left",
            va="center", fontsize=9, fontweight="bold")

    ax.annotate("", xy=(-0.5, 0), xytext=(-0.5, 4.7),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.0))
    ax.text(-1, 2.35, "~400.03 µm\ntotal stack height\nper layer",
            ha="right", va="center", fontsize=9)

    ax.annotate("", xy=(0, -0.5), xytext=(30, -0.5),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax.text(15, -0.85, "30 mm cavity active area",
            ha="center", fontsize=10, fontweight="bold")

    # Side note
    ax.text(15, 5.65,
            "ZPF modes with λ > 2d ≈ 60 nm are excluded from this gap.\n"
            "Atom transits at thermal v̄ ≈ 252 m/s for ~120 µs through 30 mm.",
            ha="center", fontsize=9, color="#333333", style="italic")

    ax.set_xlim(-3, 35)
    ax.set_ylim(-1.5, 6.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("SED Casimir-cavity layer — close-up (cross-section)\n"
                 "50 such layers stacked vertically in the full apparatus",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def main():
    print("Generating SED Casimir physical-design diagrams...")
    plot_apparatus_layout()
    plot_cavity_layer()
    print("Done.")


if __name__ == "__main__":
    main()

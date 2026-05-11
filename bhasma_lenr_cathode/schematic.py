"""
Generate physical-design diagrams for the bhasma-LENR experiment:
bhasma preparation reactor + UBC-style fusion measurement apparatus.

Run with:  python schematic.py
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_bhasma_reactor(out="bhasma_lenr_cathode/bhasma_reactor.png"):
    """Stage 1: bhasma preparation flow."""
    fig, ax = plt.subplots(figsize=(13, 6))

    steps = [
        # (x, y, color, label)
        (0.5,  "#cce6ff",   "1. SHODHANA\nPd + aqua regia →\nPd(OH)₂ → calcine →\nreduce under H₂"),
        (3.0,  "#ffe0b3",   "2. BHAVANA\ngrind Pd powder\nwith aloe juice\n(6 h, agate mortar)"),
        (5.5,  "#ffcccc",   "3. PRESS\n200 MPa hydraulic\n→ Pd cake 30 × 30 × 5"),
        (8.0,  "#cc6666",   "4. PUTA × 60\n800 °C × 4 h × 60 cycles\nsealed alumina crucible\n(Ar purge between)"),
        (10.5, "#aa3333",   "5. (opt) PARADA-MARANA\nHg amalgam, sublime,\nverify residual <100 ppm"),
    ]

    for i, (x, color, label) in enumerate(steps):
        rect = patches.FancyBboxPatch((x, 2.0), 2.2, 2.5,
                                       boxstyle="round,pad=0.08",
                                       facecolor=color, edgecolor="black",
                                       linewidth=1.2)
        ax.add_patch(rect)
        text_color = "white" if i >= 3 else "black"
        ax.text(x + 1.1, 3.25, label, ha="center", va="center",
                fontsize=9, color=text_color)

    # Arrows between
    for i in range(len(steps) - 1):
        x = steps[i][0] + 2.2
        ax.annotate("", xy=(steps[i + 1][0], 3.25), xytext=(x, 3.25),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # XRD checkpoints
    for i in [3]:
        x_cp = steps[i][0] + 1.1
        ax.annotate("", xy=(x_cp, 1.5), xytext=(x_cp, 2.0),
                    arrowprops=dict(arrowstyle="->", color="gray", lw=1))
    ax.text(steps[3][0] + 1.1, 1.2,
            "XRD / TEM / BET every 10 puta cycles\n→ track crystallite size 5 µm → ~30 nm",
            ha="center", fontsize=9, color="#444", style="italic")

    # Output
    out_box = patches.FancyBboxPatch((4.0, 5.0), 5.0, 1.0,
                                      boxstyle="round,pad=0.1",
                                      facecolor="#2ca02c", edgecolor="black")
    ax.add_patch(out_box)
    ax.text(6.5, 5.5,
            "OUTPUT: Pd-bhasma pellet, 10 mm × 1 mm, ~30 nm crystallites",
            ha="center", va="center", color="white", fontweight="bold",
            fontsize=10)
    ax.annotate("", xy=(6.5, 5.0), xytext=(9.0, 4.5),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax.set_xlim(0, 13.5)
    ax.set_ylim(0.5, 6.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Stage 1: rasashastra bhasma preparation flow\n"
                 "~270 hours of furnace time + handling = ~12 weeks elapsed",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def plot_fusion_apparatus(out="bhasma_lenr_cathode/fusion_apparatus.png"):
    """Stage 2: UBC-style fusion measurement apparatus."""
    fig, ax = plt.subplots(figsize=(13, 8))

    # UHV chamber outline
    chamber = patches.FancyBboxPatch((1.5, 3.0), 8.0, 4.0,
                                      boxstyle="round,pad=0.15",
                                      facecolor="#e6e6e6", edgecolor="black",
                                      linewidth=1.5)
    ax.add_patch(chamber)
    ax.text(5.5, 6.7, "UHV chamber  (10⁻⁷ Torr base, 10⁻⁴ Torr D₂ operating)",
            ha="center", fontsize=10, style="italic")

    # RF plasma source
    plasma = patches.FancyBboxPatch((2.0, 4.5), 1.8, 1.5,
                                     boxstyle="round,pad=0.05",
                                     facecolor="#ff9933", edgecolor="black",
                                     linewidth=1)
    ax.add_patch(plasma)
    ax.text(2.9, 5.25, "RF plasma\n13.56 MHz\nD₂ → D⁺",
            ha="center", va="center", fontsize=9, fontweight="bold")

    # Einzel lens
    lens1 = patches.Rectangle((4.0, 4.85), 0.2, 0.8, facecolor="#666666",
                               edgecolor="black")
    lens2 = patches.Rectangle((4.5, 4.85), 0.2, 0.8, facecolor="#666666",
                               edgecolor="black")
    lens3 = patches.Rectangle((5.0, 4.85), 0.2, 0.8, facecolor="#666666",
                               edgecolor="black")
    ax.add_patch(lens1)
    ax.add_patch(lens2)
    ax.add_patch(lens3)
    ax.text(4.6, 4.5, "Einzel lens\n1-20 kV", ha="center", fontsize=8)

    # D+ beam arrow
    ax.annotate("", xy=(7.5, 5.25), xytext=(5.2, 5.25),
                arrowprops=dict(arrowstyle="->", color="#cc6600", lw=2.5))
    ax.text(6.35, 5.55, "D⁺ beam, 1 µA at 10 keV",
            ha="center", fontsize=9, color="#cc3300", fontweight="bold")

    # Cathode pellet
    cathode = patches.FancyBboxPatch((7.5, 4.6), 0.6, 1.3,
                                      boxstyle="round,pad=0.03",
                                      facecolor="#666633", edgecolor="black",
                                      linewidth=2)
    ax.add_patch(cathode)
    ax.text(7.8, 5.25, "Pd-bhasma\ncathode", ha="center", va="center",
            fontsize=8, color="white", fontweight="bold", rotation=90)

    # Electrochem cell on back face
    cell = patches.FancyBboxPatch((8.2, 3.5), 1.0, 3.0,
                                   boxstyle="round,pad=0.05",
                                   facecolor="#3399ff", edgecolor="black")
    ax.add_patch(cell)
    ax.text(8.7, 5.0, "D₂O +\nLiOD\nelectrochem\ncell\n(Pt mesh\ncounter)",
            ha="center", va="center", fontsize=8, color="white")

    # Neutron detector array below
    det_y = 1.2
    for i, x_d in enumerate([2.0, 3.8, 5.6, 7.4]):
        det = patches.Rectangle((x_d, det_y), 1.4, 1.0,
                                 facecolor="#9966cc", edgecolor="black")
        ax.add_patch(det)
        ax.text(x_d + 0.7, det_y + 0.5, f"³He tube\n{i+1}",
                ha="center", va="center", fontsize=8, color="white")

    # Polyethylene moderator
    mod_outline = patches.Rectangle((1.5, 1.0), 7.4, 1.5, fill=False,
                                     edgecolor="#9933ff", linewidth=2,
                                     linestyle="--")
    ax.add_patch(mod_outline)
    ax.text(5.2, 0.7, "HDPE moderator (5 cm) + borated-poly/Pb outer shield",
            ha="center", fontsize=9, color="#6600cc")

    # Neutron emission arrows
    for x_arrow in [3.5, 5.5, 7.5]:
        ax.annotate("", xy=(x_arrow, 2.7), xytext=(7.8, 5.0),
                    arrowprops=dict(arrowstyle="->", color="#33cc66",
                                    lw=1.0, alpha=0.7))
    ax.text(5.0, 3.3, "2.45 MeV neutrons\nfrom D-D fusion",
            ha="center", fontsize=9, color="#229944", style="italic")

    # DAQ
    daq = patches.FancyBboxPatch((11.0, 1.5), 2.0, 1.5,
                                  boxstyle="round,pad=0.08",
                                  facecolor="#666666", edgecolor="black")
    ax.add_patch(daq)
    ax.text(12.0, 2.25, "preamp ×4\nshaping amp\nMCA + ROOT/Python",
            ha="center", va="center", fontsize=9, color="white")
    # Arrow from detector to DAQ
    ax.annotate("", xy=(11.0, 2.25), xytext=(8.8, 1.7),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2))

    # Compare-against panel
    cmp = patches.FancyBboxPatch((10.5, 4.5), 3.0, 2.3,
                                  boxstyle="round,pad=0.1",
                                  facecolor="#fff7e6", edgecolor="black")
    ax.add_patch(cmp)
    ax.text(12.0, 6.5, "compare 3 cathodes:",
            ha="center", fontweight="bold", fontsize=10)
    ax.text(12.0, 6.0, "A:  Pd-bhasma\n     (rasashastra, N_puta=60)",
            ha="center", fontsize=9, color="#2ca02c")
    ax.text(12.0, 5.4, "B:  commercial Pd-black\n     at matched BET",
            ha="center", fontsize=9, color="#cc6600")
    ax.text(12.0, 4.8, "C:  commercial Pd-foil\n     (UBC baseline)",
            ha="center", fontsize=9, color="#3366cc")

    ax.set_xlim(0.5, 14)
    ax.set_ylim(0, 8)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Stage 2: UBC-style fusion-rate measurement\n"
                 "follows Schenkel et al. Nature 644:640 (2025) with bhasma "
                 "cathode substitution",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def main():
    print("Generating bhasma physical-design diagrams...")
    plot_bhasma_reactor()
    plot_fusion_apparatus()
    print("Done.")


if __name__ == "__main__":
    main()

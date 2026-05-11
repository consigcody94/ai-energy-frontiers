"""
Generate physical-design schematics for the bacterial neuromorphic chip:
  - chip cross-section (Geobacter layer on CMOS readout)
  - bioreactor-to-chip workflow
  - cross-bar architecture detail

Run with:  python schematic.py
"""
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def plot_chip_cross_section(out="bacterial_neuromorphic_substrate/chip_cross_section.png"):
    """Two-layer hybrid chip: Geobacter top, CMOS bottom."""
    fig, ax = plt.subplots(figsize=(13, 6.5))

    # Encapsulation glass cap
    cap = patches.Rectangle((0, 6.5), 14, 0.4,
                             facecolor="#cce6ff", edgecolor="black",
                             linewidth=1, alpha=0.6)
    ax.add_patch(cap)
    ax.text(7, 6.7, "glass window encapsulation",
            ha="center", va="center", fontsize=10, style="italic")

    # Al2O3 passivation
    pass_layer = patches.Rectangle((1, 6.0), 12, 0.3,
                                    facecolor="#aaaaff", edgecolor="black",
                                    linewidth=0.5)
    ax.add_patch(pass_layer)
    ax.text(7, 6.15, "Al₂O₃ ALD passivation (20 nm)",
            ha="center", va="center", fontsize=9)

    # Ag top electrode
    ag = patches.Rectangle((1, 5.4), 12, 0.5,
                            facecolor="#cccccc", edgecolor="black",
                            linewidth=0.8)
    ax.add_patch(ag)
    ax.text(7, 5.65, "Ag top electrode (100 nm, shadow-mask patterned)",
            ha="center", va="center", fontsize=9, fontweight="bold")

    # Geobacter nanowire layer (active!)
    pili_top = 5.4
    pili_bottom = 4.0
    # Visualize as scattered short squiggles
    import numpy as np
    rng = np.random.default_rng(2026)
    for _ in range(180):
        x_start = rng.uniform(1.1, 12.9)
        y_start = rng.uniform(pili_bottom + 0.1, pili_top - 0.1)
        angle = rng.uniform(0, 2 * np.pi)
        length = rng.uniform(0.4, 1.2)
        x_end = x_start + length * np.cos(angle)
        y_end = y_start + 0.3 * np.sin(angle)
        y_end = np.clip(y_end, pili_bottom + 0.05, pili_top - 0.05)
        ax.plot([x_start, x_end], [y_start, y_end],
                color="#7a4f10", linewidth=0.6, alpha=0.7)

    pili_box = patches.Rectangle((1, pili_bottom), 12,
                                  pili_top - pili_bottom,
                                  fill=False, edgecolor="black",
                                  linewidth=1.2, linestyle="--")
    ax.add_patch(pili_box)
    ax.text(7, 4.7,
            "GEOBACTER PROTEIN NANOWIRE LAYER (active memristor element)\n"
            "70-130 mV switching, 0.3-100 pJ/event",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color="#7a4f10")

    # Wire-bond pads + Au bonds to CMOS below
    for x in [2, 5, 9, 12]:
        ax.plot([x, x], [pili_bottom, 3.0], color="goldenrod",
                linewidth=2)
        # bond pads
        ax.add_patch(patches.Circle((x, pili_bottom), 0.12,
                                     facecolor="goldenrod",
                                     edgecolor="black"))
        ax.add_patch(patches.Circle((x, 3.0), 0.12,
                                     facecolor="goldenrod",
                                     edgecolor="black"))
    ax.text(7, 3.5, "Au wire-bond pads (0.5 mm pitch)",
            ha="center", va="center", fontsize=9,
            color="#bb8800", style="italic")

    # CMOS chip below
    cmos = patches.FancyBboxPatch((1, 1.3), 12, 1.5,
                                   boxstyle="round,pad=0.05",
                                   facecolor="#bb6633", edgecolor="black")
    ax.add_patch(cmos)
    ax.text(7, 2.05,
            "CMOS READOUT CHIP (TSMC 180 nm or equivalent)\n"
            "row/col decoders | sense amps × 1024 | state machine | PCIe x4",
            ha="center", va="center", fontsize=10, fontweight="bold",
            color="white")

    # Substrate
    sub = patches.Rectangle((0, 0.4), 14, 0.7,
                             facecolor="#444444", edgecolor="black")
    ax.add_patch(sub)
    ax.text(7, 0.75, "Si substrate", ha="center", va="center",
            color="white", fontsize=9)

    # Dimension labels
    ax.annotate("", xy=(0, -0.05), xytext=(14, -0.05),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax.text(7, -0.3, "25 × 25 mm package (1024×1024 = 1M devices)",
            ha="center", fontsize=10, fontweight="bold")

    ax.set_xlim(-0.5, 16)
    ax.set_ylim(-0.6, 7.3)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Hybrid neuromorphic chip cross-section\n"
                 "Geobacter nanowire memristor array on CMOS readout",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def plot_workflow(out="bacterial_neuromorphic_substrate/workflow.png"):
    """Bioreactor to chip workflow."""
    fig, ax = plt.subplots(figsize=(13, 5.5))

    steps = [
        (0.3,  "#dcedc8",  "1. CULTURE\nG. sulfurreducens\n30°C anaerobic,\nacetate + fumarate"),
        (2.7,  "#dcedc8",  "2. HARVEST\n4,000 g × 15 min\nresuspend in buffer"),
        (5.1,  "#fff9c4",  "3. EXTRACT\nblender shear\n+ differential\ncentrifugation\n→ free pili"),
        (7.5,  "#ffe0b2",  "4. CONCENTRATE\nAmicon 10 kDa\n0.1-1 mg/mL\nin device buffer"),
        (9.9,  "#fce4ec",  "5. DEPOSIT\ndrop-cast onto\npatterned CMOS\ntop metal"),
        (12.3, "#cce6ff",  "6. ELECTRODE\n100 nm Ag\nthermal evap\n+ ALD passivation"),
    ]

    for x, color, label in steps:
        rect = patches.FancyBboxPatch((x, 2.0), 2.0, 2.4,
                                       boxstyle="round,pad=0.1",
                                       facecolor=color, edgecolor="black",
                                       linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + 1.0, 3.2, label, ha="center", va="center",
                fontsize=9)

    # Arrows between
    for i in range(len(steps) - 1):
        x = steps[i][0] + 2.0
        ax.annotate("", xy=(steps[i + 1][0], 3.2), xytext=(x, 3.2),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # Time annotations under arrows
    for i, t in enumerate(["4-7 days", "1 hr", "4 hr", "2 hr", "30 min", "2 hr"]):
        x = steps[i][0] + 1.0
        ax.text(x, 1.6, t, ha="center", fontsize=8, color="#666",
                style="italic")

    # Output box
    out_box = patches.FancyBboxPatch((4.5, 5.0), 5.0, 1.0,
                                      boxstyle="round,pad=0.1",
                                      facecolor="#2ca02c", edgecolor="black",
                                      linewidth=1.2)
    ax.add_patch(out_box)
    ax.text(7, 5.5, "OUTPUT: chip with 1024×1024 Geobacter memristor array",
            ha="center", va="center", color="white", fontweight="bold",
            fontsize=10)
    ax.annotate("", xy=(7, 5.0), xytext=(13.3, 4.4),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax.set_xlim(0, 14.5)
    ax.set_ylim(1, 6.5)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Bioreactor-to-chip workflow\n"
                 "End-to-end: from bacterial culture to operational hybrid chip",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def plot_crossbar_detail(out="bacterial_neuromorphic_substrate/crossbar_detail.png"):
    """Zoom into the cross-bar memristor architecture."""
    fig, ax = plt.subplots(figsize=(11, 7))

    # Row lines (running horizontal)
    rows = 6
    cols = 6
    for r in range(rows):
        y = 5.5 - r * 0.8
        ax.plot([1, 8.5], [y, y], color="goldenrod", linewidth=2.5)
        ax.text(0.7, y, f"R{r}", fontsize=9, ha="right", va="center")

    # Column lines (running vertical, on top)
    for c in range(cols):
        x = 1.5 + c * 1.1
        ax.plot([x, x], [1.0, 6.0], color="#666666", linewidth=2.5,
                alpha=0.7)
        ax.text(x, 0.6, f"C{c}", fontsize=9, ha="center", va="top")

    # Memristors at intersections
    for r in range(rows):
        for c in range(cols):
            y = 5.5 - r * 0.8
            x = 1.5 + c * 1.1
            ax.add_patch(patches.Rectangle((x - 0.18, y - 0.18), 0.36, 0.36,
                                            facecolor="#cc6633",
                                            edgecolor="black",
                                            linewidth=0.6))

    # Selected cell highlight
    ax.add_patch(patches.Rectangle((1.5 + 2*1.1 - 0.3, 5.5 - 1*0.8 - 0.3),
                                    0.6, 0.6, fill=False,
                                    edgecolor="red", linewidth=2.5,
                                    linestyle="--"))
    ax.annotate("selected device\n(R1 high, C2 high)",
                xy=(1.5 + 2*1.1 + 0.3, 5.5 - 1*0.8),
                xytext=(9.5, 4.5), fontsize=10, color="red",
                arrowprops=dict(arrowstyle="->", color="red", lw=1.2))

    # Right: sense amplifier
    sa = patches.FancyBboxPatch((10, 2.8), 2.5, 1.4,
                                 boxstyle="round,pad=0.05",
                                 facecolor="#ccffcc", edgecolor="black")
    ax.add_patch(sa)
    ax.text(11.25, 3.5, "sense amp\n+ ADC\n(per column)",
            ha="center", va="center", fontsize=9)
    ax.annotate("", xy=(10, 3.5), xytext=(1.5 + 2*1.1, 0.6),
                arrowprops=dict(arrowstyle="->", color="#666666",
                                lw=1, linestyle=":"))

    # Annotation
    ax.text(4.5, 0.0,
            "Geobacter nanowires cross-bar: row lines (Au) and column "
            "lines (Pt)\nwith a protein-nanowire / Ag-filament memristor at "
            "each intersection\n(1024 × 1024 ≈ 1M devices on a 25 mm × 25 mm die)",
            ha="center", fontsize=9, color="#444",
            style="italic")

    ax.set_xlim(0, 14)
    ax.set_ylim(-0.5, 7)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title("Cross-bar architecture detail\n"
                 "6×6 zoom of a 1024×1024 memristor array",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def main():
    print("Generating bacterial neuromorphic chip schematics...")
    plot_chip_cross_section()
    plot_workflow()
    plot_crossbar_detail()
    print("Done.")


if __name__ == "__main__":
    main()

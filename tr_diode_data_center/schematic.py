"""
Generate a labeled cross-section schematic of the TR diode panel
physical design, plus a roof-scale array layout.

Run with:  python schematic.py
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms


def plot_panel_cross_section(out="tr_diode_data_center/panel_cross_section.png"):
    """Cross-section through one 1 m × 1 m TR diode panel."""
    fig, ax = plt.subplots(figsize=(13, 7))

    # Sky region (top)
    sky = patches.Rectangle((0, 8), 14, 2, facecolor="#0a1a3a",
                            edgecolor="black", linewidth=0)
    ax.add_patch(sky)
    ax.text(7, 9, "NIGHT SKY  (~248–280 K effective through 8–13 µm window)",
            color="white", ha="center", va="center", fontsize=11,
            fontweight="bold")

    # Up-arrows showing radiation
    for x in [2, 5, 9, 12]:
        ax.annotate("", xy=(x, 8), xytext=(x, 7.5),
                    arrowprops=dict(arrowstyle="->", color="#ff9933",
                                    lw=2))
    ax.text(7, 7.5, "thermal radiation upward",
            ha="center", fontsize=9, color="#ff9933", style="italic")

    # Panel stack from top to bottom
    layers = [
        ("ZnSe-AR or HDPE IR window  (2 mm)",       6.7, 0.4, "#cce6ff"),
        ("N₂-purged air gap  (3 mm)",                6.3, 0.3, "#eaf3ff"),
        ("MCT 100×100 photodiode array  (5 mm)\nHg₀.₈Cd₀.₂Te, Eg = 0.10 eV",
                                                     5.5, 0.7, "#888888"),
        ("Cu cold-plate, polished  (6 mm)",          4.9, 0.55, "#b87333"),
        ("Silica aerogel  (15 mm) — k = 0.018 W/(m·K)\nblocks hot-side heat leak",
                                                     3.7, 1.1, "#e8e8e8"),
        ("Cu hot-plate, T_h ≈ 325 K  (6 mm)",        3.1, 0.55, "#b87333"),
        ("Cu-water heat pipes  ×4  (8 mm OD)",       2.4, 0.55, "#cd853f"),
        ("Al backplane  (3 mm) + frame",             1.9, 0.45, "#bbbbbb"),
    ]

    for label, y, h, color in layers:
        rect = patches.Rectangle((1, y), 12, h, facecolor=color,
                                  edgecolor="black", linewidth=0.6)
        ax.add_patch(rect)
        ax.text(7, y + h / 2, label, ha="center", va="center",
                fontsize=9.5)

    # Frame on sides
    ax.add_patch(patches.Rectangle((0.4, 1.4), 0.6, 6.0,
                                    facecolor="#666666", edgecolor="black",
                                    linewidth=0.6))
    ax.add_patch(patches.Rectangle((13.0, 1.4), 0.6, 6.0,
                                    facecolor="#666666", edgecolor="black",
                                    linewidth=0.6))
    ax.text(0.7, 4.5, "Al\nframe", ha="center", va="center", fontsize=8,
            color="white", rotation=90)
    ax.text(13.3, 4.5, "Al\nframe", ha="center", va="center", fontsize=8,
            color="white", rotation=90)

    # Hot-aisle duct at bottom
    duct = patches.FancyBboxPatch((1, 0.3), 12, 0.8,
                                   boxstyle="round,pad=0.05",
                                   facecolor="#cc3333", edgecolor="black",
                                   linewidth=1)
    ax.add_patch(duct)
    ax.text(7, 0.7, "hot-aisle exhaust duct  (52 °C airflow)",
            ha="center", va="center", color="white",
            fontweight="bold", fontsize=10)

    # Heat-flow arrows from duct up through pipes
    for x in [3, 7, 11]:
        ax.annotate("", xy=(x, 2.4), xytext=(x, 1.2),
                    arrowprops=dict(arrowstyle="->", color="#cc3333",
                                    lw=2.0))

    # Cooler-flow arrows from cold plate (notional, just for arrows)
    for x in [3, 7, 11]:
        ax.annotate("", xy=(x, 5.45), xytext=(x, 6.3),
                    arrowprops=dict(arrowstyle="->", color="#3366cc",
                                    lw=1.5))
    ax.text(13.8, 5.7, "cold side\nradiates →", ha="left",
            color="#3366cc", fontsize=9, style="italic")

    # Outline frame for visual cleanliness
    ax.set_xlim(-0.5, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Dimensions
    ax.annotate("", xy=(0.4, -0.05), xytext=(13.6, -0.05),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax.text(7, -0.25, "1000 mm", ha="center", fontsize=10,
            fontweight="bold")

    ax.set_title("TR diode panel — cross-section (not to scale)\n"
                 "1 m × 1 m × 65 mm, ~22 kg, target 3–30 W realistic output",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def plot_roof_layout(out="tr_diode_data_center/roof_array_layout.png"):
    """Top-down view of hyperscale roof array."""
    fig, ax = plt.subplots(figsize=(11, 8))

    # Roof outline 100 m × 100 m
    roof = patches.Rectangle((0, 0), 100, 100, facecolor="#e0e0e0",
                              edgecolor="black", linewidth=1.5)
    ax.add_patch(roof)

    # Panels (drawn at 5x scale for visibility, 4 m apparent = 1 m actual)
    # We don't render all 80,000; just a grid pattern to show layout
    panel_grid_step = 4   # apparent — represents 1 m + 50 mm gap
    walkway_step = 40     # walkway every 10 panels apparent
    for x in range(2, 99, panel_grid_step):
        for y in range(2, 99, panel_grid_step):
            # skip walkway rows
            if (y - 2) % walkway_step == 0 and y > 2:
                continue
            p = patches.Rectangle((x, y), 3.5, 3.5,
                                   facecolor="#1f4880", edgecolor="#000033",
                                   linewidth=0.2, alpha=0.85)
            ax.add_patch(p)

    # Walkways
    for y in range(40, 100, 40):
        ax.add_patch(patches.Rectangle((0, y - 1), 100, 2,
                                        facecolor="white", edgecolor="black",
                                        linewidth=0.3, alpha=0.7))

    # Inverter cluster
    for ix, iy in [(10, 95), (50, 95), (90, 95)]:
        ax.add_patch(patches.Rectangle((ix - 3, iy - 1), 6, 3,
                                        facecolor="#cc6600",
                                        edgecolor="black"))
    ax.text(50, 99, "microinverter/string-aggregator boards",
            ha="center", fontsize=10, color="#cc3300", fontweight="bold")

    # Edge labels
    ax.annotate("", xy=(0, -3), xytext=(100, -3),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax.text(50, -6, "316 m (100,000 m² roof)",
            ha="center", fontsize=11, fontweight="bold")

    ax.text(105, 50, "wind direction",
            ha="left", va="center", color="gray", fontsize=9, rotation=270)

    # Roof-edge note
    ax.text(-3, 50, "panels lay flat (zenith-facing);\n"
                    "50 mm gaps for thermal expansion;\n"
                    "walkways every 10 panels (~2 m)",
            ha="right", va="center", fontsize=9, color="#222222")

    ax.set_xlim(-25, 120)
    ax.set_ylim(-10, 105)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title("Roof-scale TR diode array layout\n"
                 "~80,000 panels on a 10 ha hyperscale data-center roof",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def plot_wiring_diagram(out="tr_diode_data_center/wiring_diagram.png"):
    """Single-line electrical architecture."""
    fig, ax = plt.subplots(figsize=(12, 6))

    # Panel block
    p = patches.FancyBboxPatch((0.5, 3.5), 2.5, 1.5,
                                boxstyle="round,pad=0.08",
                                facecolor="#cce6ff", edgecolor="black")
    ax.add_patch(p)
    ax.text(1.75, 4.25, "1 panel\n10,000 MCT diodes\n100 strings × 100 parallel",
            ha="center", va="center", fontsize=9)

    # MPPT
    m = patches.FancyBboxPatch((4.0, 3.5), 2.0, 1.5,
                                boxstyle="round,pad=0.08",
                                facecolor="#ffe0b3", edgecolor="black")
    ax.add_patch(m)
    ax.text(5.0, 4.25, "MPPT\nTI BQ24650\n0–30 V boost", ha="center",
            va="center", fontsize=9)

    # String (×8 panels)
    s = patches.FancyBboxPatch((7.0, 3.5), 2.0, 1.5,
                                boxstyle="round,pad=0.08",
                                facecolor="#cce6cc", edgecolor="black")
    ax.add_patch(s)
    ax.text(8.0, 4.25, "string bus\n200–240 V DC\n8 panels series",
            ha="center", va="center", fontsize=9)

    # Microinverter
    i = patches.FancyBboxPatch((10.0, 3.5), 2.0, 1.5,
                                boxstyle="round,pad=0.08",
                                facecolor="#ffcccc", edgecolor="black")
    ax.add_patch(i)
    ax.text(11.0, 4.25, "microinverter\nEnphase IQ8M\n240 VAC out",
            ha="center", va="center", fontsize=9)

    # Grid-tie
    g = patches.FancyBboxPatch((10.0, 1.0), 2.0, 1.5,
                                boxstyle="round,pad=0.08",
                                facecolor="#aaaaaa", edgecolor="black")
    ax.add_patch(g)
    ax.text(11.0, 1.75, "facility transformer\n480 V three-phase\nbehind the meter",
            ha="center", va="center", fontsize=9)

    # Arrows
    arrow_style = dict(arrowstyle="->", color="black", lw=1.8)
    ax.annotate("", xy=(4.0, 4.25), xytext=(3.0, 4.25),
                arrowprops=arrow_style)
    ax.text(3.5, 4.5, "5 V / 50 A", ha="center", fontsize=8)

    ax.annotate("", xy=(7.0, 4.25), xytext=(6.0, 4.25),
                arrowprops=arrow_style)
    ax.text(6.5, 4.5, "30 V DC", ha="center", fontsize=8)

    ax.annotate("", xy=(10.0, 4.25), xytext=(9.0, 4.25),
                arrowprops=arrow_style)
    ax.text(9.5, 4.5, "200 V DC", ha="center", fontsize=8)

    ax.annotate("", xy=(11.0, 2.5), xytext=(11.0, 3.5),
                arrowprops=arrow_style)
    ax.text(11.5, 3.0, "240 VAC", ha="left", fontsize=8)

    # Scale note
    ax.text(6.0, 0.3, "Scale: 1 microinverter per 8-panel string. "
                       "Roof @ 80,000 panels → 10,000 strings → 10,000 microinverters → 5 grid-tie boards.",
            ha="center", fontsize=9, style="italic", color="#444")

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("TR diode array — electrical architecture",
                 fontsize=12, pad=12)

    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"  -> {out}")


def main():
    print("Generating TR diode physical-design diagrams...")
    plot_panel_cross_section()
    plot_roof_layout()
    plot_wiring_diagram()
    print("Done.")


if __name__ == "__main__":
    main()

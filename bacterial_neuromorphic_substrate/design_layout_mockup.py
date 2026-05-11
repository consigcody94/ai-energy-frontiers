"""
Low-fidelity matplotlib mockup of the proposed infographic design
layout. Produces design_layout_mockup.png — a structural reference
that pairs with design_brief.md.

Use this output to:
  - verify the 6-region layout fits the canvas
  - validate label readability at the chosen aspect ratio
  - hand off to a designer or AI image generator with concrete content

Run with:  python design_layout_mockup.py
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


def main(out="bacterial_neuromorphic_substrate/design_layout_mockup.png"):
    fig = plt.figure(figsize=(19.2, 10.8))
    fig.patch.set_facecolor("white")

    # Title bar across the top
    title_ax = fig.add_axes([0, 0.92, 1, 0.08])
    title_ax.set_facecolor("#0d5556")
    title_ax.set_xticks([])
    title_ax.set_yticks([])
    for s in title_ax.spines.values():
        s.set_visible(False)
    title_ax.text(0.5, 0.65,
                  "Bacterial Neuromorphic Chip — Physical Design",
                  ha="center", va="center", color="white",
                  fontsize=24, fontweight="bold")
    title_ax.text(0.5, 0.22,
                  "Geobacter Nanowire AI Compute Substrate",
                  ha="center", va="center", color="#cfeaea",
                  fontsize=14, style="italic")

    # ------- Region A: chip cross-section (large, left half) -------
    A = fig.add_axes([0.02, 0.45, 0.48, 0.45])
    A.set_xticks([]); A.set_yticks([])
    A.set_facecolor("#fafcff")
    A.set_title("A. Chip cross-section", fontsize=12, loc="left",
                fontweight="bold", pad=8)

    # Layered stack (bottom to top)
    layers = [
        ("Si substrate",                  "#444444", "white"),
        ("CMOS READOUT (TSMC 180 nm)\nrow/col decoders, sense amps, PCIe x4",
                                          "#bb6633", "white"),
        ("Au wire-bond pads (0.5 mm pitch)", "#d4af37", "black"),
        ("GEOBACTER NANOWIRE LAYER\n70-130 mV, 0.3-100 pJ/event\n(squiggle pattern = protein nanowires)",
                                          "#7a4f10", "white"),
        ("Ag top electrode (100 nm)",     "#cccccc", "black"),
        ("Al₂O₃ ALD passivation (20 nm)", "#aaaaff", "black"),
        ("glass window encapsulation",    "#cce6ff", "black"),
    ]
    n = len(layers)
    y0 = 0.05
    h = 0.85 / n
    for i, (label, fill, txt) in enumerate(layers):
        y = y0 + i * h
        A.add_patch(patches.Rectangle((0.05, y), 0.90, h * 0.92,
                                       facecolor=fill, edgecolor="black",
                                       linewidth=1.2,
                                       transform=A.transAxes))
        A.text(0.5, y + h * 0.46, label, transform=A.transAxes,
               ha="center", va="center", fontsize=8, color=txt)

    # Pili squiggles inside the Geobacter layer
    rng = np.random.default_rng(2026)
    geob_y = y0 + 3 * h + h * 0.1
    geob_h = h * 0.7
    for _ in range(80):
        x_s = rng.uniform(0.08, 0.92)
        y_s = rng.uniform(geob_y, geob_y + geob_h)
        ang = rng.uniform(0, 2*np.pi)
        L = rng.uniform(0.02, 0.05)
        A.plot([x_s, x_s + L*np.cos(ang)],
               [y_s, y_s + L*np.sin(ang)*0.3],
               color="#3a2400", linewidth=0.5, alpha=0.7,
               transform=A.transAxes)

    # Dimension labels
    A.annotate("", xy=(0.05, 0.02), xytext=(0.95, 0.02),
               xycoords=A.transAxes,
               arrowprops=dict(arrowstyle="<->", lw=1.0))
    A.text(0.5, -0.005, "25 × 25 mm  (1024 × 1024 = 1M devices)",
           transform=A.transAxes, ha="center", fontsize=9,
           fontweight="bold")

    # ------- Region B: workflow (upper right) -------
    B = fig.add_axes([0.51, 0.70, 0.47, 0.20])
    B.set_xticks([]); B.set_yticks([])
    B.set_facecolor("#fafcff")
    B.set_title("B. Bioreactor → chip workflow",
                fontsize=12, loc="left", fontweight="bold", pad=8)

    steps = [
        ("CULTURE",     "#dcedc8", "4-7 days"),
        ("HARVEST",     "#dcedc8", "1 hr"),
        ("EXTRACT",     "#fff9c4", "4 hr"),
        ("CONCENTRATE", "#ffe0b2", "2 hr"),
        ("DEPOSIT",     "#fce4ec", "30 min"),
        ("ELECTRODE",   "#cce6ff", "2 hr"),
    ]
    n = len(steps)
    box_w = 0.85 / n
    for i, (label, color, time) in enumerate(steps):
        x = 0.05 + i * box_w
        B.add_patch(patches.FancyBboxPatch(
            (x + 0.005, 0.30), box_w - 0.01, 0.40,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor="black", linewidth=1.0,
            transform=B.transAxes))
        B.text(x + box_w/2, 0.50, label, transform=B.transAxes,
               ha="center", va="center", fontsize=9, fontweight="bold")
        B.text(x + box_w/2, 0.12, time, transform=B.transAxes,
               ha="center", va="center", fontsize=7, style="italic",
               color="#555")
        # Arrow to next
        if i < n - 1:
            B.annotate("", xy=(x + box_w + 0.002, 0.50),
                       xytext=(x + box_w - 0.005, 0.50),
                       xycoords=B.transAxes,
                       arrowprops=dict(arrowstyle="->", lw=1.0))

    # ------- Region C: crossbar zoom (mid right) -------
    C = fig.add_axes([0.51, 0.45, 0.30, 0.22])
    C.set_xticks([]); C.set_yticks([])
    C.set_facecolor("#fafcff")
    C.set_title("C. Crossbar architecture detail",
                fontsize=12, loc="left", fontweight="bold", pad=8)

    rows, cols = 6, 6
    for r in range(rows):
        y = 0.85 - r * 0.13
        C.plot([0.10, 0.90], [y, y], color="#d4af37",
               linewidth=2.5, transform=C.transAxes)
    for cc in range(cols):
        x = 0.15 + cc * 0.135
        C.plot([x, x], [0.15, 0.95], color="#666666",
               linewidth=2.5, alpha=0.7, transform=C.transAxes)
    for r in range(rows):
        for cc in range(cols):
            y = 0.85 - r * 0.13
            x = 0.15 + cc * 0.135
            C.add_patch(patches.Rectangle(
                (x - 0.025, y - 0.025), 0.05, 0.05,
                facecolor="#cc6633", edgecolor="black", linewidth=0.5,
                transform=C.transAxes))

    # Highlighted device (R1, C2)
    sel_x = 0.15 + 2 * 0.135
    sel_y = 0.85 - 1 * 0.13
    C.add_patch(patches.Rectangle(
        (sel_x - 0.04, sel_y - 0.04), 0.08, 0.08,
        fill=False, edgecolor="red", linewidth=2.0, linestyle="--",
        transform=C.transAxes))
    C.text(0.5, 0.05,
           "Geobacter memristor at each intersection",
           transform=C.transAxes, ha="center", fontsize=8,
           style="italic", color="#444")

    # ------- Region F: key parameters callout (right of C) -------
    F = fig.add_axes([0.82, 0.45, 0.16, 0.22])
    F.set_xticks([]); F.set_yticks([])
    F.set_facecolor("#fff7e6")
    F.set_title("F. Key parameters", fontsize=11, loc="left",
                fontweight="bold", pad=8)
    F_text = (
        "• V_op = 70-130 mV\n"
        "    (biological match)\n\n"
        "• E/spike = 0.3-100 pJ\n\n"
        "• Cross-bar = 1024×1024\n"
        "    = 1M devices/chip\n\n"
        "• CMOS readout:\n"
        "    TSMC 180 nm, PCIe x4\n\n"
        "• Package: 25 × 25 mm\n"
        "    CFP-256"
    )
    F.text(0.05, 0.95, F_text, transform=F.transAxes,
           ha="left", va="top", fontsize=8, family="monospace")

    # ------- Region D: energy per token bar chart (lower left) -------
    D = fig.add_axes([0.05, 0.06, 0.42, 0.33])
    D.set_facecolor("#fafcff")
    D.set_title("D. Energy per token — LLaMA-70B reference",
                fontsize=12, loc="left", fontweight="bold", pad=8)

    bars = [
        ("H100 silicon",            7.0,       "#cc3333"),
        ("Loihi-2 si neuromorphic", 0.32,      "#666666"),
        ("Geobacter DEMO today",    1.4,       "#cc9933"),
        ("Geobacter TARGET (eng.)", 0.014,     "#33aa33"),
        ("Biological brain floor",  0.0014,    "#1166aa"),
    ]
    names = [b[0] for b in bars]
    values = [b[1] for b in bars]
    colors = [b[2] for b in bars]
    bars_obj = D.bar(range(len(names)), values, color=colors,
                     edgecolor="black", linewidth=0.6)
    D.set_yscale("log")
    D.set_ylim(1e-3, 30)
    D.set_xticks(range(len(names)))
    D.set_xticklabels(names, rotation=15, fontsize=9, ha="right")
    D.set_ylabel("energy per token (J, log)", fontsize=10)
    D.grid(axis="y", which="both", alpha=0.3)
    for bar, v in zip(bars_obj, values):
        if v >= 1:
            txt = f"{v:.1f} J"
        elif v >= 1e-3:
            txt = f"{v*1000:.0f} mJ"
        D.text(bar.get_x() + bar.get_width()/2, v * 1.3,
               txt, ha="center", fontsize=8, fontweight="bold")
    D.text(0.5, -0.32,
           "→ Engineered Geobacter target is 500× lower than silicon",
           transform=D.transAxes, ha="center", fontsize=9, style="italic",
           color="#33aa33", fontweight="bold")

    # ------- Region E: scaling roadmap (lower right) -------
    E = fig.add_axes([0.51, 0.06, 0.47, 0.33])
    E.set_facecolor("#fafcff")
    E.set_title("E. Scaling roadmap",
                fontsize=12, loc="left", fontweight="bold", pad=8)

    milestones = [
        ("today\nFu 2020",           5,             "#ffeb3b"),
        ("year 2\n1 head",      64_000,             "#ffc107"),
        ("year 5\nLoihi-2",  1_000_000,             "#cc9933"),
        ("year 10\nmulti-chip", 1_000_000_000,      "#33aa33"),
        ("target\nLLaMA-class", 1_000_000_000_000,  "#33aa33"),
        ("ref\nbio brain", 86_000_000_000,          "#1166aa"),
    ]
    names = [m[0] for m in milestones]
    vals = [m[1] for m in milestones]
    colors = [m[2] for m in milestones]
    bars_e = E.bar(range(len(names)), vals, color=colors,
                   edgecolor="black", linewidth=0.6)
    E.set_yscale("log")
    E.set_ylim(1, 1e14)
    E.set_xticks(range(len(names)))
    E.set_xticklabels(names, fontsize=8)
    E.set_ylabel("neuron count (log)", fontsize=10)
    E.grid(axis="y", which="both", alpha=0.3)
    for bar, v in zip(bars_e, vals):
        E.text(bar.get_x() + bar.get_width()/2, v * 2,
               f"{v:,}", ha="center", fontsize=7, rotation=0)

    # Save
    fig.savefig(out, dpi=130, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"  -> {out}")


if __name__ == "__main__":
    main()

# Visual design brief — bacterial neuromorphic chip infographic

Design layout to produce a polished engineering infographic of the bacterial neuromorphic chip, matching the visual style of `tr_diode_data_center/design_rendering.png`.

## Canvas

- 16:9 landscape, minimum 1920 × 1080
- White background with subtle technical-blueprint grid
- Dark green/teal title bar across the top

## Six-region layout

```
┌─────────────────────────────────────────────────────────────────┐
│ TITLE: Bacterial Neuromorphic Chip — Physical Design            │
│ Subtitle: Geobacter Nanowire AI Compute Substrate               │
├─────────────────────────────────────────────────────────────────┤
│                                  │                              │
│   A: chip cross-section          │   B: bioreactor → chip       │
│   (largest panel, ~50% canvas)   │      workflow (6 boxes)      │
│                                  ├──────────────────────────────┤
│                                  │   C: crossbar 6×6 zoom       │
│                                  │      with sense amp          │
├──────────────────────────────────┼──────────────────────────────┤
│                                  │                              │
│   D: energy/token bar chart      │   E: scaling roadmap         │
│      (5 bars, log scale)         │      (5 milestones to 10¹²)  │
│                                  ├──────────────────────────────┤
│                                  │   F: key parameters callout  │
└──────────────────────────────────┴──────────────────────────────┘
```

## Region A — chip cross-section (the hero)

Vertical stack, bottom-to-top:

| Layer | Color | Label |
|---|---|---|
| Si substrate | dark gray (#444) | `Si substrate` |
| CMOS readout | orange (#bb6633) | `CMOS READOUT (TSMC 180 nm)` |
| Au wire-bond region | gold (#d4af37) | `Au wire-bond pads, 0.5 mm pitch` |
| Geobacter nanowire layer | warm brown (#7a4f10) | `GEOBACTER PROTEIN NANOWIRE LAYER` |
|  |  | `70-130 mV switching, 0.3-100 pJ/event` |
|  |  | (render as scattered squiggly lines for pili) |
| Ag top electrode | silver (#ccc) | `Ag top electrode (100 nm)` |
| Al₂O₃ passivation | light blue (#aaaaff) | `Al₂O₃ ALD passivation (20 nm)` |
| Glass cap | translucent blue (#cce6ff) | `glass window encapsulation` |

Bottom dimension: `25 × 25 mm package (1024×1024 = 1M devices)`

## Region B — Bioreactor-to-chip workflow

Six color-graded boxes connected by arrows, green → blue:

1. **CULTURE** (light green) — Geobacter sulfurreducens, 30 °C, anaerobic
2. **HARVEST** (light green) — 4,000 g × 15 min
3. **EXTRACT** (yellow) — blender shear + diff. centrifuge
4. **CONCENTRATE** (orange) — Amicon 10 kDa, 0.1-1 mg/mL
5. **DEPOSIT** (pink) — drop-cast onto patterned CMOS
6. **ELECTRODE** (light blue) — 100 nm Ag thermal evap + ALD

Time labels under each arrow: `4-7 days`, `1 hr`, `4 hr`, `2 hr`, `30 min`, `2 hr`.

## Region C — Crossbar 6×6 zoom

- 6 gold horizontal row lines (R0-R5)
- 6 gray vertical column lines (C0-C5)
- Brown memristor squares at each intersection
- One device highlighted with red dashed box: `selected device (R1, C2)`
- Sense-amp box on the right with arrow pointing to a column
- Caption: `Geobacter memristor at each intersection; 1024×1024 per chip`

## Region D — Energy per token (log-scale bar chart)

Five bars on log y-axis (1 mJ to 10 J):

| Bar | Color | Height label |
|---|---|---|
| H100 silicon | red (#cc3333) | **7 J** |
| Loihi-2 silicon neuromorphic | gray (#666666) | 320 mJ |
| Geobacter demo today | tan (#cc9933) | 1.4 J |
| Geobacter engineered target | green (#33aa33) | **14 mJ** |
| Biological brain floor | blue (#1166aa) | 1.4 mJ |

Title: `Energy per token, LLaMA-70B reference`
Footnote: `Engineered Geobacter is 500× lower than silicon`

## Region E — Scaling roadmap

Five horizontal milestones on a log y-axis, color-graded yellow → green → blue:

1. **Today** — 5 neurons (Fu 2020 demo)
2. **Year 2** — 64K neurons (single attention head)
3. **Year 5** — 1M neurons (Loihi-2 class)
4. **Year 10** — 1B neurons (multi-chip system)
5. **Target** — 1T neurons (LLaMA-class)
6. **Reference** — 86B neurons (biological brain) — shown as a dashed line

## Region F — Key parameters callout

White-bordered box, 5 bullet lines:

- V_op = **70-130 mV** (biological match)
- E/spike = **0.3-100 pJ**
- Cross-bar: **1024 × 1024 = 1M devices**
- CMOS readout: **TSMC 180 nm**, **PCIe x4**
- Package: **25 × 25 mm** CFP-256

## Color palette (consolidated)

| Element | Hex |
|---|---|
| Biology / Geobacter | `#7a4f10` |
| Silicon CMOS | `#bb6633` |
| Gold (bonds + row lines) | `#d4af37` |
| Tech blue (glass + tech accents) | `#cce6ff` |
| "Target / success" green | `#33aa33` |
| "Baseline / what to beat" red | `#cc3333` |
| Biological reference blue | `#1166aa` |
| Neutral gray | `#666666` |

## Typography

- Title: sans-serif bold, white-on-dark-teal, 32-40 pt (Inter Bold / Helvetica Bold)
- Region labels: sans-serif bold, 14 pt
- Body callouts: sans-serif regular, 10-11 pt
- Measurements/specs: mono (JetBrains Mono), e.g. "70-130 mV", "0.3-100 pJ"

## AI image generation prompt

> A high-resolution technical engineering infographic with a title bar reading "Bacterial Neuromorphic Chip — Physical Design: Geobacter Nanowire AI Compute Substrate". Layout in a 16:9 landscape canvas with six labeled regions: (A) a large cross-section diagram of a layered semiconductor chip showing from bottom to top — dark gray silicon substrate, rich orange CMOS readout layer labeled "TSMC 180 nm", gold wire-bond pads with bridge wires going up, a brown layer filled with scattered short squiggly protein nanowires labeled "Geobacter protein nanowire layer, 70-130 mV switching, 0.3-100 pJ/event", a silver Ag top electrode, light blue Al₂O₃ passivation, and translucent blue glass encapsulation cap; with dimension lines reading "25 × 25 mm package, 1024 × 1024 = 1M devices"; (B) on the upper right, six horizontal connected boxes for a bioreactor-to-chip workflow labeled CULTURE → HARVEST → EXTRACT → CONCENTRATE → DEPOSIT → ELECTRODE, color-graded from green to blue with duration labels; (C) on the mid-right, a 6×6 cross-bar grid schematic with gold horizontal row lines, gray vertical column lines, brown memristor squares at intersections, one device highlighted with a red dashed box; (D) on the lower left, a log-scale bar chart titled "Energy per token, LLaMA-70B" comparing five substrates with the engineered Geobacter target visibly 500× lower than silicon; (E) on the lower right, a scaling roadmap from 5 neurons today to 1 trillion neurons future; (F) a corner callout box with key specs (V_op, energy per spike, package size). Clean technical-blueprint style on white background with subtle grid, drop shadows on layers, color-coded sections, sans-serif typography. Engineering-grade rendering, like a high-quality patent figure or product datasheet infographic.

## Style references

- `tr_diode_data_center/design_rendering.png` — the visual reference for this style in the repo
- Patent figures with clean line art + annotations
- NVIDIA whitepaper-style product datasheets (e.g. H100 cross-section diagrams)
- IEEE Spectrum infographics

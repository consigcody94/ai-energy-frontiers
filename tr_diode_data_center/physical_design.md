# TR diode panel — physical design

Translation of the simulation into a manufacturable hardware system. This is the engineering layer: real materials, real dimensions, real wiring, real costs. Sized for a single deployable **panel** plus the **array** of panels that covers a hyperscale data-center roof.

## Table of contents

1. [System overview](#1-system-overview)
2. [Single-panel mechanical design](#2-single-panel-mechanical-design)
3. [Thermal interface to hot exhaust](#3-thermal-interface-to-hot-exhaust)
4. [Electrical architecture](#4-electrical-architecture)
5. [Roof-scale array layout](#5-roof-scale-array-layout)
6. [Tolerances and failure modes](#6-tolerances-and-failure-modes)
7. [Costs](#7-costs)

---

## 1. System overview

```
            ╔═══════════════════════════════════════════╗
            ║                NIGHT SKY                  ║   ~248–280 K effective
            ║    (8–13 µm atmospheric window open)      ║
            ╚════════════╤══════════════════════════════╝
                         │ thermal radiation upward
                         │
   ┌─────────────────────┴──────────────────────────────┐
   │       ZnSe or HDPE IR-transparent window           │   95% transmission 8–13 µm
   ├────────────────────────────────────────────────────┤
   │   MCT (HgCdTe) photodiode array, Eg = 0.10 eV      │   ← here is where current flows
   │   1 m × 1 m, 100×100 = 10,000 elements             │
   ├────────────────────────────────────────────────────┤
   │   Cu cold-plate (electrical contact + heat sink)   │
   ├────────────────────────────────────────────────────┤
   │   Aerogel thermal blanket  (low-k insulator)       │   prevents hot side from
   │                                                    │   warming the photodiode
   ├────────────────────────────────────────────────────┤
   │   Cu hot-plate, T_h = 325 K                        │
   │   ╱╲╱╲╱╲╱╲╱╲ heat-pipe array (water-Cu) ╱╲╱╲╱╲╱╲   │   thermally coupled to
   └─────┬──────────────────────────────────────────────┘   exhaust duct
         │
         ▼ to hot-aisle exhaust duct (52 °C airflow)
```

The panel is **600 W radiative-limit class** (1 m² at ~600 W/m² mid-range realistic device target). At today's 0.5% device efficiency it actually delivers ~3 W; at a 5-year roadmap 5% device efficiency, ~30 W. Sized so that 1 m² is the manufacturing/handling unit and a hyperscale roof needs ~50,000 panels.

## 2. Single-panel mechanical design

### Panel envelope

| dimension | value |
|---|---|
| outer width × length | 1000 mm × 1000 mm |
| total thickness | 65 mm |
| frame | extruded 6061-T6 aluminum, 30 mm × 50 mm box section |
| sealed weight | ~22 kg |
| operating temperature range | -20 °C to +85 °C |
| ingress protection | IP65 (rain/dust) |

### Stack (top to bottom)

| layer | material | thickness | function |
|---|---|---|---|
| top cover | ZnSe-AR coated optical window OR aluminized HDPE film | 2 mm / 0.05 mm | IR-transparent atmospheric barrier |
| air gap (anti-condensation) | N₂-filled cavity, vented via dessicator | 3 mm | prevents fog/dew on cover |
| photodiode array | Hamamatsu G14045-2DP or equivalent MCT (Hg₁₋ₓCd ₓTe) 100×100 elements wire-bonded to FR-4 carrier | 5 mm including carrier | radiative emitter / current generator |
| cold-plate | Cu C11000, polished top surface | 6 mm | electrical bus + heat sink |
| insulation | silica aerogel blanket, k ≈ 0.018 W/(m·K) | 15 mm | prevents hot-side heat leak into the diode |
| hot-plate | Cu C11000, top side bonded to insulation, bottom side coupled to heat pipes | 6 mm | thermal mass at T_h ≈ 325 K |
| heat-pipe matrix | 4× Cu-water heat pipes, 8 mm OD, parallel | 8 mm | thermal flow from exhaust duct to hot plate |
| backplane | painted aluminum 6061-T6 plate | 3 mm | structural + duct mount |
| mounting standoffs | 4× M8 stainless-steel | 25 mm | attach to roof channel |

### IR window choice

| option | transmission (8–13 µm) | cost ($/m²) | UV/weather rating |
|---|---|---|---|
| ZnSe-AR (optical grade) | 95% | ~3,000 | excellent, 20+ year |
| polished CsI | 90% | ~6,000 | poor (hygroscopic, ruled out) |
| HDPE film, aluminized | 85% | ~80 | moderate, 3–5 year replacement |
| BaF₂ | 92% | ~2,500 | moderate |

**Recommended for prototype:** HDPE film (cheap, replaceable). **Recommended for production at scale:** ZnSe-AR if cost falls to ~$500/m² (already manufactured for thermal imaging optics).

### Photodiode array spec

- **Material:** Hg₀.₈Cd₀.₂Te (HgCdTe / MCT), bandgap 0.10 eV (12.4 µm cutoff)
- **Pixel:** 8 mm × 8 mm, ~6 mm × 6 mm active area
- **Array:** 100 × 100 elements per panel = 10,000 diodes, ~36% fill factor
- **Operating bias:** reverse-biased at the maximum-power point V_mp ≈ 50–100 mV
- **Series-resistance budget:** R_s × I_mp < 5 mV per diode (set by contact metallization)
- **Wire-bond pitch:** 0.5 mm to FR-4 carrier with parallel/series interconnect matrix
- **Interconnect scheme:** 100 strings of 100 diodes in parallel → ~5 V open-circuit, ~50 A short-circuit per panel at maximum power

## 3. Thermal interface to hot exhaust

The hot side must stay at ~325 K (52 °C, typical hot-aisle exhaust) without conducting that heat into the photodiode (which wants to stay cool to maximize ΔT_radiative).

### Heat-pipe matrix

- **4 × Cu-water heat pipes**, 8 mm OD × 600 mm length per panel
- **Evaporator end:** flat-clamped to exhaust-duct sheet metal (52 °C airflow surface temperature)
- **Condenser end:** brazed to the panel's Cu hot-plate
- **Heat transport capacity:** ~50 W per pipe at this ΔT → 200 W per panel (vastly more than needed; the limiting factor is radiation, not conduction)
- **Working fluid:** distilled water (0–200 °C range, freeze-protected by the always-warm exhaust)

### Aerogel insulation

The aerogel blanket between hot- and cold-plate is the critical component for preventing the photodiode from warming. Silica aerogel at k = 0.018 W/(m·K) is the lowest commercial value short of vacuum insulation.

- **Heat leak budget:** Q_leak ≤ 10 W/m² panel area
- **Required thickness:** Q_leak = k·ΔT/L → L ≥ k·ΔT/Q = 0.018·(52−27)/10 ≈ 45 mm
- **Conservative:** use 15 mm aerogel + active TEC cooling on the diode (offsets remaining leak)

### Active cold-side cooling

If passive insulation is insufficient (humid sites where the diode must stay below ambient for the sky-radiation differential to exist), add a 50 W TEC (Peltier) module on the cold-plate. This consumes ~25 W of electricity per panel — eats into the recovered power but enables operation in marginal climates.

## 4. Electrical architecture

```
Per-panel:
  100 diode strings × 100 diodes/string  →  panel bus  →  MPPT controller
                                                          (TI BQ24650 or eq.)
                                                                │
                                                                ▼
String of 8 panels → 200 V DC bus → solar-style microinverter → grid-tie 120/240 VAC

Roof aggregation:
  50,000 panels / 8 = 6,250 strings → 6,250 microinverters → switchgear → utility
```

### Per-panel MPPT controller

- **Part:** Texas Instruments BQ24650 or Analog Devices LT8490
- **Tracks:** maximum power point of each panel independently (sky temperature varies across the roof due to local atmospheric humidity, panel orientation, shading)
- **Efficiency:** ~95%
- **Output:** 0–30 V boost to a string bus at 200 V DC

### String aggregation

- **8 panels in series at MPPT output** → 200–240 V DC string bus
- **Microinverter per string:** Enphase IQ8M class or equivalent grid-tie unit
- **Output:** 240 VAC, anti-island, UL 1741-compliant

### Roof-scale aggregator

- **6,250 microinverters** feed into 5–10 main panel boards
- **Each board:** 480 VAC three-phase output to facility transformer
- **Grid-tie:** behind the meter, offset against facility load (~5 MW)

### Night-only operation

- TR diodes only produce at night (sun overwhelms the sky-temperature signal during day)
- Microinverters drop into standby below threshold; minimum drag ~0.5 W per unit
- Solar PV on the same roof in daytime + TR diode at night = 24-hour roof harvest

## 5. Roof-scale array layout

### Panel placement

- **Tilt:** flat (zenith-facing) — the sky radiates uniformly above ~45° elevation; tilt adds no benefit and increases wind load
- **Gap between panels:** 50 mm (thermal expansion, maintenance access)
- **Walkways every 10 panels:** 600 mm wide service paths

### Hyperscale (10 ha = 100,000 m²) deployment

| quantity | value |
|---|---|
| total panels | ~80,000 (after walkways + edge gaps reduce 100,000 to ~80,000 effective) |
| total mass | ~80,000 × 22 kg = 1,760 t (added roof load) |
| total wired cost | ~$28 M at $350/panel (see BOM) |
| installation labor | ~25 panels/person·day × 200 person-days = 5,000 panels/day → 16 days for 80,000 panels |
| total install cost | ~$8 M labor + commissioning |
| **CapEx** | **~$36 M one-time** |
| annual yield | 170 MWh × 0.8 (real array efficiency) = 136 MWh |
| at $0.10/kWh | $13,600/year — **NOT economic at this scale today** |

The cost of MCT photodiode arrays must come down ~10x for hyperscale deployment to be economic. The technology roadmap exists (the same MCT arrays are mass-produced for thermal imaging, at falling cost) but is not there yet in 2026.

## 6. Tolerances and failure modes

### Critical tolerances

| parameter | spec | what fails if missed |
|---|---|---|
| photodiode bandgap uniformity | E_g = 0.10 ± 0.005 eV across array | output variance + mismatched MPPT |
| IR window flatness | < λ/4 across 1 m | spectral interference fringes |
| aerogel thickness uniformity | 15 ± 1 mm | hot spots that thermally damage diodes |
| heat-pipe inclination | ≥ 2° from horizontal | reduced thermal transport |
| diode wire-bond pull strength | > 5 g (0.05 N) | open circuits in field |

### Failure modes

| failure | symptom | mitigation |
|---|---|---|
| moisture ingress through IR window seam | reduced QE, eventually short | dessicator + N₂ purge; replace HDPE film every 4 years |
| heat-pipe leak | hot-plate cools to ambient | redundant pipes (4 per panel); single failure tolerated |
| MPPT controller fail | one panel zero output | independent per-panel MPPT means no string-level dropout |
| storm / hail impact | broken IR window | ZnSe windows have polycarbonate hail shield (5 mm); HDPE film simply replaced |
| photodiode array shorting | open-circuit string voltage drops | per-string fusing, automatic isolation |

## 7. Costs

See [`bom.csv`](bom.csv) for the full per-panel bill of materials with vendors.

| category | $/panel | $/W (panel rated 3 W realistic) |
|---|---|---|
| MCT photodiode array | $185 | $62 |
| IR window (HDPE film + frame) | $25 | $8 |
| Cu hot/cold plate + heat pipes | $42 | $14 |
| aerogel insulation | $18 | $6 |
| frame + mounting hardware | $30 | $10 |
| FR-4 carrier + wiring | $15 | $5 |
| MPPT controller | $20 | $7 |
| microinverter (1/8 panel allocation) | $15 | $5 |
| **total parts** | **$350** | **$117** |
| labor (assembly + install) | $100 | $33 |
| **total installed** | **$450** | **$150** |

For comparison: utility-scale solar PV is currently ~$1.20/W installed. TR diode is **~100× more expensive per W** today. The path to parity is photodiode-array cost reduction (which is the dominant line item).

### Pilot-scale economics (10 panels)

| item | cost |
|---|---|
| 10 panels delivered | $3,500 |
| installation (1 person-day) | $1,000 |
| balance of system (inverter, wiring, monitoring) | $2,000 |
| commissioning, instrumentation | $1,500 |
| **pilot total** | **~$8,000** |

A 10-panel pilot is achievable in a university or corporate skunkworks budget. It validates the model, reveals real failure modes, and gives an honest device-efficiency measurement that the current ~0.5% derate could be revised against.

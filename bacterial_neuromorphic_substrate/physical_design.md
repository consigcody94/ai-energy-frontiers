# Bacterial neuromorphic chip — physical design

Translation of the substrate-comparison numbers into a buildable hybrid chip. The architecture is **Geobacter protein nanowires** providing the memristor elements (the low-voltage, low-energy "synapses"), bonded to a **silicon CMOS readout** layer that handles I/O, addressing, and clocking. The bacteria grow the nanowires *outside* the chip — they are not part of the operating circuit.

This document specifies the hardware path from a published 5-neuron demonstration to a transformer-block-scale (~10⁵ neurons) prototype on a 5 cm × 5 cm test chip.

## Table of contents

1. [Two-layer architecture overview](#1-two-layer-architecture-overview)
2. [Bioreactor: growing the nanowires](#2-bioreactor-growing-the-nanowires)
3. [Nanowire processing and deposition](#3-nanowire-processing-and-deposition)
4. [CMOS readout chip](#4-cmos-readout-chip)
5. [Integration and packaging](#5-integration-and-packaging)
6. [Scaling roadmap](#6-scaling-roadmap)
7. [Costs](#7-costs)

---

## 1. Two-layer architecture overview

```
                  ┌────────────────────────────────────────────┐
                  │  TOP: Geobacter protein nanowire memristor │
                  │       array, 1024 × 1024 cross-bar         │
                  │       70-130 mV switching, 0.3-100 pJ/event│
                  └──────────────────┬─────────────────────────┘
                                     │ Au wire-bond pads
                                     │ 0.5 mm pitch
                                     │
                  ┌──────────────────▼─────────────────────────┐
                  │  BOTTOM: CMOS readout (180 nm or 65 nm)    │
                  │  - row/column decoders                     │
                  │  - sense amplifiers per column             │
                  │  - state-machine sequencer                 │
                  │  - SPI/PCIe interface                      │
                  └────────────────────────────────────────────┘
```

The Geobacter layer is the **active element** — what fires the spikes at biological voltage. The CMOS layer is the **mundane infrastructure** — addressing, clocking, I/O. Each is a mature technology in isolation; the contribution is the integration.

## 2. Bioreactor: growing the nanowires

Bacteria are grown in an anaerobic bioreactor; the harvested protein nanowires are *not* part of the operating chip. Growth conditions ([Lovley lab protocols](https://www.nature.com/articles/s41467-020-15759-y)):

| parameter | value |
|---|---|
| organism | *Geobacter sulfurreducens* PCA strain |
| growth medium | freshwater medium with 20 mM acetate (electron donor) + 40 mM fumarate (electron acceptor) |
| atmosphere | 80% N₂ / 20% CO₂ anaerobic |
| temperature | 30 °C |
| pH | 6.8 |
| growth time | 4-7 days to harvest density |
| yield | ~3 mg dry nanowire mass per litre culture |

For a 5 cm × 5 cm chip with 10⁶ nanowire devices, total mass required is ~10 µg — three orders of magnitude below what a 1-L bioreactor produces per cycle. **Material supply is not a bottleneck.**

### Bioreactor equipment

- 1-L jacketed glass fermenter (BioFlo 120 or Eppendorf DASGIP)
- anaerobic gas mixing manifold (Cole-Parmer)
- peristaltic pump + sterile media feed
- temperature + pH controllers (standard fermenter accessories)
- harvest centrifuge (Beckman Avanti J-26)

## 3. Nanowire processing and deposition

Once harvested, pili are extracted from the bacterial cell membrane and prepared for chip deposition.

### Extraction protocol

1. Centrifuge culture at 4,000 g for 15 min; resuspend cells in low-ionic-strength buffer.
2. Blend at low speed (10,000 rpm × 2 min) to shear pili off the cell surface.
3. Differential centrifugation: 16,000 g × 30 min removes cells; supernatant contains free pili.
4. Buffer exchange via dialysis into device-deposition buffer (10 mM ammonium acetate).
5. Concentrate to 0.1–1 mg/mL via Amicon centrifugal filter (10 kDa MWCO).

### Deposition onto chip

Two routes have been demonstrated in the literature:

**Route A — drop-cast (Fu 2020):** Apply a 1-µL droplet of nanowire suspension to the patterned CMOS top metal. Air-dry. Pili form a randomly oriented mat between bottom and top electrodes. Simple, ~5% device yield.

**Route B — directed assembly (Yao 2023+):** Use AC dielectrophoresis to align pili across pre-patterned electrode gaps. Higher yield (~60%) but requires additional integration.

The pilot chip should use **Route A** for speed; production scale-up uses Route B.

### Top-electrode deposition

After nanowire mat is dry:
1. Deposit 100-nm Ag top electrode via shadow-mask thermal evaporation
2. Patterned to 1024 × 1024 grid matching the bottom-electrode addressing
3. Final encapsulation: 20-nm Al₂O₃ via atomic layer deposition (protects pili from oxidation)

## 4. CMOS readout chip

A standard mixed-signal ASIC on a mature node (180 nm or 65 nm — no advanced node is needed because the active devices are above-die).

### Block diagram

```
   ┌─────────────────────────────────────────────┐
   │              CMOS readout chip              │
   │                                             │
   │  ┌──────────┐    ┌────────────────────┐   │
   │  │ row decoder │ ─▶│ Geobacter cross-bar │  ─── memristor array above
   │  │  10 bits   │   │ select line         │   │
   │  └──────────┘    └────────────────────┘   │
   │       │                  │                 │
   │       ▼                  ▼                 │
   │  ┌──────────┐    ┌────────────────────┐   │
   │  │ column decoder │  sense amps × 1024 │   │
   │  │  10 bits   │   │ + ADC per 16 cols  │   │
   │  └──────────┘    └────────────────────┘   │
   │                          │                 │
   │  ┌──────────────────────┴───────────┐    │
   │  │ state-machine sequencer + DRAM    │    │
   │  │ + SPI/PCIe interface              │    │
   │  └───────────────────────────────────┘    │
   └─────────────────────────────────────────────┘
```

### Spec

| feature | value |
|---|---|
| process node | TSMC 180 nm CL018ULP (low power, low cost) |
| die size | 25 mm × 25 mm |
| cross-bar size | 1024 × 1024 = ~1M devices |
| supply voltage | 0.18 V core (low V for low energy) |
| memristor write/read voltage range | 50–300 mV |
| sense amplifier count | 1024 (one per column) |
| ADC | 8-bit, 1 per 16 columns = 64 total |
| state-machine clock | 10 MHz |
| host interface | PCIe x4 Gen 2 |
| power (silicon) | < 0.5 W at 10 MHz operation |
| cost (production) | $30–50 per die at 100k volume |

## 5. Integration and packaging

The chip ships as a hybrid package:
1. CMOS die wire-bonded into a ceramic flat-pack (CFP-256)
2. Bond pads exposed to receive the Geobacter top layer
3. Nanowire deposition + Ag top electrode + Al₂O₃ passivation performed at the package level
4. Final encapsulation with a glass window over the active area (allows visual inspection)

### Operating environment

| condition | spec | reason |
|---|---|---|
| operating temperature | 10–45 °C | pili degrade above ~50 °C |
| humidity | 20–60% RH | controlled to prevent water bridging |
| atmosphere | inert (N₂) or low-O₂ | Ag electrodes oxidize in air at high humidity |
| operating life | 3+ years | demonstrated by accelerated aging (Yao 2023) |

The wet biological substrate is the **operating-environment fragility** of this design. Silicon ASICs operate in any conditions; this chip needs a controlled atmosphere.

## 6. Scaling roadmap

| milestone | year | neurons | what it proves |
|---|---|---|---|
| Fu 2020 baseline | done | 5 | physics works |
| 256-neuron pattern recognition | 1 yr | 256 | classifier-class task on hybrid chip |
| 64K-neuron attention head | 2 yr | 64,000 | single transformer block runs |
| 1M-neuron transformer | 3 yr | 1,000,000 | toy language model |
| 1B-neuron multi-chip | 5 yr | 1,000,000,000 | LLaMA-scale, multi-chip system |
| 1T-neuron data center | 7-10 yr | 1,000,000,000,000 | full transformer-class deployment |

The 64K-neuron attention-head milestone is the critical "is this real" test. If a single 256×256 attention head runs at expected energy and accuracy, the scale-up path is engineering, not physics.

## 7. Costs

See [`bom.csv`](bom.csv) for the per-component breakdown.

### Pilot chip (1M neurons, 5 cm × 5 cm)

| category | cost (USD) |
|---|---|
| CMOS readout chip (custom 180 nm, low volume) | $80,000 (NRE) + $1,500/die |
| bioreactor + media + Geobacter culture | $35,000 |
| nanowire extraction + processing equipment | $25,000 |
| nanowire deposition + Ag evaporation | $15,000 (per-chip cost) |
| packaging + atmosphere control | $10,000 |
| test + characterization | $25,000 |
| **NRE total** | **~$190,000** |
| per-additional-chip after first | ~$3,500 |

### Scale-up to 1B neurons (next milestone)

Requires ~1,000 of the pilot chips wired together. Per-chip cost falls to ~$500 in volume; total ~$500k in silicon + ~$200k in integration. Achievable as a university-startup co-investment.

### Scale-up to 1T neurons

Requires 1,000,000 chips and a custom interconnect fabric. Total ~$50M in pure hardware. **Comparable to a single hyperscale data-center building, but for substantially less power-draw than a silicon AI data center.**

The economic case becomes obvious if the per-token energy reduction is real and the integration works.

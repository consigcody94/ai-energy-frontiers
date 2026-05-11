# Bhasma-LENR cathode — physical design

The simulation predicts a 4–5× boost in D-D fusion rate from rasashastra Pd-bhasma cathodes. This document specifies the apparatus: both the **bhasma preparation chamber** (modernized rasashastra cycle) and the **fusion-rate measurement apparatus** (UBC-style Thunderbird Reactor with a single substitution).

This is the **cross-disciplinary validation experiment**. A graduate student with a furnace, an XRD, and access to a benchtop accelerator beamline can run it in ~12 weeks.

## Table of contents

1. [Two-stage apparatus overview](#1-two-stage-apparatus-overview)
2. [Stage 1: bhasma preparation reactor](#2-stage-1-bhasma-preparation-reactor)
3. [Stage 2: UBC-style fusion measurement](#3-stage-2-ubc-style-fusion-measurement)
4. [Cathode pellet pressing](#4-cathode-pellet-pressing)
5. [Neutron detector array](#5-neutron-detector-array)
6. [Process flow](#6-process-flow)
7. [Costs](#7-costs)

---

## 1. Two-stage apparatus overview

```
  ┌─────────────────────────────────┐         ┌──────────────────────────────┐
  │   STAGE 1                       │         │   STAGE 2                    │
  │   Bhasma preparation reactor    │ ── Pd ─►│   UBC-style fusion apparatus │
  │                                 │ pellet  │                              │
  │   • Shodhana (purification)     │         │   • D⁺ plasma source         │
  │   • Bhavana (wet trituration)   │         │   • Electrochem cell (back)  │
  │   • Puta cycles (calcination)   │         │   • Cathode (front, target)  │
  │   • Optional parada-marana      │         │   • Neutron detector array   │
  │     (Hg amalgamation)           │         │                              │
  │                                 │         │   yields → neutron count    │
  │   Output:                       │         │            rate vs time      │
  │   • Pd-bhasma pellet, 30 nm     │         │                              │
  │     mean crystallite size       │         │   compare against:           │
  │   • XRD-confirmed nanostructure │         │   • commercial Pd-foil       │
  │                                 │         │   • commercial Pd-black at   │
  │                                 │         │     matched BET surface area │
  └─────────────────────────────────┘         └──────────────────────────────┘
```

Stage 1 produces 3 cathode types in parallel batches:
- A: classical Pd-bhasma (rasashastra protocol, N_puta = 60)
- B: commercial Pd-black at matched BET surface area
- C: commercial Pd foil (UBC baseline replication)

Stage 2 runs each cathode under identical conditions. The three-way comparison disentangles whether the bhasma boost is from raw surface area alone (then B ≈ A) or from rasashastra-specific factors (then A > B).

## 2. Stage 1: bhasma preparation reactor

### Bhasma reactor envelope

| feature | spec |
|---|---|
| outer dimensions | 600 × 600 × 1200 mm |
| furnace volume | 200 × 200 × 200 mm crucible chamber |
| max temperature | 1100 °C (limit for sealed Pd-bhasma) |
| atmosphere | argon purge during firing; air admitted only during opening |
| heating | SiC heating elements, PID controlled |
| crucible material | high-density alumina (Coors AD-998) |

### Process equipment list

| equipment | function | rasashastra term |
|---|---|---|
| 1 L glass round-bottom flask + condenser | acid dissolve / reprecipitate | shodhana |
| 250 mL agate mortar + pestle | hand-grind Pd powder with organic juice | bhavana |
| programmable ball mill (1 L jar) | mechanized bhavana option | bhavana (modernized) |
| 200 mm × 100 mm Ti-coated stainless press | compact Pd cake before firing | puta prep |
| muffle furnace 1100 °C with Ar inlet | calcination cycles | puta |
| 200 g triple-beam balance | mass tracking through cycles | quality |
| Hg-amalgamation flask (PTFE-lined) | optional mercury step | parada-marana |
| Hg-sublimation vacuum apparatus | recover Hg after amalgam | parada-marana |

### Modernized rasashastra cycle (60 puta target)

| step | duration | action | modern equivalent |
|---|---|---|---|
| 1 | 8 h | dissolve 50 g Pd sponge in aqua regia, reprecipitate as Pd(OH)₂ with NaOH | shodhana via classical chem |
| 2 | 4 h | calcine PdO at 600 °C, reduce under flowing H₂ at 400 °C | initial reduction step |
| 3 | 6 h | triturate Pd powder with 100 mL aloe vera juice in agate mortar | bhavana |
| 4 | 1 h | press into 30 × 30 × 5 mm cakes at 200 MPa | preparing for puta |
| 5 | 4 h | fire in sealed Coors crucible at 800 °C for 4 h, cool, regrind | one puta cycle |
| 6 | repeat 5 | × 59 more cycles | reach N_puta = 60 |
| 7 (opt) | 12 h | triturate with metallic Hg until amalgam, sublime under vacuum, ICP-MS verify Hg < 100 ppm | parada-marana |
| 8 | 2 h | final pellet pressing at 500 MPa to 10 mm × 1 mm cathode | cathode form factor |

**Total elapsed time:** ~270 hours of furnace time + ~80 hours of handling = ~12 weeks calendar with one student / one furnace.

### Characterization between cycles

After every 10 puta cycles, take a small powder sample for:
- **XRD** (Bruker D8 or equivalent) — measure crystallite size via Scherrer broadening
- **TEM** (FEI Tecnai or equivalent) — direct image of particle morphology
- **BET surface area** (Micromeritics TriStar) — to match commercial Pd-black sample C
- **ICP-MS** (Agilent 7900 or shared facility) — verify purity, residual Hg if parada-marana

This gives the time-course of nanostructure evolution and feeds into the model.

## 3. Stage 2: UBC-style fusion measurement

Directly follows the published methods of Schenkel et al., *Nature* 644:640–645 (2025), with cathode substitution as the single deliberate change.

### Apparatus overview

```
              ┌──────────────────────────────┐
              │     UHV chamber (10⁻⁷ Torr) │
              │                              │
   D₂ gas →   │  ┌────────┐                 │
              │  │  RF    │       D⁺ beam   │
              │  │ plasma │─────────►● cathode (pellet, 10 mm dia)
              │  │ source │       (1-20 keV)│   │
              │  │ 13.6   │                 │   │ electrochem cell
              │  │ MHz    │                 │   │ on back face:
              │  └────────┘                 │   │ D₂O + LiOD
              │                              │   │ Pt counter-electrode
              │                              │   │ 1-10 mA/cm² loading
              │                              │   │
              └──────────────────────────────┘
                          │
                          ▼ neutron emission (2.45 MeV from D-D)
              ┌──────────────────────────────┐
              │ ³He proportional counter     │
              │ array, 4× tubes at 10 cm     │
              │ from cathode, polyethylene-  │
              │ moderated                    │
              └──────────────────────────────┘
                          │
                          ▼ pulse height + count rate
              ┌──────────────────────────────┐
              │ multichannel analyzer (MCA)  │
              │ + Python/ROOT data logging   │
              └──────────────────────────────┘
```

### Vacuum and plasma

| item | spec |
|---|---|
| chamber | 6" CF crossover, stainless 304L, 10 L volume |
| pumping | Pfeiffer HiPace 80 + dry scroll backing |
| base pressure | 10⁻⁷ Torr |
| operating pressure | 10⁻⁴ Torr D₂ during plasma |
| plasma source | inductively coupled RF, 13.56 MHz, 0–200 W |
| beam acceleration | adjustable Einzel lens, 1–20 kV (D⁺ → cathode) |
| beam current | 0.1–5 µA (variable; typical 1 µA at 10 keV) |

### Electrochemical loading cell (back face of cathode)

| item | spec |
|---|---|
| cell volume | 5 mL |
| electrolyte | 0.1 M LiOD in D₂O (99.9% isotopic purity) |
| counter electrode | Pt mesh, 5 cm² geometric area |
| reference | Ag/AgCl in saturated KCl |
| current density | 1–10 mA/cm² across cathode area |
| temperature | 20 ± 2 °C, water-cooled jacket |

The cathode pellet sits between the plasma side (front, target for D⁺ beam) and the electrolyte (back). The cathode is one Pd disk; D atoms migrate through it from the electrolyte side, accumulating in the Pd lattice. The plasma-side D⁺ bombardment hits this loaded surface.

## 4. Cathode pellet pressing

Each cathode preparation produces a **10 mm diameter × 1 mm thick pellet** from the bhasma powder, pressed at 500 MPa in a hardened-steel die. Post-pressing density target: ≥ 95% theoretical bulk Pd (12.0 g/cm³).

Pellet handling protocol:
- Store under Ar in a desiccator until installation
- Mount via tungsten-foil edge clamp (avoids contamination of test face)
- Verify electrical contact via 4-wire ohmic test (R < 1 mΩ)

## 5. Neutron detector array

Bosch-Hale predicts ~10⁴–10⁵ n/s emission rate; the array must distinguish this from natural background (~10⁻¹ n/s/cm² from cosmic rays).

| detector spec | value |
|---|---|
| element | ³He proportional counter tubes (Reuter-Stokes or LND-2526) |
| pressure | 4 atm ³He, 1 atm CF₄ quench |
| dimensions | 25 mm OD × 300 mm active length |
| count rate | up to 10⁵ cps without dead-time correction |
| array geometry | 4 tubes parallel, 100 mm from cathode in a polyethylene moderator block (5 cm thick) |
| moderator | high-density polyethylene, slows 2.45 MeV neutrons to thermal for ³He capture |
| shielding | 30 cm borated polyethylene exterior + 5 cm Pb (gamma) |
| absolute efficiency | calibrated against ²⁵²Cf source to 5% |

### Data acquisition

- Charge-sensitive preamp per tube (Mesytec MPR-1)
- Shaping amp + ADC (CAEN N1145 or equivalent multichannel)
- Computer-readable rate output at 1 Hz
- Pulse-shape discrimination rejects gamma background (~99% rejection)

## 6. Process flow

```
   week 1:  acquire equipment, calibrate detectors against ²⁵²Cf
   weeks 2-3: prepare Pd-bhasma batch A (30 puta cycles)
   weeks 4-5: characterize batch A (XRD/TEM/BET); prepare batches B & C
   week 6:   pellet pressing + UHV install for cathode A
   week 7:   plasma calibration with cathode A unloaded (background)
   week 8:   electrochem loading curve A; D⁺ beam on; record neutron rate
   week 9:   swap to cathode B (commercial Pd-black); repeat
   week 10:  swap to cathode C (commercial Pd-foil); repeat (UBC baseline)
   weeks 11-12: data analysis; statistical comparison of three rates
   ```

### Decisive outcome

| measurement | interpretation |
|---|---|
| A > B > C with ≥ 5σ separations | Bhasma rasashastra-specific factors matter; *Nature*-tier finding |
| A ≈ B > C | Surface-area-driven; bhasma route is just a path to nano-Pd that modern chemistry has cheaper analogs of |
| A ≈ B ≈ C (all = baseline) | UBC's +15% does not reproduce in our apparatus; calls UBC into question |
| A < C | Bhasma-prep introduces neutron poisoning (likely residual Hg from parada-marana); abandon optional step |

All four outcomes are publishable.

## 7. Costs

See [`bom.csv`](bom.csv) for the full breakdown.

| category | cost (USD) |
|---|---|
| Stage 1: bhasma preparation reactor | $32,000 |
| Stage 2: vacuum chamber + plasma source | $48,000 |
| Stage 2: electrochem cell | $4,000 |
| Stage 2: ³He neutron detector array + DAQ | $85,000 |
| characterization (XRD/TEM/BET access fees, 3 mo) | $12,000 |
| consumables (D₂O, LiOD, Pd starting material) | $9,000 |
| labor (1 grad student + 0.25 postdoc, 3 months) | $35,000 |
| **total** | **~$225,000** |

The neutron detector array is the dominant capital line. If a university physics or nuclear-engineering department already has a calibrated array, the marginal cost drops below $100k.

### Pilot path

A reduced-scope pilot drops the parada-marana step (saving Hg risk and ICP-MS overhead) and uses an existing university accelerator beamline (most US/EU universities with a nuclear engineering program have one). This brings the project budget to ~$50–80k and the timeline to ~10 weeks — fundable as a single semester of graduate research.

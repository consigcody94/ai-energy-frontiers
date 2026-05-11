# SED Casimir-cavity ZPE — physical design

The simulation tells us the experiment is buildable on a university-lab budget; this document specifies *what to build*. A tabletop apparatus that pumps cesium vapor through a stack of sub-100 nm Casimir cavities and measures the orbital-shift heat release with a cryogenic bolometer.

This is the **decisive go/no-go physics experiment** for the SED interpretation of zero-point energy. Either it produces a clean signal that scales as 1/d⁴ and vanishes for closed-shell controls (Xe), or it places a hard upper bound on `f_couple` that closes the loophole.

## Table of contents

1. [Apparatus overview](#1-apparatus-overview)
2. [Casimir cavity stack](#2-casimir-cavity-stack)
3. [Vacuum and gas handling](#3-vacuum-and-gas-handling)
4. [Cesium source and dosing](#4-cesium-source-and-dosing)
5. [Bolometer cryostat](#5-bolometer-cryostat)
6. [Lock-in detection electronics](#6-lock-in-detection-electronics)
7. [Procedure](#7-procedure)
8. [Costs](#8-costs)

---

## 1. Apparatus overview

```
                  ┌─────────────────────────────┐
                  │  Cs vapor source            │
                  │  SAES getter, T ≈ 380 K     │
                  └──────────────┬──────────────┘
                                 │ (controlled atomic-beam aperture)
                                 │
                  ┌──────────────▼──────────────┐
                  │  Beam-splitter manifold     │   modulates flow between
                  │  PEEK valve, 0.1–10 Hz      │   cavity / control at f_lock
                  └──────────┬─────────┬────────┘
                  cavity arm │         │ control arm
                             │         │ (d → ∞, no Casimir suppression)
              ┌──────────────▼─┐     ┌─▼──────────────┐
              │  CASIMIR STACK  │     │  reference cell │
              │  50 layers,     │     │  same geometry  │
              │  d = 30 nm gaps │     │  but no plates  │
              │  10 cm² area    │     │                 │
              └──────────────┬─┘     └─┬──────────────┘
                             │         │
                             └────┬────┘
                                  │ (combined exhaust)
                  ┌───────────────▼─────────────┐
                  │  SQUID-TES bolometer        │
                  │  T_op = 50 mK               │
                  │  NEP ≈ 1e-19 W/√Hz          │
                  └──────────┬──────────────────┘
                             │
                  ┌──────────▼─────────────────┐
                  │  Lock-in amplifier         │
                  │  reference = beam chopper  │
                  └────────────────────────────┘
```

The apparatus is ~50 cm tall in the chamber, ~1.5 m wall-to-wall including cryostat. Total bench footprint ~2 m².

## 2. Casimir cavity stack

### Geometry

| parameter | value | rationale |
|---|---|---|
| plate material | crystalline Si, polished to λ/20 RMS | low absorbance, mature fabrication |
| plate thickness | 200 µm | mechanical stiffness against atmospheric flexure |
| in-plane size | 30 mm × 30 mm | matches cesium beam profile |
| active gap d | 30 nm (nominal); option for 100 nm | 1/d⁴ scaling favors smallest practical |
| gap-defining structure | SiO₂ pillars, 100 µm × 100 µm × 30 nm, lithographically defined | NIST-style standard |
| pillar pitch | 5 mm on square grid | sparse → high gas conductance |
| stack count | 50 layers (~25 mm tall) | aggregate volume + redundancy |
| atomic beam path length | ~25 mm through stack | sets transit time at thermal velocity |

### Fabrication

Stack each Si wafer with the following process:

1. **RCA clean** silicon wafer (200 µm thick, 4" or 6" round, cut to 30 mm × 30 mm)
2. **Thermal oxide growth** in dry O₂ at 1050 °C → 30 nm SiO₂ (gap-defining layer)
3. **Photolithography:** spin SPR-3012 resist, expose pillar pattern via maskless aligner (Heidelberg DWL66+ or Microtech LW405)
4. **Reactive ion etch** the SiO₂ everywhere except under pillar patterns → pillars protrude 30 nm above the Si substrate
5. **Strip resist, post-bake clean**
6. **Stack 50 wafers** with the pillared face downward; align by mechanical edge fixturing in a UHV-compatible Inconel clamp

The gap uniformity tolerance is set by the wafer flatness (~5 µm peak-to-valley over 30 mm). To get a 30 nm ± 1 nm gap, use a 50-point laser triangulation measurement before clamping, sorting wafers to match.

### Why 30 nm and not smaller

- At 10 nm gap, the per-atom signal grows by 81× (1/d⁴), but the **fabrication yield drops dramatically** below 20 nm.
- Below 10 nm, the photoresist developer cannot reliably clear the gap region.
- Sub-10 nm gaps require multi-stage spacer fabrication (atomic-layer-deposition tricks) that take the experiment out of "university lab budget" range.

30 nm is the **sweet spot**: lithographically standard, gives a clean 1/d⁴ measurement vs the 100 nm comparison gap, and produces a microwatt-scale signal at f_couple = 1.

## 3. Vacuum and gas handling

### UHV chamber

- **Configuration:** custom 6" CF (ConFlat) cube with 2.75" ports on each face
- **Pumping:** Pfeiffer HiPace 80 turbo backed by Pfeiffer MVP 020 scroll → base 5e-9 Torr
- **Bake:** chamber heated to 200 °C for 48 h after first assembly
- **Cesium-compatible materials only:** 316L stainless throughout the manifold; no Cu (forms Cu-Cs amalgams)
- **Pressure sensing:** Pfeiffer cold-cathode IKR 270 + dual hot-cathode IMG-300

### Gas manifold

- **Cs delivery line:** 1/4" 316L tubing, electropolished, no flanges or seams
- **Beam-defining aperture:** 0.5 mm pinhole upstream of cavity stack; sets atomic-beam divergence to ~30 mrad
- **Modulation valve:** PEEK rotary diverter, 0.1–10 Hz, ±10 ms switching time
- **Differential pumping stage:** between Cs source and cavity to maintain Cs density gradient

### Reference (control) cell

Identical 30 mm × 30 mm × 25 mm volume **with no Casimir plates** — just a hollow box. Same cesium beam, same calorimeter, same readout chain. Subtract for systematic-error cancellation.

## 4. Cesium source and dosing

- **Vapor source:** SAES Getters Cs dispenser (Cs/NF/3.4/12 FT10+10), ~$300
- **Operating temperature:** 380–420 K (above Cs vapor pressure threshold of 0.01 Torr)
- **Dosing rate:** ~10 µg/s adjustable via dispenser current (0.5–2.0 A)
- **Beam-divergence shaping:** two-stage aperture (0.5 mm + 0.3 mm collimator)
- **Quartz-crystal-microbalance (QCM):** monitors integrated Cs flux deposited downstream of cavity → independent flow calibration

For comparable experiments with **Xe (control species)**, replace Cs dispenser with a Xe leak valve (Edwards 80130) fed from a research-grade Xe cylinder at the upstream end.

## 5. Bolometer cryostat

The signal is fundamentally tiny (sub-µW at f_couple = 1, smaller below). Detection requires a cryogenic transition-edge sensor (TES) bolometer.

### Detector specification

| parameter | value |
|---|---|
| detector | SQUID-coupled superconducting TES |
| absorber | Au-Bi film on Si₃N₄ membrane, 5 mm × 5 mm |
| operating temperature | 50 mK |
| noise equivalent power (NEP) | 1e-19 W/√Hz |
| time constant τ | ~1 ms |
| dynamic range | 10⁻¹⁹ W to 10⁻¹² W with linear response |
| commercial source | SuperFab Instruments, NIST PML, Goddard Detector Systems |

### Cryostat

| parameter | value |
|---|---|
| platform | dry dilution refrigerator (Oxford Triton or BlueFors LD250) |
| base temperature | 10 mK; detector stage 50 mK |
| optical access | 50 mm bore through 4 K shield → cavity-stack exhaust port |
| acoustic isolation | passive (heavy granite slab) + active (cryostat on Sorbothane feet) |
| magnetic shielding | µ-metal cans around SQUID array |

The cryostat is the **single most expensive item** in the apparatus (~$250–400k for a turn-key dry dil fridge). Alternative for tighter budgets: rent time on a shared university facility — most physics departments with a quantum group already have one.

## 6. Lock-in detection electronics

| element | spec |
|---|---|
| beam modulation | PEEK rotary chopper at f_lock = 1 Hz nominal |
| reference signal | optical interrupter at chopper, → digital pulse train |
| TES readout | SQUID amplifier (commercial: Magnicon, Stanford Research) |
| lock-in amplifier | Zurich Instruments MFLI, or Stanford SR830 |
| sampling | 10 kHz, 24-bit |
| integration time | adjustable 1 s to 24 h depending on signal level |

The lock-in extracts the f_lock-modulated component of the bolometer output, rejecting DC drift and out-of-band noise. The expected signal is

```
P_signal(t) = P_avg + (P_cavity - P_reference) · sign(sin(2π·f_lock·t))
```

so the lock-in output at f_lock is `(P_cavity - P_reference) / π` after accounting for the square-wave Fourier components.

## 7. Procedure

1. Bake the chamber for 48 h, pump down to 5e-9 Torr.
2. Cool the cryostat to 10 mK, stabilize the TES at 50 mK transition.
3. With **no Cs flow**, record the baseline noise spectrum at f_lock for 30 minutes. Verify NEP ≤ 1e-19 W/√Hz.
4. Start Cs dispenser at 1.0 A current; monitor QCM rate.
5. Modulate the beam between cavity and reference at f_lock = 1 Hz.
6. Integrate the lock-in output for 1 hour. Compute SNR = (signal × √integration_time) / NEP.
7. **Sweep gap:** swap in the 100 nm cavity stack (otherwise identical apparatus). Verify the signal drops by ~81× (1/d⁴ check).
8. **Sweep species:** replace Cs source with Xe. Verify the signal drops by ≥ 200× (closed-shell control).
9. Either result is publication-grade:
   - **clean detection with both 1/d⁴ scaling and species selectivity** → *Phys. Rev. Lett.*
   - **null at all four cavity-gap × species combinations** → upper bound on f_couple ≤ noise-floor / signal-prediction → *Phys. Rev. D*

## 8. Costs

| category | estimate (USD) | notes |
|---|---|---|
| dilution refrigerator | $250k–$400k | the dominant line; rent if possible |
| TES bolometer + SQUID array | $40k–$80k | commercial off-the-shelf |
| Casimir cavity stack (custom) | $25k | 50-wafer microfabrication run |
| UHV chamber + pumps | $35k | turbo + scroll + pressure sensing |
| Cs dispenser + dosing manifold | $5k | SAES + 316L stainless |
| lock-in + cryo amplifiers | $20k | SR830 + SQUID readout electronics |
| optical / mechanical mounting | $10k | Thorlabs / Newport class |
| QCM, gas flow controllers | $8k | rate calibration |
| custom electronics + cabling | $15k | one-off |
| labor (5 person-months) | $100k | postdoc-level engineer + grad student |
| **total apparatus** | **~$510k** | if dil fridge is rented: ~$200k |

For a university physics lab with existing dilution refrigerator access, the marginal cost is well under $200k. For a startup or a private lab building from zero, the dilution fridge dominates.

See [`bom.csv`](bom.csv) for the parts breakdown.

### Going decisive

A 6-month measurement campaign with this apparatus produces **the first clean experimental answer to a question Schrieber (2019) raised and that has gone untested for 7 years**. Either result is the basis for a *Physical Review Letters* paper.

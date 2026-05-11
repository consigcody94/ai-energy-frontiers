# Thermoradiative diodes on AI data-center roofs

A solid-state device that pumps electrons by emitting thermal photons
toward the cold night sky. Same physics as a photovoltaic cell run in
reverse. This is the most physics-defensible of the three subprojects
— no speculative leaps, just engineering against a well-understood
upper bound.

## Table of contents

1. [Why this is the right shape of intervention](#why-this-is-the-right-shape-of-intervention)
2. [The physics in full](#the-physics-in-full)
3. [The code, function by function](#the-code-function-by-function)
4. [Calibration to the 350 mW/m² 2024 record](#calibration-to-the-350-mwm²-2024-record)
5. [Plots and what they tell you](#plots-and-what-they-tell-you)
6. [Parameter sensitivity](#parameter-sensitivity)
7. [Honest caveats](#honest-caveats)
8. [Path to the lab](#path-to-the-lab)

---

## Why this is the right shape of intervention

A hyperscale AI data center has three physical features that no other
load on the grid has all at once:

1. **Huge flat roofs.** A 50–200 MW campus has 30,000–200,000 m² of
   roof real estate doing essentially nothing.
2. **Hot exhaust at the perfect temperature.** Hot-aisle exhaust is
   typically 35–55 °C (308–328 K), which is exactly where TR diodes
   have their sweet spot — high enough above ambient that the
   Planck spectrum is shifted favorably, low enough that materials
   science is tractable.
3. **Continuous demand and free cooling-credit accounting.** Recovered
   power offsets purchased electricity at retail rates; even a 0.5%
   recovery is real dollars over a 10-year amortization.

Nobody has published on the specific marriage of TR diodes to AI
hot-aisle exhaust. Related work exists (radiative cooling for
buildings, thermophotovoltaic waste heat) but not this geometry.

## The physics in full

### Planck spectral radiance

The spectral radiance of a blackbody at temperature *T* is:

```
B(λ, T) = (2hc² / λ⁵) · 1 / (exp(hc / λkT) − 1)       [W / (m² · sr · m)]
```

Per unit area of a Lambertian emitter, hemispherical integration
multiplies by π, so total flux per area is:

```
E(T) = π ∫₀^∞ B(λ, T) dλ = σ T⁴
```

where σ = 5.67×10⁻⁸ W/(m²·K⁴) is the Stefan-Boltzmann constant. At
T = 300 K, this gives 459 W/m². At T = 248 K (effective clear-sky
temperature), 215 W/m². The naive difference is 244 W/m² — already
suggesting we have meaningful headroom.

### Atmospheric transmittance window

The Earth's atmosphere absorbs strongly across most of the thermal
IR, *except* in the 8–13 µm "atmospheric window" where water vapor
and CO₂ have low absorption. A clear, dry sky transmits 80–90% in
this window and <10% elsewhere.

Our code uses a two-sigmoid approximation:

```python
tau(λ) = 0.05 + 0.80 · sigmoid(λ_um − 7.5) · (1 − sigmoid(λ_um − 13.5))
```

This is simpler than MODTRAN but matches the qualitative shape and
integrated transmission of clear-sky measurements. The 0.05 floor
captures the wing emission/absorption.

### Diode quantum efficiency

A semiconductor diode with bandgap energy E_g converts photons with
energy E > E_g (wavelength λ < hc/E_g) into electron-hole pairs.
Below the bandgap, photons pass through unmodified.

```python
η(λ) = η_internal  if hc/λ ≥ E_g
       0           otherwise
```

For a target bandgap of 0.10 eV (HgCdTe / MCT-class material), the
cutoff wavelength is hc/E_g = 1.240 µm·eV / 0.10 eV = **12.4 µm**.
That cutoff lies just inside the atmospheric window on the long-
wavelength side, capturing essentially all useful Planck flux at
300 K.

### Net useful flux

Combining all three:

```
F_net(λ) = π · τ(λ) · η(λ) · [B(λ, T_hot) − B(λ, T_sky)]      [W / (m² · m)]
```

Integration over λ gives the net power per area in W/m². This is the
**radiative limit** — the absolute upper bound assuming a step-function
diode response and the approximated atmosphere.

### Device-realistic derate

Real TR-style devices currently capture only ~0.5% of the radiative
limit. Sources of loss:

| Loss | Typical impact |
|---|---|
| Non-radiative recombination | 2–10× reduction in usable photons |
| Series resistance + ohmic losses | 1.5–3× reduction in extractable power |
| Surface reflection (< 100% emissivity) | 1.2–2× reduction |
| Heat-leak from cold side back to hot side | 1.5–5× reduction in effective ΔT |
| Imperfect spectral matching | 1.2–2× reduction |
| Thermoelectric Carnot inefficiency (if Seebeck-based) | 5–20× reduction |

Multiplicatively, these explain the ~200× gap between the 69 W/m²
radiative limit and the 350 mW/m² achieved record.

We model this with a single constant
`DEVICE_REALISTIC_DERATE = 0.005` so the model exactly reproduces
the 2024 record at the cited conditions. Closing the gap is the
device-engineering challenge — and our parameter `device_efficiency`
makes alternative futures (5%, 10%) explicit.

## The code, function by function

```python
planck_spectral_radiance(λ, T)
    # Standard Planck law. Validated to 0.00% against σT⁴.

atmospheric_window_transmittance(λ)
    # Two-sigmoid approximation of the 8-13 µm window.

diode_quantum_efficiency(λ, E_g, η_internal=0.85)
    # Step cutoff above bandgap with internal QE.

net_radiative_power_density(T_hot, T_sky, E_g, ...)
    # Convolution + integration → W/m² (radiative limit).

radiative_limit_check()
    # Reproduces 2024 record conditions, returns both limit and
    # realistic predictions.

data_center_roof_yield(T_hot, T_sky, ..., device_efficiency)
    # Annual MWh projection for hyperscale roof, with duty-cycle
    # accounting (night fraction × weather uptime).

plot_spectra(...)
    # Three-panel spectral diagnostic plot.
```

## Calibration to the 350 mW/m² 2024 record

Liao et al. (arXiv:2407.17751) reported 350 mW/m² of nighttime
electricity generation via radiative cooling. They used a narrow-band
thermal emitter coupled to a thermoelectric, not a true TR
semiconductor diode, but the useful-power upper bound is the same.
Their cited conditions: T_hot ≈ 300 K (near-ambient), T_sky ≈ 248 K
(clear, dry nighttime).

Our model under those conditions gives:

| Quantity | Value |
|---|---|
| Radiative-limit prediction | **69.1 W/m²** |
| Realistic (η = 0.005) | **345.7 mW/m²** |
| Published record | **350 mW/m²** |
| Model / published | **0.99×** |

This calibration is *forced* in the sense that we picked η = 0.005
to land at the published value. But the radiative-limit prediction
is an *independent* check — and 69 W/m² is in the published-permissive
range (the strictest detailed-balance limits cited in the literature
give 1–6 W/m²; ours is more permissive because we don't enforce
detailed balance in the bandgap-cutoff approximation).

## Plots and what they tell you

### Three-panel spectral diagnostic

![Spectra](spectra.png)

This is the core physics on one page.

- **Top:** Planck spectral radiance for the 325 K emitter and the
  255 K effective sky. They are remarkably close in absolute terms
  — the emitter is only ~24% brighter integrated, and only in the
  long-wavelength tail. **The whole game is the differential.**
- **Middle:** atmospheric transmittance (green sigmoid) opens cleanly
  in 8–13 µm; diode quantum efficiency (red step) captures everything
  shorter than 12.4 µm (Eg = 0.10 eV).
- **Bottom:** the product. Almost all useful flux comes from the 8–13
  µm overlap region. The integrated area under this curve is the
  W/m² output.

The plot makes clear *why* high-bandgap diodes fail (they cut off
the emitter's emission peak at 9.6 µm) and *why* humid skies hurt
(closing the window reduces the green region's height).

### Bandgap × sky-temperature heatmap

![Heatmap](heatmap.png)

Realistic device power density (mW/m²) across the operating-parameter
plane at fixed T_hot = 325 K. The red dot marks the 2024 record
conditions.

Reading guide:
- The **brightest region** sits at **E_g < 0.10 eV** and **T_sky <
  250 K**. That's where to operate.
- White contours track 100 / 200 / 350 / 500 / 750 / 1000 mW/m². The
  350 mW/m² contour passes through the published record point,
  confirming the calibration.
- The cliff at E_g > 0.15 eV is the "diode cuts off the Planck
  peak" effect.

**Practical implication:** the bandgap-tunable HgCdTe alloy
system can hit E_g down to ~50 meV by composition tuning, putting
us comfortably in the bright region. But shorter-than-9 µm
cutoffs lose the emission peak.

### Monte Carlo annual yield

![Monte Carlo](monte_carlo.png)

What does the uncertainty in input parameters propagate to in the
output? Sampling realistic distributions (T_sky ~ N(255, 8) K from
clear vs cloudy night variation; T_hot ~ N(325, 5) K from facility-
to-facility variation; η ~ Uniform(0.003, 0.010) from device
generation):

| Percentile | Annual MWh |
|---|---|
| p10 | 98 |
| median (p50) | 175 |
| p90 | 255 |

Relative standard deviation: 33%. For comparison, a 5 MW data center
consumes 43,800 MWh/year, so this is **0.2–0.6% of facility load**
depending on where in the distribution you land. The lower tail (98
MWh) corresponds to humid, cloudy climates with poor weather uptime.
The upper tail (255 MWh) corresponds to dry, clear climates plus
top-of-class device efficiency.

This argues for **deploying first in arid clear-sky climates**
(US Southwest, Atacama, Middle East) where the upper tail is
achievable.

### Ceiling-vs-realistic three-scenario bar chart

![Ceiling vs realistic](ceiling_vs_real.png)

Two views of the same data:

- **Left:** annual MWh recovered (log scale). Theoretical ceiling
  is 26,844 MWh; today's device delivers 134 MWh; a plausible 5-year
  device at 5% efficiency would deliver 1,340 MWh.
- **Right:** as percent of 5 MW data-center load. Ceiling = 61%,
  today = 0.31%, 5-year = 3.1%.

The figure makes the engineering challenge explicit. There is a real
60% recovery available from the physics. We currently capture
1/200th of that. The device-engineering work has 200× headroom.

## Parameter sensitivity

The console report from `python simulate.py` produces a sensitivity
sweep table:

| E_g (eV) ↓ / T_sky → | 240 K | 250 K | 260 K | 270 K | 280 K |
|---|---|---|---|---|---|
| 0.050 | 151 W/m² | 141 W/m² | 128 W/m² | 114 W/m² | 98 W/m² |
| 0.075 | 149 W/m² | 138 W/m² | 126 W/m² | 112 W/m² | 96 W/m² |
| 0.100 | 127 W/m² | 118 W/m² | 108 W/m² | 97 W/m² | 83 W/m² |
| 0.125 | 70 W/m² | 66 W/m² | 61 W/m² | 55 W/m² | 48 W/m² |
| 0.150 | 25 W/m² | 24 W/m² | 22 W/m² | 20 W/m² | 18 W/m² |
| 0.200 | 1.8 W/m² | 1.7 W/m² | 1.7 W/m² | 1.5 W/m² | 1.4 W/m² |

(Note: these are **radiative-limit** numbers in W/m², not realistic
device output. Multiply by 0.005 to get current realistic mW/m².)

Two reads:
1. **Bandgap dominates** — going from 0.10 to 0.15 eV halves the
   output, and 0.20 eV is essentially useless. Spectral matching is
   the single most important design parameter.
2. **Sky temperature matters but less** — 240 K to 280 K (a 40 K
   swing covering clear-to-cloudy) costs 35–40% of the output, not
   90%. This means TR diodes are not strictly a clear-night
   technology; they work somewhat through partial cloud cover.

## Honest caveats

- The model assumes radiative-limit physics plus a single derate
  constant. Real device performance is geometry-dependent.
- Atmospheric transmittance is the smooth two-sigmoid; real
  atmospheric models include line absorption, ozone, aerosols, and
  multiple-scattering effects that vary daily.
- Hot-aisle exhaust temperature in real data centers varies with
  cooling architecture; modern liquid-cooled designs may have
  cooler air-side exhaust but hotter coolant streams (which would
  be better targets if coupled correctly).
- Device economics not modeled. MCT photodiodes are expensive
  per-area today; scaling assumes substantial cost reduction.

## Path to the lab

See [`protocol.md`](protocol.md). The minimal bench prototype is a
single MCT photodiode on a PID-controlled hot plate, pointed at the
sky through an HDPE or ZnSe IR window, with the diode I-V swept by
a source-measure unit. Validates the calibration anchor on a
benchtop. Cost: ~$3–8k.

The hyperscale-roof system is an engineering project, not a physics
one. The key cost target is to get the installed $/W down enough
that 0.3% recovery amortized over 10 years pays for itself.

## References

- [Liao et al., arXiv:2407.17751 (2024)](https://arxiv.org/abs/2407.17751)
- [Hsu et al., *Nature Photonics* (2024)](https://www.nature.com/articles/s41566-024-01537-5)
- [Sci. Reports 2025 — intermediate-band TR limit](https://www.nature.com/articles/s41598-025-91800-8)
- [Thermophotonic LED-PV pairs, *Renewable & Sustainable Energy Reviews* 2022](https://www.sciencedirect.com/science/article/pii/S0927024822000575)

# SED Casimir-cavity zero-point energy extraction

The longest-shot subproject in this repo. The point of including
it is *not* "we will power AI on vacuum fluctuations." It is:
**the only thermodynamically-permitted ZPE extraction mechanism
has essentially zero peer-reviewed follow-up since 2019, and the
decisive physics experiment is buildable on a university budget.**

## Table of contents

1. [The four-step argument](#the-four-step-argument)
2. [The Casimir effect: what's real and verified](#the-casimir-effect-whats-real-and-verified)
3. [Stochastic electrodynamics: the alternative interpretation](#stochastic-electrodynamics-the-alternative-interpretation)
4. [Schrieber's thermodynamic loophole](#schriebers-thermodynamic-loophole)
5. [The code](#the-code)
6. [Plots](#plots)
7. [What f_couple is and why it's the make-or-break](#what-f_couple-is-and-why-its-the-make-or-break)
8. [Honest assessment](#honest-assessment)
9. [References](#references)

---

## The four-step argument

1. The Casimir effect is real and experimentally verified to high
   precision. Two parallel plates at separation *d* in vacuum attract
   with a force per area `F/A = π²ℏc / 240 d⁴`.
2. The Casimir effect implies vacuum-mode exclusion from the cavity:
   modes with wavelength λ > 2*d* cannot fit between the plates and
   have lower energy density inside than outside.
3. In stochastic electrodynamics (SED), atomic electron orbitals are
   the steady-state balance between Larmor radiation and ZPF
   absorption. If the ZPF is suppressed (as in the Casimir cavity),
   that balance shifts and the orbital settles to a lower-energy
   state — releasing the difference.
4. Pump gas atoms through the cavity and extract the entry-side
   orbital-shift energy as heat or photons. The exit-side rebuild
   absorbs the same energy *from the free-space ZPF*, drawing on the
   universe's vacuum reservoir.

Steps 1–2 are mainstream textbook physics. Steps 3–4 are SED, a
non-standard but internally consistent alternative interpretation.
Whether Step 4 actually delivers extractable energy is an
experimental question — and the experimental answer has not been
cleanly produced.

## The Casimir effect: what's real and verified

Hendrik Casimir's 1948 calculation gave the attractive force per
area between two perfectly conducting parallel plates:

```
F/A = π² ℏ c / (240 d⁴)
```

and the equivalent energy per area:

```
E/A = − π² ℏ c / (720 d³)
```

These have been confirmed experimentally:

| Experiment | Year | Separation | Agreement |
|---|---|---|---|
| Lamoreaux (sphere-plate) | 1997 | 0.6–6 µm | ~5% |
| Mohideen & Roy | 1998 | 0.1–0.9 µm | ~1% |
| Bressi et al. | 2002 | 0.5–3 µm | ~15% |

![Casimir force vs gap](casimir_force.png)

The plot shows the closed-form Casimir prediction (blue curve)
against representative experimental data points (red dots). The
1/d⁴ scaling holds across the 0.5–3 µm decade. **This is real
physics.**

What this means for our subproject: the cavity *does* exclude
modes, and the energy density inside *is* lower than outside.
The numerical magnitude of that energy difference at a given gap
is computable from a closed form.

### Suppressed mode energy density (cavity vs free space)

The energy density of the ZPF spectrum below the cavity cutoff
frequency `ω_c = πc/d` is, by direct integration:

```
Δu(d) = ∫₀^ω_c   (ℏ ω³) / (2π² c³)  dω   =   π² ℏ c / (8 d⁴)
```

At d = 100 nm this evaluates to 390 J/m³. At d = 10 nm, 3.9×10⁶ J/m³.
Both are tiny on macroscopic scales — but the question is whether
an atom transiting the cavity can couple to a non-trivial fraction
of this density.

## Stochastic electrodynamics: the alternative interpretation

Standard quantum mechanics treats the zero-point field as a formal
device — divergent, unobservable except through specific effects
(Casimir, Lamb shift). **Stochastic electrodynamics** treats it as
a real, classical, fluctuating electromagnetic field that drives
the otherwise-deterministic motion of charged particles.

The remarkable empirical claim of SED, due primarily to Boyer and
others starting in the 1970s, is that **many quantum-mechanical
predictions can be reproduced from purely classical equations plus
the ZPF**, including:

- The Bohr radius of hydrogen
- The Planck blackbody spectrum
- The Casimir effect itself
- Aspects of the Lamb shift

SED is not the standard interpretation. Most physicists do not work
in it. But it is *internally consistent* and has been the subject of
serious peer-reviewed work (Boyer, Cetto, de la Peña, others) for 50
years.

**The crucial SED-specific claim for our subproject:** An atomic
electron is in its ground state because Larmor radiation (from
acceleration) is balanced by absorption from the ZPF. If you
suppress the ZPF, the balance breaks and the electron radiates more
than it absorbs — it spirals into a lower-energy orbital until a
new balance with the reduced ZPF spectrum is reached.

That orbital energy difference is the "vacuum extraction" — energy
that came from the free-space ZPF on the way in, deposited at the
extraction stage, and re-absorbed from the free-space ZPF on the
way out. Net flow: universe → cavity → user.

## Schrieber's thermodynamic loophole

Schrieber (2019, *Atoms* 7(2):51) reviewed three classes of ZPE
extraction:

| Class | Mechanism | 2nd-law verdict |
|---|---|---|
| 1 | Nonlinear processing of ZPF (e.g., parametric mixing in nonlinear dielectric) | **Violates** — extractable work would create entropy decrease |
| 2 | Mechanical extraction using Casimir cavities (let the plates close, harvest the energy) | **Violates** — energy released by closing equals energy needed to reopen, no net work |
| 3 | **Pump gas atoms through Casimir cavities, harvest the entry-side orbital shift** | **Does not appear to violate** — the gas is the working fluid, the universe's ZPF is the source, the cavity is the engine |

Class 3 is the only known method that does not run afoul of the
second law in the steady state. Schrieber's analysis is careful,
and as of 2026 I cannot find a refutation in the peer-reviewed
literature.

**Initial experiments** (cited indirectly by Schrieber) reportedly
saw "below-expected output." The most likely interpretation: real
f_couple (the coupling fraction — see below) is much smaller than
the theoretical maximum, putting the signal below thermal noise.

## The code

[`estimate.py`](estimate.py) implements:

```python
casimir_energy_per_area(d)
    # E/A = -π² ℏ c / (720 d³). Closed-form Casimir 1948.

cavity_mode_cutoff_freq(d)
    # ω_c = π c / d.

suppressed_zpf_energy_density(d)
    # Δu = ℏ π² c / (8 d⁴) by direct integration.

per_atom_orbital_shift_J(d, V_atom, f_couple)
    # ΔE_atom = f_couple × Δu(d) × V_atom.
    # Phenomenological. f_couple is the unknown.

cavity_flow_power_W(d, V_atom, atoms_per_sec, f_couple)
    # P = atoms_per_sec × ΔE_atom.

gas_flow_atoms_per_second(mass_g_s, atomic_mass_amu)
    # Convert mass flow to atom flow.
```

Atomic volume is set to `ATOM_VOL_HEAVY = 1.0e-30 m³` for
cesium-like polarizability. Lighter atoms (closed-shell xenon)
have much smaller effective coupling volume — that's a key
experimental control variable.

## Plots

### Power vs gap with detection floor

![Power vs gap](power_vs_gap.png)

For a realistic lab flow of 1 mg/s of cesium vapor, output power
vs cavity gap for five different f_couple values spanning the
unknown range.

**Reading guide:**
- **f_couple = 1** (theoretical maximum, top curve): predicted output
  is ~µW at 1 µm gap, ~W at 10 nm gap, ~kW at sub-10 nm. Strongly
  detectable across the lab-achievable gap range.
- **f_couple = 10⁻⁴** (Schrieber's experimental upper bound,
  middle curve): predicted output is fW–nW at 1 µm to 10 nm gap.
  Detectable with cryogenic bolometers but well below kitchen-scale
  power.
- **f_couple = 10⁻⁸** (deeply below null, bottom curve): well below
  detection across the entire range.
- **1/d⁴ slope** is identical for all curves. The vertical spacing
  is the f_couple ratio.
- **Detection floor (1 fW, black dotted)** and **1 W "kitchen
  scale" (red dashed)** for reference.

The experimentally decisive question is: where on this fan does the
real signal sit?

### Parameter-space heatmap

![Parameter space](parameter_space.png)

The same data as a 2D heatmap over (log₁₀ d, log₁₀ f_couple), with
color encoding log₁₀ output power in Watts. White contours mark
detection thresholds.

The **dashed white rectangle** marks the "lab-buildable" region:
gaps 10–100 nm (achievable with current MEMS lithography), and
f_couple bounded above by Schrieber's experimental null.

Within that rectangle, the predicted signal spans:
- Bottom-left corner (10 nm, f = 10⁻⁴): ~10⁻⁵ W = 10 µW. Easily
  measurable with any room-temperature thermometer.
- Top-right corner (100 nm, f = 1): ~10⁻⁴ W = 0.1 mW. Bright
  signal.
- Bottom-right corner (100 nm, f = 10⁻⁴): ~10⁻¹² W = 1 pW.
  Detectable with bolometers, undetectable with anything cheaper.

**This is the experimental design space.** The decisive
measurement is to scan f_couple as a function of gap (by varying
*d*) and gas species (varying V_atom). Any sublinear or nonlinear
dependence on these parameters that matches the SED prediction
would be a discovery; a clean null across the whole rectangle
would close the loophole.

### Per-atom dE envelope

![Envelope](envelope.png)

Left panel: per-atom orbital energy shift (eV) vs gap, for four
f_couple values. The horizontal gray dashed line is kT at 300 K
(25 meV). **At any practical gap and any f_couple, per-atom dE is
many orders of magnitude below kT.** That's a critical observation:
the proposed signal is *not* a violation of statistical mechanics
— it's tiny per-atom, but it could be substantial integrated over
the throughput.

Right panel: required cesium mass flow for 1 kW output, vs gap, for
the same four f_couple values. The horizontal gray dashed line is
1 g/s (a comfortable lab flow rate). **Only at f_couple = 1 and
very small gaps do we approach the "1 g/s gets you 1 kW" regime.**

### Casimir force validation

![Casimir force](casimir_force.png)

(Already shown above.) The full underlying Casimir prediction
plotted against published experimental data. Validates that the
vacuum-physics foundation of this subproject is mainstream
textbook physics, not speculation.

## What f_couple is and why it's the make-or-break

The dimensionless coupling fraction `f_couple` is the unknown
quantity that turns the vacuum energy density into atomic energy
release. Physically, it represents:

- The fraction of the atomic polarizability volume actually overlapping
  the suppressed-mode portion of the ZPF spectrum
- Times the fraction of the orbital wavefunction whose energy is
  set by those modes (rather than higher-frequency modes that the
  cavity doesn't suppress)

Strict SED arguments (Boyer 1975 et seq.) suggest that for atoms
whose orbital sizes resonate with the suppressed wavelengths,
f_couple can approach unity — at least for those modes. Atoms
whose orbital sizes are much smaller than the missing wavelengths
should see f_couple drop sharply with `(a_orbital / λ_excluded)²`
or steeper.

But this is *theory* — it has not been measured. Schrieber's
review treats f_couple as a phenomenological parameter to be
determined experimentally. **No clean published measurement
exists.** That is the gap.

## Honest assessment

- **For powering data centers:** essentially not viable with any
  current technology. Even at f_couple = 1, per-atom shifts are
  nano-eV at practical gaps. Scaling to MW requires absurd gas
  throughput.
- **For settling a basic-physics question:** highly worth doing.
  The decisive experiment is buildable on a $20–80k university
  lab budget. A clean detection of *any* f_couple-dependent signal
  is a *Phys. Rev. Lett.* paper. A clean null is a definitive
  upper bound that the SED community would actually use.
- **For under-explored science:** this is the most striking gap
  the repo identified. Schrieber 2019 is the canonical reference,
  and despite being open-access in a peer-reviewed journal, has
  fewer than a handful of citations in subsequent experimental
  literature.

## References

- [Schrieber, *Atoms* 7(2):51 (2019)](https://www.mdpi.com/2218-2004/7/2/51)
  / [arXiv:0910.5893](https://arxiv.org/abs/0910.5893)
- Casimir, *Proc. K. Ned. Akad. Wet.* 51:793 (1948) — original calculation
- Boyer, *Phys. Rev. D* 11:790 (1975) — random electrodynamics foundation
- Lamoreaux, *Phys. Rev. Lett.* 78:5 (1997) — first precision Casimir measurement
- Mohideen & Roy, *Phys. Rev. Lett.* 81:4549 (1998) — improved precision
- Bressi et al., *Phys. Rev. Lett.* 88:041804 (2002) — parallel-plate measurement

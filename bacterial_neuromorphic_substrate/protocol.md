# Wet-lab protocol — bacterial neuromorphic chip

End-to-end procedure to build and test a **1024 × 1024 Geobacter-nanowire memristor array** on a CMOS readout chip. Sized to fit a graduate student + postdoc team in a 12-month project, with shared access to a cleanroom and a bioreactor.

## Goal

Demonstrate a fully-functional 256×256 attention-head equivalent on hybrid Geobacter-CMOS hardware, with measured energy per spike matching the engineered target of ≤1 pJ/spike at biological-class voltage (70–130 mV).

## Bill of materials

See [`bom.csv`](bom.csv). **NRE cost ≈ $750 k** including custom CMOS tape-out; per-chip cost after the first ≈ $3,500. With shared facility access, NRE drops to ~$300 k.

## Procedure

### Phase 1: Bioreactor culture (weeks 1–4)

1. Obtain *Geobacter sulfurreducens* PCA strain from ATCC (15944) or DSMZ.
2. Inoculate 1-L jacketed fermenter with 100 mL starter culture in defined freshwater medium with 20 mM acetate + 40 mM fumarate. Maintain 80% N₂ / 20% CO₂ atmosphere at 30 °C, pH 6.8.
3. Grow for 4-7 days until OD₆₀₀ reaches ~0.4 (mid-log phase).
4. Harvest by centrifugation (4000 g × 15 min, 4 °C).
5. Resuspend pellet in 50 mL low-ionic-strength buffer (10 mM ammonium acetate).

**Expected yield:** ~3 mg dry pilus mass per liter culture.

### Phase 2: Nanowire extraction (weeks 4-6)

6. Blend resuspended cells at 10,000 rpm × 2 min (Waring blender on low) to shear pili off the cell surface.
7. Differential centrifugation: 16,000 g × 30 min removes cells; transfer supernatant (now contains free pili).
8. Buffer-exchange supernatant via 10-kDa MWCO Amicon centrifugal filter into device-deposition buffer.
9. Concentrate to 0.1–1 mg/mL via Amicon centrifuge filter.
10. Characterize: TEM (FEI Tecnai or equivalent) for pilus diameter/length distribution; UV-vis 280 nm for protein concentration.

**Acceptance criteria:** > 90% of detected fibers are 3 ± 1 nm diameter, > 5 µm long. Protein concentration ≥ 0.1 mg/mL.

### Phase 3: CMOS chip preparation (weeks 4-8, parallel with phases 1-2)

11. Custom CMOS readout chip (TSMC 180 nm or equivalent) — tape-out and packaging into open-cavity CFP-256.
12. Inspect chip top-metal layer for cleanliness (visual + AFM if available).
13. Plasma-treat (O₂ plasma, 5 min, 100 W) to enhance nanowire adhesion to the top metal.

### Phase 4: Hybrid assembly (weeks 8-10)

14. **Drop-cast deposition:** apply 1 µL of nanowire suspension (0.5 mg/mL) onto the chip active area (5 × 5 mm). Air-dry for 30 min in low-humidity (< 30% RH) environment.
15. **Top electrode:** thermal evaporation of 100 nm Ag through a shadow mask matched to the chip's column-line pattern.
16. **Passivation:** atomic layer deposition of 20 nm Al₂O₃ at 100 °C (Veeco Savannah or equivalent).
17. **Encapsulation:** glass window cover with edge seal under dry N₂.

### Phase 5: Electrical characterization (weeks 10-12)

18. **Yield assay:** sweep voltage 0 → 200 mV across each (row, col) pair and record set events. Acceptance criterion: ≥ 30% of devices show clean switching in the 70–130 mV range.
19. **Energy measurement:** at 100 mV write voltage, integrate I·V·dt during the switching event. Compare to Fu 2020 published 0.3–100 pJ range.
20. **Endurance test:** 10⁴ set/reset cycles on a sample of 100 devices. Track resistance ratio drift.
21. **Retention test:** measure resistance state immediately after set, then 24 h later in storage at 25 °C / 35 % RH. Tolerance ≤ 10× drift.

### Phase 6: SNN workload (weeks 12-16)

22. Load a 256×256 attention-head weight matrix into the cross-bar via state-machine writes.
23. Drive the array with a representative input sequence (e.g., a tokenized sentence in 8-bit quantized form).
24. Measure: per-token energy, throughput, output correctness vs reference silicon implementation.

**Decision point:**
- If per-token energy ≤ 1 mJ AND output matches silicon reference within 5% → **success.** Move to scale-up planning.
- If per-token energy is in 1–10 mJ range → partial success; identify dominant loss term and engineer.
- If per-token energy > 10 mJ → reassess; capacitance reduction did not deliver expected gain.

## Where to publish

- *Nature Electronics* or *Nature Communications* for the hybrid-chip-class result
- *IEEE TED* or *IEEE J-EDS* for the detailed device-physics characterization
- *NeurIPS / ICLR* for the application-level "SNN-on-Geobacter-runs-a-transformer-block" demonstration
- arXiv preprint regardless

## Honest expectations

The protocol has been engineered for a 12-month timeline, but in practice:
- Phase 1 timing depends on the lab's existing experience with anaerobic culture (add 4 weeks if first-time)
- Phase 3 CMOS tape-out has a 4-month minimum lead time from design
- Phase 6 is where the project either fails fast or succeeds — it is the integration test

A reasonable best-case demonstration timeline from project start is 14-16 months. A successful Phase-6 measurement is *Nature-tier* publishable in either direction:
- **Positive result:** confirms the substrate works at scale
- **Negative result:** quantitatively bounds where the engineering reality differs from the theoretical prediction, and that bound is itself publishable

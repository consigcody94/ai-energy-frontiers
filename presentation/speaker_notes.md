# AI Energy Frontiers — Speaker Notes

Pacing target: ~2–3 minutes per slide for a 45–60 minute talk.

---

## Slide 1 — Title (1 min)

Open by anchoring the talk. Something like:

> "Tonight I want to walk you through four bets — four physics bets — on what could close the AI electricity gap. They're not Silicon Valley bets, they're not nuclear lobby bets. They're under-explored physics from four different fields, and they're all real enough to ship code, simulations, and engineering plans for. The whole thing is on GitHub, MIT-licensed. Let me show you."

Pause. Click to next slide.

---

## Slide 2 — The 950 TWh problem (2 min)

This is the framing. Don't rush it.

> "The IEA's most recent forecast says global data-center electricity demand is going to roughly double by 2030 — from 485 TWh today to about 950 TWh. That's the entire annual electricity consumption of Japan. Just for our data centers. Just by 2030. And it's growing 30% per year on the AI side, four times faster than the rest of the grid."

> "The grid build-out is not on pace. Everyone in this room is using something built on this — and there is a real question about whether we have the wattage to keep building."

Move on. Don't dwell on doom.

---

## Slide 3 — Two attack vectors (2 min)

> "There are two ways to close this gap, and most people only ever talk about one."

> "Supply-side: generate more energy. Build more solar. Build more nuclear. We're doing it. Probably not fast enough."

> "Demand-side: use less per inference. Change the substrate the AI is running on. This is the lever that hardly anyone is talking about and that we're going to spend the back half of this talk on."

> "I have three supply-side bets and one demand-side bet. All four ship as working physics simulations, calibrated to peer-reviewed papers, with real engineering designs and real bills of materials. Let me walk you through them."

---

## Slide 4 — Map of four approaches (2 min)

Quick tour. Don't go deep — just the names and the headline number.

> "Number one: thermoradiative diodes — the cold night sky as a heat sink. Buildable today. Recovers about 0.3% of facility load with current devices."

> "Number two: stochastic-electrodynamics Casimir-cavity zero-point energy. Long-shot basic physics. The decisive experiment costs about $200k."

> "Number three: bhasma-prepared cold-fusion cathodes. Cross-disciplinary — Sanskrit alchemical metallurgy meets the cold-fusion field that just got rehabilitated in *Nature* last year. Predicts a 5× boost over the UBC baseline."

> "Number four: bacterial neuromorphic compute. Bacteria grow protein nanowires; you use them as the active element in AI compute. The energy advantage is up to 500× per inference. This one is on the demand side."

> "We'll do them in order."

---

## Slide 5 — TR diodes physics (2 min)

> "Photovoltaic cells absorb photons from the sun and pump electrons. Thermoradiative diodes do the exact opposite: they sit at a hot temperature, like a data-center exhaust duct, and they emit photons toward the cold sky."

> "Through the 8–13 micrometer atmospheric window, the night sky is effectively looking out at 3 Kelvin — deep space. That's a huge temperature differential, and if you build a semiconductor diode that's tuned to those wavelengths, the photon flow pumps a current."

> "The 2024 record for this kind of device is 350 milliwatts per square meter. That's our calibration anchor. We took that number, took the physics, and re-ran it against real hourly weather data at six actual hyperscale data-center locations."

(Pointing to image on right) "And this is what the engineered panel looks like."

---

## Slide 6 — Six cities (2 min)

> "Open-Meteo has a free API that gives you the ERA5 atmospheric reanalysis — real measured weather, hour by hour, going back decades. We pulled a full year of 2024 for six cities: Phoenix, Northern Virginia, Dublin, Frankfurt, Atacama, and Singapore."

> "Every site except one delivers between 167 and 177 megawatt-hours per year on a 100,000 square meter roof. The exception is Singapore, at 115. Tropical humidity raises the sky's effective temperature and closes the radiative window."

> "Practical implication: deploy first in arid clear-sky climates. The Atacama in Chile, the US Southwest, the Middle East. Tropical sites are last-priority."

---

## Slide 7 — The $8k pilot (1.5 min)

> "Here's the punchline for this subproject. To validate everything in the model, you need ten panels installed and instrumented on an actual roof, with a real source-measure unit logging the I-V curve. The bill of materials adds up to about $8,000. One corporate skunkworks Friday afternoon."

> "What that pilot tells you is the real device efficiency in field conditions, the failure modes the model misses, and the cost trajectory at scale. If MCT photodiode arrays drop in price by 10×, which they will because thermal imaging is mass-producing them, this becomes a real bolt-on for any hyperscaler."

---

## Slide 8 — Casimir effect introduction (2 min)

> "Now the long shot. Hendrik Casimir in 1948 showed that if you take two parallel conducting plates and put them at separation *d* in vacuum, they attract each other. The reason: the vacuum modes longer than 2*d* can't fit in the cavity, so the cavity has less vacuum energy than the same volume in open space. Nature pushes the plates together to minimize that energy difference."

> "This is experimentally verified to one percent across four precision measurements between 1997 and 2007 — the plot on the right shows them. **This part is not speculative**. The Casimir effect is mainstream textbook physics."

> "In 2019, a physicist named Gerhardt Schrieber wrote a paper reviewing three possible ways to extract energy from this vacuum-mode structure. Two of them violate the second law of thermodynamics. **One doesn't appear to**. And almost nobody has followed up on it."

---

## Slide 9 — Casimir decisive experiment (2 min)

> "Schrieber's loophole: pump a flow of gas atoms through a Casimir cavity. In the stochastic-electrodynamics interpretation, the gas atoms' electron orbitals shift to lower energies because the long-wavelength zero-point field modes that normally support them are excluded from the cavity. Each atom releases that energy on entering, then re-fills its orbital from the universe's free-space vacuum field on the way out."

> "It's not a perpetual motion machine. The energy comes from the universe's vacuum reservoir."

> "Here's what's striking: the experiment to test this — to either detect a clear signal or definitively close the loophole — costs about $200,000 with shared dilution-fridge access. Six months of measurement. Either outcome is a *Physical Review Letters* paper. And almost no peer-reviewed work has touched it since 2019. **That's the gap.**"

---

## Slide 10 — LENR rehabilitated (2 min)

> "Cold fusion. Most of you know it as the Pons and Fleischmann fiasco from 1989. Everybody got it wrong. The field has been a quiet backwater for thirty years."

> "Last August — *Nature*, volume 644, pages 640 to 645 — researchers at the University of British Columbia, the Thunderbird Reactor team, published a clean result: when you electrochemically load deuterium into a palladium foil and bombard it with deuterium ions, the fusion rate goes up 15% over an unloaded foil. **Neutron signatures. Not calorimetry. Real fusion.**"

> "This is the first *Nature*-tier validation of electrochemical enhancement of cold fusion. ARPA-E is now funding $10M across eight LENR projects. The taboo is breaking."

---

## Slide 11 — Rasashastra angle (2.5 min)

This is the slide for your community audience — bridge the technical to the heritage knowledge.

> "Here's the cross-disciplinary thesis. *Rasashastra* — the Sanskrit \"science of mercury\" — is the classical Indian alchemical tradition. Twelve hundred years of texts describing how to take metals and produce something called *bhasma*. Repeatedly calcined, repeatedly purified, with mercury amalgamation as the deepest preparation."

> "Modern peer-reviewed materials science — XRD, TEM imaging, BET surface area — confirms that classical bhasma preparations are nanoparticulate metals. *Tamra bhasma* is sub-100 nm copper. *Jasada bhasma* is non-stoichiometric nanoscale zinc oxide. **This is real, peer-reviewed, modern-technique-confirmed nanoparticle chemistry.**"

> "Nobody — and I have searched — has tried using Pd-bhasma as a cathode in a UBC-style LENR apparatus. The thesis is simple: bulk palladium maxes out at D/Pd loading of about 0.70 because of phase-boundary stress. Sub-100 nanometer particles can stably hold 0.85 to 0.95. And there are roughly 300 times more grain-boundary surface area per unit mass. Both of those things should help LENR enhancement, if any of the theoretical mechanisms in the field are right."

---

## Slide 12 — The three-way bake-off (2 min)

> "Here's the experimental design. Three cathodes, same UBC apparatus."

> "Cathode A: classical Pd-bhasma. 60 puta cycles, optional mercury amalgamation. Cathode B: commercial nano-Pd at matched BET surface area — that's the critical control for \"is it just surface area?\" Cathode C: commercial Pd foil, reproduces the UBC baseline."

> "If A beats B significantly, then rasashastra-specific factors — the organic-acid bhavana step, the mercury template, the specific defect structure produced by the puta cycle — matter beyond raw surface area. That would be a *Nature*-tier finding. Twelve weeks. Eighty thousand dollars with shared facility access. **Graduate student project.**"

---

## Slide 13 — Bacterial substrate (2 min)

Bridge to the demand-side play. Slow down here — this is the biggest claim.

> "Silicon hit a wall. CMOS gates can't drop below about 0.6 volts because of exponentially-growing leakage current. And memory access dominates everything — the famous \"memory wall.\" Even with all the AI accelerator improvements, an H100 spends about 50 picojoules per useful FLOP at the system level. Multiply that by a 100-billion-FLOP forward pass and you get about 7 joules per token of inference."

> "*Geobacter sulfurreducens* is a soil bacterium. It grows electrically conductive protein nanowires — pili — as part of its metabolism. In 2020, the Lovley and Yao labs at UMass Amherst harvested those pili and used them as the active element in memristors that operate at 70 to 130 millivolts and 0.3 to 100 picojoules per switching event."

> "**Biological voltage. Biological energy. First non-biological substrate to hit those numbers.** That's what's on the right — the physical chip design."

---

## Slide 14 — The 500× lever (2 min)

> "Here's the energy comparison across substrates for a LLaMA-70B token. H100 silicon: 7 joules. Today's Geobacter demo: 1.4 joules — actually slightly worse than silicon today. Loihi-2 silicon neuromorphic from Intel: 320 millijoules. The engineered Geobacter target with sub-femtofarad capacitance scaling: 14 millijoules. And the biological brain floor: 1.4 millijoules per equivalent token of compute."

> "The number that matters: the engineered Geobacter target is **500 times lower energy** than silicon for the same inference. That's not a 10% improvement. That's not a 2× speedup. **That's a 500× lever.**"

---

## Slide 15 — The grid picture (1.5 min)

> "If the engineered Geobacter neuromorphic substrate works at scale, this is what global AI inference electricity demand in 2030 looks like by substrate."

> "Silicon path: 1,100 terawatt-hours. That's above the entire IEA forecast for all data center electricity. Engineered target: 2.2 terawatt-hours. It's off the chart, downward. **It takes the AI energy problem off the global grid entirely.**"

> "That's the lever. That's why this one is worth all four subprojects' worth of attention even though it's the most engineering-uncertain."

---

## Slide 16 — Comparison plot (1.5 min)

> "Here's the full picture — four approaches, three milestones each. Today, five-year horizon, theoretical ceiling. The bars are annual megawatt-hours delivered to a 5-megawatt data center, log scale. Red dashed line is the data center's total annual load."

> "Look at the orange bar — bacterial neuromorphic. At the ceiling milestone it doesn't just contribute; it eliminates more than the data center even consumes, because it's a demand-side reduction. The three supply-side bars combined never reach the load line. The demand-side bar exceeds it by orders of magnitude."

> "**This is the picture that says: one of these is the actual lever and three of them are buying time.**"

---

## Slide 17 — What's already built (1.5 min)

> "Everything you've seen so far is already in code. Four subprojects. 62 physics validation tests, all passing. 50 engineering stress tests across wind, hail, thermal, vacuum, magnetic, radiation safety — zero FAIL items. Every subproject ships with a working simulator, a validation suite, the physical design document, a bill of materials with vendor part numbers, a schematic generator, a wet-lab protocol, and the engineering-validation test."

> "It's all open source. MIT license. github.com/consigcody94/ai-energy-frontiers. Pull request welcome. Fork it. Fix it. **Prove it wrong.**"

---

## Slide 18 — Honest assessment (2 min)

This is the credibility-builder slide. Be slow and specific.

> "Three columns for each approach: what's true, what's hypothesis, what's unknown."

> "TR diodes. *True*: Planck physics, the 350 mW/m² record, the atmospheric window. *Hypothesis*: device efficiency improves 10–20× in five years. *Unknown*: capital cost trajectory of MCT arrays at scale."

> "SED Casimir. *True*: Casimir effect verified to 1%, Schrieber's thermodynamic argument. *Hypothesis*: the SED interpretation of atomic ground states. *Unknown*: the coupling fraction has never been measured."

> "Bhasma LENR. *True*: UBC 2025, bhasma nano-particles confirmed. *Hypothesis*: the cross-disciplinary connection, the model coefficients. *Unknown*: does bhasma-prep actually beat commercial nano-Pd."

> "Bacterial neuromorphic. *True*: Geobacter pilus memristors at biological voltage. *Hypothesis*: sub-femtofarad capacitance scaling gives the 500× advantage. *Unknown*: 8 to 9 orders of magnitude of integration scaling."

> "**No claim is bigger than its evidence.** Every hypothesis is labeled."

---

## Slide 19 — Roadmap (2 min)

> "Three time horizons. Near-term, one year: TR diode 10-panel pilot. Bhasma-Pd cathode preparation and characterization. The first real-deployment measurements."

> "Mid-term, 2 to 5 years: the bhasma three-way cathode test. The SED Casimir cavity experiment — *PRL-tier result either way*. A Loihi-2-equivalent SNN running on Geobacter neurons."

> "Long-term, 5 to 10 years: MCT photodiode cost reduction makes TR diodes economic at hyperscale. If LENR scales, net-positive bhasma reactor. Hybrid Geobacter-CMOS at transformer-block scale."

> "These don't have to win in order. Different funding levers for different phases — skunkworks for near-term, grants for mid-term, seed and Series A for long-term. **Multiple shots on goal.**"

---

## Slide 20 — Why this matters (2 min)

This is the close. Slow down. Let it land.

> "AI's energy problem isn't just engineering. **It's a question about what physics we have ignored.**"

> "The cold sky is a heat sink we don't use. The vacuum has a thermodynamic loophole nobody followed up. Ancient metallurgy may have already solved the LENR cathode problem. And bacteria grow the lowest-energy compute substrate known."

> "These are all real. They're all peer-reviewed. They're all under-explored. And they're all sitting there waiting for someone to take them seriously."

---

## Slide 21 — Q&A (2 min open, then 10-15 min discussion)

> "Take this and run with it. The repo is at github.com/consigcody94/ai-energy-frontiers — MIT licensed, four subprojects, 112 tests passing, real BOMs, real protocols. If any of you want to talk about a specific one, I'm here for the rest of the evening."

> "Questions?"

---

## After-talk: anticipated questions

**Q: "How is bacterial neuromorphic different from Loihi-2 silicon neuromorphic?"**
A: Loihi-2 is silicon at 23 pJ/spike — already 10× better than H100 dense compute. Bacterial neuromorphic at biological voltage is another 23× lower energy because of V² scaling. The Loihi-2 path is real and shipping; bacterial is the next floor below it.

**Q: "Has anyone replicated the UBC LENR result yet?"**
A: Multiple groups are working on it under ARPA-E funding (LBNL + UC Davis are public; others are quiet). Independent replication is the open question; the Nature paper is one data point.

**Q: "Why don't hyperscalers fund this themselves?"**
A: They do fund some — Microsoft has SMR nuclear deals, Google has fusion equity. But these are 10-year capex bets. The skunkworks-scale work I'm describing falls below the procurement threshold for big tech and above the grant threshold for academia. That's the gap this repo lives in.

**Q: "What's your background?"**
A: [Customize — your spiritual community knows you as Os Lamia. Your tech community knows you as Cody. Both audiences should hear you say "I'm not a credentialed physicist — I'm a researcher who can read the papers and write the simulations. The repo is open; the math is auditable. The point isn't to trust me; it's to give other people the starting point they need to build."]

**Q: "Is this dual-use? Could it weaponize?"**
A: LENR neutron rates are research-scale, way below weapons-relevant. TR diodes are passive. SED Casimir at proof-of-concept scale is harmless. Bacterial neuromorphic is just compute. None of these are export-controlled or proliferation-sensitive at the scale we're talking about.

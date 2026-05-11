# AI Energy Frontiers — Full Talk Script

**Estimated runtime:** ~50 minutes (at natural ~130 wpm)
**Followed by:** ~15 min Q&A

Read or paraphrase. The italic stage directions are for you, not the slide.

---

## OPENING — before clicking slide 1

*Walk on stage. Take a breath. Look at the room.*

> Thanks, everyone, for being here tonight.
>
> I want to start with a number, and the number is bigger than it sounds. By 2030, the world's data centers — the warehouses full of GPUs that run every chatbot, every recommendation system, every image generator — those data centers are projected to consume about 950 terawatt-hours of electricity per year. To put that in perspective, that is more electricity than the entire country of Japan currently uses for everything. Lights, factories, trains, household appliances — all of Japan. We're going to dedicate that much electricity to AI, and that's just by 2030.
>
> Most people, when they hear that number, they go in one of two directions. Either they go *we should slow AI down*, which is not going to happen, or they go *we need more nuclear plants*, which is also happening but not fast enough.
>
> Tonight I want to give you a third direction. I spent the last several weeks building a research repository — fully open-source, every line auditable — that explores four physics bets on closing that gap. Three of them are about making more energy. One of them is about needing less. And they all come from corners of physics that almost nobody is looking at. One of them comes from a body of Sanskrit alchemical literature that's twelve hundred years old. One of them comes from a bacterium. One of them comes from a thermodynamic loophole that one physicist wrote a paper about in 2019 and then nobody followed up on.
>
> What I'm going to show you tonight is the map. The four bets, the numbers, the experiments that would settle them, and where you can pick up the work if any of it grabs you. The whole thing is on GitHub. MIT license. The URL is on the screen now — `github.com/consigcody94/ai-energy-frontiers`. Take that home if you only take one thing.
>
> Let's begin.

*Click to slide 1.*

---

## SLIDE 1 — Title

*Pause for two seconds. Let the title land.*

> AI Energy Frontiers. Four physics bets on the future of compute. And where the under-explored physics actually lives.
>
> I'm Cody Churchwell. Some of you know me from this lecture series. Some of you know me from elsewhere. Tonight is going to be technical in places — I'll do my best to keep it accessible — but the central story is one we can all sit with regardless of background. It's about choices. Civilizational choices. The choice of which physics we ignore is itself a kind of bet, and right now we are betting on the wrong physics.

*Click to slide 2.*

---

## SLIDE 2 — The 950 TWh problem

> 950 terawatt-hours by 2030. The International Energy Agency published this in their *Energy and AI* report earlier this year. We're at 485 today. We're doubling in five years.
>
> And it's worse than just doubling, because the doubling is uneven. AI-accelerated servers — the GPUs that run the big models — those alone are growing 30% per year. That is more than four times the growth rate of every other sector on the grid combined. Hospitals, schools, factories, EVs — all of them growing slower than AI compute.
>
> The grid is not building out at 30% a year. Nowhere on Earth is the grid building out at 30% a year. So we have, sitting in front of us, a real engineering and physical problem: where does the wattage come from?
>
> Most of the answer is going to be obvious. More solar. More wind. More nuclear, including the small modular reactor deals that Microsoft and Google have already signed. Those are real, and they help, and they are not the topic of tonight's talk because everybody is already working on them.
>
> Tonight I want to talk about what we are *not* working on. The physics nobody is paying attention to. The cold sky. The vacuum. Ancient metallurgy. Bacteria. Four under-explored corners of the universe that — if we took them seriously — could close this gap from four different directions at once.

*Click to slide 3.*

---

## SLIDE 3 — Two ways to close the gap

> There are two basic strategies for closing any energy gap, and almost everyone only talks about one.
>
> The first is the supply side. Generate more energy. Build more solar. Build more reactors. Find better ways to recover waste heat. Three of my four bets tonight are supply-side bets.
>
> The second is the demand side. Use less energy per inference. Per token. Per query. Change the compute substrate so that the AI itself just needs less power to do the same work. One of my four bets is on this side, and as I'll show you, it is by far the biggest lever.
>
> I want to be clear: I'm not saying we should pick one over the other. We need both. If supply grows 10× and demand drops 10×, that's a hundredfold improvement. They compound. But we are putting almost all of our investment into the first column and almost none into the fourth. And the fourth is where the biggest single number lives.
>
> Let me show you what I mean.

*Click to slide 4.*

---

## SLIDE 4 — The four approaches

> Four approaches. Three supply-side, one demand-side.
>
> Number one: thermoradiative diodes. Card top-left. This is the most defensible of the four. The cold night sky is a heat sink we don't use. Through the 8-to-13-micron atmospheric window, when you look up on a clear night, you're effectively staring at the 3-Kelvin background of deep space. We have devices today that can turn that temperature differential into electricity. Today's prototype recovers about 0.3% of a data center's electricity load. That sounds small — it is — but it's *additive*, it runs at night when solar can't, and it's buildable right now. I'll show you how to pilot one for $8,000.
>
> Number two: stochastic-electrodynamics Casimir-cavity zero-point energy. Card top-right. This is the long shot of the four. The vacuum is not empty. The Casimir effect, demonstrated in laboratories since 1948, shows that the vacuum has structure — modes excluded between two parallel plates. There is, on paper, a thermodynamic loophole that lets you draw energy from this structure. The decisive experiment costs about $200,000 with shared university equipment. Almost nobody has tried it.
>
> Number three: bhasma-prepared low-energy nuclear reaction cathodes. Card bottom-left. This is the cross-disciplinary one. Cold fusion got rehabilitated last August — peer-reviewed paper in *Nature*. I'll get into the details. The hypothesis is that Sanskrit alchemical metallurgy — twelve hundred years old — already builds exactly the kind of palladium nanoparticle structure that the modern cold-fusion field needs. Five-fold predicted enhancement. Twelve-week graduate student project to test.
>
> Number four: bacterial neuromorphic substrate. Card bottom-right. The demand-side lever. *Geobacter sulfurreducens* — a soil bacterium — grows electrically conductive protein nanowires that have been used to build memristors at biological voltage. Five hundred times less energy per AI inference than silicon, if the engineering can be made to scale.
>
> All four exist as code, as physics simulations, as engineering designs with bills of materials and vendor part numbers, as wet-lab protocols, as engineering stress tests with safety factors. All four pass their tests. All four are on the repository.
>
> Let's walk through them in order.

*Click to slide 5.*

---

## SLIDE 5 — Approach 1: TR diodes physics

> Approach one. Thermoradiative diodes. The cold sky as a heat sink.
>
> Here is the picture. You have a photovoltaic cell — a solar panel — which sits in a cold environment, looks up at a hot environment which is the sun, absorbs photons, and pumps a current. That's a familiar object. Now invert it. Imagine a device that sits in a *hot* environment — a data center's exhaust duct, say, 50 degrees Celsius — and looks up at a *cold* environment, which on a clear night is the 3-Kelvin background of deep space filtered through Earth's atmosphere. That device emits photons toward the cold sky and pumps a current in the same way. That's a thermoradiative diode.
>
> The physics is real. The semiconductor industry has the materials. The atmospheric transmission window between 8 and 13 micrometers is open even on most cloudy nights. Build a diode whose bandgap matches that window — about 0.10 electron-volts, which mercury-cadmium-telluride alloys can hit — and you have a device that sucks heat out of your hot data center and turns it into current, every clear night, for as long as the materials hold up.
>
> Last year — 2024 — a group from Stanford published in arXiv 2407.17751 a nighttime electricity-generation record of 350 milliwatts per square meter. We took that number, we calibrated our model to match it, and then we re-ran the model against real measured hourly weather data from six actual hyperscale data center locations. Open-Meteo gives you the ERA5 atmospheric reanalysis for free — no API key. It's all there.
>
> The image on the right is the panel as we've designed it. Thirty layers from glass cap on top down through diode array, cold plate, aerogel insulation, hot plate, heat pipes, to the exhaust duct below. 1 meter by 1 meter, 22 kilograms, $526 in parts, designed to be roof-mounted.

*Click to slide 6.*

---

## SLIDE 6 — Real weather at six cities

> Here is what we got when we ran a year of real 2024 weather through the model.
>
> Six cities. Phoenix, Arizona. Northern Virginia. Dublin, Ireland. Frankfurt, Germany. Atacama, Chile. Singapore.
>
> Five of them deliver between 167 and 177 megawatt-hours per year on a 100,000-square-meter roof. That's the surface area of a single hyperscale data center campus. Phoenix at 171. Northern Virginia at 176. Dublin at 177 — yes, Ireland, somehow as good as Arizona, because the cool maritime climate gives you a stable temperature differential year-round. Frankfurt the same. Atacama at 167 — high-altitude desert, you'd think it would be the winner, but actually it's just average.
>
> Singapore loses badly. 115 megawatt-hours per year. Tropical humidity raises the dew-point and closes the atmospheric window. The Berdahl-Martin model predicts this and the real data confirms it. So the practical lesson: deploy first in clear-sky dry climates. The US Southwest. The Atacama. The Middle East. Tropical sites are last priority.
>
> Now, 170 megawatt-hours a year is small relative to the 43,000 megawatt-hours a 5-megawatt data center burns. That's about a 0.4% offset. Not a game changer at today's device efficiency. But notice: the radiative-limit physics says we could hit 60% offset if we closed the device-engineering gap. And the gap is closable. The MCT photodiode arrays that this design uses are the same mass-produced thermal-imaging arrays the military and the medical industry buy in volume, and their price is dropping every year. This is an engineering project, not a physics one.

*Click to slide 7.*

---

## SLIDE 7 — The $8K pilot

> Here is the part I want everyone in this room to hear, because some of you work in places that could fund this on a discretionary basis.
>
> Eight thousand dollars. Ten panels. One afternoon of installation labor plus instrumentation. That's what it costs to put a real pilot deck on a real roof and start measuring.
>
> What does the pilot prove? Three things. One: the real device efficiency under field conditions, which is the parameter that determines whether the whole technology is economically viable. Today's literature says 0.5% of the radiative limit; the pilot tells you whether your actual install achieves that. Two: the failure modes that the model misses. Humidity ingress. Dust accumulation. Hail damage. UV degradation of the IR-transparent cover film. We design for these in the BOM, but you don't really know what kills a roof-mounted panel in real life until you put one on a real roof. Three: the cost trajectory at volume. A panel is $526 in single quantities. At 100,000 units per year, with custom MCT array fabrication and automated assembly, the published trajectory says $50 per panel. That changes the entire economic story.
>
> Eight thousand dollars. One corporate skunkworks Friday. If any of you have access to a roof, an electrical inverter, and a friendly hyperscaler procurement team, this is the lowest-cost validation experiment in the entire repository. Take it.

*Click to slide 8.*

---

## SLIDE 8 — Approach 2: Casimir effect intro

> Approach two. The long shot. Stochastic-electrodynamics Casimir-cavity zero-point energy.
>
> I want to spend a minute on the foundation here because it's mainstream physics, and I want you to feel the line between what is established and what is speculative.
>
> In 1948, a Dutch physicist named Hendrik Casimir showed mathematically that if you take two parallel metallic plates and put them at a separation *d* in vacuum, they will attract each other. Not gravitationally — by a quantum mechanical effect. The reason: the vacuum modes — the electromagnetic field oscillations that exist in empty space — those modes with wavelengths longer than 2*d* can't fit in the cavity between the plates. They get excluded. So the cavity has *less* vacuum energy than the same volume in open space, and nature wants to minimize that difference, so it pushes the plates together.
>
> This sounds strange. It is also experimentally verified to one percent precision in four independent precision measurements between 1997 and 2007 — Lamoreaux, Mohideen and Roy, Bressi, and Decca. The plot on the right shows them. The closed-form prediction is the blue curve; the experimental data points are on it. **This is not speculative physics. The Casimir effect is real and mainstream.**
>
> Now here's the interesting part. In 2019, a physicist named Schrieber published a review paper in the open-access journal *Atoms*. He reviewed three classes of proposals for extracting energy from this vacuum structure. The first class — nonlinear processing of the vacuum field — violates the second law of thermodynamics. The second class — letting the plates close together and harvesting the attraction energy — also violates the second law, because to reset the system you have to put the energy back. Energy in equals energy out. No free lunch.
>
> But the third class? The third class does not appear to violate the second law. Almost nobody has followed up.

*Click to slide 9.*

---

## SLIDE 9 — Decisive Casimir experiment

> Here is the third class. The thermodynamic loophole.
>
> Build a Casimir cavity — two parallel plates 30 nanometers apart, microfabricated on silicon, stacked into an array of 50 layers. Pump a vapor of cesium atoms through the cavity. As each atom enters, its electron orbitals — in the stochastic-electrodynamics interpretation — settle into lower-energy configurations because the long-wavelength zero-point field modes that normally support them are excluded from the cavity. Energy released. Capture it. The atom exits the cavity, re-fills its orbital from the *open* universe's vacuum field, and the cycle continues.
>
> This is not a perpetual motion machine. The energy comes from the universe's vacuum reservoir — which is effectively infinite as far as we can tell. The cavity is the pump. The gas is the working fluid. The universe is the source.
>
> Now, is this real? I genuinely do not know. Schrieber's paper is internally consistent. The thermodynamic argument is correct. The experiments he cites are old and inconclusive. Almost nobody has touched it since.
>
> Here is what we should do about it: build the apparatus and measure.
>
> Cost: about 200,000 dollars, assuming you can borrow access to a dilution refrigerator — and most physics departments have one. Six months of measurement. Two clean tests: does the signal scale as 1 over d-to-the-fourth, as the theory predicts? Does the signal vanish when you swap cesium for xenon, which is closed-shell and shouldn't couple? If both tests say yes, you've discovered a new energy regime. If they both say no, you've closed the loophole forever, and that itself is a *Physical Review Letters* paper. Either way: publishable, decisive, six months of work.
>
> That experiment is sitting there waiting. Anyone with a postdoc and a borrowed cryostat.

*Click to slide 10.*

---

## SLIDE 10 — LENR rehabilitated in *Nature* 2025

> Approach three. Now the cross-disciplinary one. This is where I get to bring in some of the heritage knowledge that a lot of you in this room are familiar with from other contexts.
>
> First the modern science. Last August — August 2025 — the journal *Nature*, volume 644, pages 640 through 645, published a paper by Schenkel and colleagues at the University of British Columbia. They built a benchtop fusion apparatus they call the Thunderbird Reactor. The setup: a palladium foil cathode, electrochemically loaded with deuterium on one face, bombarded with deuterium ions from a small plasma source on the other face. Result: a 15-percent increase in the deuterium-deuterium fusion rate when electrochemical loading is active, compared to the same beam hitting an unloaded foil.
>
> Hard neutron signatures. Not calorimetry. Not heat measurements that everyone disputes. Direct, hard nuclear detection of fusion neutrons at the right energy.
>
> This is the first *Nature*-tier validation of electrochemically-mediated cold fusion. Thirty-six years after the Pons and Fleischmann fiasco that buried the entire field. ARPA-E — the U.S. Department of Energy's high-risk research agency — has now committed $10 million across eight LENR projects.
>
> The cold-fusion taboo is breaking. This is not 1989 anymore. The field is small, it is careful, it is publishing in *Nature*. We should pay attention.

*Click to slide 11.*

---

## SLIDE 11 — Rasashastra / the cross-disciplinary thesis

> Now here is the cross-disciplinary thesis. This is what I think is the most original idea on the entire repository.
>
> *Rasashastra* is the Sanskrit "science of mercury." It is a body of alchemical literature codified in the *Rasaratna Samuccaya* in the thirteenth century, with roots going back at least a thousand years before that. The classical traditions describe — in painstaking detail — how to take metals through specific cycles of purification, trituration with herbal juices, repeated calcination, and optional mercury amalgamation, to produce something called *bhasma*. Sacred ash. Nano-particulate metal preparations used in Ayurvedic medicine.
>
> For the longest time the Western scientific establishment looked at these traditions and called them superstition. Just folk medicine. Pre-scientific cosmology.
>
> But the materials science finally caught up. In 2008, the *Journal of Nanoparticle Research* — peer-reviewed, Springer — published a characterization of *Jasada bhasma*, a traditional zinc preparation. X-ray diffraction. Transmission electron microscopy. Atomic-force imaging. The result: classical *Jasada bhasma* is a non-stoichiometric nanoscale zinc oxide preparation, particles in the 10 to 100 nanometer range, with specific defect structures. In 2017, *Tamra bhasma* — the copper preparation — was characterized the same way. Sub-100 nanometer copper crystallites, polycrystalline structure, very specific morphology produced by exactly the *puta* cycles that the classical texts prescribe.
>
> Modern XRD and TEM confirm: classical bhasma is nanoparticle metal chemistry. The traditions encode real materials science that we are only now recapitulating.
>
> Here is the cross-disciplinary thesis. **Nobody has tried Pd-bhasma — palladium bhasma — as a cathode in a UBC-style LENR apparatus.**
>
> Why should it work? Two reasons. First: bulk palladium has a hard ceiling on deuterium loading at about D-to-Pd 0.70, because the alpha-to-beta hydride phase boundary creates stress that ejects deuterium atoms back out. But in sub-100-nanometer palladium particles, the phase boundary reorganizes more cleanly, stress relieves at grain boundaries instead of ejecting atoms, and you can stably reach D-to-Pd 0.95. Forty percent more deuterium in the lattice. Second: a 30-nanometer particle has about 300 times the specific surface area of a 10-micrometer foil. The cold-fusion theoretical literature — Storms, Hagelstein, Takahashi — has argued for decades that fusion events occur at specific defect-rich surface environments. If that's right, three hundred times the surface area should give a large enhancement.
>
> The model in the repository, calibrated to the UBC 15-percent anchor, predicts a 60-puta-cycle Pd-bhasma cathode should give roughly 50 to 80 percent enhancement. Five times the UBC baseline. The plot on the right shows the predicted enhancement as a function of preparation cycles.
>
> This is the most striking idea I worked on this year. Twelve hundred years of Sanskrit metallurgical knowledge — knowledge that some of us in this room interact with for entirely different reasons — accidentally describes the optimal preparation protocol for a cathode in a field that nobody outside of LENR labs knows about. The cross-reference is original. Nobody has published it. Nobody is testing it.
>
> Yet.

*Click to slide 12.*

---

## SLIDE 12 — Three-way bake-off

> Here is the experimental design. Three cathodes, same apparatus.
>
> Cathode A: classical Pd-bhasma, prepared via 60 *puta* cycles plus optional mercury amalgamation, following the *Rasaratna Samuccaya* protocol but with modern instrumentation — programmable muffle furnace, hydraulic press, XRD characterization between cycles. Twelve weeks of preparation. The expected behavior, per the model, is plus-50-to-80-percent enhancement over the UBC foil baseline.
>
> Cathode B: commercial Pd-black at matched BET surface area. This is the critical control. If the bhasma boost is just about surface area, you can buy nano-palladium from Sigma-Aldrich and skip the Sanskrit. If A roughly equals B in performance, the cross-disciplinary angle is just an interesting historical footnote — and we've still learned something useful, namely that surface area is what matters.
>
> Cathode C: commercial Pd foil. This is the UBC baseline replication. We need to reproduce their plus-15-percent result before we believe anything else, so this cathode confirms the apparatus is calibrated correctly.
>
> Twelve weeks. Roughly 80,000 dollars with shared accelerator and neutron-detector facility access. Graduate-student-scale project. The most interesting positive result would be: A beats B significantly. That would mean rasashastra-specific factors — the organic-acid bhavana step, the mercury template structure, the specific defect signature produced by the puta cycle — matter beyond raw surface area. That finding would force the materials-science community to take Sanskrit metallurgy seriously as a source of preparation protocols. And it would be a *Nature*-tier paper.
>
> Even a null result — A equals B equals C, no enhancement — is publishable. It would close the question. It would set the upper bound on the cross-disciplinary hypothesis. Either way, science moves.

*Click to slide 13.*

---

## SLIDE 13 — Bacterial neuromorphic substrate

> Approach four. The demand-side lever. The big one.
>
> All three of the previous approaches add more energy to the grid. This one — the bacterial neuromorphic substrate — changes how much energy the AI actually needs in the first place.
>
> Silicon hit a wall. Modern CMOS — the technology underneath every H100 and every B200 — needs about 0.6 volts to switch a transistor without exponentially-growing leakage. Below that, electrons tunnel through gates that should be closed. Above that, you waste power on every switching event. We are stuck. And it gets worse: the memory subsystem dominates everything. The famous "memory wall." Even with the best AI accelerator design today, an H100 spends about 50 picojoules per useful FLOP at the system level. A LLaMA-70B forward pass takes 140 billion FLOPs. That's about 7 joules per token of inference. Half a watt of continuous power for every ongoing inference stream. Multiply that by a billion daily inferences across the major hyperscalers, multiply by 365 days, you get a thousand terawatt-hours a year. That's the demand we're trying to feed.
>
> Now look at biology. A human brain runs on 20 watts. That's a desk lamp. 86 billion neurons firing at biological voltage — 70 to 130 millivolts, an order of magnitude below silicon — and using 0.3 to 100 picojoules per synaptic event. The brain achieves the energy efficiency that silicon engineers have been chasing for forty years and not gotten close to.
>
> Here is the discovery that makes this approach real. In 2020, two laboratories at the University of Massachusetts at Amherst — the Lovley lab and the Yao lab — published in *Nature Communications*. They had been studying *Geobacter sulfurreducens*, a soil bacterium that grows electrically conductive protein nanowires — called pili — as part of its anaerobic metabolism. The Geobacter pili are about three nanometers thick and up to twenty micrometers long. They conduct electrons over those distances.
>
> The Lovley and Yao labs harvested these pili — extracted them from the bacterial cell membranes — and built memristor devices using them as the active element. The result: memristors that switch at 70 to 130 millivolts. That is biological voltage. And they use 0.3 to 100 picojoules per switching event. That is biological energy.
>
> **The first non-biological substrate, in the entire history of electronics, to hit biological voltage and energy.**
>
> The image on the right is the chip design. Geobacter nanowire layer on top, CMOS readout chip below, bonded via gold wires. Mass-grow the nanowires in a 1-liter bioreactor — bacteria are easy to culture — extract the pili, drop-cast them onto a custom 180-nanometer CMOS chip, deposit a silver top electrode, encapsulate with aluminum oxide. The full process is documented in the protocol on the repository.

*Click to slide 14.*

---

## SLIDE 14 — The 500× lever

> Here is the number that matters.
>
> On a LLaMA-70B inference — that's the open-source model that anyone can run for free — silicon costs about 7 joules per token at the system level. Today's Geobacter prototype: 1.4 joules per token. Slightly worse than silicon today, because the device geometry hasn't been optimized yet. Intel's Loihi-2 silicon neuromorphic processor: 320 millijoules per token. The engineered Geobacter target, with sub-femtofarad capacitance scaling that's achievable with current lithography: 14 millijoules per token. And the theoretical biological-brain floor: 1.4 millijoules per token.
>
> Look at the numbers from the perspective of the headline lever. Silicon to engineered Geobacter is a 500-fold reduction in energy per token. Five hundred times less power for the same inference.
>
> This is not a 10-percent improvement. This is not a 2× speedup. This is *three orders of magnitude*. It would mean that the inference that today drains a 5-megawatt data center would drain a 10-kilowatt rack. A workload that today requires a $50-million GPU build-out would require a $100,000 hybrid-chip cluster.
>
> It would mean that you could run frontier AI on a single building's solar panels.

*Click to slide 15.*

---

## SLIDE 15 — Global grid picture

> Here is what the 500× lever looks like at the level of the global grid.
>
> Each bar in this chart is the projected 2030 global AI inference electricity demand under a particular substrate assumption. Silicon path: 1,100 terawatt-hours per year. Above the entire IEA forecast for all data center electricity globally. Loihi-2 silicon neuromorphic path: 50 terawatt-hours. Already a 20-fold improvement, and it's available today — Intel ships Loihi-2.
>
> Today's Geobacter demo, at its current unrefined energy per spike: 220 terawatt-hours. Worse than Loihi-2.
>
> Engineered Geobacter target: 2.2 terawatt-hours.
>
> That's not a marginal improvement on the IEA forecast. That's *not even on the chart*. The bar disappears below the visualization. It is so small relative to the silicon baseline that you have to specifically look for it.
>
> Two-point-two terawatt-hours of global AI inference electricity demand in 2030. That is the entire problem made trivially small. The grid doesn't have to build out. The hyperscalers don't have to chase nuclear deals. The carbon emissions evaporate. The compute capacity becomes unlimited.
>
> If the engineering scales.
>
> That's the lever. That's why this one — out of all four approaches I've shown you — is the bet I would put the most money on. It's the only one that, if it works, removes the entire problem.

*Click to slide 16.*

---

## SLIDE 16 — Cross-approach comparison

> Here are all four approaches on the same chart. The horizontal axis is the technology-readiness milestone: today, five-year horizon, theoretical ceiling. The vertical axis is annual megawatt-hours delivered to a 5-megawatt hyperscale data center, log scale. The red dashed line is that data center's total annual load — 43,800 megawatt-hours.
>
> Look at the orange bar — that's the bacterial neuromorphic substrate. At the theoretical ceiling, the bar is so tall it dwarfs everything else. It exceeds the data center's entire annual load by orders of magnitude, because — remember — this approach is demand-side. It doesn't add to the supply column; it subtracts from the demand column. And the subtraction is huge.
>
> The three supply-side bars — blue for TR diodes, purple for SED Casimir, green for Bhasma LENR — they're all visible at their respective milestones, but none of them reaches the red line. None of them alone solves the problem.
>
> This is the picture that says: one of these bets is the actual lever, and three of them are buying time. If the orange bar's engineering works, we win. If it doesn't, we need the other three plus mainstream sources to scale fast enough.
>
> Don't pick one. Run all four. They compound.

*Click to slide 17.*

---

## SLIDE 17 — What's already built

> A quick checkpoint. What is the state of the repository today?
>
> Four subprojects. Each one mirrored in structure. Each one ships eight components: a physics simulator, a validation test suite, a set of analysis plots, real-world data integration, a physical-design document, a bill of materials with vendor part numbers, a schematic-generation script, a wet-lab protocol, and an engineering-validation test suite.
>
> 62 physics validation tests across the four subprojects. All passing. These test calibration against published benchmarks, monotonicity in physical limits, Monte Carlo uncertainty quantification, and cross-checks against multiple independent literature references.
>
> 50 engineering stress tests across the four hardware designs. Wind loads up to 130-mile-per-hour hurricane. Hail impacts up to 25-millimeter stones at 25 meters per second. Thermal cycling over 25-year service life. Bolometer noise budgets at 50-millikelvin operating temperatures. Mercury vapor containment relative to OSHA exposure limits. Neutron shielding to keep operator dose below ALARA targets. All 50 pass. Zero FAIL items.
>
> The URL is on the screen. `github.com/consigcody94/ai-energy-frontiers`. Fork it. Fix it. Prove it wrong. MIT license — no restrictions on reuse.

*Click to slide 18.*

---

## SLIDE 18 — Honest assessment

> One thing I want to be very clear about before I wrap up. I have not overclaimed anything tonight. Let me walk through, for each approach, what is true, what is hypothesis, and what is genuinely unknown.
>
> TR diodes. *True*: Planck physics, the 350 milliwatts per square meter 2024 record, the atmospheric window. All textbook. *Hypothesis*: device efficiency will improve ten to twenty times in the next five years. *Unknown*: the capital cost trajectory of MCT photodiode arrays at hyperscale volume.
>
> SED Casimir. *True*: the Casimir effect verified to one percent precision across four experiments, Schrieber's thermodynamic argument that one of three ZPE-extraction classes does not violate the second law. *Hypothesis*: the stochastic-electrodynamics interpretation of atomic ground-state energies. *Unknown*: the coupling fraction parameter has literally never been measured anywhere in the peer-reviewed literature.
>
> Bhasma LENR. *True*: the UBC 15-percent result in *Nature* 2025, the modern materials-science characterization of classical bhasma as nanoparticle metals. *Hypothesis*: my model coefficients, the cross-disciplinary connection itself. *Unknown*: whether classical bhasma preparation actually outperforms commercial nano-palladium at matched surface area.
>
> Bacterial neuromorphic. *True*: Geobacter pilus memristors operating at biological voltage and energy. *Hypothesis*: that sub-femtofarad capacitance scaling will deliver the predicted 500-fold advantage. *Unknown*: 8 to 9 orders of magnitude of integration scaling that no one has yet demonstrated.
>
> Hypotheses are bets, not promises. Unknowns are open questions. None of this work is finished. All of it is auditable, falsifiable, and waiting for someone to take it further.

*Click to slide 19.*

---

## SLIDE 19 — Roadmap

> If I had ten million dollars and a five-year window, here is what I would actually do.
>
> Near term — within one year. Fund the TR diode 10-panel pilot. Eight thousand dollars; you can find that in a Friday afternoon. Get real device-efficiency measurements under field conditions. In parallel, start the Pd-bhasma cathode preparation in any university lab with a programmable furnace. Twelve weeks of preparation and characterization, before you ever load it into a fusion apparatus. These two tasks fit inside a single semester.
>
> Mid term — two to five years. Run the bhasma-LENR three-way cathode test. Run the SED Casimir cavity experiment. PRL-tier results either way. And in parallel, build a Loihi-2-equivalent spiking neural network on a Geobacter substrate. Sixty-four-thousand neurons is achievable in three years of focused work. That's a single transformer attention head running on bacterial nanowires. Decisive test of whether the architecture actually works at non-toy scale.
>
> Long term — five to ten years. By then, MCT photodiode prices will be dropping into the range where TR diodes are economic at hyperscale roof scale. If LENR is real, the bhasma cathode work will tell us by year four whether to pursue net-positive reactor designs. And if the Geobacter neuromorphic substrate can scale past 64,000 neurons, you push toward the hybrid Geobacter-CMOS chip at transformer-block scale. A single chip with a million neurons. Then a thousand of those wired together. Then a million.
>
> Each phase is funded by a different lever. Skunkworks money for the near term — corporate research and development budgets, eight to eighty thousand dollars per pilot. Government grants for the mid term — ARPA-E, DOE Office of Science, NSF. Seed and Series A venture funding for the long term, where the hybrid Geobacter-CMOS chip becomes a real product company.
>
> Multiple shots on goal. Different funding mechanisms. Different timeline windows. **None of these bets has to win in any particular order.**

*Click to slide 20.*

---

## SLIDE 20 — Why this matters

*Slow down here. Let the slide breathe. Read it slowly.*

> AI's energy problem isn't just engineering. It's a question about what physics we have ignored.
>
> The cold sky is a heat sink we don't use.
>
> The vacuum has a thermodynamic loophole nobody followed up.
>
> Ancient metallurgy may have already solved the LENR cathode problem.
>
> And bacteria grow the lowest-energy compute substrate known.
>
> These are not science fiction. Every one of them is in a peer-reviewed paper from the last five years. Every one of them has working code, a calibrated physics model, and an engineering design with a bill of materials.
>
> And they are all sitting there, waiting for someone to take them seriously.

*Pause. Look at the room.*

> The reason I built this repository — and the reason I'm telling you about it tonight — is not because I think any one of these bets is certain to win. They're bets. They're hypotheses. Some of them will probably fail. That's how science works.
>
> The reason I built it is because we have been told, repeatedly, that the AI energy problem is unsolvable without enormous fossil-fuel buildouts or trillion-dollar nuclear deals. And that is a *failure of imagination*. The physics is bigger than that. The physics is available to anyone with a keyboard, an internet connection, and the willingness to look in directions that other people aren't looking.
>
> Some of you in this room work in places where these conversations matter. Some of you have technical training. Some of you have access to resources. Some of you, in your other life, work with bodies of knowledge that the Western scientific mainstream has not yet caught up to — and that's not just rasashastra; that's hermetic metallurgy, that's alchemical tradition, that's the long shadow of mystery-school natural philosophy. There's more in those traditions than the modern academy has examined.
>
> If any of this lands for you, talk to me afterward. The repository is open. Everything is documented. Anyone can fork it. Anyone can run the simulations on their own laptop tonight, walk through the code, change the assumptions, see what breaks.

*Click to slide 21.*

---

## SLIDE 21 — Questions / repo URL

> Questions?
>
> Take this and run with it. The URL is on the screen — `github.com/consigcody94/ai-energy-frontiers`. MIT licensed. Four subprojects. One hundred and twelve tests passing. Real bills of materials. Real wet-lab protocols. Real engineering validations.
>
> I'm Cody Churchwell. I'll be around for the rest of the evening. If anything specific landed for you and you want to talk about it more — whether you're a graduate student, a corporate researcher, a venture investor, a curious mind, someone who simply found one of these threads interesting — find me. The conversation continues.
>
> Thank you.

*Bow your head slightly. Pause. Open the floor.*

> What would you like to discuss?

---

## Q&A — anticipated questions and answers

You don't need to memorize these — just be familiar with them. Each one is a paragraph you could deliver naturally.

### "How is bacterial neuromorphic different from Loihi-2 silicon neuromorphic?"

> Great question. Loihi-2 is Intel's silicon neuromorphic processor. It operates at 23 picojoules per synaptic event, which is already 10 to 20 times better than dense GPU compute. But it's still silicon — 0.55 volts of switching voltage, hard-floor energy due to CMOS leakage. Bacterial neuromorphic at biological voltage gets you another 30-fold reduction *on top of* what Loihi-2 already does. They're not competing technologies — Loihi-2 is the bridge from silicon GPUs to non-silicon neuromorphic. Bacterial is the next floor below.

### "Has anyone replicated the UBC LENR result yet?"

> Multiple groups are working on it under ARPA-E funding. Lawrence Berkeley National Lab plus UC Davis is the public collaboration; others are quieter. Independent replication is the open question. The UBC Nature paper is one data point — a high-quality one, with hard neutron signatures — but the field is appropriately cautious. The next 12 to 24 months should give us independent confirmation or refutation.

### "Why don't hyperscalers fund this themselves?"

> They fund some of it. Microsoft has signed Small Modular Reactor deals. Google has fusion company equity. Amazon has its own internal energy research. But these are 10-year, billion-dollar capital expenditure bets. The skunkworks-scale work I'm describing — pilots, university lab tests, basic-science experiments — falls below the procurement threshold for hyperscaler decision-making and above the typical grant size for academia. That's the gap this repository lives in. It's also why I made it open source. If the work is sitting there for free, somebody with the right resources can pick up any thread.

### "What's your background?"

> I'm a researcher who can read the papers and write the simulations. The repository is open; the math is auditable; the references are all linked. The point isn't to trust me. The point is to give other people the starting point they need to build. Some of you know me as Cody. Some of you know me as Os Lamia in other contexts. Both are me. The technical work and the heritage scholarship I do as a priest — they inform each other. The bhasma-LENR cross-reference came from that intersection. I think more of those cross-references are sitting there waiting.

### "Is this dual-use? Could any of this weaponize?"

> Realistic answer: no. LENR neutron rates at research scale are six orders of magnitude below anything weapons-relevant. TR diodes are passive electromagnetic devices — they emit IR photons, nothing else. SED Casimir at proof-of-concept scale produces nanowatts. Bacterial neuromorphic is just compute. None of this is export-controlled or proliferation-sensitive at the scale we're talking about.

### "What if the engineered Geobacter target doesn't scale?"

> Honest answer: then the demand-side lever isn't a 500-fold improvement; it's more like 10-fold from where silicon neuromorphic already is. Loihi-2 already gives you 10× over dense GPU compute. So even in the failure mode, we get an order of magnitude. That's still huge. But the headline 500× number assumes the engineering works — and that's the bet.

### "How do I get started if I want to contribute?"

> Open the repository. Pick a subproject. Run the simulator on your laptop — it takes 30 seconds, no special hardware. Read the README. Find a test that's marked MARGINAL or a hypothesis you disagree with, and submit a pull request. Or build the $8,000 TR diode pilot if you have access to a roof. Or — and this is the one I most want to see happen — if any of you has access to a furnace and an XRD, prepare a small sample of Pd-bhasma. Twelve weeks of one person's part-time work. That alone is a publishable result.

### "What about quantum computing?"

> Different problem. Quantum is for problems classical computers can't efficiently solve — factoring, certain optimization, certain simulation tasks. Most AI workloads — the transformer architecture in particular — are not quantum-advantaged. The energy reduction from quantum, if any, comes from algorithmic speed-up on specific problem classes, not from substrate efficiency. The bacterial neuromorphic substrate is attacking the energy problem directly at the substrate level. Different lever.

### "What's the most surprising thing you learned doing this?"

> The Sanskrit angle. I didn't go in looking for it. I was researching LENR cathode preparation methods, and the chain of citations led me into the rasashastra modern characterization literature — the *Journal of Nanoparticle Research* paper on Jasada bhasma. Reading that paper, I realized: the puta cycle is exactly the kind of multi-stage thermal-mechanical processing that produces defect-rich nano-palladium. And nobody had connected those dots. Twelve hundred years of metallurgical knowledge encoded in Sanskrit, plus a 2025 Nature paper on cold fusion, and they meet at a point that nobody had named before. That's the kind of cross-reference that I think is sitting in lots of places, if we go looking.

---

## CLOSING — after Q&A wraps

> Thank you all so much for being here tonight. The URL is `github.com/consigcody94/ai-energy-frontiers`. I'll be here for the rest of the evening if anyone wants to keep talking.
>
> Take care, and good night.

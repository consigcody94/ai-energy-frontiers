/**
 * AI Energy Frontiers — presentation deck builder
 *
 * Run with: node build_deck.js
 * Output:   presentation/ai_energy_frontiers.pptx
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";          // 13.3" x 7.5"
pres.author = "Cody Churchwell";
pres.title = "AI Energy Frontiers";
pres.subject = "Four physics bets on the future of compute";

// =====================================================================
// Color palette — content-informed (energy + biology + cross-cultural)
// =====================================================================
const C = {
  teal:       "0D5556",   // primary — title slides, headers
  cream:      "F5F2E8",   // off-white content slide bg accent
  white:      "FFFFFF",
  ink:        "1A2424",   // body text dark
  ink_muted:  "657272",
  cream_text: "F5F2E8",
  // Per-approach accents:
  tr:         "1F4880",   // TR diode — tech blue
  sed:        "7B4F9F",   // SED Casimir — quantum purple
  bhasma:     "2C5F2D",   // Bhasma LENR — forest green
  bact:       "7A4F10",   // Bacterial neuromorphic — earth gold
  // Signal colors
  good:       "2C5F2D",
  bad:        "B91C1C",
  highlight:  "D4AF37",
};

// =====================================================================
// Layout constants
// =====================================================================
const SLIDE_W = 13.3, SLIDE_H = 7.5;
const PAD = 0.6;
const TITLE_Y = 0.45;

// =====================================================================
// Reusable layouts
// =====================================================================
function addAccentBar(slide, color) {
  // Thin vertical accent on the left edge, NOT under the title
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: SLIDE_H,
    fill: { color },
    line: { color, width: 0 },
  });
}

function addTitle(slide, title, subtitle, color = C.ink) {
  slide.addText(title, {
    x: 0.5, y: TITLE_Y, w: SLIDE_W - 1, h: 0.7,
    fontFace: "Georgia",
    fontSize: 36,
    bold: true,
    color,
    align: "left",
    valign: "middle",
    margin: 0,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5, y: TITLE_Y + 0.75, w: SLIDE_W - 1, h: 0.35,
      fontFace: "Calibri",
      fontSize: 16,
      italic: true,
      color: C.ink_muted,
      align: "left",
      valign: "top",
      margin: 0,
    });
  }
}

function addFooter(slide, leftText, rightText, accentColor) {
  slide.addText(leftText, {
    x: 0.5, y: SLIDE_H - 0.45, w: 8, h: 0.3,
    fontFace: "Calibri", fontSize: 10, color: C.ink_muted,
    align: "left", margin: 0,
  });
  if (rightText) {
    slide.addText(rightText, {
      x: SLIDE_W - 4.5, y: SLIDE_H - 0.45, w: 4, h: 0.3,
      fontFace: "Calibri", fontSize: 10, color: accentColor || C.ink_muted,
      bold: true, align: "right", margin: 0,
    });
  }
}

// Resolve image paths relative to this script
const repoRoot = path.resolve(__dirname, "..");
function img(rel) { return path.join(repoRoot, rel); }

// =====================================================================
// SLIDE 1: Title
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.teal };

  s.addText("AI ENERGY", {
    x: 1.0, y: 1.8, w: 11, h: 0.9,
    fontFace: "Georgia", fontSize: 64, bold: true,
    color: C.cream_text, align: "left", margin: 0, charSpacing: 4,
  });
  s.addText("FRONTIERS", {
    x: 1.0, y: 2.7, w: 11, h: 0.9,
    fontFace: "Georgia", fontSize: 64, bold: true,
    color: C.highlight, align: "left", margin: 0, charSpacing: 4,
  });

  s.addShape(pres.shapes.LINE, {
    x: 1.0, y: 3.9, w: 4, h: 0,
    line: { color: C.cream_text, width: 1 },
  });

  s.addText("Four physics bets on the future of compute", {
    x: 1.0, y: 4.1, w: 11, h: 0.6,
    fontFace: "Georgia", fontSize: 24, italic: true,
    color: C.cream_text, align: "left", margin: 0,
  });
  s.addText("...and where the under-explored physics actually lives", {
    x: 1.0, y: 4.7, w: 11, h: 0.4,
    fontFace: "Calibri", fontSize: 16, color: "C5BFAF",
    align: "left", margin: 0,
  });

  s.addText("Cody Churchwell", {
    x: 1.0, y: 6.4, w: 8, h: 0.35,
    fontFace: "Calibri", fontSize: 14, color: C.cream_text,
    align: "left", margin: 0, bold: true,
  });
  s.addText("github.com/consigcody94/ai-energy-frontiers", {
    x: 1.0, y: 6.75, w: 8, h: 0.3,
    fontFace: "Consolas", fontSize: 12, color: C.highlight,
    align: "left", margin: 0,
  });
}

// =====================================================================
// SLIDE 2: The problem in one big number
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bad);
  addTitle(s, "AI is about to eat the grid", "International Energy Agency, 2025 forecast");

  // BIG number — sized to fit the 2.0" tall box without overflow
  s.addText("950", {
    x: 0.5, y: 2.4, w: 5.5, h: 2.4,
    fontFace: "Georgia", fontSize: 180, bold: true,
    color: C.bad, align: "center", valign: "middle", margin: 0,
  });
  s.addText("TWh", {
    x: 0.5, y: 4.85, w: 5.5, h: 0.6,
    fontFace: "Georgia", fontSize: 32, color: C.ink,
    align: "center", margin: 0, bold: true,
  });
  s.addText("global data-center electricity by 2030", {
    x: 0.5, y: 5.45, w: 5.5, h: 0.35,
    fontFace: "Calibri", fontSize: 14, italic: true,
    color: C.ink_muted, align: "center", margin: 0,
  });

  // Right column — context
  s.addText([
    { text: "From 485 TWh (2025)", options: { fontSize: 18, bold: true, color: C.ink, breakLine: true } },
    { text: "to ~950 TWh (2030)", options: { fontSize: 18, bold: true, color: C.bad, breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "AI-accelerated servers", options: { fontSize: 16, color: C.ink, breakLine: true } },
    { text: "grow at ", options: { fontSize: 16, color: C.ink } },
    { text: "30% per year", options: { fontSize: 16, color: C.bad, bold: true, breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "≈ the entire electricity ", options: { fontSize: 16, color: C.ink, breakLine: true } },
    { text: "consumption of Japan", options: { fontSize: 16, color: C.ink, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "Grid build-out is NOT on pace.", options: { fontSize: 18, bold: true, color: C.bad } },
  ], {
    x: 7.0, y: 2.3, w: 5.7, h: 4.5,
    fontFace: "Calibri", align: "left", valign: "middle", margin: 0,
  });

  addFooter(s, "Source: IEA Energy and AI report, 2025", "the problem", C.bad);
}

// =====================================================================
// SLIDE 3: Two attack vectors
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "Two ways to close the gap", "Most people only see one of them");

  // Left card — SUPPLY
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 2.0, w: 5.9, h: 4.6,
    fill: { color: C.cream },
    line: { color: "C5BFAF", width: 0.75 },
  });
  s.addText("SUPPLY", {
    x: 0.7, y: 2.15, w: 5.5, h: 0.55,
    fontFace: "Georgia", fontSize: 26, bold: true, color: C.tr,
    align: "left", margin: 0,
  });
  s.addText("Generate more energy", {
    x: 0.7, y: 2.7, w: 5.5, h: 0.4,
    fontFace: "Calibri", fontSize: 14, italic: true, color: C.ink_muted,
    align: "left", margin: 0,
  });
  s.addText([
    { text: "1. Thermoradiative diodes", options: { bold: true, color: C.tr, fontSize: 18, breakLine: true } },
    { text: "    Cold sky as heat sink", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "2. Casimir-cavity vacuum energy", options: { bold: true, color: C.sed, fontSize: 18, breakLine: true } },
    { text: "    Stochastic-electrodynamics loophole", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "3. Bhasma-prepared LENR cathodes", options: { bold: true, color: C.bhasma, fontSize: 18, breakLine: true } },
    { text: "    Rasashastra × Nature 2025", options: { fontSize: 13, color: C.ink_muted, italic: true } },
  ], {
    x: 0.7, y: 3.3, w: 5.5, h: 3.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  // Right card — DEMAND
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.9, y: 2.0, w: 5.9, h: 4.6,
    fill: { color: C.cream },
    line: { color: "C5BFAF", width: 0.75 },
  });
  s.addText("DEMAND", {
    x: 7.1, y: 2.15, w: 5.5, h: 0.55,
    fontFace: "Georgia", fontSize: 26, bold: true, color: C.bact,
    align: "left", margin: 0,
  });
  s.addText("Use less per inference", {
    x: 7.1, y: 2.7, w: 5.5, h: 0.4,
    fontFace: "Calibri", fontSize: 14, italic: true, color: C.ink_muted,
    align: "left", margin: 0,
  });
  s.addText([
    { text: "4. Bacterial neuromorphic compute", options: { bold: true, color: C.bact, fontSize: 18, breakLine: true } },
    { text: "    Geobacter protein nanowires", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: "    at biological voltage and energy", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "If it works:", options: { fontSize: 16, color: C.ink, bold: true, breakLine: true } },
    { text: "100×–1000× less energy", options: { fontSize: 16, color: C.bact, bold: true, breakLine: true } },
    { text: "per inference vs silicon", options: { fontSize: 16, color: C.bact, bold: true, breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "Removes ~99% of the problem.", options: { fontSize: 14, color: C.ink, italic: true } },
  ], {
    x: 7.1, y: 3.3, w: 5.5, h: 3.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  addFooter(s, "Supply adds MWh. Demand reduces them.", null, null);
}

// =====================================================================
// SLIDE 4: Map of the four approaches
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "The four approaches", "Layered: now → mid-term → long-shot → demand-side lever");

  const tiles = [
    { x: 0.5, y: 1.95, color: C.tr,     code: "01",
      title: "TR DIODES",        sub: "Cold sky as heat sink",
      stat: "0.3%",   statlbl: "of facility load today",         tag: "BUILDABLE NOW" },
    { x: 6.9, y: 1.95, color: C.sed,    code: "02",
      title: "SED CASIMIR ZPE",  sub: "Vacuum-mode exclusion",
      stat: "$200k",  statlbl: "decisive experiment",            tag: "BASIC PHYSICS BET" },
    { x: 0.5, y: 4.45, color: C.bhasma, code: "03",
      title: "BHASMA LENR",      sub: "Rasashastra × Nature 2025",
      stat: "5×",     statlbl: "predicted enhancement",          tag: "CROSS-DISCIPLINARY" },
    { x: 6.9, y: 4.45, color: C.bact,   code: "04",
      title: "BACTERIAL NEURO",  sub: "Geobacter on CMOS",
      stat: "500×",   statlbl: "lower energy per token",         tag: "DEMAND-SIDE LEVER" },
  ];

  tiles.forEach(t => {
    // Card
    s.addShape(pres.shapes.RECTANGLE, {
      x: t.x, y: t.y, w: 5.9, h: 2.3,
      fill: { color: C.white },
      line: { color: t.color, width: 1.5 },
    });
    // Code number
    s.addText(t.code, {
      x: t.x + 0.2, y: t.y + 0.08, w: 1.0, h: 0.5,
      fontFace: "Georgia", fontSize: 26, bold: true, color: t.color,
      align: "left", valign: "top", margin: 0,
    });
    // Tag
    s.addText(t.tag, {
      x: t.x + 1.4, y: t.y + 0.18, w: 4.3, h: 0.3,
      fontFace: "Calibri", fontSize: 10, bold: true, color: t.color,
      align: "right", valign: "middle", margin: 0, charSpacing: 2,
    });
    // Title
    s.addText(t.title, {
      x: t.x + 0.2, y: t.y + 0.62, w: 5.5, h: 0.45,
      fontFace: "Georgia", fontSize: 20, bold: true, color: C.ink,
      align: "left", valign: "middle", margin: 0,
    });
    // Subtitle
    s.addText(t.sub, {
      x: t.x + 0.2, y: t.y + 1.08, w: 5.5, h: 0.32,
      fontFace: "Calibri", fontSize: 12, italic: true, color: C.ink_muted,
      align: "left", margin: 0,
    });
    // Big stat
    s.addText(t.stat, {
      x: t.x + 0.2, y: t.y + 1.45, w: 2.5, h: 0.75,
      fontFace: "Georgia", fontSize: 32, bold: true, color: t.color,
      align: "left", valign: "middle", margin: 0,
    });
    s.addText(t.statlbl, {
      x: t.x + 2.8, y: t.y + 1.45, w: 3.0, h: 0.75,
      fontFace: "Calibri", fontSize: 12, italic: true, color: C.ink_muted,
      align: "left", valign: "middle", margin: 0,
    });
  });

  addFooter(s, "All four shipped: code, tests, BOM, schematic, protocol.", null, null);
}

// =====================================================================
// SLIDE 5: Approach 1 (TR Diodes) — physics
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.tr);
  addTitle(s, "01 · Thermoradiative Diodes", "The cold sky as a heat sink — every clear night", C.tr);

  s.addText([
    { text: "A photovoltaic cell ", options: { fontSize: 16, color: C.ink } },
    { text: "in reverse", options: { fontSize: 16, color: C.tr, bold: true, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "Hot data-center surface emits IR photons", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "through the 8–13 µm atmospheric window", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "toward effectively ~3 K of deep space.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "Net spectral flux drives current:", options: { fontSize: 14, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "F_net = π · τ(λ) · η(λ) · [B(λ,T_hot) − B(λ,T_sky)]",
      options: { fontSize: 13, color: C.tr, bold: true, fontFace: "Consolas", breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "We took the 2024 record of 350 mW/m²", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "and re-ran the model against real hourly", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "ERA5 weather at 6 hyperscale sites.", options: { fontSize: 14, color: C.ink } },
  ], {
    x: 0.5, y: 1.9, w: 6.5, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  s.addImage({
    path: img("tr_diode_data_center/design_rendering.png"),
    x: 7.2, y: 1.9, w: 5.7, h: 5.0,
    sizing: { type: "contain", w: 5.7, h: 5.0 },
  });

  addFooter(s, "Calibrated to arXiv:2407.17751 — Liao et al., 2024", "01 / 04", C.tr);
}

// =====================================================================
// SLIDE 6: TR Diodes — real weather
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.tr);
  addTitle(s, "Real weather, real data centers", "ERA5 reanalysis via Open-Meteo, 2024 hourly", C.tr);

  // 6 city stats
  const cities = [
    { code: "PHX", name: "Phoenix",     val: "171",   clim: "hot desert" },
    { code: "NVA", name: "N. Virginia", val: "176",   clim: "humid cont." },
    { code: "DUB", name: "Dublin",      val: "177",   clim: "maritime" },
    { code: "FRA", name: "Frankfurt",   val: "177",   clim: "cool cont." },
    { code: "ATC", name: "Atacama",     val: "167",   clim: "high desert" },
    { code: "SIN", name: "Singapore",   val: "115",   clim: "tropical" },
  ];
  cities.forEach((c, i) => {
    const x = 0.5 + (i % 3) * 4.3;
    const y = 2.1 + Math.floor(i / 3) * 1.6;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.0, h: 1.3,
      fill: { color: C.cream },
      line: { color: "C5BFAF", width: 0.5 },
    });
    s.addText(c.code, {
      x: x + 0.15, y: y + 0.1, w: 0.9, h: 0.4,
      fontFace: "Consolas", fontSize: 14, bold: true, color: C.tr,
      align: "left", margin: 0,
    });
    s.addText(c.name, {
      x: x + 1.0, y: y + 0.1, w: 2.5, h: 0.4,
      fontFace: "Calibri", fontSize: 13, color: C.ink, bold: true,
      align: "left", margin: 0,
    });
    s.addText(c.val, {
      x: x + 0.15, y: y + 0.5, w: 1.6, h: 0.75,
      fontFace: "Georgia", fontSize: 36, bold: true,
      color: c.code === "SIN" ? C.bad : C.tr,
      align: "left", margin: 0,
    });
    s.addText("MWh", {
      x: x + 1.85, y: y + 0.55, w: 1.0, h: 0.35,
      fontFace: "Calibri", fontSize: 12, color: C.ink_muted,
      align: "left", margin: 0,
    });
    s.addText(c.clim, {
      x: x + 1.85, y: y + 0.85, w: 2.1, h: 0.3,
      fontFace: "Calibri", fontSize: 11, italic: true, color: C.ink_muted,
      align: "left", margin: 0,
    });
  });

  s.addText([
    { text: "Singapore is the loser (humid tropical = warm sky).", options: { fontSize: 14, color: C.bad, italic: true, breakLine: true } },
    { text: "Everywhere else: ", options: { fontSize: 14, color: C.ink } },
    { text: "167–177 MWh/yr ", options: { fontSize: 14, color: C.tr, bold: true } },
    { text: "per 100,000 m² roof.", options: { fontSize: 14, color: C.ink } },
  ], {
    x: 0.5, y: 5.5, w: 12.3, h: 1.2,
    fontFace: "Calibri", align: "left", valign: "middle", margin: 0,
  });

  addFooter(s, "Open-Meteo Archive API, ERA5 reanalysis hourly", "01 / 04", C.tr);
}

// =====================================================================
// SLIDE 7: TR Diodes — the pilot
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.tr);
  addTitle(s, "The pilot you could fund tonight", "10 panels, $8,000, one corporate skunkworks", C.tr);

  s.addText("$8K", {
    x: 0.5, y: 2.3, w: 6.0, h: 2.5,
    fontFace: "Georgia", fontSize: 170, bold: true,
    color: C.tr, align: "center", valign: "middle", margin: 0,
  });
  s.addText("pilot deck — 10 panels installed & instrumented", {
    x: 0.5, y: 4.85, w: 6.0, h: 0.4,
    fontFace: "Calibri", fontSize: 14, italic: true, color: C.ink_muted,
    align: "center", margin: 0,
  });

  s.addText([
    { text: "What the pilot proves", options: { fontSize: 22, bold: true, color: C.tr, fontFace: "Georgia", breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "✓ Real device efficiency", options: { fontSize: 16, color: C.ink, breakLine: true } },
    { text: "    (today's 0.5% of radiative limit)", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "✓ Field failure modes", options: { fontSize: 16, color: C.ink, breakLine: true } },
    { text: "    (humidity, dust, hail — the unmodeled enemies)", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "✓ Cost trajectory at 100k volume", options: { fontSize: 16, color: C.ink, breakLine: true } },
    { text: "    (today $526/panel; ~$50 if MCT mass-produces)", options: { fontSize: 13, color: C.ink_muted, italic: true } },
  ], {
    x: 7.0, y: 1.9, w: 5.9, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  addFooter(s, "Full BOM with vendor part numbers in the repo", "01 / 04", C.tr);
}

// =====================================================================
// SLIDE 8: Approach 2 (SED Casimir ZPE) — the vacuum has structure
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.sed);
  addTitle(s, "02 · The vacuum has structure", "Casimir 1948 — and a thermodynamic loophole nobody followed up", C.sed);

  s.addText([
    { text: "Two parallel plates at separation d", options: { fontSize: 16, color: C.ink, breakLine: true } },
    { text: "attract through ", options: { fontSize: 16, color: C.ink } },
    { text: "vacuum mode exclusion.", options: { fontSize: 16, color: C.sed, bold: true, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "F/A = π² ℏc / (240 d⁴)", options: { fontSize: 18, color: C.sed, bold: true, fontFace: "Consolas", breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "Verified to 1% across Lamoreaux 1997,", options: { fontSize: 13, color: C.ink_muted, breakLine: true } },
    { text: "Mohideen 1998, Bressi 2002, Decca 2007.", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 12, breakLine: true } },
    { text: "Schrieber 2019 (Atoms 7:51)", options: { fontSize: 16, color: C.ink, bold: true, breakLine: true } },
    { text: "reviewed three classes of ZPE extraction.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "Two violate the 2nd law. ", options: { fontSize: 14, color: C.ink } },
    { text: "One does not.", options: { fontSize: 16, color: C.sed, bold: true, italic: true } },
  ], {
    x: 0.5, y: 1.9, w: 6.5, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  s.addImage({
    path: img("sed_casimir_zpe/casimir_force.png"),
    x: 7.2, y: 1.9, w: 5.7, h: 5.0,
    sizing: { type: "contain", w: 5.7, h: 5.0 },
  });

  addFooter(s, "Casimir effect: real, verified, mainstream physics", "02 / 04", C.sed);
}

// =====================================================================
// SLIDE 9: SED Casimir — the decisive experiment
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.sed);
  addTitle(s, "The decisive experiment", "Sub-100 nm cavity stack + SQUID-TES bolometer + Cs vapor", C.sed);

  // Left: the experiment description
  s.addText([
    { text: "Pump gas atoms through a Casimir cavity.", options: { fontSize: 16, color: C.ink, bold: true, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "In Schrieber's interpretation, electron orbitals", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "settle lower because long-λ ZPF modes are excluded.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Atom enters → releases energy → leaves and re-fills", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "from the universe's free-space ZPF.", options: { fontSize: 14, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 14, breakLine: true } },
    { text: "Predictions if real:", options: { fontSize: 16, color: C.sed, bold: true, breakLine: true } },
    { text: "  · scales as ", options: { fontSize: 14, color: C.ink } },
    { text: "1/d⁴", options: { fontSize: 14, color: C.sed, bold: true, fontFace: "Consolas", breakLine: true } },
    { text: "  · zero signal for closed-shell atoms (Xe control)", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "  · cleanly detectable on a cryogenic bolometer", options: { fontSize: 14, color: C.ink } },
  ], {
    x: 0.5, y: 1.9, w: 6.5, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  // Right: cost and stakes
  s.addShape(pres.shapes.RECTANGLE, {
    x: 7.2, y: 2.0, w: 5.7, h: 4.8,
    fill: { color: C.cream },
    line: { color: "C5BFAF", width: 0.75 },
  });
  s.addText("$200K", {
    x: 7.2, y: 2.2, w: 5.7, h: 1.5,
    fontFace: "Georgia", fontSize: 80, bold: true, color: C.sed,
    align: "center", valign: "middle", margin: 0,
  });
  s.addText("with shared dilution-fridge access", {
    x: 7.2, y: 3.7, w: 5.7, h: 0.4,
    fontFace: "Calibri", fontSize: 13, italic: true, color: C.ink_muted,
    align: "center", margin: 0,
  });
  s.addText([
    { text: "6-month measurement campaign.", options: { fontSize: 14, color: C.ink, bold: true, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "Either outcome = ", options: { fontSize: 13, color: C.ink } },
    { text: "Phys. Rev. Lett.", options: { fontSize: 13, color: C.sed, bold: true, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Detection → new energy regime", options: { fontSize: 13, color: C.ink, breakLine: true } },
    { text: "Null → closes the SED loophole forever", options: { fontSize: 13, color: C.ink } },
  ], {
    x: 7.5, y: 4.4, w: 5.1, h: 2.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  addFooter(s, "Almost zero peer-reviewed follow-up since Schrieber 2019", "02 / 04", C.sed);
}

// =====================================================================
// SLIDE 10: Approach 3 (Bhasma LENR) — LENR rehabilitated
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bhasma);
  addTitle(s, "03 · LENR just got rehabilitated", "Nature 644:640 (2025) — UBC Thunderbird Reactor", C.bhasma);

  s.addText("+15%", {
    x: 0.5, y: 2.5, w: 5.5, h: 2.3,
    fontFace: "Georgia", fontSize: 130, bold: true, color: C.bhasma,
    align: "center", valign: "middle", margin: 0,
  });
  s.addText("D-D fusion rate enhancement", {
    x: 0.5, y: 4.9, w: 5.5, h: 0.4,
    fontFace: "Calibri", fontSize: 14, color: C.ink, bold: true,
    align: "center", margin: 0,
  });
  s.addText("from electrochemical D loading into Pd", {
    x: 0.5, y: 5.3, w: 5.5, h: 0.35,
    fontFace: "Calibri", fontSize: 13, italic: true, color: C.ink_muted,
    align: "center", margin: 0,
  });

  s.addText([
    { text: "Hard neutron signature.", options: { fontSize: 18, bold: true, color: C.bhasma, breakLine: true } },
    { text: "Not calorimetry. Real fusion.", options: { fontSize: 13, italic: true, color: C.ink_muted, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "First Nature-tier validation of", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "electrochemical cold-fusion enhancement.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "ARPA-E funding $10M across 8 LENR projects.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "The cold-fusion taboo is breaking.", options: { fontSize: 16, color: C.bhasma, italic: true, bold: true } },
  ], {
    x: 7.0, y: 2.1, w: 5.9, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  addFooter(s, "Schenkel et al., Nature 644:640–645 (Aug 2025)", "03 / 04", C.bhasma);
}

// =====================================================================
// SLIDE 11: Bhasma LENR — the Sanskrit heritage angle
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bhasma);
  addTitle(s, "The cross-disciplinary thesis", "Indian alchemy already builds the cathode we need", C.bhasma);

  s.addText([
    { text: "Rasashastra", options: { fontSize: 22, bold: true, italic: true, color: C.bhasma, fontFace: "Georgia", breakLine: true } },
    { text: "the Sanskrit \"science of mercury\"", options: { fontSize: 14, italic: true, color: C.ink_muted, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Classical bhasma preparations are", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "repeatedly calcined nanoparticulate metals.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Modern XRD / TEM confirms:", options: { fontSize: 14, color: C.ink, bold: true, breakLine: true } },
    { text: "Tamra bhasma — < 100 nm Cu crystallites", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: "Jasada bhasma — non-stoich. nano ZnO", options: { fontSize: 13, color: C.ink_muted, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Nobody has tried Pd-bhasma.", options: { fontSize: 16, bold: true, color: C.bhasma, italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "It SHOULD outperform UBC's foil:", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "1. Higher D/Pd loading (0.95 vs 0.70)", options: { fontSize: 13, color: C.ink_muted, breakLine: true } },
    { text: "2. ~300× the grain-boundary surface area", options: { fontSize: 13, color: C.ink_muted } },
  ], {
    x: 0.5, y: 1.9, w: 6.5, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  s.addImage({
    path: img("bhasma_lenr_cathode/puta_progression.png"),
    x: 7.2, y: 1.9, w: 5.7, h: 5.0,
    sizing: { type: "contain", w: 5.7, h: 5.0 },
  });

  addFooter(s, "Wujastyk, Rasa and Rasaśāstra (Oxford, 2024)", "03 / 04", C.bhasma);
}

// =====================================================================
// SLIDE 12: Bhasma LENR — the experiment
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bhasma);
  addTitle(s, "The three-way bake-off", "Disentangles \"is it surface area?\" from \"is it rasashastra-specific?\"", C.bhasma);

  const cathodes = [
    { x: 0.5,  c: "A", title: "Pd-bhasma",         sub: "60 puta cycles + parada-marana", expect: "Model predicts +50–80%" },
    { x: 4.7,  c: "B", title: "Commercial Pd-black", sub: "Matched BET surface area",        expect: "If A ≈ B, just surface area" },
    { x: 8.9,  c: "C", title: "Commercial Pd foil",  sub: "UBC baseline replication",         expect: "Reproduces +15% UBC anchor" },
  ];

  cathodes.forEach((cat, i) => {
    const colors = [C.bhasma, C.highlight, C.ink_muted];
    const col = colors[i];
    s.addShape(pres.shapes.RECTANGLE, {
      x: cat.x, y: 2.0, w: 3.9, h: 4.5,
      fill: { color: C.white },
      line: { color: col, width: 1.5 },
    });
    s.addText(cat.c, {
      x: cat.x + 0.2, y: 2.15, w: 0.6, h: 0.55,
      fontFace: "Georgia", fontSize: 28, bold: true, color: col,
      align: "left", margin: 0,
    });
    s.addText(cat.title, {
      x: cat.x + 0.2, y: 2.8, w: 3.5, h: 0.55,
      fontFace: "Georgia", fontSize: 22, bold: true, color: C.ink,
      align: "left", margin: 0,
    });
    s.addText(cat.sub, {
      x: cat.x + 0.2, y: 3.4, w: 3.5, h: 0.6,
      fontFace: "Calibri", fontSize: 13, italic: true, color: C.ink_muted,
      align: "left", margin: 0,
    });
    s.addText(cat.expect, {
      x: cat.x + 0.2, y: 5.3, w: 3.5, h: 0.6,
      fontFace: "Calibri", fontSize: 14, color: col, bold: true,
      align: "left", margin: 0,
    });
  });

  s.addText("12-week graduate-student project · $80k with shared accelerator + neutron array", {
    x: 0.5, y: 6.8, w: 12.3, h: 0.3,
    fontFace: "Calibri", fontSize: 13, italic: true, color: C.ink_muted,
    align: "center", margin: 0,
  });

  addFooter(s, "Full protocol in bhasma_lenr_cathode/protocol.md", "03 / 04", C.bhasma);
}

// =====================================================================
// SLIDE 13: Approach 4 (Bacterial neuromorphic) — the substrate
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bact);
  addTitle(s, "04 · The demand-side lever", "Bacteria growing the AI compute substrate", C.bact);

  s.addText([
    { text: "Silicon hit a voltage wall.", options: { fontSize: 18, bold: true, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Below ~0.6V CMOS gates leak exponentially.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: "Memory access dominates everything.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Geobacter sulfurreducens", options: { fontSize: 18, bold: true, italic: true, color: C.bact, fontFace: "Georgia", breakLine: true } },
    { text: "grows electrically conductive protein nanowires.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "Fu et al., Nature Comms 11:1861 (2020)", options: { fontSize: 14, color: C.bact, bold: true, breakLine: true } },
    { text: "built memristors at ", options: { fontSize: 14, color: C.ink } },
    { text: "70–130 mV", options: { fontSize: 14, color: C.bact, bold: true, fontFace: "Consolas" } },
    { text: " and ", options: { fontSize: 14, color: C.ink } },
    { text: "0.3–100 pJ", options: { fontSize: 14, color: C.bact, bold: true, fontFace: "Consolas", breakLine: true } },
    { text: "per switching event.", options: { fontSize: 14, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 10, breakLine: true } },
    { text: "First non-biological substrate to hit biology.", options: { fontSize: 16, color: C.bact, italic: true, bold: true } },
  ], {
    x: 0.5, y: 1.9, w: 6.5, h: 5.0,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  s.addImage({
    path: img("bacterial_neuromorphic_substrate/design_rendering.png"),
    x: 7.2, y: 1.9, w: 5.7, h: 5.0,
    sizing: { type: "contain", w: 5.7, h: 5.0 },
  });

  addFooter(s, "Geobacter pili discovered: Lovley lab, UMass Amherst", "04 / 04", C.bact);
}

// =====================================================================
// SLIDE 14: Bacterial neuromorphic — the 500× number
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bact);
  addTitle(s, "The lever", "Energy per LLaMA-70B token, log scale", C.bact);

  s.addImage({
    path: img("bacterial_neuromorphic_substrate/substrate_comparison.png"),
    x: 0.5, y: 1.9, w: 8.5, h: 5.0,
    sizing: { type: "contain", w: 8.5, h: 5.0 },
  });

  s.addText("500×", {
    x: 9.2, y: 2.1, w: 3.8, h: 1.5,
    fontFace: "Georgia", fontSize: 90, bold: true, color: C.bact,
    align: "center", valign: "middle", margin: 0,
  });
  s.addText("lower energy per token", {
    x: 9.2, y: 3.55, w: 3.8, h: 0.4,
    fontFace: "Calibri", fontSize: 14, italic: true, color: C.ink_muted,
    align: "center", margin: 0,
  });
  s.addText([
    { text: "Today's silicon", options: { fontSize: 13, color: C.ink, bold: true, breakLine: true } },
    { text: "7 J/token (H100)", options: { fontSize: 16, color: C.bad, bold: true, fontFace: "Consolas", breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "Engineered target", options: { fontSize: 13, color: C.ink, bold: true, breakLine: true } },
    { text: "14 mJ/token", options: { fontSize: 16, color: C.bact, bold: true, fontFace: "Consolas", breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "Biological floor", options: { fontSize: 13, color: C.ink, bold: true, breakLine: true } },
    { text: "1.4 mJ/token", options: { fontSize: 14, color: C.ink_muted, italic: true, fontFace: "Consolas" } },
  ], {
    x: 9.2, y: 4.0, w: 3.8, h: 3.0,
    fontFace: "Calibri", align: "center", valign: "top", margin: 0,
  });

  addFooter(s, "Calibrated to Fu 2020 NatComms, Loihi-2 Davies 2021, NVIDIA H100 whitepaper", "04 / 04", C.bact);
}

// =====================================================================
// SLIDE 15: Bacterial neuromorphic — the global picture
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addAccentBar(s, C.bact);
  addTitle(s, "What that means for the grid", "2030 global AI inference electricity demand", C.bact);

  s.addImage({
    path: img("bacterial_neuromorphic_substrate/global_demand.png"),
    x: 0.5, y: 1.9, w: 8.5, h: 5.0,
    sizing: { type: "contain", w: 8.5, h: 5.0 },
  });

  s.addText([
    { text: "Silicon path", options: { fontSize: 14, bold: true, color: C.ink, breakLine: true } },
    { text: "1,100 TWh/yr", options: { fontSize: 22, bold: true, color: C.bad, fontFace: "Consolas", breakLine: true } },
    { text: "above the IEA's", options: { fontSize: 11, italic: true, color: C.ink_muted, breakLine: true } },
    { text: "entire 950 TWh", options: { fontSize: 11, italic: true, color: C.ink_muted, breakLine: true } },
    { text: "data-center forecast", options: { fontSize: 11, italic: true, color: C.ink_muted, breakLine: true } },
    { text: " ", options: { fontSize: 14, breakLine: true } },
    { text: "Engineered target", options: { fontSize: 14, bold: true, color: C.ink, breakLine: true } },
    { text: "2.2 TWh/yr", options: { fontSize: 22, bold: true, color: C.bact, fontFace: "Consolas", breakLine: true } },
    { text: "off the chart, downward.", options: { fontSize: 11, italic: true, color: C.ink_muted } },
  ], {
    x: 9.2, y: 2.1, w: 3.8, h: 5.0,
    fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
  });

  addFooter(s, "1 trillion daily inferences at 500 tokens each, GPT-4-class", "04 / 04", C.bact);
}

// =====================================================================
// SLIDE 16: The cross-approach comparison
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "Which approach wins?", "All four on the same axis, three TRL milestones");

  s.addImage({
    path: img("comparison.png"),
    x: 0.5, y: 1.6, w: 12.3, h: 5.3,
    sizing: { type: "contain", w: 12.3, h: 5.3 },
  });

  addFooter(s, "comparison.py — all four subprojects, side by side", null, null);
}

// =====================================================================
// SLIDE 17: What's already built
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "What's already built", "The repo, today");

  // Stat tiles
  const stats = [
    { x: 0.5,  v: "4",    lbl: "subprojects",         desc: "TR diode · SED Casimir · Bhasma · Bacterial", c: C.teal },
    { x: 3.75, v: "62",   lbl: "physics tests",       desc: "calibration + monotonicity + Monte Carlo",     c: C.bhasma },
    { x: 7.0,  v: "50",   lbl: "engineering tests",   desc: "wind, hail, thermal, signal, vacuum, dose",    c: C.tr },
    { x: 10.25,v: "0",    lbl: "FAIL items",          desc: "every design survives engineering review",     c: C.good },
  ];
  stats.forEach(stat => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: stat.x, y: 1.9, w: 2.85, h: 2.3,
      fill: { color: C.cream },
      line: { color: stat.c, width: 1.2 },
    });
    s.addText(stat.v, {
      x: stat.x, y: 2.0, w: 2.85, h: 1.3,
      fontFace: "Georgia", fontSize: 64, bold: true, color: stat.c,
      align: "center", valign: "middle", margin: 0,
    });
    s.addText(stat.lbl, {
      x: stat.x, y: 3.3, w: 2.85, h: 0.4,
      fontFace: "Calibri", fontSize: 14, bold: true, color: C.ink,
      align: "center", margin: 0,
    });
    s.addText(stat.desc, {
      x: stat.x + 0.1, y: 3.7, w: 2.65, h: 0.55,
      fontFace: "Calibri", fontSize: 10, italic: true, color: C.ink_muted,
      align: "center", margin: 0,
    });
  });

  // Bottom rows — what each subproject ships
  s.addText([
    { text: "Every subproject ships:", options: { fontSize: 16, bold: true, color: C.ink, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "physics simulator  ·  validation suite  ·  plots  ·  real-world data integration  ·",
      options: { fontSize: 13, color: C.ink_muted, breakLine: true } },
    { text: "physical_design.md  ·  bom.csv  ·  schematic  ·  protocol.md  ·  engineering tests",
      options: { fontSize: 13, color: C.ink_muted } },
  ], {
    x: 0.5, y: 4.7, w: 12.3, h: 1.5,
    fontFace: "Calibri", align: "center", valign: "top", margin: 0,
  });

  // Repo URL bar
  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.5, y: 6.2, w: 10.3, h: 0.65,
    fill: { color: C.teal },
    line: { color: C.teal, width: 0 },
  });
  s.addText("github.com/consigcody94/ai-energy-frontiers", {
    x: 1.5, y: 6.2, w: 10.3, h: 0.65,
    fontFace: "Consolas", fontSize: 18, color: C.cream_text, bold: true,
    align: "center", valign: "middle", margin: 0,
  });

  addFooter(s, "MIT licensed · fork it · fix it · prove it wrong", null, null);
}

// =====================================================================
// SLIDE 18: Honest assessment
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "Honest assessment", "What's true · what's hypothesis · what's unknown");

  const rows = [
    { color: C.tr,     name: "TR diodes",
      t: "Planck physics, 350 mW/m² 2024 record, atmospheric window",
      h: "Device efficiency improves 10–20× in 5 years",
      u: "Capital cost trajectory of MCT arrays at scale" },
    { color: C.sed,    name: "SED Casimir",
      t: "Casimir effect verified to 1%, Schrieber thermodynamic argument",
      h: "SED interpretation of orbital ground states",
      u: "f_couple — never measured anywhere since 2019" },
    { color: C.bhasma, name: "Bhasma LENR",
      t: "UBC +15% Nature 2025, bhasma nano-particles XRD-confirmed",
      h: "α_surface and α_loading coefficients; cross-disciplinary connection",
      u: "Whether bhasma-prep beats commercial nano-Pd" },
    { color: C.bact,   name: "Bacterial neuro",
      t: "Geobacter pilus memristors at biological voltage and energy",
      h: "Sub-fF capacitance scaling gives the 500× advantage",
      u: "8–9 orders of magnitude of integration scaling" },
  ];

  // Header row
  s.addText("APPROACH", {
    x: 0.5, y: 1.85, w: 2.3, h: 0.35,
    fontFace: "Calibri", fontSize: 11, bold: true, color: C.ink_muted,
    align: "left", margin: 0, charSpacing: 1,
  });
  s.addText("TRUE", {
    x: 2.9, y: 1.85, w: 3.7, h: 0.35,
    fontFace: "Calibri", fontSize: 11, bold: true, color: C.good,
    align: "left", margin: 0, charSpacing: 1,
  });
  s.addText("HYPOTHESIS", {
    x: 6.7, y: 1.85, w: 3.4, h: 0.35,
    fontFace: "Calibri", fontSize: 11, bold: true, color: C.highlight,
    align: "left", margin: 0, charSpacing: 1,
  });
  s.addText("UNKNOWN", {
    x: 10.2, y: 1.85, w: 2.7, h: 0.35,
    fontFace: "Calibri", fontSize: 11, bold: true, color: C.bad,
    align: "left", margin: 0, charSpacing: 1,
  });

  rows.forEach((r, i) => {
    const y = 2.4 + i * 1.15;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y, w: 0.10, h: 1.0,
      fill: { color: r.color }, line: { color: r.color, width: 0 },
    });
    s.addText(r.name, {
      x: 0.72, y, w: 2.2, h: 1.0,
      fontFace: "Calibri", fontSize: 13, bold: true, color: r.color,
      align: "left", valign: "middle", margin: 0,
    });
    s.addText(r.t, {
      x: 2.9, y, w: 3.7, h: 1.0,
      fontFace: "Calibri", fontSize: 11, color: C.ink,
      align: "left", valign: "middle", margin: 0,
    });
    s.addText(r.h, {
      x: 6.7, y, w: 3.4, h: 1.0,
      fontFace: "Calibri", fontSize: 11, color: C.ink,
      align: "left", valign: "middle", margin: 0,
    });
    s.addText(r.u, {
      x: 10.2, y, w: 2.7, h: 1.0,
      fontFace: "Calibri", fontSize: 11, color: C.ink,
      align: "left", valign: "middle", margin: 0,
    });
  });

  addFooter(s, "Hypotheses are bets, not promises. Unknowns are open questions.", null, null);
}

// =====================================================================
// SLIDE 19: The roadmap
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "Where each one goes next", "Near · mid · long — and they don't have to win in order");

  const phases = [
    { x: 0.5,  color: C.tr,
      title: "NOW · 1 year",
      items: ["TR diode 10-panel pilot ($8k)",
              "First real-deployment device-efficiency measurement",
              "Bhasma-Pd cathode prep + characterize"] },
    { x: 4.7,  color: C.bhasma,
      title: "MID · 2–5 years",
      items: ["Bhasma-LENR three-way cathode test",
              "SED Casimir cavity experiment (PRL-tier result either way)",
              "Loihi-2-equivalent SNN on Geobacter (64K neurons)"] },
    { x: 8.9,  color: C.bact,
      title: "LONG · 5–10 years",
      items: ["MCT photodiode cost reduction → economic TR roof",
              "If LENR scales: net-positive bhasma reactor",
              "Hybrid Geobacter-CMOS chip at transformer-block scale"] },
  ];

  phases.forEach(p => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: p.x, y: 1.9, w: 3.9, h: 4.8,
      fill: { color: C.white },
      line: { color: p.color, width: 1.5 },
    });
    s.addText(p.title, {
      x: p.x + 0.2, y: 2.1, w: 3.5, h: 0.55,
      fontFace: "Georgia", fontSize: 18, bold: true, color: p.color,
      align: "left", margin: 0, charSpacing: 1,
    });
    s.addShape(pres.shapes.LINE, {
      x: p.x + 0.2, y: 2.7, w: 1.3, h: 0,
      line: { color: p.color, width: 1.5 },
    });
    const txt = p.items.map((it, i) => ({
      text: `${i + 1}.  ${it}`,
      options: { fontSize: 13, color: C.ink, breakLine: true },
    }));
    txt.push({ text: " ", options: { fontSize: 10 } });
    s.addText(txt, {
      x: p.x + 0.2, y: 2.95, w: 3.5, h: 3.7,
      fontFace: "Calibri", align: "left", valign: "top", margin: 0,
      paraSpaceAfter: 8,
    });
  });

  addFooter(s, "Each phase is funded by a different lever (skunkworks → grant → seed/Series A)", null, null);
}

// =====================================================================
// SLIDE 20: Why this matters
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.teal };

  s.addText("Why this matters", {
    x: 1.0, y: 1.2, w: 11, h: 0.7,
    fontFace: "Georgia", fontSize: 32, italic: true, color: C.highlight,
    align: "left", margin: 0,
  });

  s.addText("AI's energy problem isn't just engineering.", {
    x: 1.0, y: 2.3, w: 11, h: 0.7,
    fontFace: "Georgia", fontSize: 38, bold: true, color: C.cream_text,
    align: "left", margin: 0,
  });
  s.addText("It's a question about what physics we have ignored.", {
    x: 1.0, y: 3.05, w: 11, h: 0.65,
    fontFace: "Georgia", fontSize: 28, color: "C5BFAF", italic: true,
    align: "left", margin: 0,
  });

  s.addText([
    { text: "The cold sky", options: { fontSize: 18, color: C.cream_text, bold: true, breakLine: true } },
    { text: "is a heat sink we don't use.", options: { fontSize: 14, color: "C5BFAF", italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 14, breakLine: true } },
    { text: "The vacuum", options: { fontSize: 18, color: C.cream_text, bold: true, breakLine: true } },
    { text: "has a thermodynamic loophole nobody followed up.", options: { fontSize: 14, color: "C5BFAF", italic: true } },
  ], {
    x: 1.0, y: 4.5, w: 5.7, h: 2.5,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });

  s.addText([
    { text: "Ancient metallurgy", options: { fontSize: 18, color: C.cream_text, bold: true, breakLine: true } },
    { text: "may have already solved the LENR cathode problem.", options: { fontSize: 14, color: "C5BFAF", italic: true, breakLine: true } },
    { text: " ", options: { fontSize: 14, breakLine: true } },
    { text: "Bacteria", options: { fontSize: 18, color: C.cream_text, bold: true, breakLine: true } },
    { text: "grow the lowest-energy compute substrate known.", options: { fontSize: 14, color: "C5BFAF", italic: true } },
  ], {
    x: 6.9, y: 4.5, w: 5.7, h: 2.5,
    fontFace: "Calibri", align: "left", valign: "top", margin: 0,
  });
}

// =====================================================================
// SLIDE 21: Q&A / take this and run with it
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.teal };

  s.addText("Questions?", {
    x: 1.0, y: 1.0, w: 11, h: 1.0,
    fontFace: "Georgia", fontSize: 56, bold: true, color: C.highlight,
    align: "left", margin: 0,
  });

  s.addText("Take this and run with it.", {
    x: 1.0, y: 2.2, w: 11, h: 0.7,
    fontFace: "Georgia", fontSize: 28, italic: true, color: C.cream_text,
    align: "left", margin: 0,
  });

  // Big URL box
  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.0, y: 3.5, w: 11.3, h: 1.0,
    fill: { color: C.cream_text },
    line: { color: C.highlight, width: 1.5 },
  });
  s.addText("github.com/consigcody94/ai-energy-frontiers", {
    x: 1.0, y: 3.5, w: 11.3, h: 1.0,
    fontFace: "Consolas", fontSize: 30, bold: true, color: C.teal,
    align: "center", valign: "middle", margin: 0,
  });

  s.addText("MIT licensed. 4 subprojects. 112 tests passing. Real BOMs. Real protocols.", {
    x: 1.0, y: 4.8, w: 11.3, h: 0.5,
    fontFace: "Calibri", fontSize: 16, italic: true, color: "C5BFAF",
    align: "center", margin: 0,
  });

  s.addText([
    { text: "Cody Churchwell", options: { fontSize: 14, bold: true, color: C.cream_text, breakLine: true } },
    { text: "AI Energy Frontiers · 2026", options: { fontSize: 12, italic: true, color: "C5BFAF" } },
  ], {
    x: 1.0, y: 6.4, w: 11.3, h: 0.7,
    fontFace: "Calibri", align: "center", valign: "bottom", margin: 0,
  });
}

// =====================================================================
// Write
// =====================================================================
pres.writeFile({ fileName: path.join(__dirname, "ai_energy_frontiers.pptx") })
  .then(fn => console.log("Wrote:", fn))
  .catch(e => { console.error("Error:", e); process.exit(1); });

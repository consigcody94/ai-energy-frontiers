"""
Patch the design_rendering.png to clean up Region E's labels.

The image generator wrapped the parenthetical subtext to two lines for
several columns. This script:
  1. Opens the rendering
  2. Whites out the label row beneath Region E's bars
  3. Re-draws clean single-line labels with shortened parentheticals
  4. Saves as design_rendering.png (overwriting)

Run with:  python fix_region_e.py
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent
INPUT_PATH = REPO / "design_rendering.png"
OUTPUT_PATH = REPO / "design_rendering.png"

# Region E label-area pixel box (determined by inspection of 2816x1536 source).
# We white out the area BELOW the bars and re-draw labels.
# The original panel uses a near-white panel background; match it.
LABEL_BOX = (1430, 1350, 2810, 1530)
PANEL_BG = (252, 252, 252, 255)        # near-white panel background

# 6 column centers across region E's bars
COL_CENTERS_X = [1530, 1755, 1985, 2225, 2480, 2700]

# Cleaned single-line labels for each milestone
LABELS = [
    ("Today:",     "5 neurons",     "(Fu 2020)"),
    ("Year 2:",    "64K neurons",   "(attn head)"),
    ("Year 5:",    "1M neurons",    "(Loihi-2)"),
    ("Year 10:",   "1B neurons",    "(multi-chip)"),
    ("Reference:", "86B neurons",   "(brain)"),
    ("Target:",    "1T neurons",    "(LLaMA-class)"),
]


def load_font(size, bold=False):
    """Try Windows Segoe UI; fall back to PIL's bundled DejaVu."""
    candidates = []
    if bold:
        candidates += [
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ]
    else:
        candidates += [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main():
    im = Image.open(INPUT_PATH).convert("RGBA")
    draw = ImageDraw.Draw(im)
    print(f"Loaded {INPUT_PATH.name}, size = {im.size}")

    # 1. White out the existing label region
    draw.rectangle(LABEL_BOX, fill=PANEL_BG)
    print(f"  cleared box {LABEL_BOX}")

    # 2. Re-draw clean labels (large fonts for 2816 px wide image)
    font_bold = load_font(46, bold=True)
    font_regular = load_font(40, bold=False)
    font_small = load_font(32, bold=False)

    # The 3 lines are stacked vertically per column
    LINE_Y = [1365, 1420, 1475]

    for cx, (line1, line2, line3) in zip(COL_CENTERS_X, LABELS):
        # Helper to draw centered text
        def draw_centered(y, text, font, color=(30, 30, 30, 255)):
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            draw.text((cx - w // 2, y), text, fill=color, font=font)

        draw_centered(LINE_Y[0], line1, font_bold, (10, 10, 10, 255))
        draw_centered(LINE_Y[1], line2, font_regular, (40, 40, 40, 255))
        draw_centered(LINE_Y[2], line3, font_small, (90, 90, 90, 255))

    im.save(OUTPUT_PATH)
    print(f"  saved -> {OUTPUT_PATH.name}")
    print("Done.")


if __name__ == "__main__":
    main()

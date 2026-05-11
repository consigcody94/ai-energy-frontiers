"""
Top-level comparison plot: the three approaches on common axes.

Shows expected contribution to a 5 MW data-center load from each
subproject, at three plausible technology readiness levels (TRL):
  - "today"    : current published device performance
  - "5-yr"     : plausible near-term improvement
  - "ceiling"  : theoretical upper bound

Saved to comparison.png at the repo root.
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "tr_diode_data_center"))
sys.path.insert(0, str(REPO / "sed_casimir_zpe"))
sys.path.insert(0, str(REPO / "bhasma_lenr_cathode"))

import simulate as TR
import estimate as SED
import model as BH


DATA_CENTER_MW = 5.0
DATA_CENTER_MWh_year = DATA_CENTER_MW * 1000 * 8760 / 1000.0  # 43,800 MWh


def tr_diode_yields():
    """Today / 5-yr / ceiling for TR diode on 100k m^2 roof."""
    now = TR.data_center_roof_yield(device_efficiency=0.005)
    near = TR.data_center_roof_yield(device_efficiency=0.05)
    ceil = now["annual_MWh_radiative_ceiling"]
    return {
        "today":   now["annual_MWh"],
        "5-yr":    near["annual_MWh"],
        "ceiling": ceil,
    }


def sed_casimir_yields():
    """SED Casimir: with 1 mg/s Cs flow at 100 nm gap.
    today  = f_couple = 1e-8 (deeply below Schrieber upper bound)
    5-yr   = f_couple = 1e-4 (Schrieber's experimental upper bound)
    ceiling= f_couple = 1.0  (theoretical maximum)
    Convert annualized power to MWh: P (W) * 8760 / 1e6.
    """
    d = 100e-9
    flow = SED.gas_flow_atoms_per_second(1e-3, 132.9)
    out = {}
    for label, f in [("today", 1e-8), ("5-yr", 1e-4), ("ceiling", 1.0)]:
        P = SED.cavity_flow_power_W(d, SED.ATOM_VOL_HEAVY, flow, f)
        out[label] = P * 8760 / 1e6
    return out


def bhasma_yields():
    """Bhasma LENR: project to a 1 kW lab apparatus output (the UBC
    Thunderbird Reactor produces fusion events at neutron rate; the
    energy production is currently net-negative). We compute the
    *gain factor* over the UBC baseline and report MWh assuming the
    apparatus is in a future regime where the UBC baseline produces
    1 W gross from the reactor and the bhasma multiplier applies.

    today  = 1.15x (UBC foil baseline at d=10um)
    5-yr   = ~5x   (50 nm bhasma, plausible)
    ceiling= 10x   (model cap)

    Annual MWh from 1 W * 8760 hr / 1e6 = 0.00876 MWh baseline.
    """
    base_W = 1.0  # assume net-positive lab reactor produces 1 W
    out = {}
    enh_today = BH.enhancement_model(BH.UBC_BASELINE_FOIL_THICKNESS_M)
    enh_5yr = BH.enhancement_model(50e-9)
    enh_ceil = BH.ENHANCEMENT_CAP
    for label, enh in [("today", enh_today),
                       ("5-yr", enh_5yr),
                       ("ceiling", enh_ceil)]:
        out[label] = base_W * (1 + enh) * 8760 / 1e6
    return out


def main():
    tr = tr_diode_yields()
    sed = sed_casimir_yields()
    bh = bhasma_yields()

    fig, ax = plt.subplots(figsize=(11, 6))
    categories = ["today", "5-yr horizon", "theoretical\nceiling"]
    keys = ["today", "5-yr", "ceiling"]
    x = np.arange(len(categories))
    width = 0.27

    bars_tr = ax.bar(x - width, [tr[k] for k in keys], width,
                     label="TR diode + DC roof", color="#1f77b4")
    bars_sed = ax.bar(x, [sed[k] for k in keys], width,
                      label="SED Casimir flow", color="#9467bd")
    bars_bh = ax.bar(x + width, [bh[k] for k in keys], width,
                     label="Bhasma LENR", color="#2ca02c")

    ax.axhline(DATA_CENTER_MWh_year, color="red", linestyle="--",
               linewidth=1.2,
               label=f"5 MW DC annual load ({DATA_CENTER_MWh_year:.0f} MWh)")
    ax.set_yscale("symlog", linthresh=1e-12)
    ax.set_ylabel("annual MWh contribution (log scale, symmetric)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_title("Three approaches × three TRL milestones\n"
                 "all values are annual MWh delivered to a hyperscale "
                 f"({DATA_CENTER_MW:.0f} MW) data center")
    ax.legend(loc="lower right")
    ax.grid(True, axis="y", which="both", alpha=0.3)

    for bars, vals in [(bars_tr, tr), (bars_sed, sed), (bars_bh, bh)]:
        for bar, k in zip(bars, keys):
            v = vals[k]
            if v <= 0 or not np.isfinite(v):
                continue
            if v > 1e-12:
                txt = f"{v:.2e}" if (v < 0.1 or v > 1e4) else f"{v:.1f}"
                ax.text(bar.get_x() + bar.get_width() / 2,
                        max(v * 1.2, 1e-12),
                        txt, ha="center", va="bottom", fontsize=7,
                        rotation=90)

    fig.tight_layout()
    out = REPO / "comparison.png"
    fig.savefig(out, dpi=130)
    print(f"-> {out}")


if __name__ == "__main__":
    main()

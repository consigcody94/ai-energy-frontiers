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

import importlib.util

REPO = Path(__file__).resolve().parent


def load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


TR = load_by_path("tr_simulate",
                   REPO / "tr_diode_data_center" / "simulate.py")
SED = load_by_path("sed_estimate",
                    REPO / "sed_casimir_zpe" / "estimate.py")
BH = load_by_path("bh_model",
                   REPO / "bhasma_lenr_cathode" / "model.py")
BN = load_by_path("bn_estimate",
                   REPO / "bacterial_neuromorphic_substrate" / "estimate.py")


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


def bacterial_neuromorphic_avoided_MWh():
    """Demand-side savings: bacterial neuromorphic substrate reduces
    the data center's actual electricity consumption. Expressed as
    'avoided MWh' relative to the silicon baseline.

    Assumes: facility doing 1B daily inferences across all GPUs, at
    GPT-4-class scale, 500 tokens each. Difference between H100 dense
    consumption and substrate-X sparse-SNN consumption.

    today  = use demonstrated Geobacter (currently WORSE than silicon)
    5-yr   = use Loihi-2 sparse SNN (drops energy 10x)
    ceiling= use engineered Geobacter target sparse SNN (drops energy ~500x)
    """
    daily_inf = 1.0  # 1 billion daily inferences per facility
    tokens = 500

    # Silicon baseline
    baseline_TWh = BN.annual_TWh("h100_silicon", "gpt4_class", "dense",
                                  daily_inferences_billion=daily_inf,
                                  tokens_per_inference=tokens)
    baseline_MWh = baseline_TWh * 1e6

    scenarios = {
        "today":   ("geobacter_demo",              "sparse_snn"),
        "5-yr":    ("loihi2_silicon_neuromorphic", "sparse_snn"),
        "ceiling": ("geobacter_target",            "sparse_snn"),
    }
    out = {}
    for label, (substrate, arch) in scenarios.items():
        new_TWh = BN.annual_TWh(substrate, "gpt4_class", arch,
                                 daily_inferences_billion=daily_inf,
                                 tokens_per_inference=tokens)
        new_MWh = new_TWh * 1e6
        out[label] = max(0.0, baseline_MWh - new_MWh)
    return out


def main():
    tr = tr_diode_yields()
    sed = sed_casimir_yields()
    bh = bhasma_yields()
    bn = bacterial_neuromorphic_avoided_MWh()

    fig, ax = plt.subplots(figsize=(13, 6.5))
    categories = ["today", "5-yr horizon", "theoretical\nceiling"]
    keys = ["today", "5-yr", "ceiling"]
    x = np.arange(len(categories))
    width = 0.20

    bars_tr = ax.bar(x - 1.5*width, [tr[k] for k in keys], width,
                     label="TR diode (SUPPLY)", color="#1f77b4")
    bars_sed = ax.bar(x - 0.5*width, [sed[k] for k in keys], width,
                      label="SED Casimir (SUPPLY)", color="#9467bd")
    bars_bh = ax.bar(x + 0.5*width, [bh[k] for k in keys], width,
                     label="Bhasma LENR (SUPPLY)", color="#2ca02c")
    bars_bn = ax.bar(x + 1.5*width, [bn[k] for k in keys], width,
                     label="Bacterial neuromorphic (DEMAND ↓)",
                     color="#ff7f0e")

    ax.axhline(DATA_CENTER_MWh_year, color="red", linestyle="--",
               linewidth=1.2,
               label=f"5 MW DC annual load ({DATA_CENTER_MWh_year:.0f} MWh)")
    ax.set_yscale("symlog", linthresh=1e-12)
    ax.set_ylabel("annual MWh contribution (log scale, symmetric)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_title("Four approaches × three TRL milestones\n"
                 "Three SUPPLY-side (add MWh) vs one DEMAND-side (reduce MWh)\n"
                 f"all values are annual MWh on a hyperscale "
                 f"({DATA_CENTER_MW:.0f} MW) data center")
    ax.legend(loc="lower right")
    ax.grid(True, axis="y", which="both", alpha=0.3)

    for bars, vals in [(bars_tr, tr), (bars_sed, sed),
                        (bars_bh, bh), (bars_bn, bn)]:
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

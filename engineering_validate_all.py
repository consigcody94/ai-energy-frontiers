"""
Run the engineering-stress validation for all three subprojects.

Each subproject tests its hardware design against real loads:
  - TR diode panel: wind, hail, snow, thermal cycling, fatigue,
                    deflection, heat-pipe capacity, insulation, current,
                    lightning, UV, corrosion
  - SED Casimir: vacuum, vibration, cryo budget, magnetic, Cs safety
  - Bhasma LENR: furnace cycling, Hg containment, vacuum, neutron
                 shielding, HV isolation, RF, chemical

Exit non-zero if any subproject reports a FAIL.

Usage:  python engineering_validate_all.py
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SUBPROJECTS = [
    REPO / "tr_diode_data_center",
    REPO / "sed_casimir_zpe",
    REPO / "bhasma_lenr_cathode",
]


def run_one(subdir):
    print()
    print("#" * 72)
    print(f"# {subdir.name}")
    print("#" * 72)
    proc = subprocess.run(
        [sys.executable, "engineering_validate.py"],
        cwd=subdir,
    )
    return proc.returncode


def main():
    failures = 0
    for sub in SUBPROJECTS:
        if run_one(sub) != 0:
            failures += 1

    print()
    print("=" * 72)
    if failures == 0:
        print(f"ALL {len(SUBPROJECTS)} HARDWARE DESIGNS PASS ENGINEERING REVIEW")
    else:
        print(f"{failures}/{len(SUBPROJECTS)} HARDWARE DESIGNS HAVE OPEN FAIL ITEMS")
    print("=" * 72)
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()

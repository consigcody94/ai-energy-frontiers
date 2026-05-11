"""
Run the validation suite for all three subprojects in sequence.
Exit non-zero if any subproject reports a failure.

Usage:  python validate_all.py
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


def run_one(subdir: Path) -> int:
    print()
    print("#" * 70)
    print(f"# {subdir.name}")
    print("#" * 70)
    proc = subprocess.run(
        [sys.executable, "validate.py"],
        cwd=subdir,
    )
    return proc.returncode


def main():
    failures = 0
    for sub in SUBPROJECTS:
        if run_one(sub) != 0:
            failures += 1

    print()
    print("=" * 70)
    if failures == 0:
        print(f"ALL {len(SUBPROJECTS)} SUBPROJECT VALIDATION SUITES PASSED")
        sys.exit(0)
    else:
        print(f"{failures}/{len(SUBPROJECTS)} SUBPROJECT VALIDATION SUITES FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()

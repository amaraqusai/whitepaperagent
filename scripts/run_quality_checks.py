"""
Automated Project Quality & Compliance Checker
================================================
Runs all quality checks against the project files and exits
with code 0 (pass) or 1 (fail).

Usage:
    python scripts/run_quality_checks.py
"""

import sys
import os

# Allow imports from scripts/ directory
sys.path.insert(0, os.path.dirname(__file__))
from checkers import (
    check_python_syntax,
    get_bib_keys,
    check_latex_citations,
    check_latex_environments,
    check_assets,
)

# ─── File paths (relative to project root) ───────────────────────────
PYTHON_FILES = [
    "agent_system.py",
    "config.py",
    "agents.py",
    "tasks.py",
    "latex/scripts/generate_graph.py",
    "latex/scripts/generate_graph_anomalies.py",
]

BIB_PATH = "latex/references.bib"
TEX_PATH = "latex/main.tex"

REQUIRED_ASSETS = [
    "latex/figures/soc_control_room.png",
    "latex/figures/anomalies_over_time.pdf",
    "latex/figures/performance_plot.pdf",
]


def main():
    print("=" * 60)
    print("      AUTOMATED PROJECT QUALITY & COMPLIANCE CHECKER")
    print("=" * 60)

    success = True

    # 1. Python syntax
    print("\n--- 1. Python Code Quality Check ---")
    for py_file in PYTHON_FILES:
        if not check_python_syntax(py_file):
            success = False

    # 2. LaTeX source
    print("\n--- 2. LaTeX Source Check ---")
    bib_keys = get_bib_keys(BIB_PATH)
    if not check_latex_citations(TEX_PATH, bib_keys):
        success = False
    if not check_latex_environments(TEX_PATH):
        success = False

    # 3. Assets
    print("\n--- 3. Asset Verification ---")
    if not check_assets(REQUIRED_ASSETS):
        success = False

    # Result
    print("\n" + "=" * 60)
    if success:
        print("SUCCESS: All quality and compliance checks passed!")
        sys.exit(0)
    else:
        print("FAILURE: Code quality or document consistency errors found.")
        sys.exit(1)


if __name__ == "__main__":
    main()

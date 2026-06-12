"""Post-processing Pipeline."""
import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ── Paths (relative to project root) ─────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
POLISHED_TEX = ROOT / "output" / "polished_main.tex"
LATEX_DIR = ROOT / "latex"
MAIN_TEX = LATEX_DIR / "main.tex"
BIB_FILE = LATEX_DIR / "references.bib"
GRAPH_SCRIPTS = [
    ROOT / "latex" / "scripts" / "generate_graph.py",
    ROOT / "latex" / "scripts" / "generate_graph_anomalies.py",
]

GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _tag(ok: bool) -> str:
    return f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"


def step_copy_tex() -> bool:
    """Copy polished .tex → latex/main.tex (with backup)."""
    if not POLISHED_TEX.exists():
        print(f"  [!] {POLISHED_TEX} not found — skipping copy.")
        return False
    if MAIN_TEX.exists():
        bak = MAIN_TEX.with_suffix(".tex.bak")
        shutil.copy2(MAIN_TEX, bak)
        print(f"  Backed up → {bak.name}")
    shutil.copy2(POLISHED_TEX, MAIN_TEX)
    print(f"  Copied polished .tex → {MAIN_TEX}")
    return True


def step_generate_graphs() -> bool:
    """Run graph-generation scripts."""
    ok = True
    for script in GRAPH_SCRIPTS:
        if not script.exists():
            print(f"  [!] Script not found: {script.name}")
            ok = False
            continue
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(script.parent),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  [!] {script.name} failed:\n{result.stderr[:500]}")
            ok = False
        else:
            print(f"  ✓ {script.name}")
    return ok


def step_build_latex() -> bool:
    """Invoke the build module's build() function."""
    # Import locally so the module is optional at import time.
    from build import build  # noqa: WPS433

    return build(source=MAIN_TEX, output_dir=LATEX_DIR)


def step_quality_checks() -> bool:
    """Run quality & compliance checks via scripts/checkers.py."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from checkers import (  # noqa: WPS433
        check_latex_citations,
        check_latex_environments,
        get_bib_keys,
    )
    sys.path.pop(0)

    tex = str(MAIN_TEX)
    bib = str(BIB_FILE)
    env_ok = check_latex_environments(tex)
    bib_keys = get_bib_keys(bib)
    cite_ok = check_latex_citations(tex, bib_keys) if bib_keys else False
    return env_ok and cite_ok


def main() -> None:
    """Run the full post-processing pipeline."""
    parser = argparse.ArgumentParser(
        description="Post-processing pipeline for the whitepaper.",
    )
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--skip-graphs", action="store_true")
    parser.add_argument("--skip-quality", action="store_true")
    args = parser.parse_args()

    print(f"\n{BOLD}═══ Post-Processing Pipeline ═══{RESET}\n")
    t0 = time.perf_counter()
    results: dict[str, bool] = {}

    # 1. Copy .tex
    print(f"{BOLD}1. Copy polished .tex{RESET}")
    results["Copy .tex"] = step_copy_tex()

    # 2. Graphs
    if args.skip_graphs:
        print(f"{BOLD}2. Graphs{RESET}  [skipped]")
    else:
        print(f"{BOLD}2. Generate graphs{RESET}")
        results["Graphs"] = step_generate_graphs()

    # 3. Build
    if args.skip_build:
        print(f"\n{BOLD}3. LaTeX build{RESET}  [skipped]")
    else:
        print(f"\n{BOLD}3. LaTeX build{RESET}")
        results["LaTeX build"] = step_build_latex()

    # 4. Quality
    if args.skip_quality:
        print(f"\n{BOLD}4. Quality checks{RESET}  [skipped]")
    else:
        print(f"\n{BOLD}4. Quality checks{RESET}")
        results["Quality"] = step_quality_checks()

    # ── Summary ───────────────────────────────────────────────────────
    elapsed = time.perf_counter() - t0
    print(f"\n{BOLD}{'─' * 40}")
    print(f" Pipeline Summary  ({elapsed:.1f}s)")
    print(f"{'─' * 40}{RESET}")
    for name, ok in results.items():
        print(f"  [{_tag(ok)}]  {name}")
    all_ok = all(results.values()) if results else False
    print(f"\n  Overall: [{_tag(all_ok)}]")
    print()
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

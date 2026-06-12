"""Automated LaTeX Build Script."""
import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ── ANSI colour helpers ───────────────────────────────────────────────
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

MIKTEX_BIN = (
    r"C:\Users\USER\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
)


def _ensure_miktex_path() -> None:
    """Add MiKTeX bin directory to PATH on Windows if absent."""
    if platform.system() != "Windows":
        return
    if MIKTEX_BIN.lower() not in os.environ.get("PATH", "").lower():
        os.environ["PATH"] = MIKTEX_BIN + os.pathsep + os.environ["PATH"]
        print(f"[info] Added MiKTeX to PATH: {MIKTEX_BIN}")


def _status(label: str, ok: bool) -> None:
    """Print a coloured PASS / FAIL line."""
    tag = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"  [{tag}] {label}")


def run_step(
    cmd: list[str],
    label: str,
    cwd: str | Path,
) -> bool:
    """Execute *cmd* in *cwd* and return True on success."""
    print(f"\n{BOLD}▸ {label}{RESET}")
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        _status(label, False)
        sys.stderr.write(result.stdout[-2000:] if result.stdout else "")
        sys.stderr.write(result.stderr[-2000:] if result.stderr else "")
        return False
    _status(label, True)
    return True


def clean_artifacts(output_dir: Path) -> None:
    """Delete common LaTeX build artefacts from *output_dir*."""
    exts = {
        ".aux", ".bbl", ".bcf", ".blg", ".log", ".out",
        ".run.xml", ".toc", ".lof", ".lot", ".fls",
        ".fdb_latexmk", ".synctex.gz",
    }
    removed = 0
    for path in output_dir.iterdir():
        if path.suffix in exts:
            path.unlink(missing_ok=True)
            removed += 1
    print(f"[info] Removed {removed} build artefact(s) from {output_dir}")


def build(source: Path, output_dir: Path) -> bool:
    """Run the full 4-pass compilation. Return True on success."""
    _ensure_miktex_path()
    stem = source.stem
    cwd = source.parent
    xelatex_cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        f"-output-directory={output_dir.resolve()}",
        str(source.name),
    ]
    biber_cmd = ["biber", str(output_dir.resolve() / stem)]
    steps: list[tuple[list[str], str]] = [
        (xelatex_cmd, "xelatex  (pass 1)"),
        (biber_cmd, "biber"),
        (xelatex_cmd, "xelatex  (pass 2)"),
        (xelatex_cmd, "xelatex  (pass 3)"),
    ]
    for cmd, label in steps:
        if not run_step(cmd, label, cwd):
            return False
    return True


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compile a LaTeX document (4-pass pipeline).",
    )
    parser.add_argument(
        "--source", default="latex/main.tex",
        help="Path to the main .tex file (default: latex/main.tex)",
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Build output directory (default: same as source dir)",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Delete build artefacts before compiling",
    )
    parser.add_argument(
        "--open", action="store_true", dest="open_pdf",
        help="Open the generated PDF after a successful build",
    )
    args = parser.parse_args()
    source = Path(args.source).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else source.parent
    if args.clean:
        clean_artifacts(output_dir)
    t0 = time.perf_counter()
    ok = build(source, output_dir)
    elapsed = time.perf_counter() - t0
    print(f"\n{'=' * 50}")
    _status(f"Build {'succeeded' if ok else 'FAILED'}", ok)
    print(f"  Total time: {elapsed:.1f}s")
    print(f"{'=' * 50}")
    if ok and args.open_pdf:
        pdf = output_dir / (source.stem + ".pdf")
        if pdf.exists():
            if platform.system() == "Windows":
                os.startfile(str(pdf))  # noqa: S606
            elif shutil.which("xdg-open"):
                subprocess.Popen(["xdg-open", str(pdf)])
            else:
                print(f"[info] PDF ready at {pdf}")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()

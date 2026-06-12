"""Command-Line Interface for the Whitepaper Agent Project."""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ─── ANSI Color Helpers ──────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"


def _colored(text: str, color: str) -> str: return f"{color}{text}{RESET}"

def _banner() -> None:
    print(_colored("=" * 60, CYAN))
    print(_colored(f"  WHITEPAPER AGENT — CLI v{VERSION}", BOLD + CYAN))
    print(_colored("=" * 60, CYAN) + "\n")

def _info(msg: str) -> None: print(_colored(f"[INFO]  {msg}", GREEN))
def _warn(msg: str) -> None: print(_colored(f"[WARN]  {msg}", YELLOW))
def _error(msg: str) -> None: print(_colored(f"[ERROR] {msg}", RED))


# ─── Subcommand Handlers ─────────────────────────────────────────────
def cmd_run(args: argparse.Namespace) -> None:
    """Run the full CrewAI agent pipeline."""
    if args.dry_run:
        _info("Dry-run mode — pipeline will NOT execute.")
        _info("Would run: agent_system.main()")
        return
    _info("Starting CrewAI multi-agent pipeline …")
    try:
        from agent_system import main as run_pipeline  # noqa: WPS433
        run_pipeline()
    except ImportError as exc:
        _error(f"Import failed: {exc}")
        sys.exit(1)


def cmd_build(args: argparse.Namespace) -> None:
    """Compile the LaTeX document (4-pass xelatex + biber)."""
    tex_dir = PROJECT_ROOT / "latex"
    tex_file = tex_dir / "main.tex"
    if not tex_file.exists():
        _error(f"LaTeX source not found: {tex_file}")
        sys.exit(1)
    passes = ["xelatex", "biber", "xelatex", "xelatex"]
    for step in passes:
        target = "main" if step == "biber" else "main.tex"
        _info(f"Running {step} {target} …")
        result = subprocess.run(
            [step, "-interaction=nonstopmode", target],
            cwd=str(tex_dir),
            capture_output=not args.verbose,
        )
        if result.returncode != 0:
            _error(f"{step} failed (exit {result.returncode}).")
            sys.exit(result.returncode)
    _info("LaTeX build completed successfully.")


def cmd_check(args: argparse.Namespace) -> None:
    _info("Running quality & compliance checks …")
    check_script = PROJECT_ROOT / "src" / "scripts" / "run_quality_checks.py"
    if not check_script.exists():
        _error(f"Check script not found: {check_script}")
        sys.exit(1)
    result = subprocess.run(
        [sys.executable, str(check_script)], cwd=str(PROJECT_ROOT)
    )
    sys.exit(result.returncode)


def cmd_graphs(args: argparse.Namespace) -> None:
    scripts_dir = PROJECT_ROOT / "latex" / "scripts"
    graph_scripts = sorted(scripts_dir.glob("generate_graph*.py"))
    if not graph_scripts:
        _warn("No graph scripts found in latex/scripts/.")
        return
    for script in graph_scripts:
        _info(f"Generating graph: {script.name}")
        result = subprocess.run(
            [sys.executable, str(script)], cwd=str(PROJECT_ROOT)
        )
        if result.returncode != 0:
            _error(f"{script.name} failed (exit {result.returncode}).")


def cmd_status(args: argparse.Namespace) -> None:
    key_files = [
        "src/agent_system.py", "src/agents.py", "src/tasks.py", "src/config.py",
        "src/cli.py", "src/logger_setup.py", "latex/main.tex",
        "latex/references.bib", "src/scripts/run_quality_checks.py",
    ]
    _info("Project file status:")
    header = f"  {'File':<35} {'Lines':>6}  {'Modified':<20}  Status"
    print(_colored(header, BOLD))
    print("  " + "-" * 75)
    for rel in key_files:
        path = PROJECT_ROOT / rel
        if path.exists():
            lines = len(path.read_text(encoding="utf-8").splitlines())
            mtime = datetime.fromtimestamp(
                os.path.getmtime(path)
            ).strftime("%Y-%m-%d %H:%M")
            status = _colored("OK", GREEN)
        else:
            lines, mtime, status = 0, "—", _colored("MISSING", RED)
        print(f"  {rel:<35} {lines:>6}  {mtime:<20}  {status}")


# ─── Argument Parser ─────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="whitepaperagent",
        description="CLI for the Autonomous Threat Hunting Whitepaper project.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    run_p = sub.add_parser("run", help="Run the CrewAI agent pipeline.")
    run_p.add_argument("--dry-run", action="store_true", help="Simulate run.")
    sub.add_parser("build", help="Compile LaTeX (xelatex + biber).")
    sub.add_parser("check", help="Run checks.")
    sub.add_parser("graphs", help="Generate graphs.")
    sub.add_parser("status", help="Show status.")
    return parser

DISPATCH = {
    "run": cmd_run, "build": cmd_build, "check": cmd_check,
    "graphs": cmd_graphs, "status": cmd_status,
}
if __name__ == "__main__":
    _banner()
    cli_parser = build_parser()
    cli_args = cli_parser.parse_args()
    DISPATCH[cli_args.command](cli_args)

"""
Configuration & Environment Setup for the CrewAI Pipeline
==========================================================
Loads API keys, configures the LLM, reads project input files,
and defines shared constants used by the agent and task modules.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crewai import LLM

# ─── Load environment variables from .env ────────────────────────────
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("=" * 60)
    print("ERROR: GEMINI_API_KEY environment variable is not set.")
    print("Please create a .env file with: GEMINI_API_KEY=your-key")
    print("Or set it in your shell:")
    print('  PowerShell:  $env:GEMINI_API_KEY = "your-key"')
    print('  Bash:        export GEMINI_API_KEY="your-key"')
    print("=" * 60)
    sys.exit(1)

# ─── Configure the LLM (Gemini via LiteLLM) ─────────────────────────
# The "gemini/" prefix is required by LiteLLM for proper routing.
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=api_key,
    temperature=0.7,
)

# ─── Ensure output directory exists ──────────────────────────────────
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# ─── Read the project outline if available ───────────────────────────
outline_path = Path("docs/OUTLINE.md")
if outline_path.exists():
    outline_content = outline_path.read_text(encoding="utf-8")
else:
    outline_content = "Topic: Autonomous Threat Hunting using LLMs in Enterprise Networks"

research_notes_path = Path("docs/RESEARCH_NOTES.md")
if research_notes_path.exists():
    research_notes = research_notes_path.read_text(encoding="utf-8")
else:
    research_notes = ""

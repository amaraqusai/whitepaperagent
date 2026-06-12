"""
Autonomous Threat Hunting Whitepaper — CrewAI Multi-Agent Pipeline
==================================================================
Main entry point that assembles the Crew from the agent and task
modules and kicks off the sequential pipeline.

Pipeline:  Researcher → Data Scientist → Markdown Writer
           → LaTeX Typesetter → QA Editor

Requirements:
    pip install -r requirements.txt

Usage:
    1. Set your API key in .env:  GEMINI_API_KEY=your-key-here
    2. Run:  python agent_system.py
"""

from crewai import Crew, Process

from config import OUTPUT_DIR
from agents import (
    researcher,
    data_scientist,
    markdown_writer,
    latex_typesetter,
    qa_editor,
)
from tasks import (
    research_task,
    data_science_task,
    markdown_draft_task,
    latex_conversion_task,
    qa_review_task,
)


# ══════════════════════════════════════════════════════════════════════
# CREW ASSEMBLY & EXECUTION
# ══════════════════════════════════════════════════════════════════════

whitepaper_crew = Crew(
    agents=[
        researcher,
        data_scientist,
        markdown_writer,
        latex_typesetter,
        qa_editor,
    ],
    tasks=[
        research_task,
        data_science_task,
        markdown_draft_task,
        latex_conversion_task,
        qa_review_task,
    ],
    process=Process.sequential,
    verbose=True,
)


def main():
    """Run the full multi-agent whitepaper generation pipeline."""
    print("=" * 70)
    print("  AUTONOMOUS THREAT HUNTING WHITEPAPER — CrewAI Agent Pipeline")
    print("=" * 70)
    print(f"  Model:       gemini/gemini-2.0-flash")
    print(f"  Agents:      5 (Researcher → Data Scientist → Writer → Typesetter → Editor)")
    print(f"  Process:     Sequential")
    print(f"  Output Dir:  {OUTPUT_DIR.resolve()}")
    print("=" * 70)
    print()

    result = whitepaper_crew.kickoff()

    print()
    print("=" * 70)
    print("  PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("  Generated artifacts:")
    print(f"    1. {OUTPUT_DIR / 'research_brief.md'}      — Research dossier")
    print(f"    2. {OUTPUT_DIR / 'math_and_plots.md'}      — Math models & scripts")
    print(f"    3. {OUTPUT_DIR / 'article_draft.md'}       — Markdown article draft")
    print(f"    4. {OUTPUT_DIR / 'draft_main.tex'}         — Raw LaTeX draft")
    print(f"    5. {OUTPUT_DIR / 'polished_main.tex'}      — Final polished LaTeX")
    print()
    print("  Next steps:")
    print("    1. Review the Markdown draft: output/article_draft.md")
    print("    2. Copy polished_main.tex to latex/main.tex (if satisfied)")
    print("    3. Compile with: cd latex && xelatex main.tex → biber main → xelatex (×2)")
    print()

    return result


if __name__ == "__main__":
    main()

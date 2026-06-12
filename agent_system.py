"""
Autonomous Threat Hunting Whitepaper — CrewAI Multi-Agent Pipeline
==================================================================
This script orchestrates a team of 5 specialized AI agents using the
CrewAI framework to autonomously research, analyze, draft, typeset,
and quality-review a 15-page academic whitepaper on LLM-driven threat
hunting in enterprise networks.

Pipeline:  Researcher → Data Scientist → Markdown Writer → LaTeX Typesetter → QA Editor

Requirements:
    pip install -r requirements.txt

Usage:
    1. Set your API key in .env:  GEMINI_API_KEY=your-key-here
    2. Run:  python agent_system.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

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
outline_path = Path("OUTLINE.md")
if outline_path.exists():
    outline_content = outline_path.read_text(encoding="utf-8")
else:
    outline_content = "Topic: Autonomous Threat Hunting using LLMs in Enterprise Networks"

research_notes_path = Path("RESEARCH_NOTES.md")
if research_notes_path.exists():
    research_notes = research_notes_path.read_text(encoding="utf-8")
else:
    research_notes = ""


# ══════════════════════════════════════════════════════════════════════
# AGENT DEFINITIONS — 5 specialized roles
# ══════════════════════════════════════════════════════════════════════

researcher = Agent(
    role="Lead Academic Researcher",
    goal=(
        "Conduct exhaustive research on LLM-driven autonomous threat hunting "
        "in enterprise networks. Gather quantitative cybersecurity statistics, "
        "threat landscape data, MITRE ATT&CK technique mappings, and compile "
        "a comprehensive BibTeX-formatted reference list."
    ),
    backstory=(
        "You are a senior cybersecurity researcher with 15+ years of experience "
        "in threat intelligence and academic publishing. You hold a Ph.D. in "
        "Information Security and have published extensively on anomaly detection "
        "and adversarial machine learning. You are meticulous about data accuracy "
        "and always verify statistics from primary sources such as Verizon DBIR, "
        "MITRE ATT&CK, and IEEE/ACM journals."
    ),
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)

data_scientist = Agent(
    role="AI Security Data Scientist",
    goal=(
        "Formulate the mathematical framework for Bayesian threat scoring, "
        "derive the economic cost optimization formula for decision thresholds, "
        "and write Python matplotlib scripts that generate publication-quality "
        "vector graphs comparing LLM vs. heuristic detection performance."
    ),
    backstory=(
        "You are a data scientist specializing in applied Bayesian inference "
        "for cybersecurity applications. You have a strong background in "
        "statistical modeling, information theory, and Python data visualization. "
        "You think in equations first and code second, ensuring every plot "
        "has properly labeled axes, legends, and captions suitable for "
        "academic publication."
    ),
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)

markdown_writer = Agent(
    role="Senior Technical Writer (Markdown)",
    goal=(
        "Transform the raw research brief and data scientist output into a "
        "well-structured, comprehensive Markdown article draft covering all "
        "15 planned pages. The draft must include all sections from the outline, "
        "written in Hebrew with embedded English technical terms."
    ),
    backstory=(
        "You are a bilingual (Hebrew/English) technical writer with deep "
        "expertise in cybersecurity documentation. You previously authored "
        "multiple whitepapers for Israeli defense contractors and academic "
        "institutions. You understand Hebrew academic register and can "
        "seamlessly integrate English technical terminology (like SOC, LLM, "
        "RAG, MITRE ATT&CK) within Hebrew prose. You always write in clear, "
        "professional academic Hebrew."
    ),
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)

latex_typesetter = Agent(
    role="LaTeX Typesetter & Document Engineer",
    goal=(
        "Convert the approved Markdown draft into a fully compilable XeLaTeX "
        "document. The output must include: a formatted cover page, table of "
        "contents, headers/footers via fancyhdr, at least one TikZ block "
        "diagram, at least one tabularx table with booktabs, properly numbered "
        "equations using amsmath, includegraphics for figures, and a biblatex "
        "bibliography with biber backend."
    ),
    backstory=(
        "You are an expert LaTeX typesetter who has formatted hundreds of "
        "academic papers, including complex bilingual Hebrew/English documents. "
        "You are deeply familiar with XeLaTeX, polyglossia, bidi, fontspec, "
        "TikZ, amsmath, biblatex, fancyhdr, and hyperref. You ensure every "
        "\\begin{} has a matching \\end{}, every \\cite{} has a matching "
        "entry in the .bib file, and every cross-reference resolves correctly "
        "after 4 compilation passes."
    ),
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)

qa_editor = Agent(
    role="Senior Technical Editor & QA Engineer",
    goal=(
        "Review the generated LaTeX document for: correct Hebrew/English BiDi "
        "rendering, balanced \\begin{}/\\end{} environments, valid TikZ syntax, "
        "tables that fit within page margins, clickable hyperref citations, "
        "and overall compilation readiness. Fix any issues found."
    ),
    backstory=(
        "You are a QA engineer who specializes in LaTeX document validation. "
        "You have an eye for detail and can spot unclosed environments, missing "
        "packages, and BiDi rendering glitches at a glance. You verify that "
        "every \\cite{} command has a matching .bib entry, every \\label{} has "
        "a corresponding \\ref{}, and all hyperlinks are clickable. You also "
        "check that the document compiles cleanly with XeLaTeX + Biber without "
        "warnings or errors."
    ),
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False,
)


# ══════════════════════════════════════════════════════════════════════
# TASK DEFINITIONS — Sequential pipeline with file outputs
# ══════════════════════════════════════════════════════════════════════

research_task = Task(
    description=(
        f"Using the following project outline and existing research notes, "
        f"compile a comprehensive research brief for an academic whitepaper "
        f"on Autonomous Threat Hunting using LLMs.\n\n"
        f"PROJECT OUTLINE:\n{outline_content}\n\n"
        f"EXISTING RESEARCH NOTES:\n{research_notes[:3000]}\n\n"
        f"Your deliverables:\n"
        f"1. A structured research brief with quantitative data points\n"
        f"2. Key statistics (detection rates, false positive rates, MTTR)\n"
        f"3. MITRE ATT&CK technique mappings relevant to the framework\n"
        f"4. A list of 8-10 academic references in BibTeX format\n"
        f"5. A summary of the current threat landscape (2024-2025)"
    ),
    expected_output=(
        "A detailed Markdown research brief (at least 1500 words) with "
        "organized sections, quantitative data points, BibTeX references, "
        "and a threat landscape summary."
    ),
    agent=researcher,
    output_file=str(OUTPUT_DIR / "research_brief.md"),
)

data_science_task = Task(
    description=(
        "Based on the research brief provided by the previous agent, "
        "perform the following:\n\n"
        "1. Define the complete Bayesian Threat Scoring mathematical model:\n"
        "   - Prior probability P(T)\n"
        "   - Likelihood P(A|T) and P(A|¬T)\n"
        "   - Posterior computation P(T|A) using Bayes' theorem\n"
        "   - Extension to multiple independent indicators\n\n"
        "2. Derive the economic cost optimization formula:\n"
        "   - Define C_FP (cost of false positive) and C_FN (cost of false negative)\n"
        "   - Derive optimal threshold S* = C_FP / (C_FP + C_FN)\n"
        "   - Provide numerical examples for 3 industry sectors\n\n"
        "3. Define Shannon Entropy H(X) for anomaly quantification\n\n"
        "4. Write a complete Python matplotlib script that generates a "
        "time-series graph comparing LLM-detected anomalies vs. heuristic "
        "detection over a 24-hour period."
    ),
    expected_output=(
        "A Markdown document containing:\n"
        "1. All mathematical equations in LaTeX notation\n"
        "2. Numerical examples with step-by-step calculations\n"
        "3. A complete, runnable Python script for graph generation\n"
        "4. Industry cost comparison table data"
    ),
    agent=data_scientist,
    context=[research_task],
    output_file=str(OUTPUT_DIR / "math_and_plots.md"),
)

markdown_draft_task = Task(
    description=(
        "Using the research brief and data scientist output, write a complete "
        "~15-page academic article draft in MARKDOWN format.\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "- Write primarily in Hebrew with embedded English technical terms\n"
        "- Include ALL sections from the outline\n"
        "- Include placeholders for: 1 image, 1 graph, 1 table, 1 TikZ diagram\n"
        "- Include all mathematical equations\n"
        "- Mark where citations should appear using [Author, Year] format\n"
        "- Include a cover page section with:\n"
        "  - Title (Hebrew + English)\n"
        "  - Author name\n"
        "  - Date\n"
        "  - Course name\n"
        "  - Lecturer name\n\n"
        "The Markdown draft will be reviewed before LaTeX conversion."
    ),
    expected_output=(
        "A complete Markdown article draft (~8000-10000 words) with all "
        "sections, written in Hebrew with English terms, including "
        "placeholders for figures, tables, and equations."
    ),
    agent=markdown_writer,
    context=[research_task, data_science_task],
    output_file=str(OUTPUT_DIR / "article_draft.md"),
)

latex_conversion_task = Task(
    description=(
        "Convert the Markdown draft into a complete, compilable XeLaTeX "
        "document. The LaTeX file must include:\n\n"
        "STRUCTURAL REQUIREMENTS:\n"
        "- \\documentclass{article} with appropriate options\n"
        "- Packages: fontspec, polyglossia, amsmath, graphicx, tikz, "
        "  fancyhdr, biblatex, hyperref, tabularx, booktabs, listings\n"
        "- Hebrew as main language, English as other language\n"
        "- A formatted cover page (titlepage environment)\n"
        "- \\tableofcontents\n"
        "- Headers and footers on every page\n\n"
        "CONTENT REQUIREMENTS:\n"
        "- At least 1 \\includegraphics (for the SOC image or graph)\n"
        "- At least 1 TikZ block diagram of the ATH architecture\n"
        "- At least 1 tabularx table with booktabs rules\n"
        "- At least 1 numbered equation (equation environment)\n"
        "- At least 1 chapter with mixed Hebrew/English BiDi text\n"
        "- \\cite{} commands linking to references.bib\n"
        "- \\printbibliography at the end\n\n"
        "Output ONLY valid, compilable LaTeX code."
    ),
    expected_output=(
        "A complete .tex file that compiles with XeLaTeX + Biber without "
        "errors. All environments properly closed, all citations valid."
    ),
    agent=latex_typesetter,
    context=[markdown_draft_task],
    output_file=str(OUTPUT_DIR / "draft_main.tex"),
)

qa_review_task = Task(
    description=(
        "Review the LaTeX document for technical correctness:\n\n"
        "CHECK LIST:\n"
        "1. Every \\begin{} has a matching \\end{}\n"
        "2. All \\cite{} keys exist in references.bib\n"
        "3. TikZ paths are closed and arrows are properly defined\n"
        "4. Tables fit within \\textwidth (use tabularx, not tabular)\n"
        "5. Math equations compile (no missing $ signs or unescaped _)\n"
        "6. BiDi text switches are correct (\\LRE{}, \\begin{english})\n"
        "7. hyperref is loaded and colorlinks is set\n"
        "8. fancyhdr is configured with head/foot rules\n"
        "9. All \\includegraphics paths are valid\n"
        "10. Page count is approximately 15 pages\n\n"
        "Fix any issues found and output the final polished LaTeX code."
    ),
    expected_output=(
        "The final, polished, error-free LaTeX document ready for "
        "4-pass XeLaTeX + Biber compilation."
    ),
    agent=qa_editor,
    context=[latex_conversion_task],
    output_file=str(OUTPUT_DIR / "polished_main.tex"),
)


# ══════════════════════════════════════════════════════════════════════
# CREW ASSEMBLY & EXECUTION
# ══════════════════════════════════════════════════════════════════════

whitepaper_crew = Crew(
    agents=[researcher, data_scientist, markdown_writer, latex_typesetter, qa_editor],
    tasks=[research_task, data_science_task, markdown_draft_task, latex_conversion_task, qa_review_task],
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
    print("    2. Copy polished_main.tex to main.tex (if satisfied)")
    print("    3. Compile with: xelatex main.tex → biber main → xelatex (×2)")
    print()

    return result


if __name__ == "__main__":
    main()

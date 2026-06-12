"""Task definitions for the CrewAI whitepaper pipeline."""

from crewai import Task
from config import OUTPUT_DIR, outline_content, research_notes
from agents import researcher, data_scientist, markdown_writer, latex_typesetter, qa_editor

# ── Task 1: Academic Research ────────────────────────────────────────
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

# ── Task 2: Mathematical Modeling & Visualizations ───────────────────
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

# ── Task 3: Markdown Article Draft ───────────────────────────────────
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

# ── Task 4: LaTeX Conversion ────────────────────────────────────────
# Converts the Markdown article draft into compilable XeLaTeX code.
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
        "CONTENT: >=1 \\includegraphics, >=1 TikZ diagram, >=1 tabularx table, "
        ">=1 numbered equation, >=1 BiDi chapter, \\cite{} commands, "
        "and \\printbibliography. Output ONLY valid, compilable LaTeX code."
    ),
    expected_output=(
        "A complete .tex file that compiles with XeLaTeX + Biber without "
        "errors. All environments properly closed, all citations valid."
    ),
    agent=latex_typesetter,
    context=[markdown_draft_task],
    output_file=str(OUTPUT_DIR / "draft_main.tex"),
)

# ── Task 5: QA Review & Polish ──────────────────────────────────────
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

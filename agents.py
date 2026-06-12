"""
Agent Definitions for the CrewAI Whitepaper Pipeline
=====================================================
Defines the 5 specialized agents that form the sequential
research-to-publication pipeline.
"""

from crewai import Agent
from config import gemini_llm
from tools import FileWriterTool, LaTeXValidatorTool, BibTeXLookupTool, WordCountTool

file_writer = FileWriterTool()
latex_validator = LaTeXValidatorTool()
bibtex_lookup = BibTeXLookupTool()
word_counter = WordCountTool()


# ── Agent 1 ──────────────────────────────────────────────────────────
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
    tools=[file_writer, bibtex_lookup],
    verbose=True,
    allow_delegation=False,
)

# ── Agent 2 ──────────────────────────────────────────────────────────
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
    tools=[file_writer],
    verbose=True,
    allow_delegation=False,
)

# ── Agent 3 ──────────────────────────────────────────────────────────
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
    tools=[file_writer, word_counter],
    verbose=True,
    allow_delegation=False,
)

# ── Agent 4 ──────────────────────────────────────────────────────────
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
    tools=[file_writer, latex_validator],
    verbose=True,
    allow_delegation=False,
)

# ── Agent 5 ──────────────────────────────────────────────────────────
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
    tools=[file_writer, latex_validator, bibtex_lookup],
    verbose=True,
    allow_delegation=False,
)

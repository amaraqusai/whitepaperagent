# 🤖 AI-Assisted Workflow & Development Log: ATH-LLM

## 1. Pipeline Evolution & System Design

The project evolved from a single-agent baseline text generator into a robust, structured **5-agent sequential CrewAI pipeline**. Below is a log of the design changes made during this evolution:

### Version 1.0 (Single GenAI SDK script)
* **Design**: A simple Python script invoking the Gemini API directly with a long prompt to output raw text.
* **Limitations**: High rate of hallucinations, lack of mathematical consistency, LaTeX formatting errors (unclosed environments, reverse direction brackets), and bibliography entries that did not match citations.
* **Outcome**: Deprecated.

### Version 2.0 (Modular Multi-Agent Architecture)
* **Design**: Rebuilt using the **CrewAI** framework with 5 sequential agents.
* **Advantage**: Separates concerns (research -> math/plots -> writer -> typesetter -> editor). Each agent validates or enriches the output of the previous agent.
* **Outcome**: High consistency, clean equations, valid TikZ diagram blocks, and compiled output.

---

## 2. Agent Prompt Engineering & BACKSTORY Registry

Each agent in `agent_system.py` is configured with a custom `role`, `goal`, and `backstory` to align its cognitive capabilities with the task.

### 1. Lead Academic Researcher
* **Role**: `Lead Academic Researcher`
* **Goal**: Conduct research on LLM threat hunting. Gather statistics, MITRE ATT&CK mappings, and compile 10 BibTeX references.
* **Backstory**: Ph.D. in Information Security, 15+ years experience in academic publishing. Meticulous about citation matching and database integrity.

### 2. AI Security Data Scientist
* **Role**: `AI Security Data Scientist`
* **Goal**: Formulate the Bayesian threat scoring math, derive the economic cost optimization threshold, and write Python plotting code.
* **Backstory**: Expert in applied Bayesian inference, mathematical modeling, and matplotlib visualization.

### 3. Senior Technical Writer (Markdown)
* **Role**: `Senior Technical Writer (Markdown)`
* **Goal**: Write the complete ~15-page article in Markdown (Hebrew with English terms) based on research and math briefs.
* **Backstory**: Bilingual technical author who has written papers for Israeli defense contractors and academic computer science departments.

### 4. LaTeX Typesetter & Document Engineer
* **Role**: `LaTeX Typesetter & Document Engineer`
* **Goal**: Convert Markdown draft to a compilable XeLaTeX source file containing fancyhdr, TikZ, and biblatex.
* **Backstory**: LaTeX formatting engineer specializing in polyglossia and bidi setups.

### 5. Senior Technical Editor & QA Engineer
* **Role**: `Senior Technical Editor & QA Engineer`
* **Goal**: Audit LaTeX source for balanced environments, citation key matches, TikZ paths, and margins.
* **Backstory**: Code QA tester specializing in LaTeX document validation and error prevention.

---

## 3. LaTeX Technical Implementation Rationale

During the typesetter and editor agent design, several technical challenges were solved to achieve clean Hebrew/English output:

### 1. Engine Selection: XeLaTeX vs. pdfLaTeX
* **Decision**: We selected **XeLaTeX**.
* **Reasoning**: pdfLaTeX does not support modern Unicode TrueType fonts natively. Hebrew requires complex font mapping. XeLaTeX uses the `fontspec` package, allowing us to load standard system fonts like Arial or Times New Roman, which are pre-installed on the Windows host running the pipeline.

### 2. Bidirectional (BiDi) Formatting & Polyglossia
* **Decision**: Configured `polyglossia` with main language `hebrew` and other language `english`.
* **Reasoning**: This handles the right-to-left (RTL) flow for text sections automatically.
* **BiDi Glitch Prevention**: When rendering mixed English and Hebrew sentences, brackets and punctuation can shift to the wrong side of the line. We resolved this by wrapping English blocks in `\LRE{...}` (Left-to-Right English) for short phrases and using `\begin{otherlanguage}{english}...\end{otherlanguage}` for full English paragraphs.

### 3. Preventing Graphics and Code Mirroring
* **Decision**: Wrapped all TikZ diagrams, listings, and figures in `\begin{LTR}...\end{LTR}` environments.
* **Reasoning**: Under a Hebrew main language configuration, LaTeX attempts to render TikZ nodes and code listings from right-to-left. This mirrors coordinate positions in diagrams and scrambles Python syntax spacing. Forcing LTR direction rules locally preserves diagram layout and code syntax.

---

## 4. Version Control & API Security Standards

* **Secrets Management**: The Gemini API key is managed via a `.env` file and loaded into the environment at runtime using `python-dotenv`.
* **Git Security**: The `.gitignore` file is configured to exclude:
  * Local secret files (`.env`).
  * Python cache directories (`__pycache__/`, `.pytest_cache/`).
  * LaTeX auxiliary compile outputs (`.aux`, `.bbl`, `.blg`, `.log`, `.toc`, `.run.xml`, `.bcf`).
  This ensures that only clean source files (`.tex`, `.bib`, `.py`, `.md`) are tracked and pushed to the repository.

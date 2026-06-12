# 🖥️ UI/UX Design & User-Facing Showcase: ATH-LLM

## 1. System Execution & CLI Interface

The primary user-facing interface for the **Autonomous Threat Hunting (ATH)** system is a Python command-line interface (CLI) configured via environment variables.

### Initial Configuration (.env)
Users configure the system by establishing a local `.env` file containing access tokens for the large language model providers:
```env
GEMINI_API_KEY=your-api-key-here
GOOGLE_API_KEY=your-api-key-here
```

### CLI Execution
The pipeline is launched using a simple terminal command:
```bash
python agent_system.py
```

---

## 2. Interactive Console Output (UX Sequence)

When executed, the system provides real-time logging of each agent's execution phase. Below is a text-based representation of the interactive console output:

```text
======================================================================
  AUTONOMOUS THREAT HUNTING WHITEPAPER — CrewAI Agent Pipeline
======================================================================
  Model:       gemini/gemini-2.0-flash
  Agents:      5 (Researcher → Data Scientist → Writer → Typesetter → Editor)
  Process:     Sequential
  Output Dir:  C:\Users\USER\OneDrive\Desktop\whitepaperagent\whitepaperagent\output
======================================================================

[Agent 1: Lead Academic Researcher] Starting task...
----------------------------------------------------------------------
> Backstory: Senior cybersecurity researcher specializing in threat intelligence.
> Goal: Search literature, compile 10 BibTeX sources, and summarize threat statistics.
> Running local RAG & Web Search...
> Formatting reference list in IEEE style...
-> Research brief saved to output/research_brief.md

[Agent 2: AI Security Data Scientist] Starting task...
----------------------------------------------------------------------
> Backstory: Applied Bayesian statistician specializing in threat models.
> Goal: Formulate equations, calculate industry costs, write Python plotting code.
> Deriving optimal decision boundary S* = C_FP / (C_FP + C_FN)...
> Writing matplotlib scripts to scripts/generate_graph.py...
-> Math & plots saved to output/math_and_plots.md

[Agent 3: Senior Technical Writer] Starting task...
----------------------------------------------------------------------
> Backstory: Bilingual Hebrew/English cybersecurity documentation author.
> Goal: Draft complete 15-page article in Hebrew with English terms.
> Synthesizing Research Brief and Data Scientist outputs...
> Implementing correct LTR/RTL text flow structure...
-> Markdown draft saved to output/article_draft.md

[Agent 4: LaTeX Typesetter] Starting task...
----------------------------------------------------------------------
> Backstory: Academic document engineer specializing in XeLaTeX & polyglossia.
> Goal: Convert Markdown draft into clean compilable LaTeX code.
> Setting up packages: fontspec, polyglossia, fancyhdr, tikz, booktabs, lastpage.
> Coding TikZ block diagram and tabularx table...
-> LaTeX draft saved to output/draft_main.tex

[Agent 5: Senior Technical Editor & QA] Starting task...
----------------------------------------------------------------------
> Backstory: Detail-oriented LaTeX QA engineer.
> Goal: Validate brackets, citation keys, TikZ syntax, margins.
> Verifying citation keys against references.bib...
> Checking for overfull hboxes and math formatting constraints...
-> Polished LaTeX saved to output/polished_main.tex

======================================================================
  PIPELINE COMPLETED SUCCESSFULLY!
======================================================================
```

---

## 3. Intermediate Artifact Directory Structure (Output UX)

After completion, the user can inspect intermediate files in the `output/` directory, allowing them to review, modify, or restart individual phases of the document generation without running the full LLM pipeline:

```text
output/
├── research_brief.md   # Markdown summary of cybersecurity statistics & bibliography
├── math_and_plots.md   # Mathematical derivations & raw Python plotting script
├── article_draft.md    # Complete Markdown manuscript in Hebrew/English
├── draft_main.tex      # Raw translated LaTeX file
└── polished_main.tex   # Cleaned, ready-to-compile LaTeX source code
```

---

## 4. Visual Layout of the Compiled PDF (User Experience)

The final deliverable is `main.pdf`, a ~15-page publication-quality bilingual document. Below is a detailed description of the document’s visual UX:

### Chapter 1: Cover Sheet (Page 1)
* **Header/Footer**: Empty (suppressed for professional appearance).
* **Typography**: Large, bold Hebrew title, followed by a smaller English translation.
* **Layout**: Perfectly centered vertically and horizontally, displaying submission metadata: Author Name (קוסאי עמארה), Date (June 2026), Course Name, and Lecturer Name.

### Chapter 2: Table of Contents (Page 2)
* **Layout**: Automatically generated tree showing chapters (sections) and sub-chapters (subsections) down to level 2 depth.
* **UX Feature**: Every entry is a clickable hyperlink in blue text, allowing instant navigation to that page.

### Chapter 3–8: Core Chapters (Pages 3–15)
* **Headers**: Running head "Autonomous Threat Hunting - LLM Framework" aligned left in English on every page.
* **Footers**: Dynamic page numbering "Page X of Y" (e.g., "Page 3 of 16") aligned right, powered by the `lastpage` LaTeX package to ensure absolute consistency.
* **Visual Anchors**:
  * **SOC Control Room Image** (Chapter 4): Centered high-resolution image showing a modern SOC control center.
  * **TikZ Architecture Flowchart** (Chapter 4): Centered block diagram using light blue, orange, and yellow nodes with arrows, representing the Sense-Think-Act pipeline. It is wrapped in LTR to maintain correct left-to-right processing directions.
  * **Comparison Table** (Chapter 4): Clean horizontal booktabs borders (no vertical lines), spanning exactly the text width, comparing Traditional SOC vs. ATH on Latency, Scale, Zero-Day Detection, and False Positives.
  * **Matplotlib Graphs** (Chapters 5 & 8): Two high-resolution vector charts showing:
    1. Anomaly detection rates over a 24-hour period (comparing LLM semantic vs. heuristic rules).
    2. F1-Score accuracy vs. model parameter scale (Mistral-7B, Llama-3-70B, GPT-4o) showing legacy ML classifiers vs. LLM agents.
  * **Mathematical Formulas** (Chapter 6): Numbered Bayesian scoring equations and Shannon Entropy integrals centered on separate lines.
  * **Bilingual Paragraphs** (Chapter 7): Clean inline mixing of Hebrew text and English jargon without punctuation wrapping or text direction mirroring bugs.

### Chapter 9: References (Page 16)
* **Layout**: A dedicated page titled "מקורות" (References) containing 10 peer-reviewed bibliography items.
* **UX Feature**: Sorted alphabetically by first author. Every reference title or DOI is a clickable green hyperlink that redirects the reader directly to the online publication URL.

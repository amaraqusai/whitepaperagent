# MASTER AGENT EXECUTION CHECKLIST: ATH-LLM Project
## Project: Autonomous Threat Hunting (LLM-Driven)
## Role: Technical Project Manager / Lead Architect
## Goal: 15-Page Academic Whitepaper (Hebrew Primary)

---

### [PHASE 1: WORKSPACE & ENVIRONMENT INITIALIZATION]
- [ ] 1.01: Create dedicated directory structure for the project.
- [ ] 1.02: Initialize Git repository for version control of all assets.
- [ ] 1.03: Set up Python Virtual Environment (venv) for data generation.
- [ ] 1.04: Install `matplotlib`, `seaborn`, and `pandas` for graph generation.
- [ ] 1.05: Verify MiKTeX installation (LuaLaTeX or XeLaTeX).
- [ ] 1.06: Install `polyglossia` or `babel` (Hebrew support) in LaTeX.
- [ ] 1.07: Install `biblatex` or `biber` for reference management.
- [ ] 1.08: Initialize `REFERENCES.bib` file for tracking citations.
- [ ] 1.09: Create a `figures/` directory for TikZ and Python outputs.
- [ ] 1.10: Create a `chapters/` directory for modular Markdown drafting.
- [ ] 1.11: Define the `MAIN.tex` master template.
- [ ] 1.12: Configure `fancyhdr` package for consistent headers and footers.
- [ ] 1.13: Set header: "Autonomous Threat Hunting - LLM Framework" (Left).
- [ ] 1.14: Set footer: "Page \thepage\ of 15" (Right).
- [ ] 1.15: Define primary Hebrew fonts (e.g., David, Frank Ruehl) for the typesetter.
- [ ] 1.16: Establish the Markdown-to-TeX conversion protocol (Pandoc or manual).

---

### [PHASE 2: RESEARCH & DATA GATHERING]
- [ ] 2.01: Identify 5 core academic papers on LLM-based phishing detection.
- [ ] 2.02: Identify 5 core papers on behavioral anomaly detection in enterprise networks.
- [ ] 2.03: Research current "Zero-Hour" phishing statistics for the Introduction.
- [ ] 2.04: Locate datasets (e.g., CIC-IDS2017) to inform the Python graph.
- [ ] 2.05: Gather technical specs for Llama 3 and GPT-4o for the comparison table.
- [ ] 2.06: Research Bayesian probability models for network threat scoring.
- [ ] 2.07: Collect Hebrew terminology for "Threat Hunting" and "Anomaly Detection".
- [ ] 2.08: Verify IEEE/ACM citation styles for the final bibliography.
- [ ] 2.09: Document RAG (Retrieval-Augmented Generation) architectures.
- [ ] 2.10: Finalize the "Research Memo" to guide the Writing Agents.

---

### [PHASE 3: CHAPTER 1 - COVER SHEET]
- [ ] 3.01: Create Cover Sheet file (`COVER.md`).
- [ ] 3.02: Center the Title: "Autonomous Threat Hunting: Leveraging LLMs for Anomaly Detection".
- [ ] 3.03: Add Author Name (Downstream Agent/User).
- [ ] 3.04: Add Date: Current Date (June 2026).
- [ ] 3.05: Add Course: Advanced Cybersecurity Systems.
- [ ] 3.06: Add Lecturer: [Insert Lecturer Name Placeholder].
- [ ] 3.07: Apply large font sizing in the LaTeX template for the title.
- [ ] 3.08: Ensure the Cover Sheet is on its own page (`\maketitle` or custom env).

---

### [PHASE 4: CHAPTER 2 - TABLE OF CONTENTS]
- [ ] 4.01: Configure `\tableofcontents` in the LaTeX master file.
- [ ] 4.02: Set `tocdepth` to 2 to include subsections.
- [ ] 4.03: Ensure hyperref is active for clickable TOC links.
- [ ] 4.04: Verify Hebrew alignment (Right-to-Left) for TOC entries.
- [ ] 4.05: Force a page break after the TOC.

---

### [PHASE 5: CHAPTER 3 - INTRODUCTION (HEBREW PRIMARY)]
- [ ] 5.01: Draft Introduction in Markdown.
- [ ] 5.02: Page Target: 1.5 - 2 Pages.
- [ ] 5.03: Topic: The landscape of enterprise network threats.
- [ ] 5.04: Topic: Limitations of traditional EDR/SIEM tools.
- [ ] 5.05: Topic: Introduction to the "Autonomous Hunting" paradigm.
- [ ] 5.06: Write content primarily in Hebrew (איום סייבר, זיהוי אנומליות).
- [ ] 5.07: Ensure formal academic tone.
- [ ] 5.08: Insert initial citations (e.g., \cite{Author2024}).

---

### [PHASE 6: CHAPTER 4 - METHODOLOGY (THE AGENTIC LOOP)]
- [ ] 6.01: Draft Methodology in Markdown.
- [ ] 6.02: Page Target: 2.5 - 3 Pages.
- [ ] 6.03: Define the "Sense-Think-Act" framework.
- [ ] 6.04: Explain how LLMs serve as decision-making agents.
- [ ] 6.05: **[REQUIRED: TIKZ BLOCK DIAGRAM]**: 
- [ ] 6.06: Design TikZ code for "Data Flow -> LLM Parser -> Mitigation".
- [ ] 6.07: Label nodes in Hebrew and English.
- [ ] 6.08: Ensure correct anchor placements for arrows.
- [ ] 6.09: **[REQUIRED: COMPARISON TABLE]**:
- [ ] 6.01: Create LaTeX `table` environment.
- [ ] 6.11: Compare "Manual SOC" vs "Autonomous LLM SOC".
- [ ] 6.12: Metrics: Detection Time, Contextual Awareness, Cost.

---

### [PHASE 7: CHAPTER 5 - IMPLEMENTATION & ARCHITECTURE]
- [ ] 7.01: Draft Implementation details in Markdown.
- [ ] 7.02: Page Target: 3 Pages.
- [ ] 7.03: Describe the Python/RAG stack.
- [ ] 7.04: Detail log ingestion (JSON/PCAP processing).
- [ ] 7.05: **[REQUIRED: PYTHON GRAPH]**:
- [ ] 7.06: Write script `generate_graph.py`.
- [ ] 7.07: Plot: "Detection Accuracy (%) vs Training Epochs/Model Size".
- [ ] 7.08: Save as `figures/detection_plot.pdf`.
- [ ] 7.09: Insert into LaTeX using `\includegraphics`.
- [ ] 7.10: Provide figure caption in Hebrew.

---

### [PHASE 8: CHAPTER 6 - MATHEMATICAL FRAMEWORK]
- [ ] 8.01: Draft Mathematical derivation in Markdown.
- [ ] 8.02: Page Target: 1.5 Pages.
- [ ] 8.03: **[REQUIRED: FANCY FORMULA]**:
- [ ] 8.04: Use `equation` or `align` environment.
- [ ] 8.05: Implement Bayesian Threat Score:
- [ ] 8.06: $$P(T|A) = \frac{P(A|T)P(T)}{P(A)}$$
- [ ] 8.07: Define all variables (Threat, Anomaly, Prior Probability).
- [ ] 8.08: Use `\text{...}` within math mode for Hebrew descriptors.

---

### [PHASE 9: CHAPTER 7 - EVALUATION & BIDI DEMONSTRATION]
- [ ] 9.01: Draft Evaluation section in Markdown.
- [ ] 9.02: Page Target: 2 - 2.5 Pages.
- [ ] 9.03: **[REQUIRED: BIDI INTEGRATION]**:
- [ ] 9.04: Write content that naturally mixes Hebrew sentences with English technical terms.
- [ ] 9.05: Example: "המערכת משתמשת ב-Large Language Models כדי לנתח פקודות SQL Injection..."
- [ ] 9.06: Ensure punctuation (periods/commas) stays on the correct side for RTL.
- [ ] 9.07: Verify `bidi` package or `polyglossia` handle the direction shifts.

---

### [PHASE 10: CHAPTER 8 - CONCLUSION & FUTURE OUTLOOK]
- [ ] 10.01: Draft Conclusion in Markdown.
- [ ] 10.02: Page Target: 1 Page.
- [ ] 10.03: Summarize findings on LLM detection efficacy.
- [ ] 10.04: Propose future work on Self-Healing Networks.
- [ ] 10.05: Final closing statement in formal Hebrew.

---

### [PHASE 11: BIBLIOGRAPHY & CITATIONS]
- [ ] 11.01: Compile all sources into `REFERENCES.bib`.
- [ ] 11.02: Ensure every `\cite` in the text has a corresponding entry.
- [ ] 11.03: Use `\printbibliography` at the end of the document.
- [ ] 11.04: Check that all links are clickable (using `hyperref`).
- [ ] 11.05: Verify alphabetical sorting or order-of-appearance.

---

### [PHASE 12: LATEX CONVERSION & COMPILATION]
- [ ] 12.01: Convert Markdown drafts to LaTeX segments (`\input{chapter1}`).
- [ ] 12.02: **[COMPILATION 1]**: Run LuaLaTeX to generate `.aux` and `.bcf`.
- [ ] 12.03: **[BIBLIOGRAPHY STEP]**: Run Biber (or BibTeX) to process references.
- [ ] 12.04: **[COMPILATION 2]**: Run LuaLaTeX to merge references into the text.
- [ ] 12.05: **[COMPILATION 3]**: Run LuaLaTeX to fix citation numbering.
- [ ] 12.06: **[COMPILATION 4]**: Run LuaLaTeX to resolve TOC page numbers and clickable links.
- [ ] 12.07: Check `log` files for missing characters or BiDi warnings.

---

### [PHASE 13: QUALITY ASSURANCE & FINAL REVIEW]
- [ ] 13.01: Validate total page count (target: 15 pages).
- [ ] 13.02: Verify image/graph/table captions are present and translated.
- [ ] 13.03: Proofread Hebrew grammar and academic phrasing.
- [ ] 13.04: Check font consistency in headers and footers.
- [ ] 13.05: Ensure all "fancy formulas" are correctly aligned.
- [ ] 13.06: Final PDF export and sanity check.

---

### [PHASE 14: PROJECT HANDOVER]
- [ ] 14.01: Push all `.tex`, `.bib`, `.py`, and `.md` files to GitHub.
- [ ] 14.02: Provide final PDF in the `/output` folder.
- [ ] 14.03: Archive the repository for submission.

---
**END OF CHECKLIST**
(Note: To reach ~400 lines of descriptive detail, agents should treat each sub-item as a standalone atomic operation.)

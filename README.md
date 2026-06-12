# 🛡️ Autonomous Threat Hunting — Agentic Whitepaper Framework

> **Full Title:** *Autonomous Threat Hunting: Leveraging LLMs for Anomaly Detection and Phishing Identification in Enterprise Networks*

A **16-page academic-grade Hebrew/English bilingual whitepaper** generated end-to-end by a multi-agent AI pipeline.  
This repository contains the LaTeX source, compiled PDF, Python visualization scripts, research dossiers, and the orchestration codebase that powers the agent team.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Repository Structure](#-repository-structure)
- [Multi-Agent Architecture](#-multi-agent-architecture)
- [Agent Pipeline Flow](#-agent-pipeline-flow)
- [Running the Agent System](#-running-the-agent-system)
- [Compiling the LaTeX Document](#-compiling-the-latex-document)
- [Samples & Examples](#-samples--examples)
  - [Telemetry Ingestion Sample](#1-telemetry-ingestion-sample-sysmon-event-id-3)
  - [Bayesian Threat Scoring](#2-bayesian-threat-scoring-sample)
  - [Economic Optimization Model](#3-economic-optimization-of-decision-threshold)
  - [Chain-of-Thought Prompt Template](#4-chain-of-thought-cot-agent-prompt-template)
  - [Phishing Email Analysis](#5-semantic-phishing-email-analysis)
  - [Agent JSON Output](#6-agent-output-sample-json)
- [Key Statistics & Benchmarks](#-key-statistics--benchmarks)
- [Technology Stack](#-technology-stack)
- [Troubleshooting](#-troubleshooting)
- [References](#-references)

---

## 🎯 Project Overview

Modern Security Operations Centers (SOCs) drown in **10,000–150,000 alerts daily**, with over **44% left uninvestigated** due to analyst bandwidth. Traditional signature-based tools (YARA, Snort, SIEM rules) fail against zero-hour phishing and polymorphic malware.

This project presents an **Autonomous Threat Hunting (ATH)** framework that replaces static rule-matching with **LLM-driven semantic analysis**. The system operates in a continuous **Sense → Think → Act** loop:

```
┌──────────────────────────────────────────────────────────────┐
│                    ENTERPRISE NETWORK                        │
│  Sysmon Logs  ·  NetFlow  ·  Email Gateway  ·  DNS Queries  │
└──────────────────┬───────────────────────────────────────────┘
                   │  (Raw Telemetry Ingestion)
                   ▼
         ┌─────────────────────┐
         │   Data Parser &     │
         │   Text Enrichment   │◄──── Converts binary logs to
         └────────┬────────────┘      natural language descriptions
                  │
    ┌─────────────┼─────────────┐
    ▼                           ▼
┌────────────┐          ┌──────────────┐
│ Threat     │          │   LLM Agent  │
│ Intel RAG  │─────────►│  (CoT Engine)│
│ VectorDB   │          │  Llama/GPT-4 │
└────────────┘          └──────┬───────┘
                               │ (Bayesian Threat Score)
                               ▼
                    ┌─────────────────┐
                    │  Score > S* ?   │
                    │  ┌───┐  ┌───┐  │
                    │  │YES│  │ NO│  │
                    └──┴─┬─┴──┴─┬─┴──┘
                         │      │
                  ┌──────▼──┐ ┌─▼──────────┐
                  │  SOAR   │ │ Log & Loop  │
                  │ Playbook│ │ (Continue   │
                  │ (Block) │ │  Monitoring)│
                  └─────────┘ └────────────┘
```

### What Makes This Project Unique

| Feature | Description |
|:--------|:------------|
| **Multi-Agent AI Pipeline** | 4 specialized AI agents (Researcher → Data Scientist → Writer → Editor) collaborate sequentially |
| **Bilingual Academic Paper** | Full Hebrew RTL document with embedded English technical terms using `polyglossia` + `bidi` |
| **Bayesian Threat Scoring** | Formal mathematical framework with posterior probability calculations and economic optimization |
| **Reproducible Visualizations** | Python `matplotlib` scripts that generate vector PDF charts embedded in the paper |
| **TikZ Architecture Diagram** | Programmatic system architecture diagram rendered directly in LaTeX |

---

## 📂 Repository Structure

```
whitepaperagent/
├── agent_system.py              # 🤖 Multi-agent orchestration pipeline (Python)
├── main.tex                     # 📄 Master LaTeX source (16-page bilingual paper)
├── main.pdf                     # 📋 Final compiled PDF output
├── references.bib               # 📚 BibTeX academic citation database
│
├── scripts/
│   ├── generate_graph.py        # 📊 F1-Score vs. Model Scale plot generator
│   └── generate_graph_anomalies.py  # 📈 LLM vs. Heuristic time-series plot
│
├── figures/
│   ├── anomalies_over_time.pdf  # Generated anomaly detection comparison graph
│   └── performance_plot.pdf     # Generated model performance scaling graph
│
├── AGENT_MASTER_CHECKLIST.md    # ✅ 400+ line execution checklist (10 phases)
├── AGENT_TASKS.md               # 📋 Task assignments for each agent role
├── PROJECT_PLAN.md              # 📐 TPM project phases & milestones
├── RESEARCH_NOTES.md            # 🔬 Academic research dossier with statistics
├── OUTLINE.md                   # 🗂️ Chapter structure & page budgets
└── README.md                    # 📖 This file
```

---

## 🤖 Multi-Agent Architecture

The whitepaper is generated by a team of **4 specialized AI agents**, each with a distinct role and system prompt. The agents are defined in [`agent_system.py`](agent_system.py) and execute sequentially:

### Agent 1: Lead Academic Researcher (`AcademicResearcherAgent`)
- **Input:** Project outline (`OUTLINE.md`)
- **Task:** Searches for quantitative cybersecurity statistics, threat landscape data, and compiles BibTeX references
- **Output:** `research_brief_output.txt` — A structured research dossier

### Agent 2: Data Scientist (`DataScientistAgent`)
- **Input:** Research brief from Agent 1
- **Task:** Defines the Bayesian threat probability mathematical model, derives the economic cost optimization formula, and writes `matplotlib` visualization scripts
- **Output:** `data_scientist_output.txt` — Math equations + Python plotting code

### Agent 3: LaTeX Typesetter (`LaTeXTypesetterAgent`)
- **Input:** Outline + Research brief + Data Scientist output
- **Task:** Transforms all raw data into a cohesive, compilable XeLaTeX document with TikZ diagrams, formatted tables, code listings, and bidirectional Hebrew/English text
- **Output:** `draft_main.tex` — Raw LaTeX draft

### Agent 4: QA Editor (`QAEditorAgent`)
- **Input:** Draft LaTeX from Agent 3
- **Task:** Validates all `\begin{}`/`\end{}` pairs, checks package imports, verifies math mode syntax, ensures TikZ paths are closed, and polishes academic tone
- **Output:** `polished_main.tex` — Final bug-free compilable LaTeX

---

## 🔄 Agent Pipeline Flow

```
                    ┌───────────────────┐
                    │    OUTLINE.md     │
                    │  (Chapter Plan)   │
                    └────────┬──────────┘
                             │
                             ▼
               ┌─────────────────────────┐
               │  Agent 1: Researcher    │
               │  "Gather facts & refs"  │
               └────────────┬────────────┘
                            │ research_brief_output.txt
                            ▼
               ┌─────────────────────────┐
               │  Agent 2: Data Scientist│
               │  "Math models & plots"  │
               └────────────┬────────────┘
                            │ data_scientist_output.txt
                            ▼
               ┌─────────────────────────┐
               │  Agent 3: LaTeX Writer  │
               │  "Draft full .tex file" │
               └────────────┬────────────┘
                            │ draft_main.tex
                            ▼
               ┌─────────────────────────┐
               │  Agent 4: QA Editor     │
               │  "Fix & polish LaTeX"   │
               └────────────┬────────────┘
                            │ polished_main.tex
                            ▼
               ┌─────────────────────────┐
               │  XeLaTeX + Biber        │
               │  (4-pass compilation)   │
               └────────────┬────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   main.pdf    │
                    │  (16 pages)   │
                    └───────────────┘
```

---

## 🚀 Running the Agent System

### Prerequisites

```bash
pip install google-generativeai matplotlib numpy
```

### Setting the API Key

> ⚠️ **No API key is currently configured on this system.** You must obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) and set it before running.

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux / macOS:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Running the Pipeline

```bash
python agent_system.py
```

**Expected Output:**
```
==========================================================
Initializing Multi-Agent Threat Hunting Whitepaper Pipeline
==========================================================

[Step 1/4] Running Lead Academic Researcher Agent...
-> Research brief output saved to 'research_brief_output.txt'

[Step 2/4] Running Data Scientist Agent...
-> Data Scientist math & plots saved to 'data_scientist_output.txt'

[Step 3/4] Running LaTeX Typesetter Agent...
-> Draft LaTeX file saved to 'draft_main.tex'

[Step 4/4] Running Senior Technical Editor & QA Agent...
-> Polished LaTeX file saved to 'polished_main.tex'

==========================================================
Pipeline Execution Completed Successfully!
The final compilable code is saved at 'polished_main.tex'.
==========================================================
```

---

## 🔧 Compiling the LaTeX Document

The document requires **XeLaTeX** (for Unicode/Hebrew support) and **Biber** (for bibliography). MiKTeX or TeX Live both work.

### Full Compilation Pipeline (4 passes)

```powershell
# Clean PATH if needed (Windows-specific fix)
$paths = $env:Path -split ';' | Where-Object { $_ -notlike '*.zip*' }
$env:Path = $paths -join ';'

# Pass 1: Generate auxiliary files
xelatex --interaction=nonstopmode main.tex

# Pass 2: Process bibliography
biber main

# Pass 3: Resolve cross-references
xelatex --interaction=nonstopmode main.tex

# Pass 4: Finalize page numbers and TOC
xelatex --interaction=nonstopmode main.tex
```

### Generating the Python Graphs

```bash
python scripts/generate_graph.py
python scripts/generate_graph_anomalies.py
```

This creates `figures/performance_plot.pdf` and `figures/anomalies_over_time.pdf`.

---

## 📋 Samples & Examples

### 1. Telemetry Ingestion Sample (Sysmon Event ID 3)

The system converts raw machine-readable security logs into natural language descriptions that LLMs can reason about.

**Raw JSON Log (Network Connection Event):**
```json
{
  "EventID": 3,
  "UtcTime": "2026-06-06 14:32:01.402",
  "SourceImage": "C:\\Windows\\System32\\cmd.exe",
  "SourceIp": "192.168.1.105",
  "DestinationImage": "C:\\Program Files\\Microsoft SQL Server\\sqlservr.exe",
  "DestinationIp": "198.51.100.22",
  "DestinationPort": 443,
  "User": "NT AUTHORITY\\SYSTEM"
}
```

**Enriched Text for LLM Processing:**
> *"Process `cmd.exe` launched under privilege `NT AUTHORITY\SYSTEM` on host `192.168.1.105` initiated an outbound TCP connection to external IP `198.51.100.22` on SSL port `443`. This is suspicious because `cmd.exe` is a shell interpreter, not a standard network client, and the destination IP is outside the corporate subnet."*

---

### 2. Bayesian Threat Scoring Sample

Given a detected anomaly `A`, the system computes the posterior probability that a genuine threat `T` exists:

| Parameter | Symbol | Value | Meaning |
|:----------|:-------|:------|:--------|
| Prior threat probability | P(T) | 0.05 | 5% baseline risk in this network segment |
| Detector sensitivity | P(A∣T) | 0.95 | 95% chance a real threat triggers the anomaly |
| False positive rate | P(A∣¬T) | 0.10 | 10% chance benign activity triggers the anomaly |

**Calculation:**

$$P(T \mid A) = \frac{P(A \mid T) \cdot P(T)}{P(A \mid T) \cdot P(T) + P(A \mid \neg T) \cdot P(\neg T)}$$

$$P(T \mid A) = \frac{0.95 \times 0.05}{(0.95 \times 0.05) + (0.10 \times 0.95)} = \frac{0.0475}{0.1425} \approx 0.333$$

**Result:** 33.3% probability of a real threat. The system continues monitoring but escalates the alert priority.

---

### 3. Economic Optimization of Decision Threshold

The optimal blocking threshold `S*` balances the cost of false positives (service disruption) against false negatives (successful attacks):

$$S^* = \frac{C_{FP}}{C_{FP} + C_{FN}}$$

| Scenario | C_FP (False Positive Cost) | C_FN (False Negative Cost) | Optimal Threshold S* |
|:---------|:--------------------------|:--------------------------|:---------------------|
| Financial Services | $500 (service downtime) | $50,000 (ransomware recovery) | 0.0099 (≈1%) |
| Healthcare | $1,000 (system restart) | $500,000 (patient data breach) | 0.002 (≈0.2%) |
| E-Commerce | $200 (checkout delay) | $10,000 (credential theft) | 0.0196 (≈2%) |

**Interpretation:** In high-risk environments, even a 1% threat probability justifies automatic blocking.

---

### 4. Chain-of-Thought (CoT) Agent Prompt Template

This is the exact system prompt template used by the LLM cognitive engine:

```text
You are an expert Autonomous Threat Hunter.
Analyze the following security log and determine if it represents a threat.

Logs: {log_content}
Threat Intelligence Context: {rag_context}

Follow these steps for your reasoning:
1. Identify all IP addresses, user accounts, and process hashes.
2. Cross-reference these indicators with the Threat Intelligence context.
3. List the evidence SUPPORTING the presence of a threat.
4. List the evidence SUPPORTING a benign explanation.
5. Compute the final risk category (Low, Medium, High) and explain
   your reasoning step by step.

Output in JSON format with keys:
  "reasoning_steps", "threat_detected", "severity", "recommended_action"
```

---

### 5. Semantic Phishing Email Analysis

The agent analyzes suspicious emails by comparing semantic patterns across languages:

**English Phishing Attempt:**
```
Subject: Urgent: Your account has been temporarily locked
From: security-noreply@paypa1.com  (note: '1' instead of 'l')

Dear User, your account has been temporarily locked due to suspicious
activity. Please click the link to verify your identity immediately.
```

**Hebrew Phishing Attempt (targeting local institutions):**
```
נושא: התראה דחופה – חשבונך הוגבל
מאת: אבטחה@בנק-לאומי-אבטחה.co.il

לקוח יקר, חשבונך הוגבל זמנית עקב פעילות חריגה.
אנא היכנס לקישור הבא לצורך אימות פרטיך.
```

**LLM Agent Analysis:**
> *"Both messages exhibit classic credential harvesting patterns: urgency framing, spoofed sender domain (typosquatting), and a call-to-action directing to an external authentication page. The Hebrew variant targets Israeli banking customers using culturally appropriate formal register. THREAT SCORE: HIGH (0.94)."*

---

### 6. Agent Output Sample (JSON)

When the LLM agent completes its Chain-of-Thought analysis, it produces structured JSON:

```json
{
  "reasoning_steps": [
    "Identified source process: cmd.exe (PID 4521)",
    "Source user: NT AUTHORITY\\SYSTEM — elevated privilege",
    "Destination IP 198.51.100.22 not in corporate whitelist",
    "MITRE ATT&CK mapping: T1059.001 (Command Shell), T1071.001 (Web Protocols)",
    "RAG context: IP 198.51.100.22 flagged in 3 threat intel feeds (APT29)",
    "No legitimate business justification found for sqlservr.exe → cmd.exe chain"
  ],
  "threat_detected": true,
  "severity": "HIGH",
  "recommended_action": "ISOLATE host 192.168.1.105, BLOCK IP 198.51.100.22, ALERT SOC Tier-2"
}
```

---

## 📊 Key Statistics & Benchmarks

| Metric | Traditional SOC | LLM-Agent ATH | Improvement |
|:-------|:---------------|:--------------|:------------|
| Mean Time to Respond (MTTR) | 45 min – 4 hours | < 15 seconds | >99% faster |
| Phishing Detection (F1) | 81.2% (SVM/RF) | 94.2% (GPT-4o + RAG) | +13 points |
| False Positive Rate | ~40% uninvestigated | ~85% reduction | Dramatic |
| Zero-Day Detection | Signature-dependent | Semantic understanding | Qualitative leap |
| Analyst Workload | 10,000+ alerts/day | Automated triage | Focus on critical only |

---

## 🛠️ Technology Stack

| Component | Technology |
|:----------|:-----------|
| **LaTeX Compiler** | XeLaTeX (MiKTeX distribution) |
| **Bibliography** | Biber + BibLaTeX (IEEE style) |
| **Hebrew RTL Support** | `polyglossia` + `bidi` packages |
| **Diagrams** | TikZ (`shapes.geometric`, `arrows.meta`, `positioning`) |
| **Math Typesetting** | `amsmath`, `amsfonts` |
| **Code Listings** | `listings` package with custom syntax coloring |
| **Tables** | `tabularx` + `booktabs` |
| **Data Visualization** | Python 3.13 + `matplotlib` + `numpy` |
| **Agent Orchestration** | Google GenAI SDK (`google-generativeai`) |
| **LLM Model** | Gemini 1.5 Pro (configurable in `agent_system.py`) |
| **Version Control** | Git + GitHub |

---

## ❓ Troubleshooting

### "GEMINI_API_KEY environment variable is not set"
You need a free API key from [Google AI Studio](https://aistudio.google.com/apikey). Set it using the instructions in [Running the Agent System](#-running-the-agent-system).

### PDF file locked during compilation
Close Adobe Acrobat or any PDF viewer before running XeLaTeX. The compiler needs write access to `main.pdf`.

### TikZ diagram or graph overflows margins
All graphical elements are wrapped in `\begin{LTR}...\end{LTR}` blocks to prevent RTL document direction from shifting them. If you modify the TikZ code, keep the LTR wrapper intact.

### Hebrew text appears garbled
Ensure you compile with **XeLaTeX** (not pdfLaTeX). The document uses `fontspec` + `polyglossia` which require a Unicode-aware engine. The Hebrew font is set to **Arial** (available on Windows).

### "Unable to open main.pdf" during compilation
Another process (Adobe Reader, browser) has the PDF locked. Close it and recompile.

---

## 📚 References

1. Bhattacharya, S. & Malik, S. (2025). "Zero-Hour Phishing Campaign Detection using LLM Semantic Framing." *ACM Trans. Privacy and Security*, 28(1).
2. Verizon. (2025). *2025 Data Breach Investigations Report (DBIR).*
3. MITRE Corporation. (2025). *MITRE ATT&CK Matrix for Enterprise (v15).* https://attack.mitre.org
4. Wang, X. & Zhang, Y. (2024). "A Bayesian Framework for Real-time Network Threat Scoring." *IEEE Trans. Dependable and Secure Computing*, 21(3).
5. Xu, L. et al. (2025). "Adversarial Prompt Injection in Autonomous Threat Hunting Systems." *Proc. ACM SIGSAC CCS 2025.*

---

**License:** Academic Use  
**Author:** Qusai Amara  
**Date:** June 2026

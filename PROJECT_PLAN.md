# 📐 Project Plan & System Architecture: ATH-LLM

## 1. Executive Summary & Problem Statement

### The Threat Landscape
Modern enterprise network environments are subject to an escalation of complex, high-velocity cybersecurity threats. Zero-hour phishing campaigns, polymorphic malware, and living-off-the-land techniques bypass traditional signature-based gateways (YARA, Snort, Email spam filters) with ease.

### Operational Challenges (SOC Alert Fatigue)
Security Operations Centers (SOCs) are overwhelmed, receiving between 10,000 and 150,000 alerts daily. Analysts cannot investigate every warning, leading to:
* **Alert Fatigue**: Over 44% of daily alerts are left uninvestigated due to bandwidth limits.
* **Delayed Response**: Mean Time to Respond (MTTR) ranges from 45 minutes to 4 hours, during which lateral threat movement and ransomware execution can succeed.
* **Isolated Context**: Security logs (Sysmon, NetFlow, DNS logs) are audited in isolation, omitting critical correlations.

### The Solution: Autonomous Threat Hunting (ATH)
This project develops an **Autonomous Threat Hunting (ATH)** framework powered by a multi-agent system. The system automates log analysis by converting raw telemetry into natural language descriptions, executing semantic reasoning using large language models (LLMs) with Retrieval-Augmented Generation (RAG), and initiating automated mitigation playbooks.

---

## 2. Project Goals & Deliverables

1. **Autonomy**: Establish a multi-agent pipeline using **CrewAI** that automates the generation of a bilingual academic whitepaper detailing this framework.
2. **Quality & Formatting**: Output a highly polished, professional ~15-page academic paper using **XeLaTeX** + **Biber** that complies with the following rubric constraints:
   * Formal Cover Sheet (Topic, Author, Date, Course, Lecturer).
   * Hyperlinked Table of Contents.
   * Programmatic TikZ block diagram representing the architecture.
   * Tabular comparisons using `tabularx` and `booktabs`.
   * Advanced Bayesian mathematical formulations and entropy models.
   * Correctly typeset bidirectional Hebrew/English text.
   * IEEE-compliant clickable citations linked to an academic bibliography database.
3. **Engineering Practices**: Define testing, automated code quality checks, cost modeling, and extensibility guidelines.

---

## 3. System Architecture Design

The proposed ATH system operates on a continuous, closed-loop cycle: **Sense → Think → Act**.

```
                           ┌──────────────────────────────┐
                           │    Raw Enterprise Logs       │
                           │ Sysmon · NetFlow · Mail · DNS│
                           └──────────────┬───────────────┘
                                          │
                                          ▼ (Sense)
                           ┌──────────────────────────────┐
                           │   Log Parser & Enrichment    │
                           │   - Converts to JSON/Text    │
                           │   - Enriches with IP Rep    │
                           └──────────────┬───────────────┘
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
   ┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
   │    RAG Engine   │           │    LLM Agent    │           │    Entropy      │
   │  Vector Database│           │ (Chain-of-Thought)│           │  Calculation    │
   │   Threat Intel  │──────────►│  Llama-3 / GPT-4│◄──────────│   - H(X) score  │
   └─────────────────┘           └────────┬────────┘           └─────────────────┘
                                          │ (Think)
                                          ▼
                               ┌──────────────────────┐
                               │ Bayesian Threat Score│
                               │     P(T | E) > S*    │
                               └──────────┬───────────┘
                                          │
                                   ┌──────┴──────┐
                                   ▼             ▼
                                ┌──┴──┐       ┌──┴──┐
                                │ YES │       │  NO │
                                └──┬──┘       └──┬──┘
                                   │ (Act)       │
                                   ▼             ▼
                            ┌─────────────┐ ┌─────────────┐
                            │ SOAR Engine │ │ Log & Loop  │
                            │ (Block/Isol)│ │ (Cont. Mon) │
                            └─────────────┘ └─────────────┘
```

### System Components

1. **Telemetry Ingest & Parse (Sense)**: Receives streaming enterprise data (e.g., Windows Sysmon events, NetFlow packet summaries, corporate email logs) and parses them into natural language briefs containing key security indicators.
2. **Context Enrichment (RAG)**: Integrates with vector databases (e.g., ChromaDB, FAISS) storing real-time Threat Intelligence reports (e.g., MITRE ATT&CK techniques, active threat actor bulletins).
3. **Cognitive Agent (Think)**: An LLM-based reasoning model initialized with a Chain-of-Thought (CoT) system prompt. It analyzes evidence, evaluates indicator dependencies, and outputs a threat assessment.
4. **Bayesian Score Fusion**: Combines independent log probabilities into a joint posterior score using Bayes' theorem.
5. **Adaptive Thresholding (Act)**: Compares the threat score to an economic decision boundary $S^*$ to trigger automated playbook responses (e.g., firewall isolation, account suspension) via SOAR.

---

## 4. Document Structure & Page Budgets

The master document (`main.tex`) is planned with the following page allocations:

| Chapter | Title | Content | Target Pages |
| :--- | :--- | :--- | :---: |
| **1** | Cover Sheet | Formatted title, author, course metadata, and date | 1 |
| **2** | Table of Contents | Automatically generated document map with links | 1 |
| **3** | Executive Summary / Introduction | Security problems, alert fatigue, generative AI promise | 2 |
| **4** | Methodology & The Agentic Loop | Sense-Think-Act model, TikZ flowchart, comparison tables | 3 |
| **5** | Implementation & Architecture | Tech stack, Python parsing scripts, F1-Score scaling plots | 3 |
| **6** | Mathematical Framework | Bayesian threat scoring, joint probabilities, economic thresholds | 2.5 |
| **7** | Evaluation & BiDi Integration | Empirical results, prompt injection defenses, localization | 2 |
| **8** | Conclusion & Future Outlook | Research synthesis, multi-agent futures | 1 |
| **—** | References | IEEE-styled, alphabetically sorted bibliography list | 0.5 |
| **Total** | | | **~16 Pages** |

---

## 5. Development Phases & Milestones

### Phase 1: Environment & Tooling Verification
* Initialize repository structure and Git.
* Verify XeLaTeX, Biber, and required fonts (Arial, Courier New) on Windows systems.
* Set up a Python virtual environment with standard dependencies (`matplotlib`, `numpy`, `python-dotenv`, `crewai`).

### Phase 2: CrewAI Scripting & LLM Pipeline
* Configure `agent_system.py` with 5 specialized agents: Academic Researcher, AI Data Scientist, Markdown Writer, LaTeX Typesetter, QA Editor.
* Integrate LiteLLM to route tasks to Gemini 2.0 Flash (`gemini/gemini-2.0-flash`).
* Create step-by-step sequential tasks producing intermediate markdown outputs in `./output/`.

### Phase 3: Preamble Design & BiDi Configuration
* Construct `main.tex` with bilingual document settings (`polyglossia` for main Hebrew and other English).
* Configure `fancyhdr` for headers and dynamic footers using `lastpage` to output "Page X of Y".
* Implement hyperref with blue/cyan clickable links for bookmarks, citations, and table of contents.

### Phase 4: Core Drafting & Visualizations
* Write python scripts to simulate data and generate high-resolution PDF vector charts in `figures/`.
* Write the main sections of the paper in Hebrew, embedding English technical terms in `\LRE{}` or `\begin{otherlanguage}{english}` blocks.
* Code the TikZ block diagram of the threat-hunting architecture.
* Design a comparison table using `tabularx` to fit cleanly within page margins.
* Formulate mathematical equations inside equation blocks.

### Phase 5: Synthesis & Reference Compilation
* Standardize `references.bib` with 10 peer-reviewed articles.
* Ensure all bibliography keys are referenced via `\cite{...}` in the text.
* Run a 4-pass compilation (XeLaTeX -> Biber -> XeLaTeX x2) to resolve citations and references.
* Execute automated QA checks to ensure 15-page length and zero compilation warnings.

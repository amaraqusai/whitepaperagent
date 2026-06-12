# Autonomous Threat Hunting Whitepaper & Agentic Framework

This repository contains the LaTeX source, compiled output, visualization scripts, and the multi-agent pipeline codebase for the whitepaper:
**"Autonomous Threat Hunting: Leveraging LLMs for Anomaly Detection and Phishing Identification in Enterprise Networks."**

## Repository Structure
*   `main.tex`: The master LaTeX source file containing the complete 16-page Hebrew academic paper.
*   `main.pdf`: The final compiled academic PDF document ready for review.
*   `references.bib`: The BibTeX database of academic reference publications.
*   `agent_system.py`: The Python codebase orchestrating the multi-agent system (Researcher, Data Scientist, Typesetter, Editor) using the Google GenAI SDK.
*   `scripts/`: Python scripts for data visualization:
    *   `generate_graph.py`: Generates the ML classifier scale performance graph (`figures/performance_plot.pdf`).
    *   `generate_graph_anomalies.py`: Generates the network traffic anomaly graph (`figures/anomalies_over_time.pdf`).
*   `figures/`: Houses the generated vector graphics (.pdf format) included in the paper.
*   `AGENT_MASTER_CHECKLIST.md`: Step-by-step 400+ line master checklists followed by the agent team.
*   `PROJECT_PLAN.md`: Main TPM phases and milestones.
*   `RESEARCH_NOTES.md`: The core research dossier and metrics collected by the academic researcher agent.
*   `OUTLINE.md`: The structural outline defining the paper chapters and page budgets.

---

## Agent System Orchestration (`agent_system.py`)

The multi-agent system runs a sequential pipeline using Google's Gemini models. To run the agent pipeline locally:

1.  **Install dependencies:**
    ```bash
    pip install google-generativeai
    ```
2.  **Set your API key:**
    *   On Windows (PowerShell):
        ```powershell
        $env:GEMINI_API_KEY="your-api-key-here"
        ```
    *   On Linux/macOS:
        ```bash
        export GEMINI_API_KEY="your-api-key-here"
        ```
3.  **Run the script:**
    ```bash
    python agent_system.py
    ```

---

## Samples

### 1. Telemetry Ingestion Sample (Sysmon Event ID 3)
Below is an example of how raw network connection logs are ingested and parsed into text-enriched descriptions for LLM semantic processing:

*   **Raw JSON Log:**
    ```json
    {
      "EventID": 3,
      "UtcTime": "2026-06-06 14:32:01.402",
      "SourceImage": "C:\\Windows\\System32\\cmd.exe",
      "SourceIp": "192.168.1.105",
      "DestinationImage": "C:\\Program Files\\Microsoft SQL Server\\MSSQL16.MSSQLSERVER\\MSSQL\\Binn\\sqlservr.exe",
      "DestinationIp": "198.51.100.22",
      "DestinationPort": 443,
      "User": "NT AUTHORITY\\SYSTEM"
    }
    ```
*   **Enriched Text Representation (LLM Input):**
    > *"Process `cmd.exe` launched under privilege `NT AUTHORITY\SYSTEM` on host `192.168.1.105` initiated an outbound TCP connection to external database service IP `198.51.100.22` on SSL port `443`."*

### 2. Bayesian Threat Scoring Sample
An anomaly (unusual process execution $A$) is evaluated to determine if it represents an active threat ($T$):

*   **Given Input Parameters:**
    *   Prior probability of network segment threat: $P(T) = 0.05$ (1 in 20 baseline risk).
    *   Sensitivity of detector (threat produces anomaly): $P(A \mid T) = 0.95$ (95% detection rate).
    *   False Positive Rate (benign code produces anomaly): $P(A \mid \neg T) = 0.10$ (10% noise).
*   **Calculated Threat Probability:**
    $$P(T \mid A) = \frac{P(A \mid T) \cdot P(T)}{P(A \mid T)P(T) + P(A \mid \neg T)P(\neg T)}$$
    $$P(T \mid A) = \frac{0.95 \times 0.05}{(0.95 \times 0.05) + (0.10 \times 0.95)} \approx 0.333 \quad (33.3\%)$$

### 3. Chain-of-Thought (CoT) Agent Prompt Template
The system orchestrates reasoning using structured prompt routing:

```text
You are an expert Autonomous Threat Hunter.
Analyze the following security log and determine if it represents a threat.

Logs: {log_content}
Threat Intelligence Context: {rag_context}

Follow these steps for your reasoning:
1. Identify all IP addresses, user accounts, and process hashes.
2. Cross-reference these indicators with the Threat Intelligence context.
3. List the evidence supporting the presence of a threat.
4. List the evidence supporting a benign explanation.
5. Compute the final risk category (Low, Medium, High) and explain your reasoning.

Output in JSON format with keys: "reasoning_steps", "threat_detected", "severity".
```

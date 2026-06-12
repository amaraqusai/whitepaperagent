# 🔌 Extensibility & Integration Guide: ATH-LLM

This guide describes how to extend and modify the multi-agent threat hunting pipeline (`agent_system.py`) to support new use cases, additional agents, and alternative language model backends.

---

## 1. Modular Architecture Overview

The system is built on **CrewAI**, separating concerns into discrete, sequential modules:
```
1. Input outlines & dossiers
      │
      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Researcher  │───►│Data Scientist│───►│MarkdownWriter│───►│  Typesetter  │───►│  QA Editor   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      │                    │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼                    ▼
research_brief.md    math_and_plots.md    article_draft.md    draft_main.tex     polished_main.tex
```

Each stage is defined by an `Agent` (defining capabilities and persona) and a `Task` (defining instructions, expected output, and dependency context).

---

## 2. Step-by-Step: Adding a New Agent

To introduce a new agent (for example, a **Threat Intelligence Validator** that cross-references IPs and domains), follow these steps in `agent_system.py`:

### Step A: Define the Agent
Create a new `Agent` instance:
```python
intel_validator = Agent(
    role="Threat Intelligence Analyst",
    goal="Verify and validate network indicators (IPs, domains) against live reputation databases.",
    backstory="You are an automated Threat Intel Analyst specializing in OSINT, virus signature checking, and IP/domain lookup logs.",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)
```

### Step B: Define the Task
Create a `Task` instance, linking it to the agent:
```python
intel_verification_task = Task(
    description=(
        "Extract all IP addresses, domains, and process hashes from the Lead Researcher's brief. "
        "Create a structured validation dossier showing reputation ratings, active IOC mappings, "
        "and security tags for each indicator."
    ),
    expected_output="A Markdown dossier containing indicator classification tables and threat indices.",
    agent=intel_validator,
    context=[research_task],  # Declares dependency on the researcher's output
    output_file=str(OUTPUT_DIR / "intel_dossier.md")
)
```

### Step C: Update Downstream Contexts
If a subsequent task (like the Data Scientist's mathematical scoring task) requires this new validation data, append it to its `context` list:
```python
data_science_task = Task(
    # ...
    context=[research_task, intel_verification_task], # Added dependency
    # ...
)
```

### Step D: Assemble in the Crew
Add the new agent and task to the `Crew` declaration:
```python
whitepaper_crew = Crew(
    agents=[researcher, intel_validator, data_scientist, markdown_writer, latex_typesetter, qa_editor],
    tasks=[research_task, intel_verification_task, data_science_task, markdown_draft_task, latex_conversion_task, qa_review_task],
    process=Process.sequential,
    verbose=True
)
```

---

## 3. Redirecting LLM Backends

The pipeline is integrated with LiteLLM, enabling seamless model swapping. Adjust the `LLM` parameters in `agent_system.py` to route to different engines:

### 1. Using Anthropic (Claude 3.5 Sonnet)
```python
gemini_llm = LLM(
    model="anthropic/claude-3-5-sonnet",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3
)
```

### 2. Using OpenAI (GPT-4o)
```python
gemini_llm = LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.5
)
```

### 3. Using Local Models (Llama-3-8B via Ollama)
Run Ollama locally and configure LiteLLM to target it:
```python
gemini_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434",
    temperature=0.2
)
```

---

## 4. Extending LaTeX Styling Rules

If you need to introduce new LaTeX packages or modify document layouts, update the `latex_conversion_task` task instructions. The LaTeX template is maintained by the **LaTeX Typesetter** agent, so adjustments must be documented in its prompt instructions:

```python
# To add a package like 'microtype' or change margins, append to the Typesetter prompt:
latex_conversion_task = Task(
    description=(
        "..."
        "- Packages: fontspec, polyglossia, amsmath, graphicx, tikz, "
        "  fancyhdr, biblatex, hyperref, tabularx, booktabs, listings, microtype\n"
        "..."
    ),
    # ...
)
```

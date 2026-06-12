import os
import google.generativeai as genai

# Configure the Gemini API using the standard environment variable
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable is not set.")
    print("Please set it in your environment (e.g., export GEMINI_API_KEY='your-key') before running.")
else:
    genai.configure(api_key=api_key)

# Define the model to use (Gemini 1.5 Pro is recommended for complex reasoning/LaTeX generation)
MODEL_NAME = "gemini-1.5-pro"

class AcademicResearcherAgent:
    """
    Agent 1: Lead Academic Researcher
    Goal: Ingests outline, gathers quantitative cybersecurity statistics, and retrieves BibTeX citations.
    """
    def __init__(self):
        self.system_instruction = (
            "Role: Lead Academic Researcher.\n"
            "Goal: Execute the research tasks defined in the project plan and gather concrete, factual data.\n"
            "Instructions:\n"
            "Review the outline. Search for and compile highly accurate, up-to-date information, factual data points, "
            "and academic context. Extract key algorithms, architectural definitions, or historical context required. "
            "Provide a synthesized brief of raw facts, statistics, and verifiable claims. "
            "Include a list of potential references/citations in BibTeX format."
        )
        if api_key:
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=self.system_instruction
            )

    def run(self, outline_content):
        if not api_key:
            return "API Key not configured. Simulated Researcher brief output."
        prompt = f"Using this project outline, compile the research brief and BibTeX references:\n\n{outline_content}"
        response = self.model.generate_content(prompt)
        return response.text

class DataScientistAgent:
    """
    Agent 2: Lead AI Security Researcher & Data Scientist
    Goal: Formulates the Bayesian Threat Model mathematical variables and writes matplotlib scripts.
    """
    def __init__(self):
        self.system_instruction = (
            "Role: Lead AI Security Researcher and Data Scientist.\n"
            "Goal: Gather factual data, compile academic references, and generate Python plotting code.\n"
            "Instructions:\n"
            "Research the current state of LLM-driven anomaly detection.\n"
            "Gather statistics and BibTeX citations.\n"
            "Define the variables for a formal mathematical model representing threat probability (Bayesian inference).\n"
            "Write a standalone Python script using matplotlib that generates a graph titled 'Network Anomalies Over Time: LLM vs. Heuristic Detection'."
        )
        if api_key:
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=self.system_instruction
            )

    def run(self, research_brief):
        if not api_key:
            return "API Key not configured. Simulated Data Scientist math and script output."
        prompt = f"Based on this research brief, generate the mathematical threat scoring equations and the Python plotting script:\n\n{research_brief}"
        response = self.model.generate_content(prompt)
        return response.text

class LaTeXTypesetterAgent:
    """
    Agent 3: Senior Technical Writer & LaTeX Typesetter
    Goal: Ingests the outline, researcher notes, and data scientist math/code, and writes the XeLaTeX source.
    """
    def __init__(self):
        self.system_instruction = (
            "Role: Senior Technical Writer and LaTeX Typesetter.\n"
            "Goal: Draft the complete article based on the outline and research, fully formatted in LaTeX.\n"
            "Instructions:\n"
            "Transform the raw research notes and data scientist output into a cohesive, well-structured LaTeX document.\n"
            "The entire output must be valid, compilable LaTeX code.\n"
            "Include a formal cover page (Title, Author, Date).\n"
            "Generate at least one complex mathematical formula using advanced math packages.\n"
            "Generate at least one structural diagram using the TikZ library.\n"
            "Ensure proper use of sections, subsections, and bibliography structure."
        )
        if api_key:
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=self.system_instruction
            )

    def run(self, outline, research_brief, data_scientist_output):
        if not api_key:
            return "API Key not configured. Simulated LaTeX Writer output."
        prompt = (
            f"Write the complete compilable LaTeX document using the outline and research data below:\n\n"
            f"Outline:\n{outline}\n\n"
            f"Research Brief:\n{research_brief}\n\n"
            f"Data Scientist Output:\n{data_scientist_output}"
        )
        response = self.model.generate_content(prompt)
        return response.text

class QAEditorAgent:
    """
    Agent 4: Senior Technical Editor & QA Engineer
    Goal: Checks the LaTeX document for syntax, environment closures, and compilation errors.
    """
    def __init__(self):
        self.system_instruction = (
            "Role: Senior Technical Editor and QA Engineer.\n"
            "Goal: Review the generated LaTeX document for logical flow, factual consistency, and compilation readiness.\n"
            "Instructions:\n"
            "Analyze the LaTeX document. Do not change the core meaning.\n"
            "Ensure all formatting commands (TikZ, table, math) are closed and syntactically correct.\n"
            "Output the final, polished, compilable LaTeX code."
        )
        if api_key:
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=self.system_instruction
            )

    def run(self, raw_latex_content):
        if not api_key:
            return "API Key not configured. Simulated QA Editor output."
        prompt = f"Review and fix any syntax or compilation errors in the following LaTeX code:\n\n{raw_latex_content}"
        response = self.model.generate_content(prompt)
        return response.text

def run_agent_pipeline():
    print("==========================================================")
    print("Initializing Multi-Agent Threat Hunting Whitepaper Pipeline")
    print("==========================================================")
    
    # 1. Read the Outline
    outline_path = "OUTLINE.md"
    if os.path.exists(outline_path):
        with open(outline_path, "r", encoding="utf-8") as f:
            outline = f.read()
    else:
        outline = "# Outline: Autonomous Threat Hunting Whitepaper"

    # Instantiate the agents
    researcher = AcademicResearcherAgent()
    data_scientist = DataScientistAgent()
    writer = LaTeXTypesetterAgent()
    editor = QAEditorAgent()
    
    # Step 1: Research Gathering
    print("\n[Step 1/4] Running Lead Academic Researcher Agent...")
    research_brief = researcher.run(outline)
    with open("research_brief_output.txt", "w", encoding="utf-8") as f:
        f.write(research_brief)
    print("-> Research brief output saved to 'research_brief_output.txt'")
    
    # Step 2: Mathematical Derivations & Plot Scripts
    print("\n[Step 2/4] Running Data Scientist Agent...")
    ds_output = data_scientist.run(research_brief)
    with open("data_scientist_output.txt", "w", encoding="utf-8") as f:
        f.write(ds_output)
    print("-> Data Scientist math & plots saved to 'data_scientist_output.txt'")
    
    # Step 3: Typesetting Draft Document
    print("\n[Step 3/4] Running LaTeX Typesetter Agent...")
    raw_latex = writer.run(outline, research_brief, ds_output)
    with open("draft_main.tex", "w", encoding="utf-8") as f:
        f.write(raw_latex)
    print("-> Draft LaTeX file saved to 'draft_main.tex'")
    
    # Step 4: QA & Code Polish
    print("\n[Step 4/4] Running Senior Technical Editor & QA Agent...")
    polished_latex = editor.run(raw_latex)
    with open("polished_main.tex", "w", encoding="utf-8") as f:
        f.write(polished_latex)
    print("-> Polished LaTeX file saved to 'polished_main.tex'")
    
    print("\n==========================================================")
    print("Pipeline Execution Completed Successfully!")
    print("The final compilable code is saved at 'polished_main.tex'.")
    print("==========================================================")

if __name__ == "__main__":
    run_agent_pipeline()

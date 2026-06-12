# 💰 Cost & Resource Awareness Analysis: ATH-LLM

## 1. API Pricing Models & Token Rates

This project utilizes the **Gemini 2.0 Flash** model through LiteLLM (`gemini/gemini-2.0-flash`). Gemini 2.0 Flash provides a high-speed, cost-effective API tier optimized for multi-turn reasoning and code generation.

The calculations are based on the standard Google AI Studio pricing model:

| Model | Input Rate (per 1M tokens) | Output Rate (per 1M tokens) |
| :--- | :---: | :---: |
| **Gemini 2.0 Flash** | $0.075 | $0.300 |
| **GPT-4o** *(for comparison)* | $2.500 | $10.000 |
| **Claude 3.5 Sonnet** *(for comparison)* | $3.000 | $15.000 |

---

## 2. Estimated Operational Cost per Pipeline Run

Since the CrewAI pipeline operates sequentially, the context grows at each step. Below is a detailed breakdown of token consumption and operational cost per complete generation run (producing a ~15-page document):

### Token Consumption by Agent Phase

1. **Lead Academic Researcher**
   * *Inputs*: OUTLINE.md + RESEARCH_NOTES.md + System Instructions (~10,000 tokens)
   * *Outputs*: Detailed Markdown Research Brief (~2,000 tokens)
   * *Input Cost*: $0.00075 | *Output Cost*: $0.00060 | *Subtotal*: **$0.00135**

2. **AI Security Data Scientist**
   * *Inputs*: Researcher outputs + System Instructions (~12,000 tokens)
   * *Outputs*: Math models + Matplotlib Python scripts (~1,500 tokens)
   * *Input Cost*: $0.00090 | *Output Cost*: $0.00045 | *Subtotal*: **$0.00135**

3. **Senior Technical Writer (Markdown)**
   * *Inputs*: Research brief + Math context + Outlines (~15,000 tokens)
   * *Outputs*: Hebrew Markdown article draft (~6,000 tokens)
   * *Input Cost*: $0.00112 | *Output Cost*: $0.00180 | *Subtotal*: **$0.00292**

4. **LaTeX Typesetter & Document Engineer**
   * *Inputs*: Markdown article draft + Formatting rules (~20,000 tokens)
   * *Outputs*: Unpolished LaTeX code draft (~8,000 tokens)
   * *Input Cost*: $0.00150 | *Output Cost*: $0.00240 | *Subtotal*: **$0.00390**

5. **Senior Technical Editor & QA Engineer**
   * *Inputs*: LaTeX code draft + references.bib (~25,000 tokens)
   * *Outputs*: Polished, compilable LaTeX code (~8,000 tokens)
   * *Input Cost*: $0.00187 | *Output Cost*: $0.00240 | *Subtotal*: **$0.00427**

### Total Pipeline Run Summary
* **Total Input Tokens**: ~82,000 tokens
* **Total Output Tokens**: ~25,500 tokens
* **Total API Cost**: **$0.01379** (approx. **1.38 cents**)

---

## 3. Financial Comparison across Providers

Using a multi-agent sequential pipeline with larger models results in significantly higher operating costs:

```text
Gemini 2.0 Flash : $0.0138 (Base)
GPT-4o           : $0.4600 (33x baseline cost)
Claude 3.5 Sonnet: $0.6285 (45x baseline cost)
```

* **GPT-4o Cost**: 82k input ($0.205) + 25.5k output ($0.255) = **$0.460**
* **Claude 3.5 Sonnet Cost**: 82k input ($0.246) + 25.5k output ($0.3825) = **$0.628**

**Conclusion**: Operating the pipeline on Gemini 2.0 Flash is extremely economical, making iterative generation and testing viable for development.

---

## 4. Scaling Behavior & Cost Optimization

### Cost Scaling Functions
As the target page length $N$ scales, the cost curves behave as follows:
* **Research and Data Scientist Agents**: Constant complexity $O(1)$ relative to document length.
* **Writer, Typesetter, and QA Agents**: Output tokens scale linearly $O(N)$ with document page length.
* **Context accumulation**: Because each downstream agent takes the context of upstream tasks, the input tokens for late-stage agents (Typesetter, Editor) scale quadratically $O(N)$ with the text length.
* **Overall Cost Function**: $Cost(N) = \alpha N^2 + \beta N + \gamma$. For a 30-page document, the estimated run cost is ~$0.045, maintaining high feasibility.

### Caching Strategy (Resource Awareness)
To optimize resources during development:
1. **Prompt Cache**: Google AI Studio supports context caching. By caching the base research files and outlines (which remain static across runs), we can reduce input costs by up to **50%**.
2. **Local Models (Zero Cost)**: The pipeline can be redirected to a locally hosted model (e.g., Llama-3-8B via Ollama). This removes API fees entirely, incurring only the electricity cost of running a local GPU (~200W for 10 minutes $\approx$ $0.003).

# 📝 TODO — Autonomous Threat Hunting Whitepaper Project

## 🔴 High Priority

- [ ] **Test the agent pipeline end-to-end** — Run `python agent_system.py` with a valid API key (quota may have reset). Verify all 5 agents execute sequentially and produce output files.
- [ ] **Verify output files are generated** — After a successful run, check that `output/` contains:
  - `research_brief.md`
  - `math_and_plots.md`
  - `article_draft.md`
  - `draft_main.tex`
  - `polished_main.tex`
- [ ] **Compare agent output with hand-crafted LaTeX** — Review `output/polished_main.tex` vs. `latex/main.tex` and decide if the agent-generated version is usable or needs manual corrections.
- [ ] **Get a fresh API key or wait for quota reset** — The free-tier Gemini key may be rate-limited (429 error). Consider upgrading to a paid tier or waiting for the daily reset.

---

## 🟡 Medium Priority

- [ ] **Add real author name to all documents** — Verify `קוסאי עמארה` appears consistently everywhere (cover sheet, README footer, etc.).
- [ ] **Populate the `output/` directory with sample files** — Even if the pipeline can't run live, place example outputs so a reviewer can see the intermediate artifacts.
- [ ] **Add a `run.sh` / `run.ps1` compilation script** — One-click script that runs all 4 LaTeX passes from the `latex/` folder.
- [ ] **Review bibliography entries** — Some citations contain synthetic/fabricated metadata. Replace with real DOIs and verify journal names.
- [ ] **Test on a clean machine** — Clone the repo fresh, install dependencies from `requirements.txt`, and verify everything works from scratch.

---

## 🟢 Low Priority / Nice-to-Have

- [ ] **Add unit tests for the quality check script** — Test edge cases like missing files, malformed .bib entries, etc.
- [ ] **Add a GitHub Actions CI workflow** — Automatically run `scripts/run_quality_checks.py` on every push.
- [ ] **Generate a second TikZ diagram** — Add a diagram showing the CrewAI agent pipeline itself (not just the ATH architecture).
- [ ] **Add `\listoffigures` and `\listoftables`** — Optional academic enhancement after the Table of Contents.
- [ ] **Translate the README to Hebrew** — Provide a bilingual README matching the bilingual paper theme.
- [ ] **Record a demo video** — Screen-capture the pipeline running and the PDF output for the submission.
- [ ] **Clean up the AGENT_MASTER_CHECKLIST.md** — Mark completed items and remove redundant phases.

---

## ✅ Done

- [x] Rewrite `agent_system.py` using CrewAI (5 agents, sequential, Gemini 2.0 Flash)
- [x] Create `requirements.txt` with all dependencies
- [x] Set up `.env` with API keys (gitignored)
- [x] Generate SOC control room image → `latex/figures/soc_control_room.png`
- [x] Generate both Python graphs → `latex/figures/anomalies_over_time.pdf` + `latex/figures/performance_plot.pdf`
- [x] Write complete 17-page bilingual LaTeX paper (`latex/main.tex`)
- [x] Compile with 4-pass XeLaTeX + Biber — clean build
- [x] Add `lastpage` for dynamic page footer
- [x] Fix headheight warning and long equation overflow
- [x] Include both graphs as figures in the paper
- [x] Set real author name on cover sheet
- [x] Cite all 10 bibliography entries
- [x] Create comprehensive README.md
- [x] Create PROJECT_PLAN.md, AI_WORKFLOW_LOG.md, COST_PRICING_ANALYSIS.md, UI_UX_SHOWCASE.md, EXTENSIBILITY_GUIDE.md
- [x] Create automated quality check script (`scripts/run_quality_checks.py`)
- [x] Reorganize LaTeX files into `latex/` folder
- [x] Push everything to GitHub

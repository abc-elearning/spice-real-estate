---
name: spice-re
status: backlog
created: 2026-03-29T13:58:45Z
updated: 2026-03-29T14:02:54Z
progress: 0%
priority: P1
prd: .claude/prds/spice-re.md
task_count: 8
github: "https://github.com/abc-elearning/spice-real-estate/issues/1"
---

# Epic: spice-re

## Overview

We build a single Agent Skill `deciding-real-estate` that implements a 6-step cognitive loop for real estate cash flow investment decisions. The architecture follows Anthropic's 3-level progressive disclosure: Level 1 (YAML frontmatter, ~100 tokens, always loaded), Level 2 (SKILL.md body, <5k tokens, loaded on trigger), Level 3 (reference MDs + Python scripts, loaded on demand). This keeps Claude's context lean while providing deep domain knowledge when needed. The main technical risk is fitting the full cognitive loop instructions into SKILL.md's ~5k token budget — we mitigate by aggressively delegating detail to Level 3 reference files and using concise directive-style instructions.

## Architecture Decisions

### AD-1: One Smart Skill vs Multi-Skill Orchestration
**Context:** Original PRD proposed 6 interconnected skills with an orchestrator. Agent Skills are designed for independent triggering by Claude's skill matcher.
**Decision:** Single `deciding-real-estate` skill containing the full cognitive loop. Reference files and scripts provide depth.
**Alternatives rejected:** 6-skill architecture — complex orchestration, skill-to-skill invocation is non-standard, harder to debug.
**Trade-off:** Simpler architecture and deployment, but SKILL.md must be very concise. If it proves too constrained, we can split into 2-3 skills later.
**Reversibility:** Easy — splitting one skill into multiple is straightforward; reference files and scripts remain unchanged.

### AD-2: CLI Args + JSON Stdout for Script Interface
**Context:** SKILL.md needs to invoke Python scripts and parse results. Claude can run bash commands.
**Decision:** All scripts accept `--param value` CLI arguments and output JSON to stdout. Errors to stderr.
**Alternatives rejected:** (a) Claude reads script source and generates inline Python — non-deterministic, can't test independently. (b) Scripts read from stdin — harder to invoke from bash one-liners.
**Trade-off:** Verbose CLI invocations but fully testable and deterministic. Claude only needs to know the interface contract, not the implementation.
**Reversibility:** Easy — interface is a thin wrapper; internals can change freely.

### AD-3: Reference File Architecture for Token Budget
**Context:** SKILL.md body limited to ~5k tokens. The cognitive loop has 6 steps, each with substantial detail (bias catalog, formulas, personas, debate protocol).
**Decision:** SKILL.md contains step-by-step orchestration with `bash cat` commands to load reference files on demand. Heavy content lives in: FORMULAS.md, BIASES.md, PERSONAS.md, DECISION-CARD.md, SOURCES-VN.md.
**Alternatives rejected:** Embedding everything in SKILL.md — would exceed token limit. Using separate skills per reference — unnecessary complexity.
**Trade-off:** Extra context window usage when loading reference files, but keeps SKILL.md focused and each reference file independently maintainable.
**Reversibility:** Easy — reference files can be inlined or split further without changing the cognitive loop logic.

### AD-4: Markdown Decision Archive
**Context:** Need to store past Decision Cards for reflection step. PRD defers SQLite to v2.
**Decision:** Save Decision Cards as markdown files in `.spice_re/decisions/YYYY-MM-DD-{slug}.md`. No database.
**Alternatives rejected:** SQLite — overkill for v1 single-user, adds dependency. JSON files — less readable.
**Trade-off:** Simple file I/O, human-readable, but no query capability. Adequate for <50 decisions.
**Reversibility:** Easy — markdown can be migrated to SQLite later by parsing frontmatter.

## Technical Approach

### Skill Structure (`.claude/skills/spice-re/deciding-real-estate/`)

```
deciding-real-estate/
├── SKILL.md                  # Level 2: Cognitive loop orchestrator (~4k tokens)
├── FORMULAS.md               # Level 3: Financial formulas + OPEX checklist
├── BIASES.md                 # Level 3: 12 RE biases + detection markers + reframes
├── PERSONAS.md               # Level 3: 5 debate personas definitions
├── DECISION-CARD.md          # Level 3: Decision Card template (Vietnamese)
├── SOURCES-VN.md             # Level 3: Vietnam market data sources
├── EXAMPLES.md               # Level 3: 2-3 worked example scenarios
└── scripts/
    ├── monte_carlo.py        # Price projection (numpy)
    ├── dcf_calculator.py     # NPV, IRR, cash-on-cash (stdlib math)
    ├── cashflow_proforma.py  # 10-year pro-forma + DSCR (stdlib)
    └── bayesian_updater.py   # Prior/posterior + overconfidence (stdlib math)
```

### Python Environment

Scripts require numpy. Per CLAUDE.md, all Python runs from `.venv`:
```
cd .claude/skills/spice-re/deciding-real-estate
python3 -m venv .venv
.venv/bin/pip install numpy
```
SKILL.md MUST use `.venv/bin/python3` (not bare `python3`) for all script invocations.

### SKILL.md Cognitive Loop (Level 2)

The SKILL.md body orchestrates 6 steps in directive style. Each step is 3-5 lines of instruction telling Claude what to do, when to load reference files, and when to run scripts.

**HARD RULE: Selective Loading** — NEVER load more than one reference file per step. Load BIASES.md only in Step 3, FORMULAS.md only when calculating, PERSONAS.md only in Step 5, DECISION-CARD.md only in Step 5 output. This prevents context window crowding (~9-10k tokens if all loaded at once).

Approximate token budget per step:

| Step | Tokens | Key actions |
|------|--------|-------------|
| 1. Perception | ~400 | Parse intent (buy/sell/hold/compare), extract attributes, ask max 3 questions |
| 2. State Modeling | ~500 | Build user/property/market/constraint models as structured markdown |
| 3. Analysis | ~800 | `cat BIASES.md` → scan for biases; select framework; optionally `cat SOURCES-VN.md` → web search |
| 4. Simulation | ~600 | Run scripts: `monte_carlo.py`, `dcf_calculator.py`, `cashflow_proforma.py`; optionally `bayesian_updater.py` |
| 5. Decision | ~800 | `cat PERSONAS.md` → run debate; `cat DECISION-CARD.md` → generate card |
| 6. Reflection | ~400 | Save to archive, compare with past decisions if exist |
| Frontmatter + framing | ~500 | Skill metadata, trigger description, disclaimer |
| **Total** | **~4,000** | Within 5k budget |

### Python Scripts Interface Contracts

All scripts follow the same pattern:
- **Input:** `.venv/bin/python3 scripts/{name}.py --param1 value1 --param2 value2`
- **Output:** JSON to stdout with `status: "success"` or `status: "error"` + `message`
- **Errors:** stderr for warnings/errors, non-zero exit code on failure
- **Dependencies:** stdlib + numpy (monte_carlo only)
- **Input validation:** Every script validates input ranges before computation. Invalid inputs return `{"status":"error", "message":"..."}` JSON (not crash). Ranges: price>0, rates∈[0,1], years∈[1,50], sims∈[100,100000], prior∈(0,1) exclusive.
- **Shared utilities:** `scripts/utils.py` provides: `json_output(status, **data)`, `json_error(message)`, `validate_positive(name, value)`, `validate_range(name, value, min, max)`. All scripts import from utils.

**monte_carlo.py:**
```
--price FLOAT --growth FLOAT --std FLOAT --years INT --sims INT [--seed INT]
→ {"status":"success", "p10":F, "p25":F, "p50":F, "p75":F, "p90":F, "prob_loss":F, "mean":F}
```

**dcf_calculator.py:**
```
--monthly_rent FLOAT --growth FLOAT --opex_ratio FLOAT --discount FLOAT --years INT --initial FLOAT [--loan FLOAT --rate FLOAT]
→ {"status":"success", "npv":F, "irr":F, "cash_on_cash":F, "equity_multiple":F}
```

**cashflow_proforma.py:**
```
--price FLOAT --rent FLOAT --vacancy FLOAT --mgmt_fee FLOAT --tax_rate FLOAT --maintenance FLOAT --loan FLOAT --interest FLOAT --years INT [--rent_growth FLOAT --furniture FLOAT]
→ {"status":"success", "monthly_cf":F, "annual_coc":F, "dscr":F, "dscr_flag":"green|yellow|red", "year_by_year":[...]}
```

**bayesian_updater.py:**
```
--prior FLOAT --evidence_strength STR(weak|moderate|strong|very_strong) --evidence_direction STR(positive|negative)
→ {"status":"success", "prior":F, "posterior":F, "shift":F, "interpretation":"..."}
```

### Data Storage (`.spice_re/`)

```
.spice_re/
├── config.json              # User profile (NTH-4, created on first use)
└── decisions/               # Decision Card archive
    └── 2026-03-29-district7-apartment.md
```

Created lazily — scripts check `mkdir -p` before writing.

## Traceability Matrix

| PRD Requirement | Epic Coverage | Task(s) | Verification |
|-----------------|---------------|---------|--------------|
| FR-1: Cognitive Loop Orchestration | §SKILL.md Cognitive Loop | T1 | Manual: run 3 diverse queries, verify all 6 steps execute |
| FR-2: Bias Detection Engine | §BIASES.md + SKILL.md step 3 | T1, T2 | Manual: 5 biased inputs, verify correct bias flagged |
| FR-3: Cash Flow Pro-forma Calculator | §cashflow_proforma.py | T6, T2 | Automated: known inputs → expected JSON output |
| FR-4: Monte Carlo Simulation | §monte_carlo.py | T4 | Automated: fixed seed → deterministic output |
| FR-5: DCF Calculator | §dcf_calculator.py | T5 | Automated: cross-validate vs Excel |
| FR-6: Bayesian Updater | §bayesian_updater.py | T7 | Automated: known prior + evidence → expected posterior |
| FR-7: Multi-Persona Debate | §PERSONAS.md + SKILL.md step 5 | T1, T3 | Manual: verify 5 personas respond, tensions identified |
| FR-8: Decision Card Generation | §DECISION-CARD.md + SKILL.md step 5 | T1, T3 | Manual: verify all sections present, disclaimer included |
| NTH-1: Web Research | §SOURCES-VN.md + SKILL.md step 3 | T1, T3 | Manual: verify web search triggered for macro data |
| NTH-2: Decision Archive | §Data Storage + SKILL.md step 6 | T8 | Manual: verify card saved to .spice_re/decisions/ |
| NTH-3: Sensitivity Analysis | Prompt-based in SKILL.md step 4 | T1 | Deferred — manual prompt capability |
| NTH-4: User Profile Persistence | Deferred | — | Deferred to follow-up |
| NFR-1: Token Budget <5k | §SKILL.md token budget table | T1 | Automated: `wc -w SKILL.md` × 1.3 < 5000 |
| NFR-2: CLI + JSON Interface | §Script Interface Contracts | T4-T7 | Automated: verify JSON output validity |
| NFR-3: Script Reliability | §monte_carlo.py --seed | T4 | Automated: same seed → same output |
| NFR-4: Decision Card Completeness | §DECISION-CARD.md template | T3, T8 | Manual: parse card, verify all sections |
| NFR-5: Platform Compatibility | All tasks — stdlib + numpy only | All | Automated: no external imports |

## Implementation Strategy

### Phase 1: Foundation (T1, T2, T3 — parallel)
Build the skill skeleton and all reference files. After this phase, the skill can trigger and run the cognitive loop prompt-based (without scripts). Exit criterion: SKILL.md triggers on RE queries, loads reference files, produces a basic Decision Card using Claude's reasoning alone.

### Phase 2: Quantitative Engine (T4, T5, T6, T7 — parallel)
Build all 4 Python scripts with CLI interfaces. Each script is independently testable. After this phase, the skill can invoke scripts for financial calculations. Exit criterion: all 4 scripts produce valid JSON for test inputs, SKILL.md instructions reference correct invocation syntax.

### Phase 3: Integration & Polish (T8)
Create example scenarios, test end-to-end flow, set up decision archive, verify token budget. Exit criterion: 3 real-world scenarios run through full cognitive loop with scripts, all Decision Cards complete, SKILL.md under 5k tokens.

## Task Breakdown

##### T1: SKILL.md — Cognitive Loop Orchestrator
- **Phase:** 1 | **Parallel:** yes (with T2, T3) | **Est:** 2d | **Depends:** — | **Complexity:** complex
- **What:** Create `SKILL.md` with Agent Skills frontmatter (name: `deciding-real-estate`, description per Anthropic spec) and Level 2 body implementing the 6-step cognitive loop. Each step is 3-5 directive lines telling Claude: what to extract, when to `cat` reference files (HARD RULE: one file per step max), when to run scripts via `.venv/bin/python3`, what to output. Include framework selection logic (cash flow → DCF+DSCR; capital gain → EV+Monte Carlo; sell/hold → Prospect Theory+Regret). Set up `.venv` with numpy. Must stay under ~3,800 words (~5k tokens).
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/SKILL.md`
- **PRD requirements:** FR-1, FR-2 (partial), FR-7 (partial), FR-8 (partial), NFR-1
- **Key risk:** Token budget is tight — every word counts. Iterate after T2/T3 to ensure reference file paths are correct.
- **Interface produces:** Skill entry point that T2-T8 all reference. File paths for reference files and scripts. `.venv/` with numpy installed.

##### T2: FORMULAS.md + BIASES.md — Financial & Behavioral Reference
- **Phase:** 1 | **Parallel:** yes (with T1, T3) | **Est:** 1d | **Depends:** — | **Complexity:** moderate
- **What:** Create `FORMULAS.md` with all financial formulas (cap rate, gross/net rental yield, cash-on-cash, DSCR, NPV, IRR, break-even horizon, LTV, GRM, vacancy rate, CapEx reserve, NOI, operating expense ratio, break-even occupancy) plus CASHFLOW-VERIFICATION checklist with Vietnam-specific cost ranges. Create `BIASES.md` with 12 RE-specific biases, each having: name, description, RE-specific example, linguistic detection markers (phrases/patterns that signal the bias), and reframed question. Priority biases (anchoring, loss aversion, herding, disposition effect) get more detailed markers. **Source material:** Port formulas from `docs/PRD_SpiceRE.md` §1.4 and §4.3, bias table from §4.2.
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/FORMULAS.md`, `.claude/skills/spice-re/deciding-real-estate/BIASES.md`
- **PRD requirements:** FR-2, FR-3 (formula reference)
- **Key risk:** Bias detection markers need to be specific enough for reliable matching but general enough to catch variants.

##### T3: PERSONAS.md + DECISION-CARD.md + SOURCES-VN.md — Debate & Output Reference
- **Phase:** 1 | **Parallel:** yes (with T1, T2) | **Est:** 1d | **Depends:** — | **Complexity:** moderate
- **What:** Create `PERSONAS.md` defining 5 debate personas (Veteran Investor, Cash Flow Investor, Risk Analyst, End User, Contrarian) — each with: lens, style, tendency, key questions, framework preference, and tension relationships with other personas. Create `DECISION-CARD.md` as the Vietnamese-language template for Decision Card output with all required sections (situation, framework, bias alerts, scenarios P10/P50/P90, debate summary, recommendation + confidence %, next steps, disclaimer). Create `SOURCES-VN.md` with Vietnam market data sources table (batdongsan, cafeland, CBRE, Savills, SBV, GSO, etc.) with query patterns for Claude's web_search. **Source material:** Port personas from `docs/PRD_SpiceRE.md` §4.4, Decision Card template from §4.1, sources from §4.5.
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/PERSONAS.md`, `.claude/skills/spice-re/deciding-real-estate/DECISION-CARD.md`, `.claude/skills/spice-re/deciding-real-estate/SOURCES-VN.md`
- **PRD requirements:** FR-7, FR-8, NTH-1
- **Key risk:** Personas must have genuinely conflicting viewpoints to produce useful tension, not just varied perspectives.

##### T4: monte_carlo.py — Price Projection Script
- **Phase:** 2 | **Parallel:** yes (with T5, T6, T7) | **Est:** 1d | **Depends:** T1 | **Complexity:** moderate
- **What:** Create `scripts/monte_carlo.py` implementing Geometric Brownian Motion for property price simulation. Accept CLI args (price, growth, std, years, sims, optional seed). Use numpy for vectorized simulation (1000 iterations default). Output JSON with P10/P25/P50/P75/P90, probability of loss, mean. Include argparse with help text. Fixed seed produces deterministic output for testing. Input validation via `scripts/utils.py` (price>0, std>0, years 1-50, sims 100-100000). Fallback to stdlib `random` if numpy unavailable with stderr warning.
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/scripts/monte_carlo.py`, `scripts/utils.py`
- **PRD requirements:** FR-4, NFR-2, NFR-3
- **Key risk:** numpy import failure on some environments — add fallback to stdlib `random` with warning.
- **Interface receives from T1:** Script invocation syntax documented in SKILL.md step 4.

##### T5: dcf_calculator.py — Discounted Cash Flow Script
- **Phase:** 2 | **Parallel:** yes (with T4, T6, T7) | **Est:** 1d | **Depends:** T1 | **Complexity:** moderate
- **What:** Create `scripts/dcf_calculator.py` computing NPV (sum of discounted cash flows minus initial investment), IRR (rate where NPV=0, using bisection method for reliability), cash-on-cash return, and equity multiple. Accept CLI args for monthly rent, growth rate, OPEX ratio, discount rate, years, initial investment, optional loan/rate. Output JSON. Use stdlib `math` only — no numpy needed. Input validation via `scripts/utils.py` (discount_rate>0, years 1-50, initial>0). IRR solver: max 1000 iterations, return `"irr": null` with `"irr_note": "..."` if no convergence.
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/scripts/dcf_calculator.py`
- **PRD requirements:** FR-5, NFR-2
- **Key risk:** IRR calculation can fail to converge for edge cases — add max iterations and fallback to "IRR not calculable" with explanation.

##### T6: cashflow_proforma.py — 10-Year Cash Flow Pro-forma Script
- **Phase:** 2 | **Parallel:** yes (with T4, T5, T7) | **Est:** 1.5d | **Depends:** T1 | **Complexity:** complex
- **What:** Create `scripts/cashflow_proforma.py` building a 10-year monthly cash flow model. Inputs: property price, monthly rent, vacancy rate, management fee per sqm, tax rate (default 10%), maintenance (default 1.5% of price/year), loan amount, interest rate, optional rent growth, optional furniture depreciation. Compute: monthly net cash flow, annual cash-on-cash return, DSCR, DSCR flag (red <1.0, yellow 1.0-1.3, green ≥1.3), and year-by-year breakdown. Output JSON with summary + `year_by_year` array. DSCR < 1.0 must be flagged as RED FLAG per FR-3. Input validation via `scripts/utils.py` (price>0, rent≥0, rates∈[0,1]). Guard against rent=0 with loan>0 (DSCR would be 0, not division error).
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/scripts/cashflow_proforma.py`
- **PRD requirements:** FR-3, NFR-2, NFR-4
- **Key risk:** OPEX parameter defaults must match Vietnam market reality. Conservative defaults: vacancy 12.5% (1.5 months/year), management 10k VND/m², tax 10%, maintenance 1.5%.

##### T7: bayesian_updater.py — Probability Updating Script
- **Phase:** 2 | **Parallel:** yes (with T4, T5, T6) | **Est:** 1d | **Depends:** T1 | **Complexity:** moderate
- **What:** Create `scripts/bayesian_updater.py` implementing Bayesian probability updating. Accept CLI args: prior probability (0-1 exclusive), evidence strength (weak/moderate/strong/very_strong), evidence direction (positive/negative). Map evidence strength to likelihood ratios (weak: 1.5, moderate: 3, strong: 6, very_strong: 12). Compute posterior using Bayes' theorem. Include overconfidence detection: if user's stated confidence diverges >20% from base rate, flag it. Output JSON with prior, posterior, shift, interpretation text. Input validation via `scripts/utils.py`: prior must be strictly between 0 and 1 (exclusive) — Bayes' theorem is undefined at boundaries.
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/scripts/bayesian_updater.py`
- **PRD requirements:** FR-6, NFR-2
- **Key risk:** Likelihood ratio calibration is inherently subjective — document the mapping clearly and allow user override.

##### T8: EXAMPLES.md + Integration Testing + Decision Archive
- **Phase:** 3 | **Parallel:** no | **Est:** 1.5d | **Depends:** T1-T7 | **Complexity:** moderate
- **What:** Create `EXAMPLES.md` with 3 worked scenarios: (1) Buy apartment for rental — positive cash flow, (2) Buy apartment — negative cash flow detected and flagged, (3) Sell vs hold land with loss aversion bias detected. Each example shows full cognitive loop flow with script outputs. Set up `.spice_re/decisions/` archive directory. Test end-to-end: create `scripts/test_all.py` with ~15 test cases — 3 per script (happy path, boundary inputs, invalid inputs) + JSON validity check + SKILL.md token count check. Verify Decision Card template produces complete output.
- **Key files:** `.claude/skills/spice-re/deciding-real-estate/EXAMPLES.md`, `.claude/skills/spice-re/deciding-real-estate/scripts/test_all.py`
- **PRD requirements:** NTH-2, NFR-1, NFR-2, NFR-4
- **Key risk:** End-to-end testing depends on all Phase 2 scripts working correctly. If any script has bugs, integration testing will surface them here.
- **Interface receives from T1-T7:** All skill files and scripts complete and individually tested.

## Risks & Mitigations

| Risk | Severity | Likelihood | Impact | Mitigation |
|------|----------|------------|--------|------------|
| SKILL.md exceeds 5k token budget | High | Medium | Skill won't load correctly, cognitive loop incomplete | Token budget table per step, aggressive delegation to Level 3, iterate compression after Phase 1 |
| Cash flow script produces incorrect financial results | High | Low | User makes bad investment based on wrong numbers | Test against 5 known Excel scenarios, cross-validate NPV/IRR with financial calculator, conservative OPEX defaults |
| Bias detection false positives | Medium | Medium | User loses trust, ignores valid warnings | Question-based framing, require 2+ markers, review with real conversations |
| numpy not available in target environment | Medium | Low | Monte Carlo script fails | Fallback to stdlib `random` with performance warning, test on fresh Claude Code CLI |
| Agent Skills triggering unreliable | Medium | Medium | Skill doesn't activate for RE queries | Broad trigger description in frontmatter, test with 10 diverse RE phrasings |
| Debate personas produce superficial or repetitive positions | Medium | Medium | Debate adds no value, waste of context | Rich persona definitions with specific key questions and tension relationships, test with 5 scenarios |

## Dependencies

- **Anthropic Agent Skills standard** — `.claude/skills/` directory support in Claude Code CLI. Owner: Anthropic. Status: resolved.
- **numpy** — Required for monte_carlo.py. Owner: pre-installed. Status: resolved (fallback planned).
- **Claude web_search** — Required for NTH-1 market research. Owner: Claude Code CLI. Status: resolved.
- **Python 3.8+** — Required for all scripts. Owner: system. Status: resolved.

## Success Criteria (Technical)

| PRD Criterion | Technical Metric | Target | How to Measure |
|---------------|-----------------|--------|----------------|
| Bias detection precision ≥80% | Correct bias ID on test inputs | ≥16/20 correct | Manual: run 20 biased scenarios through SKILL.md |
| Decision Card completeness 100% | All template sections non-empty | 100% | Automated: parse card against DECISION-CARD.md template |
| Negative CF detection 100% | cashflow_proforma.py DSCR flag | All DSCR<1.0 flagged red | Automated: 10 negative CF test inputs |
| DSCR alert accuracy 100% | Script dscr_flag field | Correct flag for all test cases | Automated: test with known DSCR values |
| SKILL.md token budget <5k | `wc -w SKILL.md` × 1.3 | < 5000 | Automated: word count check |
| Script JSON validity 100% | Output passes json.tool | All outputs valid | Automated: `python3 -m json.tool` on each script |
| Cognitive loop completion ≥90% | All 6 steps execute | ≥9/10 test queries | Manual: run 10 diverse queries |
| Monte Carlo accuracy | Match analytical GBM | Within 5% for simple cases | Automated: compare with closed-form |
| DCF accuracy | Match Excel | NPV/IRR within 0.1% | Automated: 5 cross-validation cases |
| Debate tensions ≥3 per debate | Count identified tensions | ≥3 | Manual: review 5 debate outputs |

## Estimated Effort

- **Total:** ~10 days
- **Critical path:** T1 (2d) → T6 (1.5d) → T8 (1.5d) = 5 days
- **With parallelism:** Phase 1 (2d) → Phase 2 (1.5d) → Phase 3 (1.5d) = **5 days**
- **Buffer:** +2 days for SKILL.md token optimization and script edge cases

## Deferred / Follow-up

- **NTH-3: Sensitivity Analysis** — Claude handles prompt-based in v1. Dedicated script if usage shows need.
- **NTH-4: User Profile Persistence** — `.spice_re/config.json` created on demand. Full profile management deferred.
- **SQLite decision database** — Markdown archive sufficient for v1 (<50 decisions).
- **Location Intelligence 8-tool toolkit** — General web search guidance in SOURCES-VN.md for now.
- **Reflection loop with prediction tracking** — Archive decisions but don't track outcomes yet.
- **Additional scripts** (sensitivity.py, scenario_builder.py, ev_calculator.py, risk_classifier.py) — Prompt-based in v1.

## Tasks Created

| # | Task | Phase | Parallel | Est. | Depends On | Status |
|---|------|-------|----------|------|------------|--------|
| 001 | SKILL.md — Cognitive Loop Orchestrator | 1 | yes | 2d | — | open |
| 002 | FORMULAS.md + BIASES.md | 1 | yes | 1d | — | open |
| 003 | PERSONAS.md + DECISION-CARD.md + SOURCES-VN.md | 1 | yes | 1d | — | open |
| 010 | monte_carlo.py + utils.py | 2 | yes | 1d | 001 | open |
| 011 | dcf_calculator.py | 2 | yes | 1d | 001, 010 | open |
| 012 | cashflow_proforma.py | 2 | yes | 1.5d | 001, 010 | open |
| 013 | bayesian_updater.py | 2 | yes | 1d | 001, 010 | open |
| 090 | EXAMPLES.md + test_all.py + Integration | 3 | no | 1.5d | all | open |

### Summary
- **Total tasks:** 8
- **Parallel tasks:** 6 (Phase 1: 3, Phase 2: 4 minus sequential utils.py)
- **Sequential tasks:** 2 (critical path boundaries)
- **Estimated total effort:** 10 days
- **Critical path:** 001 (2d) → 012 (1.5d) → 090 (1.5d) = ~5 days

### Dependency Graph
```
001 ─┬──→ 010 ─┬──→ 011 ──→ 090
     │         ├──→ 012 ──→ 090
     │         └──→ 013 ──→ 090
002 ─────────────────────→ 090
003 ─────────────────────→ 090

Critical path: 001 → 010 → 012 → 090 (~6d)
```

### PRD Coverage
| PRD Requirement | Covered By | Status |
|-----------------|-----------|--------|
| FR-1: Cognitive Loop | 001 | ✅ Covered |
| FR-2: Bias Detection | 001, 002 | ✅ Covered |
| FR-3: Cash Flow Pro-forma | 012, 002 | ✅ Covered |
| FR-4: Monte Carlo | 010 | ✅ Covered |
| FR-5: DCF Calculator | 011 | ✅ Covered |
| FR-6: Bayesian Updater | 013 | ✅ Covered |
| FR-7: Multi-Persona Debate | 001, 003 | ✅ Covered |
| FR-8: Decision Card | 001, 003 | ✅ Covered |
| NFR-1: Token Budget | 001, 090 | ✅ Covered |
| NFR-2: CLI + JSON | 010-013, 090 | ✅ Covered |
| NFR-3: Reliability | 010 | ✅ Covered |
| NFR-4: Card Completeness | 003, 090 | ✅ Covered |
| NFR-5: Platform | All | ✅ Covered |

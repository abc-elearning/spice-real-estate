---
name: spice-re
description: One Smart Skill for structured real estate cash flow investment decisions on Claude Code CLI
status: validated
priority: P1
scale: medium
created: 2026-03-29T13:53:51Z
updated: 2026-03-29T13:56:53Z
---

# PRD: spice-re

## Executive Summary

SpiceRE is a single Agent Skill (`deciding-real-estate`) for Claude Code CLI that transforms Claude into a structured decision advisor for real estate cash flow investments. It solves the problem that investors make emotional decisions driven by cognitive biases (anchoring to listing price, overestimating gross yield, ignoring hidden OPEX) rather than systematic analysis. The skill implements a 6-step cognitive loop (perception → state modeling → analysis → simulation → decision → reflection) backed by 4 Python scripts for financial reliability, 12-bias detection, and 5-persona adversarial debate. Target user: Vietnamese cash flow real estate investors who need consistent, bias-aware decision support.

## Problem Statement

Real estate investment decisions are among the largest financial decisions an individual makes — often 30-70% of total net worth. Research from behavioral finance shows:

- **Anchoring bias** causes investors to fixate on listing prices or original purchase prices, ignoring current market fundamentals (Northcraft & Neale, 1987)
- **Loss aversion** prevents timely selling of underperforming assets — investors hold losers too long and sell winners too early (Disposition Effect)
- **Gross yield illusion**: Vietnamese cash flow investors routinely overestimate returns by using gross rental yield instead of net yield after management fees (5-15k VND/m²/month), taxes (10% gross rent), maintenance (1-2% property value/year), vacancy (1.5-2 months/year), and furniture depreciation
- **FOMO/herding** drives purchases in hot markets without fundamental analysis

Currently, no AI agent combines cognitive bias detection with cash flow analysis and scientific decision frameworks running natively on Claude Code. Existing workarounds — manual Excel spreadsheets, ad-hoc Claude prompting, broker advice — lack consistency, miss biases, and don't stress-test assumptions.

## Target Users

**1. Cash Flow Investor (Primary)**
- **Context:** Evaluating specific properties for rental income. Owns or plans to own 1-20+ rental properties. Prioritizes monthly cash flow over capital gains.
- **Primary need:** Reliable net yield calculation with realistic OPEX, bias detection when evaluating deals, stress testing (interest rate +2%, vacancy ×2, rental -15%).
- **Pain level:** High — one bad deal with negative cash flow costs millions of VND per month indefinitely.

**2. First-time Buyer (Secondary)**
- **Context:** Considering first property purchase, torn between buying vs renting, overwhelmed by information.
- **Primary need:** Structured framework to think through the decision, bias awareness (FOMO, herding), clear comparison of buy vs rent scenarios.
- **Pain level:** High — irreversible decision with limited experience.

**3. Existing Owner Considering Sale (Secondary)**
- **Context:** Holds property that may be underperforming, anchored to purchase price, struggling with loss aversion.
- **Primary need:** Objective reframing (Prospect Theory), opportunity cost analysis, regret minimization framework.
- **Pain level:** Medium — ongoing holding cost but emotional attachment prevents action.

## User Stories

**US-1: Cash Flow Analysis for Rental Property**
As a cash flow investor, I want to get a realistic net cash flow projection for a specific property so that I know the true monthly return after all expenses.

Acceptance Criteria:
- [ ] System calculates net yield using actual OPEX (management fees, taxes, maintenance, vacancy, depreciation) not just gross yield
- [ ] DSCR is computed and flagged if below 1.3
- [ ] Negative cash flow scenarios are explicitly warned before any recommendation
- [ ] Output includes comparison with alternatives (bank deposit, bonds)

**US-2: Cognitive Bias Detection**
As a cash flow investor evaluating a rental property, I want the system to detect when I'm being influenced by cognitive biases so that I can make a more rational decision.

Acceptance Criteria:
- [ ] System scans user input for linguistic markers of at least 4 key biases (anchoring, loss aversion, herding, disposition effect)
- [ ] Detected biases are presented as questions ("Are you anchoring to X?") not assertions
- [ ] Each bias detection includes a reframed perspective

**US-3: Multi-Perspective Debate**
As a cash flow investor about to commit to a deal, I want to hear structured arguments from multiple viewpoints so that I can stress-test my assumptions.

Acceptance Criteria:
- [ ] 5 distinct personas provide position statements with key reasoning
- [ ] Tension points between personas are identified and synthesized
- [ ] Cash Flow Investor persona always evaluates DSCR and net yield
- [ ] Output includes what the tensions reveal about hidden risks

**US-4: Decision Card Output**
As a cash flow investor, I want a structured Decision Card summarizing all analysis so that I have a single reference document for my decision.

Acceptance Criteria:
- [ ] Decision Card includes: situation summary, framework used, bias alerts, scenario table (P10/P50/P90), debate summary, recommendation with confidence level, next steps
- [ ] Confidence scoring: Low (<40%), Medium (40-70%), High (>70%)
- [ ] Disclaimer is always present
- [ ] Card is saved to decision archive for future reference

**US-5: Monte Carlo Price Projection**
As a cash flow investor, I want probabilistic price projections so that I understand the range of possible outcomes for property value, not just point estimates.

Acceptance Criteria:
- [ ] 1000-iteration simulation with configurable parameters (mean growth, std dev, years)
- [ ] Output includes P10, P25, P50, P75, P90 distribution
- [ ] Probability of loss is explicitly calculated
- [ ] Script runs via CLI args and outputs JSON

**US-6: Bayesian Probability Updating**
As a cash flow investor receiving new market information (e.g., infrastructure announcements, policy changes), I want to update my probability estimates systematically so that I don't overreact or underreact to new evidence.

Acceptance Criteria:
- [ ] Accepts prior probability + evidence strength as input
- [ ] Outputs posterior probability with explanation
- [ ] Detects overconfidence by comparing user confidence vs base rates
- [ ] Script runs via CLI args and outputs JSON

**US-7: First-time Buy vs Rent Decision**
As a first-time buyer, I want a structured comparison of buying versus renting so that I can make an informed decision about my first property.

Acceptance Criteria:
- [ ] System runs break-even horizon calculation (transaction costs / monthly delta)
- [ ] Bias detection flags FOMO and herding if present
- [ ] Output includes both financial and non-financial factors

**US-8: Sell vs Hold Reframing**
As an existing owner considering selling, I want objective reframing of my situation so that I can overcome loss aversion and make a rational decision.

Acceptance Criteria:
- [ ] Prospect Theory reframe: "If you didn't own this, would you buy at current price?"
- [ ] Opportunity cost calculation vs alternatives (bank deposit, bonds)
- [ ] Disposition effect check: holding losers too long?

## Requirements

### Functional Requirements (MUST)

**FR-1: Cognitive Loop Orchestration**
The skill MUST implement a 6-step cognitive loop that processes any real estate decision query through: perception (parse intent + extract attributes), state modeling (build user/property/market/constraint models), analysis (bias scan + framework selection + market context), simulation (Monte Carlo + DCF + scenarios), decision (5-persona debate + synthesis + Decision Card), reflection (archive + comparison with past decisions).

Scenario: Standard buy decision
- GIVEN user asks "Should I buy this 2BR apartment in District 7 for 3.2B VND, rental 13M/month, 50% loan?"
- WHEN the cognitive loop runs
- THEN system parses intent as BUY, extracts property attributes, asks max 3 clarifying questions, and proceeds through all 6 steps to produce a Decision Card

Scenario: Insufficient information
- GIVEN user provides incomplete property details (missing price or location)
- WHEN perception step runs
- THEN system asks targeted questions (max 3 per turn) before proceeding

**FR-2: Bias Detection Engine**
The skill MUST detect and report cognitive biases from user input using linguistic marker scanning for 12 RE-specific biases, with priority detection for: anchoring, loss aversion, herding, disposition effect, sunk cost, overconfidence, familiarity, confirmation, recency, status quo, endowment effect, framing.

Scenario: Anchoring detected
- GIVEN user says "I bought this land for 3.2B, now market is 2.6B but I listed at 3B"
- WHEN bias detection runs
- THEN system flags ANCHORING (neo vào giá mua 3.2B) and LOSS AVERSION, presents reframed question: "If you didn't own this, would you buy at 2.6B?"

Scenario: No biases detected
- GIVEN user provides objective, data-driven analysis without emotional framing
- WHEN bias detection runs
- THEN system notes "No significant biases detected" and proceeds

**FR-3: Cash Flow Pro-forma Calculator**
The skill MUST generate a 10-year cash flow pro-forma using `cashflow_proforma.py` with realistic OPEX assumptions following CASHFLOW-VERIFICATION checklist.

Scenario: Positive cash flow property
- GIVEN property with gross rent 15M/month, price 2.8B, 40% loan at 9%
- WHEN cashflow_proforma.py runs with all OPEX inputs (management, tax, maintenance, vacancy, depreciation, debt service)
- THEN output shows monthly net cash flow, annual cash-on-cash return, DSCR, and 10-year NPV

Scenario: Negative cash flow detection
- GIVEN property where debt service + OPEX exceeds rental income
- WHEN cashflow_proforma.py runs
- THEN DSCR < 1.0 is flagged as RED FLAG, monthly negative amount shown, and system warns before any recommendation

**FR-4: Monte Carlo Simulation**
The skill MUST run probabilistic price simulations using `monte_carlo.py` with configurable parameters.

Scenario: 5-year projection
- GIVEN current price 3.2B, mean annual growth 5%, std dev 8%
- WHEN monte_carlo.py runs with n_sims=1000, n_years=5
- THEN output JSON contains P10/P25/P50/P75/P90 price distribution and probability of loss

**FR-5: DCF Calculator**
The skill MUST compute NPV and IRR using `dcf_calculator.py` for rental income streams.

Scenario: Standard rental DCF
- GIVEN rental income 12M/month, growth rate 3%, OPEX 40%, discount rate 10%, holding period 10 years
- WHEN dcf_calculator.py runs
- THEN output JSON contains NPV, IRR, cash-on-cash return, equity multiple

**FR-6: Bayesian Updater**
The skill MUST update probability estimates using `bayesian_updater.py` when new evidence is provided.

Scenario: New infrastructure announcement
- GIVEN prior probability of price increase 40%, new evidence: metro line confirmed (evidence strength: strong)
- WHEN bayesian_updater.py runs
- THEN posterior probability is calculated and explained, overconfidence check compares with base rates

**FR-7: Multi-Persona Debate**
The skill MUST conduct structured debate with 5 personas: Veteran Investor, Cash Flow Investor, Risk Analyst, End User, Contrarian Devil's Advocate.

Scenario: Contentious deal
- GIVEN apartment in Thu Duc, 2.5B VND, rental 10M/month, buyer also plans weekend personal use, 50% loan at 9%
- WHEN debate runs
- THEN each persona gives 3-5 sentence position, tension points are identified (e.g., Veteran vs End User on ROI vs livability, Cash Flow Investor flags low net yield vs End User values personal use), synthesis reveals what tensions mean for the decision

**FR-8: Decision Card Generation**
The skill MUST produce a structured Decision Card in Vietnamese combining all analysis outputs.

Scenario: Complete analysis
- GIVEN all prior steps have completed (bias scan, simulation, debate)
- WHEN Decision Card is generated
- THEN card includes all sections (situation, framework, bias alerts, scenario table, debate summary, recommendation with confidence %, next steps, disclaimer)
- AND card is saved to `.spice_re/decisions/` archive

### Functional Requirements (NICE-TO-HAVE)

**NTH-1: Web Research for Market Context**
The skill SHOULD use Claude's web_search tool to gather macro indicators (interest rates, credit growth, market cycle phase) when making decisions. Property-specific data comes from user input.

Scenario: Macro context enrichment
- GIVEN user asks about buying in Da Nang
- WHEN market research step runs
- THEN system searches for current interest rates, Da Nang market cycle, recent comparable transactions from batdongsan.com.vn / CBRE / Savills

**NTH-2: Decision Archive with History Comparison**
The skill SHOULD save decisions to markdown archive and reference past decisions during reflection step.

Scenario: Repeat analysis
- GIVEN user previously analyzed a property in the same area
- WHEN reflection step runs
- THEN system references past Decision Card and notes changes in market conditions or user profile

**NTH-3: Sensitivity Analysis (Prompt-based)**
The skill SHOULD perform sensitivity analysis on 3 key variables (price, interest rate, rental yield) using Claude's reasoning rather than a dedicated script.

Scenario: Interest rate stress test
- GIVEN base case with 9% interest rate
- WHEN user asks "what if rates go to 12%?"
- THEN system recalculates cash flow and DSCR with new rate, shows impact

**NTH-4: User Profile Persistence**
The skill SHOULD maintain a user profile in `.spice_re/config.json` tracking risk tolerance, investment horizon, portfolio composition, and preferred metrics.

Scenario: Returning user
- GIVEN user has config.json with risk_tolerance: 6/10, horizon: 10 years
- WHEN new analysis starts
- THEN system uses profile to calibrate recommendations and framework selection

### Non-Functional Requirements

**NFR-1: Agent Skills Token Budget**
SKILL.md Level 2 instructions MUST be under 5,000 tokens. Reference files (Level 3) loaded on demand.
- Threshold: SKILL.md < 5,000 tokens measured by `wc -w` × 1.3

**NFR-2: Script Execution Interface**
All Python scripts MUST accept CLI arguments and output JSON to stdout. Error output to stderr.
- Interface: `python3 scripts/{name}.py --param1 value1 --param2 value2`
- Output: Valid JSON parseable by Claude
- Dependencies: stdlib + numpy only

**NFR-3: Script Reliability**
Python scripts MUST produce identical output for identical input (deterministic with fixed seed for Monte Carlo).
- Threshold: 100% reproducibility when `--seed` parameter is provided

**NFR-4: Decision Card Completeness**
Every Decision Card MUST contain all required sections. No empty sections allowed.
- Threshold: 100% field completion rate verified by automated check

**NFR-5: Platform Compatibility**
v1 MUST work on Claude Code CLI with full network access. Scripts use Python 3.8+ stdlib + numpy.
- No external API calls in scripts
- Web research via Claude's native web_search tool only

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Bias detection precision | ≥80% on 20 test cases | Manual review: present biased scenario, check if correct bias flagged |
| Decision Card completeness | 100% fields filled | Automated: parse Decision Card, verify all sections non-empty |
| Negative cash flow detection | 100% catch rate | Test 10 negative CF scenarios, verify all flagged before recommendation |
| DSCR alert accuracy | 100% when DSCR < 1.0 | Automated: run cashflow_proforma.py with known negative CF inputs |
| SKILL.md token budget | < 5,000 tokens | `wc -w SKILL.md` × 1.3 < 5,000 |
| Script JSON output validity | 100% valid JSON | Automated: pipe output through `python3 -m json.tool` |
| Cognitive loop completion rate | ≥90% of queries complete all 6 steps | Test 10 diverse queries, verify all steps executed |
| Monte Carlo accuracy | Output within 5% of analytical solution for known distributions | Compare with closed-form GBM for simple cases |
| DCF calculation accuracy | NPV/IRR match Excel within 0.1% | Cross-validate 5 test cases against Excel |
| Debate produces actionable tensions | ≥3 tension points identified per debate | Manual review of 5 debate outputs |
| User uses Decision Card to inform decision | ≥1 real decision by Chef | Self-reported after real property evaluation |

## Risks & Mitigations

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| SKILL.md exceeds 5k token limit causing poor skill behavior | High | Medium | Aggressive compression, delegate detail to Level 3 reference files, iterate through testing |
| Cash flow formulas produce incorrect results leading to bad investment decisions | High | Low | Test all scripts against known Excel spreadsheets, cross-validate with manual calculations, mandatory disclaimer |
| Bias detection generates false positives eroding user trust | Medium | Medium | Use question-based framing ("Are you...?") not assertions, require 2+ linguistic markers for detection |
| User treats output as financial advice | High | Medium | Mandatory disclaimer on every Decision Card, frame as "analysis suggests" not "you should" |
| OPEX assumptions don't match Vietnam market reality | Medium | Medium | Conservative defaults, CASHFLOW-VERIFICATION checklist with local cost ranges, allow user override |

## Constraints & Assumptions

**Constraints:**
- Agent Skills Level 2 (SKILL.md body) limited to ~5,000 tokens — all detailed instructions must live in Level 3 reference files
- Python scripts limited to stdlib + numpy (no pandas, no external packages)
- No external API calls in scripts — web research only through Claude's native tools
- v1 targets Claude Code CLI only (full network + script execution access)

**Assumptions:**
- Claude Code CLI supports Agent Skills with SKILL.md + scripts/ directory structure. If wrong: need to restructure as prompt-based workflow.
- numpy is pre-installed in Claude Code Python environment. If wrong: rewrite Monte Carlo using stdlib `random` module (minor effort).
- Vietnamese RE market data is searchable via web_search (batdongsan.com.vn, cafeland.vn). If wrong: user provides all market data manually (fallback already designed).
- Users provide property-specific data (price, area, rental) accurately. If wrong: add validation ranges per property type and location.

## Out of Scope

- **6-skill orchestrated architecture** — One skill is sufficient for v1; split only if SKILL.md proves too complex
- **SQLite decision database** — Markdown archive files for v1; upgrade if >50 decisions
- **Location Intelligence 8-tool toolkit** — General web search guidance instead; dedicated toolkit is v2
- **Reflection loop with prediction tracking** — Archive decisions but don't track outcomes yet; v2 feature
- **sensitivity.py, scenario_builder.py, ev_calculator.py, risk_classifier.py** — Claude handles these prompt-based in v1
- **Claude Desktop / Claude.ai / Claude API deployment** — v1 is CLI-only
- **Community contribution system** — No plugin architecture needed for single-user v1
- **MCP server for external data feeds** — Claude's web_search is sufficient for v1
- **Multi-language output** — Vietnamese only for Decision Cards

## Dependencies

- **Anthropic Agent Skills standard** — Claude Code must support `.claude/skills/` directory with SKILL.md + scripts. Status: resolved (documented standard)
- **numpy** — Required for Monte Carlo simulation. Status: resolved (pre-installed in Claude Code)
- **Claude web_search tool** — Required for market research. Status: resolved (available in Claude Code CLI)
- **Spice cognitive loop concept** — Architectural inspiration. Status: resolved (public repo, concept only — no code dependency)
- **OpenClaw debate concept** — Architectural inspiration. Status: resolved (public repo, concept only — no code dependency)

## _Metadata
<!-- Auto-generated. Updated by prd-edit. Read by prd-parse, prd-validate. -->
requirement_ids:
  must: [FR-1, FR-2, FR-3, FR-4, FR-5, FR-6, FR-7, FR-8]
  nice_to_have: [NTH-1, NTH-2, NTH-3, NTH-4]
  nfr: [NFR-1, NFR-2, NFR-3, NFR-4, NFR-5]
scale: medium
discovery_mode: express
validation_status: passed
last_validated: 2026-03-29T13:56:53Z

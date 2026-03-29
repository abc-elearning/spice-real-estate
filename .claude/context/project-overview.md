---
created: 2026-03-29T14:39:41Z
last_updated: 2026-03-29T14:39:41Z
version: 1.0
author: Claude Code PM System
---

### Features

**Cognitive Loop (6 steps):**
1. Perception — Parse intent (buy/sell/hold/compare), extract property attributes
2. State Modeling — Build user/property/market/constraint models
3. Analysis — Bias detection (12 RE biases) + framework selection + market research
4. Simulation — Monte Carlo, DCF, cash flow pro-forma, Bayesian updating
5. Decision — 5-persona adversarial debate + Decision Card generation
6. Reflection — Archive decision, compare with past decisions

**Quantitative Tools:**
- `monte_carlo.py` — GBM price projection (P10-P90, prob_loss)
- `dcf_calculator.py` — NPV, IRR, cash-on-cash, equity multiple
- `cashflow_proforma.py` — 10-year pro-forma with DSCR flagging (red/yellow/green)
- `bayesian_updater.py` — Probability updating with overconfidence detection

**Behavioral Finance:**
- 12 cognitive biases with Vietnamese linguistic detection markers
- Question-based reframing ("Bạn có đang neo vào giá X?")
- Prospect Theory analysis for sell/hold decisions

**Adversarial Debate:**
- 5 personas: Veteran Investor, Cash Flow Investor, Risk Analyst, End User, Contrarian
- Each with conflicting lenses, tension relationships, key questions
- Synthesis reveals hidden risks

**Output:**
- Structured Decision Card (Vietnamese) with confidence scoring
- Mandatory disclaimer on every card
- Archived to `.spice_re/decisions/`

### Current State
v1 COMPLETE — all features implemented and tested. Ready for real-world usage.

### Integration Points
- Claude Code CLI (Agent Skills standard)
- Claude's native web_search tool (for market research)
- File system (markdown decision archive)

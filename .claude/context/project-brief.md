---
created: 2026-03-29T14:39:41Z
last_updated: 2026-03-29T14:39:41Z
version: 1.0
author: Claude Code PM System
---

### What It Does
SpiceRE is a single Agent Skill (`deciding-real-estate`) for Claude Code CLI that transforms Claude into a structured decision advisor for real estate cash flow investments in Vietnam.

### Why It Exists
Real estate investment decisions in Vietnam are heavily influenced by cognitive biases (anchoring to listing price, FOMO in hot markets, overestimating gross yield by ignoring hidden OPEX). No existing AI tool combines cognitive bias detection with cash flow analysis and scientific decision frameworks running natively on Claude Code.

### Key Insight
Quyết định BĐS thất bại chủ yếu vì tâm lý, không phải thiếu data. "Thinking Coach" (bias detection + structured reasoning) mang giá trị lớn hơn "Analysis Platform" (thêm data/tools).

### Success Criteria
- Bias detection ≥80% precision on test scenarios
- 100% negative cash flow detection (DSCR < 1.0 flagged)
- Decision Card 100% complete every time
- SKILL.md < 5,000 tokens
- 14/14 automated tests pass
- ≥1 real investment decision informed by SpiceRE

### Scope (v1)
IN: Cognitive loop, bias detection (12 biases), cash flow analysis, Monte Carlo, DCF, Bayesian updating, 5-persona debate, Decision Card, Vietnam market sources
OUT: SQLite database, Location Intelligence toolkit, Reflection/prediction loop, Multi-platform deployment, Sensitivity script

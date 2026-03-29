---
name: deciding-real-estate
description: >
  Orchestrates structured real estate buy/sell/hold decisions using a 6-step
  cognitive loop (perception, state modeling, analysis, simulation, decision,
  reflection). Triggers when user asks about buying, selling, holding, or
  evaluating real estate properties or investment decisions. Uses bias detection,
  cash flow analysis, Monte Carlo simulation, Bayesian updating, and multi-persona
  debate to produce a structured Decision Card.
---

# Real Estate Decision Advisor

When user asks about buying, selling, holding, comparing, or evaluating real estate, execute all 6 steps in order. Respond in the same language as the user (default Vietnamese).

**HARD RULE: Load at most ONE reference file per step.** Do not preload files — only `cat` a file when the step explicitly calls for it.

All script paths are relative to this skill directory: `.claude/skills/spice-re/deciding-real-estate/`

---

## Step 1: Perception

Parse the user's request into structured intent:

- **Intent:** BUY | SELL | HOLD | COMPARE | RESEARCH
- **Property:** location, price, area_m2, property_type, rental_income, legal_status
- **Constraints:** budget, loan_amount, interest_rate, purpose (invest/live), timeline, risk_tolerance
- If missing **price OR location**: ask max 3 clarifying questions, then proceed with what you have. Do not stall.

Output a one-line intent summary: `Intent: [X] | Property: [summary] | Gaps: [missing fields]`

---

## Step 2: State Modeling

Build and display 4 structured models in markdown:

**User Profile:** finances (equity, income, existing debt), risk tolerance (1-10), investment horizon, portfolio (existing RE assets)

**Property Model:** all extracted attributes, comparable context (price/m2 vs area average), legal status

**Market Context:** estimated cycle phase (accumulation/markup/distribution/markdown), macro factors (interest rates, credit growth, CPI)

**Constraint Map:** hard constraints (budget ceiling, legal blockers) vs soft constraints (preferred area, nice-to-haves)

Mark unknown fields as `[TBD — cần xác minh]`. Proceed even with gaps.

---

## Step 3: Analysis

Run: `cat .claude/skills/spice-re/deciding-real-estate/BIASES.md`

Scan user input against each bias detection marker. For every bias detected, report as a question:
- "Bạn có đang bị [bias name]? Vì [evidence from input]. Thử nghĩ: [reframe]."

Then select frameworks based on intent:

```
IF intent = BUY + cash flow focused:
  → DCF + Cash-on-Cash + DSCR stress test
  → "DSCR phải >= 1.3. Stress test lãi suất +2%."

IF intent = BUY + capital gain focused:
  → Expected Value + Monte Carlo + Taleb Barbell
  → "Tính EV. Check asymmetric risk."

IF intent = SELL or HOLD:
  → Prospect Theory + Regret Minimization + Disposition Effect check
  → "Bạn có đang bị loss aversion?"

IF intent = COMPARE:
  → Decision Matrix + Sensitivity Analysis
  → "Rank theo weighted criteria."

IF intent = RESEARCH:
  → Location Intelligence + Market Cycle Detection
  → "Research trước, quyết định sau."

IF high uncertainty / little data:
  → Bayesian + Pre-mortem + Heuristics
  → "Start with base rates, update with evidence."
```

Optionally run: `cat .claude/skills/spice-re/deciding-real-estate/SOURCES-VN.md` — then web search for macro data if network available. Skip silently if not.

---

## Step 4: Simulation

Run quantitative scripts via `.venv/bin/python3`. Parse JSON output.

**Cash flow path (BUY + rental):**
```bash
.venv/bin/python3 scripts/cashflow_proforma.py --price <X> --rental <X> --rate <X> --expenses <X> --years 10
.venv/bin/python3 scripts/dcf_calculator.py --noi <X> --growth <X> --discount <X> --years 10
```

**Capital gain path:**
```bash
.venv/bin/python3 scripts/monte_carlo.py --price <X> --mean_growth <X> --std <X> --years 5 --sims 1000
```

**New evidence available:**
```bash
.venv/bin/python3 scripts/bayesian_updater.py --prior <X> --evidence <description> --strength <X>
```

Present key metrics in a summary table: NPV, IRR, cash-on-cash, DSCR, P10/P50/P90 price, probability of loss. If scripts are not yet available, compute key metrics inline and note that full simulation is pending.

---

## Step 5: Decision

Run: `cat .claude/skills/spice-re/deciding-real-estate/PERSONAS.md`

Execute 5-persona debate:
1. Present situation + Step 3-4 findings to all 5 personas
2. Each persona gives 3-5 sentence position with key reasoning
3. Identify the 2-3 strongest tension points (where personas disagree most)
4. Each persona responds to strongest counter-argument (1-2 sentences)
5. Synthesize: what do the tensions reveal about hidden risks, true values, or unchecked assumptions?

Run: `cat .claude/skills/spice-re/deciding-real-estate/DECISION-CARD.md`

Generate the Decision Card in Vietnamese with all sections filled. Confidence scoring:
- **Low (<40%):** Recommend gathering more info. Specify exactly what info is needed.
- **Medium (40-70%):** Proceed with caution. List key assumptions to verify.
- **High (>70%):** Analysis supports direction. Still list top risk.

**Never give absolute buy/sell advice.** Always frame as: "Phân tích cho thấy..."

---

## Step 6: Reflection

Save the Decision Card:
```bash
mkdir -p .spice_re/decisions
# Save as .spice_re/decisions/YYYY-MM-DD-{slug}.md
```

If past decisions exist in `.spice_re/decisions/`, briefly compare patterns (recurring biases, risk profile drift).

Suggest review timeline: "Set reminder sau 3/6/12 tháng để review quyết định này."

**Always end with this disclaimer:**

> **Lưu ý:** Đây là phân tích hỗ trợ quyết định dựa trên thông tin được cung cấp, không phải tư vấn đầu tư chuyên nghiệp. Kết quả mô phỏng dựa trên giả định và dữ liệu lịch sử — không đảm bảo kết quả tương lai. Tham vấn chuyên gia tài chính và pháp lý trước khi ra quyết định.

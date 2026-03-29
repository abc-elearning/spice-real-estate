# PRD: SpiceRE — Agent Skills Hỗ Trợ Ra Quyết Định Mua Bán Bất Động Sản

**Version:** 1.0  
**Author:** Chef  
**Date:** 2026-03-29  
**Status:** Draft  
**Runtime:** Claude Code CLI / Claude Desktop App / Claude API  
**Architecture:** Anthropic Agent Skills standard  
**Base:** Fork cognitive loop từ [Dyalwayshappy/Spice](https://github.com/Dyalwayshappy/Spice), debate engine từ [openclaw/multi-viewpoint-debates](https://github.com/openclaw/skills)

---

## 1. Tầm nhìn sản phẩm

### 1.1 Problem Statement

Quyết định mua bán bất động sản là một trong những quyết định tài chính lớn nhất đời người — thường chiếm 30-70% tổng tài sản cá nhân. Nghiên cứu từ behavioral finance cho thấy:

- Trong thị trường bull, overconfidence và optimism đẩy giá vượt xa giá trị cơ bản (Beracha & Skiba, 2014)
- Trong thị trường bear, loss aversion và anchoring bias kéo giá dưới giá trị hợp lý
- Tính thanh khoản thấp + chi phí giao dịch cao + không thể short sell → khuếch đại sai lệch giá
- Ngay cả chuyên gia định giá BĐS cũng bị anchoring bias từ giá rao và peer valuations (Ali et al., 2020)
- Prospect Theory (Kahneman & Tversky, 1979) giải thích tại sao người bán giữ BĐS lỗ quá lâu và bán BĐS lời quá sớm

Hiện tại **không tồn tại** AI agent nào kết hợp scientific decision frameworks với real estate domain knowledge chạy trên Claude Code.

### 1.2 Solution

**SpiceRE** là một bộ Agent Skills cho Claude Code, biến Claude thành một decision advisor chuyên biệt cho bất động sản. SpiceRE kế thừa:

- **Từ Spice:** Cognitive loop architecture (perception → state → simulation → decision → reflection)
- **Từ Multi-Viewpoint Debates:** Multi-persona adversarial debate engine
- **Mới:** Scientific decision frameworks + market intelligence + Vietnam RE context

### 1.3 Target Users

| Persona | Use case chính |
|---------|---------------|
| Nhà đầu tư cá nhân (1-5 BĐS) | Mua thêm? Bán cái nào? Timing? |
| Nhà đầu tư BĐS dòng tiền | Cash flow analysis, rental yield optimization, portfolio dòng tiền |
| Người mua nhà lần đầu | Mua hay thuê? Khu vực nào? Giá hợp lý? |
| Chủ đầu tư nhỏ (xây 5-10 tầng) | ROI projection, phân tích rủi ro, go/no-go |
| Người cần bán | Pricing strategy, timing, negotiation framing |

#### Persona chi tiết: Nhà đầu tư BĐS dòng tiền

**Profile:** Nhà đầu tư ưu tiên thu nhập thụ động ổn định từ cho thuê hơn lãi vốn (capital gain). Có thể sở hữu 3-20+ BĐS cho thuê. Tư duy như quản lý portfolio tài sản sinh dòng tiền, không phải speculator.

**Đặc điểm tư duy:**
- **Metrics ưu tiên:** Net rental yield, cash-on-cash return, DSCR (Debt Service Coverage Ratio), occupancy rate, NOI growth — KHÔNG phải giá tăng/giảm
- **Quyết định mua:** "BĐS này tạo ra bao nhiêu dòng tiền ròng/tháng sau khi trừ mọi chi phí (vay, quản lý, bảo trì, thuế, vacancy)?"
- **Quyết định bán:** Chỉ bán khi (a) có thể 1031 exchange sang asset yield cao hơn, (b) chi phí bảo trì vượt ngưỡng, hoặc (c) rebalance portfolio
- **Risk profile:** Moderate — chấp nhận leverage nhưng DSCR phải ≥1.3, vacancy buffer 2 tháng/năm
- **Time horizon:** 10-20 năm, compound qua reinvestment
- **Biases thường gặp:** Overweight yield mà bỏ qua capital depreciation, underestimate chi phí quản lý/bảo trì, anchoring vào gross yield thay vì net yield

**Workflow đặc thù:**
1. Screen BĐS theo net yield threshold (VD: ≥5% net cho căn hộ, ≥7% cho nhà trọ/phòng cho thuê)
2. Build pro-forma cash flow 10 năm (rental income - OPEX - debt service - vacancy - CapEx reserve)
3. Stress test: lãi suất tăng 2-3%, vacancy tăng gấp đôi, rental giảm 15% — vẫn cash flow positive?
4. So sánh với alternatives (gửi bank, trái phiếu, cổ phiếu cổ tức, REITs)
5. Portfolio-level analysis: diversification theo khu vực, loại BĐS, tenant profile

**Formulas bổ sung (tích hợp vào FORMULAS.md):**

```
Monthly Cash Flow = Gross Rent - Vacancy - OPEX - Debt Service - CapEx Reserve
Cash-on-Cash Return = Annual Pre-tax Cash Flow / Total Cash Invested
  → Target: ≥8% cho Việt Nam (sau khi trừ mọi chi phí thực tế)
DSCR = NOI / Annual Debt Service
  → <1.0 = negative cash flow (red flag)
  → 1.0-1.2 = fragile (không có buffer)
  → 1.3-1.5 = healthy
  → >1.5 = strong
Gross Rent Multiplier (GRM) = Property Price / Annual Gross Rent
  → <12 = attractive, 12-15 = fair, >15 = expensive for cash flow
Vacancy Rate assumption = max(market average, 2 months/year)
CapEx Reserve = 1-2% property value / year
Effective Gross Income = Gross Rent × (1 - Vacancy Rate) + Other Income
NOI = Effective Gross Income - Operating Expenses
Operating Expense Ratio = Operating Expenses / Effective Gross Income
  → >40% = investigate cost structure
Break-even Occupancy = Operating Expenses + Debt Service / Gross Potential Rent
  → <75% = safe, 75-85% = watch, >85% = risky
```

### 1.4 Disclaimer

SpiceRE là công cụ hỗ trợ phân tích, **không phải** tư vấn tài chính hoặc đầu tư. Mọi quyết định cuối cùng thuộc về người dùng. Output luôn kèm confidence level và khuyến nghị tham vấn chuyên gia khi cần.

---

## 2. Kế thừa, loại bỏ trùng lặp & bổ sung mới

### 2.1 Ma trận nguồn gốc

| Component | Spice | Multi-viewpoint Debates | Mới | Ghi chú |
|-----------|:-----:|:-----------------------:|:---:|---------|
| Cognitive loop (perception→state→simulation→decision→reflection) | ✅ | | | Giữ nguyên concept, rewrite thành Agent Skills |
| State modeling | ✅ | | | Extend cho RE-specific attributes |
| Simulation engine | ✅ | | | Thêm Monte Carlo, DCF |
| Decision Card output | ✅ | | | Extend thêm RE fields |
| Reflection/learning loop | ✅ | | | Track prediction accuracy |
| Multi-persona debate | | ✅ | | Port sang prompt-based, bỏ OpenClaw dependency |
| Debate archive + tension analysis | | ✅ | | Integrate vào decision history |
| Bayesian updater | | | ✅ | Mới — scientific framework |
| Expected Value calculator | | | ✅ | Mới — decision trees |
| Prospect Theory analyzer | | | ✅ | Mới — loss aversion detection |
| Cognitive bias scanner (12 RE biases) | | | ✅ | Mới — behavioral finance |
| Bezos reversibility classifier | | | ✅ | Mới — one-way/two-way door |
| Taleb barbell analyzer | | | ✅ | Mới — asymmetric risk |
| Market intelligence (web research) | | | ✅ | Mới — comparable analysis, macro data |
| Location intelligence toolkit (8 tools) | | | ✅ | Mới — location-specific research workflow |
| Cash flow investor persona + formulas | | | ✅ | Mới — DSCR, cash-on-cash, pro-forma, GRM |
| Pre-mortem + regret minimization | | | ✅ | Mới — scenario analysis |

### 2.2 Loại bỏ (trùng lặp / không phù hợp)

| Component | Nguồn | Lý do loại |
|-----------|-------|-----------|
| SDEP protocol | Spice | Quá phức tạp cho Agent Skills — Claude Code đã có tool execution |
| Wrapper ecosystem | Spice | Không cần — Agent Skills native trong Claude Code |
| Shadow-run evaluation | Spice | Scope v2+, không cần cho v1 |
| Domain starter templates | Spice | Thay bằng RE-specific skill pack |
| LLM adapter layer | Spice | Claude Code đã handle multi-model |
| OpenClaw Clawdbot dependency | Debates | Platform lock-in, thay bằng prompt-based |
| Isolated session spawn | Debates | Thay bằng structured multi-turn prompting |
| Elon/Capitalist/Monkey personas | Debates | Thay bằng RE-specific personas |
| pyproject.toml / pip package | Spice | Agent Skills dùng filesystem, không cần Python package |

---

## 3. Kiến trúc Agent Skills

### 3.1 Tuân thủ Anthropic Agent Skills Standard

Theo [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), SpiceRE được thiết kế theo mô hình 3-level progressive disclosure:

- **Level 1 (Metadata, ~100 tokens/skill):** YAML frontmatter — luôn loaded ở startup
- **Level 2 (Instructions, <5k tokens):** SKILL.md body — loaded khi skill triggered
- **Level 3+ (Resources, unlimited):** Scripts, templates, reference data — loaded as needed qua bash

### 3.2 Skills Directory Structure

```
.claude/skills/spice-re/
│
├── deciding-real-estate/              # 🧠 SKILL CHÍNH — Orchestrator
│   ├── SKILL.md                       # Entry point, cognitive loop instructions
│   ├── DECISION-CARD.md               # Decision Card template + output format
│   ├── EXAMPLES.md                    # Ví dụ input/output cho các use cases
│   └── scripts/
│       ├── decision_card.py           # Generate structured Decision Card JSON
│       └── history.py                 # Read/write decision archive
│
├── analyzing-re-biases/              # 🧪 Cognitive Bias Scanner
│   ├── SKILL.md                       # 12 RE-specific biases + detection prompts
│   ├── BIAS-CATALOG.md                # Chi tiết từng bias + ví dụ BĐS Việt Nam
│   └── scripts/
│       └── bias_report.py             # Generate bias analysis report
│
├── simulating-re-scenarios/          # 📊 Simulation & Quantitative Analysis
│   ├── SKILL.md                       # Monte Carlo, DCF, scenario builder
│   ├── FORMULAS.md                    # Cap rate, rental yield, NPV, IRR formulas
│   └── scripts/
│       ├── monte_carlo.py             # Monte Carlo price simulation
│       ├── dcf_calculator.py          # Discounted Cash Flow
│       ├── sensitivity.py             # Sensitivity analysis
│       └── scenario_builder.py        # Best/base/worst case generator
│
├── debating-re-decisions/            # 🗣️ Multi-Viewpoint Debate Engine
│   ├── SKILL.md                       # Debate orchestration instructions
│   ├── PERSONAS.md                    # 5 RE-specific persona definitions
│   ├── SYNTHESIS.md                   # How to synthesize from tension
│   └── scripts/
│       ├── debate_runner.py           # Run structured debate
│       └── debate_archive.py          # Archive + pattern analysis
│
├── researching-re-market/            # 🔍 Market Intelligence
│   ├── SKILL.md                       # Web research + data gathering workflow
│   ├── SOURCES-VN.md                  # Vietnam RE data sources catalog (detailed table)
│   ├── MACRO-INDICATORS.md            # Key macro indicators + interpretation
│   ├── LOCATION-CHECKLIST.md          # 8-tool location intelligence checklist
│   ├── CASHFLOW-VERIFICATION.md       # OPEX reality check for cash flow investors
│   └── scripts/
│       ├── comparable_analyzer.py     # Comp analysis calculator
│       ├── location_scorer.py         # Location scoring model (infra + demand)
│       ├── cycle_detector.py          # Market cycle phase detection
│       ├── rental_yield_calc.py       # Net rental yield with real OPEX
│       ├── supply_demand_ratio.py     # Absorption rate + inventory months
│       └── cashflow_proforma.py       # 10-year pro-forma cash flow builder
│
└── applying-re-frameworks/           # 📐 Scientific Decision Frameworks
    ├── SKILL.md                       # Framework selection guide
    ├── BAYESIAN.md                    # Bayesian reasoning for RE
    ├── EXPECTED-VALUE.md              # EV calculation with decision trees
    ├── PROSPECT-THEORY.md             # Loss aversion analysis
    ├── BEZOS-REVERSIBILITY.md         # One-way vs two-way door
    ├── TALEB-BARBELL.md               # Asymmetric risk analysis
    ├── PREMORTEM.md                   # Pre-mortem scenario analysis
    ├── REGRET-MINIMIZATION.md         # Regret minimization framework
    └── scripts/
        ├── ev_calculator.py           # Expected Value computation
        ├── bayesian_updater.py        # Prior/posterior probability updater
        └── risk_classifier.py         # Reversibility + convexity classifier
```

### 3.3 Skill Metadata (Level 1)

Mỗi skill có YAML frontmatter tuân thủ spec (name ≤64 chars, lowercase+hyphens, description ≤1024 chars, third person):

```yaml
# deciding-real-estate/SKILL.md
---
name: deciding-real-estate
description: >
  Orchestrates structured real estate buy/sell/hold decisions using a cognitive
  loop (perception, state modeling, simulation, decision, reflection). Triggers
  when user asks about buying, selling, holding, or evaluating real estate
  properties, investment decisions, or housing market analysis. Coordinates
  with analyzing-re-biases, simulating-re-scenarios, debating-re-decisions,
  researching-re-market, and applying-re-frameworks skills.
---
```

```yaml
# analyzing-re-biases/SKILL.md
---
name: analyzing-re-biases
description: >
  Detects and reports 12 cognitive biases specific to real estate decisions
  including anchoring to listing price, herding in hot markets, sunk cost
  on renovations, familiarity bias for neighborhoods, and loss aversion
  when selling below purchase price. Triggers when user describes a property
  decision and may be influenced by emotional or irrational factors.
---
```

```yaml
# simulating-re-scenarios/SKILL.md
---
name: simulating-re-scenarios
description: >
  Runs quantitative simulations for real estate investment analysis including
  Monte Carlo price projections, discounted cash flow, cap rate, rental yield,
  sensitivity analysis, and best/base/worst case scenario modeling. Triggers
  when user needs financial projections, ROI estimates, or risk quantification
  for property investments.
---
```

```yaml
# debating-re-decisions/SKILL.md
---
name: debating-re-decisions
description: >
  Runs multi-viewpoint adversarial debates on real estate decisions using five
  personas with conflicting frameworks — seasoned investor, cash flow investor,
  risk analyst, end-user advocate, and contrarian devil's advocate. Exposes
  blind spots through structured disagreement. Triggers when user faces a
  complex property decision with multiple valid perspectives or needs
  assumption stress-testing.
---
```

```yaml
# researching-re-market/SKILL.md
---
name: researching-re-market
description: >
  Gathers and analyzes real estate market intelligence for specific locations
  via 8-step research toolkit: comparable transactions, rental market scanning,
  infrastructure and zoning verification, population and demand analysis,
  market cycle detection, competitive supply scanning, macro-economic
  indicators, and cash flow cost verification. Specialized for Vietnam market
  with batdongsan, cafeland, CBRE, Savills sources. Triggers when user needs
  current market data, location analysis, or property valuation context.
---
```

```yaml
# applying-re-frameworks/SKILL.md
---
name: applying-re-frameworks
description: >
  Applies scientific decision-making frameworks to real estate choices including
  Bayesian probability updating, Expected Value with decision trees, Prospect
  Theory loss aversion analysis, Bezos reversibility classification, Taleb
  barbell strategy for asymmetric risk, pre-mortem failure analysis, and regret
  minimization. Triggers when user needs structured analytical reasoning beyond
  gut feeling for property decisions.
---
```

---

## 4. Chi tiết từng Skill

### 4.1 deciding-real-estate (Orchestrator)

**Nguồn gốc:** Cognitive loop từ Spice (perception → state → simulation → decision → reflection)

**SKILL.md body (~3000 tokens):**

#### Cognitive Loop

Khi user đưa ra một quyết định BĐS, chạy qua 6 bước:

**Bước 1 — Perception (Thu nhận)**
- Parse intent: mua / bán / giữ / cho thuê / so sánh
- Extract property attributes (vị trí, diện tích, giá, loại hình)
- Identify user constraints (ngân sách, timeline, mục đích sử dụng)
- Nếu thiếu info, hỏi user — tối đa 3 câu hỏi mỗi lượt

**Bước 2 — State Modeling (Mô hình hóa)**
- Build User Profile: tài chính hiện tại, portfolio BĐS, risk tolerance (1-10), investment horizon
- Build Property Model: attributes, comparable context, legal status
- Build Market Context: chu kỳ thị trường, macro indicators, khu vực cụ thể
- Build Constraint Map: hard constraints (ngân sách) vs soft constraints (preferences)
- Output: State Summary dạng structured markdown

**Bước 3 — Analysis (Phân tích)**
- Gọi `analyzing-re-biases` — scan cognitive biases trong cách user frame vấn đề
- Gọi `applying-re-frameworks` — chọn framework phù hợp nhất:
  - Quyết định lớn + irreversible → Bayesian + Pre-mortem + Bezos
  - Quyết định đầu tư → Expected Value + Taleb Barbell
  - Đang sở hữu, cân nhắc bán → Prospect Theory + Regret Minimization
- Gọi `researching-re-market` — thu thập market data nếu cần

**Bước 4 — Simulation (Mô phỏng)**
- Gọi `simulating-re-scenarios` với state data
- Chạy Monte Carlo cho price projection (1000 iterations, 1/3/5/10 năm)
- Build 3 scenarios: optimistic / base / pessimistic
- Tính sensitivity trên 3 key variables (giá, lãi suất, rental yield)

**Bước 5 — Decision (Ra quyết định)**
- Gọi `debating-re-decisions` — 5 personas debate
- Synthesize: tổng hợp tất cả signals → Decision Card
- Confidence scoring: Low (<40%) / Medium (40-70%) / High (>70%)
- Nếu confidence < 40%: recommend thu thập thêm thông tin, chỉ rõ thông tin nào cần
- **Không bao giờ đưa ra lời khuyên mua/bán tuyệt đối** — luôn frame là "phân tích cho thấy..."

**Bước 6 — Reflection (Phản ánh)**
- Lưu decision vào archive (scripts/history.py)
- So sánh với decisions trước (nếu có)
- Gợi ý: "Set reminder sau 3/6/12 tháng để review quyết định này"
- Track prediction accuracy nếu user cập nhật outcome

#### Decision Card Format (DECISION-CARD.md)

```markdown
## 📋 Decision Card: [Tên quyết định]
**Ngày:** [date]  |  **Confidence:** [Low/Medium/High] ([X]%)

### Tình huống
[1-2 câu tóm tắt]

### Phân tích theo framework
- **Framework được dùng:** [tên]
- **Kết quả chính:** [findings]

### Bias Alert
- [Bias detected] → [Impact] → [Mitigation]

### Scenarios (Monte Carlo, n=1000)
| Kịch bản | Probability | ROI | NPV |
|-----------|------------|-----|-----|
| Pessimistic (P10) | X% | X% | X |
| Base (P50) | X% | X% | X |
| Optimistic (P90) | X% | X% | X |

### Debate Summary
| Persona | Stance | Key argument |
|---------|--------|-------------|
| Nhà đầu tư kỳ cựu | [Buy/Sell/Hold] | [1 câu] |
| Nhà đầu tư dòng tiền | [Buy/Sell/Hold] | [1 câu — focus cash flow metrics] |
| Chuyên gia rủi ro | [Buy/Sell/Hold] | [1 câu] |
| Người dùng cuối | [Buy/Sell/Hold] | [1 câu] |
| Devil's advocate | [Contrarian view] | [1 câu] |

### Đề xuất
[Phân tích cho thấy... với confidence X%]

### Bước tiếp theo
1. [Action cụ thể + timeline]
2. [Action cụ thể + timeline]
3. [Action cụ thể + timeline]

### ⚠️ Lưu ý
Đây là phân tích hỗ trợ quyết định, không phải tư vấn đầu tư.
Tham vấn chuyên gia tài chính/pháp lý trước khi quyết định.
```

---

### 4.2 analyzing-re-biases (Cognitive Bias Scanner)

**Nguồn gốc:** Mới — dựa trên nghiên cứu behavioral finance trong BĐS

**12 biases cụ thể cho BĐS:**

| # | Bias | Mô tả RE-specific | Ví dụ |
|---|------|--------------------|-------|
| 1 | **Anchoring** | Neo vào giá rao / giá mua ban đầu | "Đất tôi mua 2 tỷ, giờ rao 3 tỷ nhưng thị trường chỉ 2.5" — neo vào 3 tỷ |
| 2 | **Loss Aversion** | Không chịu bán lỗ dù fundamentals đã thay đổi | Giữ BĐS vùng ven đã mất quy hoạch, không cut loss |
| 3 | **Sunk Cost** | Đã đổ tiền sửa chữa nên không bán | "Đã bỏ 500tr renovate, phải bán ít nhất X" |
| 4 | **Herding** | Mua theo đám đông khi thị trường nóng | FOMO mua đất nền khi sốt đất vùng ven |
| 5 | **Overconfidence** | Quá tự tin vào khả năng chọn BĐS | "Tôi đầu tư BĐS 10 năm, không thể sai" |
| 6 | **Familiarity** | Chỉ mua BĐS gần nhà / quen thuộc | Bỏ qua khu vực ROI tốt hơn vì không biết |
| 7 | **Confirmation** | Chỉ tìm info ủng hộ quyết định đã có | Google "tại sao nên mua đất X" thay vì "rủi ro đất X" |
| 8 | **Recency** | Quá trọng xu hướng giá gần nhất | "3 tháng qua tăng 20%, sẽ tiếp tục tăng" |
| 9 | **Status Quo** | Không hành động dù nên mua/bán | "Để đó, chờ thêm" khi data đã rõ |
| 10 | **Endowment Effect** | Định giá BĐS mình cao hơn thị trường | "Nhà tôi view đẹp, phải hơn giá thị trường 30%" |
| 11 | **Framing** | Cách đặt vấn đề thay đổi quyết định | "Mất 500tr" vs "tiết kiệm 1 tỷ so với peak" |
| 12 | **Disposition Effect** | Bán winner quá sớm, giữ loser quá lâu | Bán căn hộ lời 30% ngay, giữ đất nền lỗ 40% |

**Detection method:** Scan user input cho linguistic markers → flag potential biases → present reframed perspective

---

### 4.3 simulating-re-scenarios (Quantitative Engine)

**Nguồn gốc:** Spice simulation concept + mới (RE-specific formulas)

**Scripts (Level 3 resources) — tất cả stdlib + numpy only:**

**monte_carlo.py** — Input: giá hiện tại, mean annual growth, std dev, n_years, n_simulations. Output: P10/P25/P50/P75/P90 price distribution + probability of loss.

**dcf_calculator.py** — Input: rental income, growth rate, operating expenses, discount rate, holding period. Output: NPV, IRR, cash-on-cash return, equity multiple.

**sensitivity.py** — Input: base case + 3 variables to stress test. Output: tornado chart data showing which variable has most impact.

**scenario_builder.py** — Input: state model. Output: 3 scenarios (pessimistic/base/optimistic) with probability weights.

**Key formulas (FORMULAS.md):**

```
Cap Rate = NOI / Property Value
Gross Rental Yield = Annual Rent / Purchase Price
Net Rental Yield = (Annual Rent - Expenses) / Purchase Price
Cash-on-Cash = Annual Pre-tax Cash Flow / Total Cash Invested
NPV = Σ [CFt / (1+r)^t] - Initial Investment
IRR = rate where NPV = 0
Price-to-Rent Ratio = Median Home Price / Median Annual Rent
  → >20 = overvalued for buying
Break-even Horizon = Transaction Costs / (Monthly Ownership Cost - Monthly Rent)
Loan-to-Value (LTV) = Loan Amount / Property Value
  → >70% = high leverage risk
Debt Service Coverage Ratio = NOI / Annual Debt Service
  → <1.2 = risky
```

---

### 4.4 debating-re-decisions (Adversarial Debate)

**Nguồn gốc:** Multi-viewpoint debates (OpenClaw) — redesigned personas cho BĐS

**5 Personas (PERSONAS.md):**

**1. Nhà Đầu Tư Kỳ Cựu (The Veteran)**
- Lens: ROI, cash flow, portfolio diversification, market timing
- Style: Pragmatic, numbers-driven, "show me the cap rate"
- Tendency: Bullish on RE as asset class, but ruthless about specific deals
- Framework: Expected Value + historical comparables

**2. Nhà Đầu Tư Dòng Tiền (The Cash Flow Investor)**
- Lens: Monthly cash flow, net yield, DSCR, occupancy, operating expenses
- Style: Disciplined, spreadsheet-driven, "giá tăng là bonus, dòng tiền mới là lương"
- Tendency: Chỉ quan tâm BĐS tạo positive cash flow từ ngày 1. Không speculate. Sẵn sàng mua BĐS "xấu" nếu yield tốt. Ghét leverage quá cao.
- Key questions:
  - "Cash flow ròng/tháng sau mọi chi phí là bao nhiêu?"
  - "DSCR có trên 1.3 không? Nếu vacancy tăng gấp đôi, vẫn positive?"
  - "So với gửi bank 6%, BĐS này yield bao nhiêu? Có xứng đáng với effort quản lý?"
  - "Chi phí quản lý + bảo trì thực tế là bao nhiêu, không phải con số lý thuyết?"
- Tension chính: Xung đột với Veteran (capital gain vs cash flow), xung đột với End User (yield vs livability)
- Framework: DCF + Cash-on-Cash + DSCR stress test + Portfolio yield optimization

**3. Chuyên Gia Rủi Ro (The Risk Analyst)**
- Lens: Downside protection, liquidity risk, leverage risk, tail events
- Style: Conservative, "what if worst case happens?"
- Tendency: Focus on what could go wrong, stress test assumptions
- Framework: Taleb Barbell + Pre-mortem + Monte Carlo P10

**4. Người Dùng Cuối (The End User)**
- Lens: Livability, convenience, personal fit, quality of life
- Style: Emotional but valid — "numbers aren't everything"
- Tendency: Weight non-financial factors (commute, schools, community)
- Framework: Regret Minimization + Values Alignment

**5. Devil's Advocate (The Contrarian)**
- Lens: Challenge every assumption, find the hidden flaw
- Style: Provocative, "everyone's wrong, here's why"
- Tendency: Steelman the opposite position, find analogies where consensus was wrong
- Framework: Counterfactual reasoning + Base rate analysis

**Debate Protocol (SKILL.md):**

1. Present situation to all 5 personas
2. Each gives 3-5 sentence position with key reasoning
3. Identify tension points (where personas disagree most)
4. Each responds to strongest counter-argument
5. Synthesize: what did the tensions reveal?

**Synthesis method (SYNTHESIS.md):** Tensions thường reveal: giá trị thực sự của user (khi Veteran và End User xung đột), rủi ro bị bỏ qua (khi Risk Analyst đơn độc chống lại), và assumption chưa kiểm chứng (khi Contrarian tìm được analogies).

---

### 4.5 researching-re-market (Market Intelligence)

**Nguồn gốc:** Mới

**Workflow (SKILL.md):**

1. Identify research scope từ state model (khu vực, loại BĐS, price range)
2. Web search cho comparable transactions (3-6 tháng gần nhất)
3. Thu thập macro indicators: lãi suất cho vay, tăng trưởng tín dụng BĐS, CPI
4. Location scoring: hạ tầng giao thông, quy hoạch, tiện ích, an ninh
5. Legal check: quy hoạch sử dụng đất, sổ đỏ/sổ hồng, tranh chấp
6. Market cycle detection: accumulation → markup → distribution → markdown

#### Location Intelligence Toolkit

Khi user đưa ra một địa điểm cụ thể (VD: "căn hộ gần biển Mỹ Khê, Đà Nẵng" hoặc "đất Hòa Xuân"), skill chạy qua 8 bước research có cấu trúc:

**Tool 1 — Comparable Transaction Search (web_search)**
- Query pattern: `"giá [loại BĐS] [khu vực] [năm hiện tại]"`, `"[khu vực] giao dịch thực tế"`, `"[dự án] review 2025 2026"`
- Sources: batdongsan.com.vn, cafeland.vn, nhadat24h.net, alonhadat.com.vn
- Extract: giá/m², số lượng tin rao, tỷ lệ bán/rao (absorption rate)
- Output: bảng 5-10 comparable gần nhất với giá, diện tích, thời gian, nguồn

**Tool 2 — Rental Market Scanner (web_search)**
- Query pattern: `"cho thuê [loại BĐS] [khu vực] giá"`, `"rental yield [khu vực]"`, `"[dự án] cho thuê bao nhiêu"`
- Mục tiêu: xác định rental income thực tế (không phải giá rao)
- Phân tích: occupancy rate khu vực, seasonal pattern (biển vs nội thành), tenant profile (expat/local/tourist)
- Output: rental range (min-median-max), estimated vacancy rate, net yield calculation

**Tool 3 — Infrastructure & Quy Hoạch Scanner (web_search + web_fetch)**
- Query pattern: `"quy hoạch [khu vực/quận] [năm]"`, `"hạ tầng giao thông [khu vực] mới"`, `"dự án [đường/cầu/metro] [thành phố]"`
- Checklist hạ tầng:
  - Giao thông: đường lớn, cao tốc, cầu, metro/BRT, sân bay — hiện hữu vs quy hoạch
  - Tiện ích: trường học (international/public), bệnh viện, siêu thị, công viên
  - Công nghiệp/việc làm: KCN gần, văn phòng cho thuê, co-working space
  - Hành chính: trung tâm hành chính mới, khu đô thị mới
- Output: Infrastructure Score (1-10) + timeline các dự án hạ tầng sắp triển khai

**Tool 4 — Legal & Zoning Verifier (web_search)**
- Query pattern: `"quy hoạch sử dụng đất [khu vực]"`, `"[khu vực] đất thổ cư hay nông nghiệp"`, `"tranh chấp [dự án/khu vực]"`
- Checklist pháp lý:
  - Loại đất (thổ cư/nông nghiệp/hỗn hợp) theo quy hoạch 1/500
  - Sổ đỏ/sổ hồng: đã có hay chờ cấp? Dự án đã nghiệm thu?
  - Quy hoạch tương lai: có bị giải tỏa? Nằm trong khu vực hạn chế xây dựng?
  - Lịch sử tranh chấp: dự án chủ đầu tư, khiếu nại cư dân
- Red flags: đất nông nghiệp phân lô bán nền, dự án chưa giấy phép, chủ đầu tư nợ xấu

**Tool 5 — Population & Demand Analyzer (web_search)**
- Query pattern: `"dân số [thành phố/quận] tăng trưởng"`, `"nhập cư [khu vực]"`, `"FDI [tỉnh] [năm]"`
- Yếu tố demand:
  - Tăng trưởng dân số khu vực (>2%/năm = positive)
  - Dòng nhập cư ròng (net migration) — đặc biệt quan trọng cho Đà Nẵng, Bình Dương, Long An
  - FDI vào khu vực (KCN mới = demand lao động = demand nhà ở)
  - Du lịch (nếu BĐS nghỉ dưỡng): lượt khách, công suất phòng
- Output: Demand Score (1-10) + demand drivers + risk factors

**Tool 6 — Market Cycle Detector (web_search + analysis)**
- Query pattern: `"thị trường BĐS [khu vực] [năm] nhận định"`, `"tồn kho BĐS [thành phố]"`, `"thanh khoản [khu vực]"`
- Indicators chu kỳ:
  - **Accumulation** (đáy): giá thấp, volume giao dịch thấp, ít tin rao mới, nhà đầu tư lớn bắt đầu mua
  - **Markup** (tăng): volume tăng, giá bắt đầu tăng, tin tức tích cực, dự án mới khởi công
  - **Distribution** (đỉnh): giá cao, volume giảm, nhiều dự án mới, tin tức quá lạc quan, "ai cũng nói BĐS tăng"
  - **Markdown** (giảm): giá giảm, thanh khoản thấp, dự án đình trệ, tín dụng siết
- Output: Current cycle phase + estimated position (early/mid/late) + historical comparison

**Tool 7 — Competitive Supply Scanner (web_search)**
- Query pattern: `"dự án mới [khu vực] [năm]"`, `"nguồn cung căn hộ [thành phố]"`, `"mở bán [khu vực]"`
- Phân tích:
  - Số lượng dự án đang/sắp mở bán trong bán kính 3-5km
  - Nguồn cung tương lai (dự án đã cấp phép nhưng chưa triển khai)
  - Absorption rate: số lượng bán/tháng so với tổng nguồn cung
  - Đối thủ trực tiếp: dự án cùng phân khúc, cùng target tenant/buyer
- Red flags: oversupply (>24 tháng inventory), quá nhiều dự án cùng phân khúc

**Tool 8 — Cash Flow Verification (web_search — cho nhà đầu tư dòng tiền)**
- Query pattern: `"chi phí quản lý [dự án]"`, `"phí dịch vụ [dự án/khu vực] /tháng"`, `"thuế cho thuê BĐS Việt Nam"`
- Checklist chi phí thực tế:
  - Phí quản lý tòa nhà (thường 5,000-15,000 VNĐ/m²/tháng)
  - Phí dịch vụ (nếu condotel/serviced apartment)
  - Thuế cho thuê: 5% VAT + 5% TNCN = 10% gross rent (hoặc 7% cho cá nhân khoán)
  - Chi phí bảo trì trung bình: 1-2% giá trị BĐS/năm
  - Chi phí nội thất (nếu cho thuê furnished): khấu hao 5-7 năm
  - Commission môi giới cho thuê: 1 tháng tiền thuê/năm
- Output: Pro-forma cash flow 10 năm with realistic OPEX assumptions

**Vietnam Data Sources (SOURCES-VN.md):**

| Category | Source | Data type | Access |
|----------|--------|-----------|--------|
| Listing & comps | batdongsan.com.vn | Giá rao, volume, phân khúc | Web search |
| Listing & comps | cafeland.vn | Market analysis, giá khu vực | Web search |
| Listing & comps | alonhadat.com.vn | Giá thực tế (C2C listings) | Web search |
| Listing & comps | nhadat24h.net | Listings vùng ven, đất nền | Web search |
| Rental market | batdongsan.com.vn/cho-thue | Rental listings | Web search |
| Rental market | Airbnb, Booking.com | Short-term rental yield | Web search |
| Macro — lãi suất | Ngân hàng Nhà nước (sbv.gov.vn) | Lãi suất, tín dụng BĐS | Web fetch |
| Macro — kinh tế | Tổng cục Thống kê (gso.gov.vn) | CPI, GDP, dân số | Web fetch |
| Quy hoạch | Sở Xây dựng / Sở TN&MT tỉnh | Quy hoạch 1/500, pháp lý | Web search |
| Market reports | CBRE Vietnam | Quarterly market overview | Web search |
| Market reports | Savills Vietnam | Market pulse, pricing index | Web search |
| Market reports | JLL Vietnam | Research & trends | Web search |
| Market reports | Vietnam Report (vietnamreport.net) | Top 10 BĐS uy tín | Web search |
| News & analysis | cafef.vn, vnexpress.net/bat-dong-san | Tin tức thị trường | Web search |
| FDI & industry | Bộ KH&ĐT, VCCI | FDI theo tỉnh, KCN | Web search |

**Macro Indicators (MACRO-INDICATORS.md):**

| Indicator | Signal Bullish | Signal Bearish |
|-----------|---------------|---------------|
| Lãi suất cho vay BĐS | Giảm / thấp (<8%) | Tăng / cao (>12%) |
| Tăng trưởng tín dụng BĐS | 15-20% YoY | <5% hoặc >25% (quá nóng) |
| Tồn kho BĐS | Giảm | Tăng >20% |
| Giá/thu nhập (Price-to-Income) | <25x | >35x |
| Rental yield | >5% net | <3% net |
| Thanh khoản (days on market) | <60 ngày | >180 ngày |
| GDP growth | >6% | <5% |

---

### 4.6 applying-re-frameworks (Scientific Frameworks)

**Nguồn gốc:** Mới — bổ sung lớp scientific rigor mà cả 2 repo gốc đều thiếu

**Framework Selection Logic (SKILL.md):**

```
IF quyết định irreversible (mua BĐS lớn, vay dài hạn):
  → Bayesian + Pre-mortem + Bezos Reversibility
  → "Đây là one-way door. Cần phân tích kỹ."

IF quyết định đầu tư dòng tiền (rental income-focused):
  → DCF + Cash-on-Cash + DSCR stress test + Cash Flow Verification (Tool 8)
  → "Tính cash flow ròng thực tế. DSCR phải ≥1.3. Stress test lãi suất +2%."
  → Bắt buộc chạy CASHFLOW-VERIFICATION.md checklist
  → So sánh net yield vs alternatives (bank deposit, bonds, REITs, cổ tức)

IF quyết định đầu tư lãi vốn (capital gain-focused):
  → Expected Value + Taleb Barbell + Monte Carlo
  → "Tính EV, check asymmetric risk profile."

IF đang giữ, cân nhắc bán:
  → Prospect Theory + Regret Minimization + Disposition Effect check
  → "Bạn có đang bị loss aversion?"

IF so sánh nhiều options:
  → Decision Matrix + Sensitivity Analysis
  → "Rank theo weighted criteria."

IF khảo sát khu vực mới:
  → Location Intelligence Toolkit (8 tools) + Market Cycle Detection
  → "Research khu vực trước, quyết định sau."

IF uncertainty cao, ít data:
  → Bayesian + Heuristics + Pre-mortem
  → "Start with base rates, update with evidence."
```

**Chi tiết từng framework (Level 3 markdown files):**

**BAYESIAN.md** — Cách dùng Bayesian cho BĐS:
- Prior: Base rate tăng giá BĐS khu vực X trong 5 năm qua
- Evidence: Thông tin mới (quy hoạch, hạ tầng, chính sách)
- Posterior: Xác suất cập nhật
- Calibration: So sánh confidence của user vs base rates để detect overconfidence
- Script: `bayesian_updater.py` — input prior probability + evidence strength → output posterior

**EXPECTED-VALUE.md** — Decision tree cho BĐS:
- Identify scenarios (tăng giá / đi ngang / giảm giá)
- Assign probabilities (from Bayesian or Monte Carlo)
- Calculate payoff mỗi scenario (including opportunity cost)
- EV = Σ probability × payoff
- Include non-monetary value nếu mua để ở
- Script: `ev_calculator.py`

**PROSPECT-THEORY.md** — Detect loss aversion:
- Reference point: giá mua, giá peak, hoặc giá hàng xóm?
- Loss aversion coefficient: losses felt ~2.5x gains (Kahneman)
- Key question: "Nếu bạn KHÔNG sở hữu BĐS này, bạn có mua ở giá hiện tại không?"
- Reframe: absolute gain/loss → opportunity cost so với alternatives

**BEZOS-REVERSIBILITY.md** — Classification:
- One-way door (khó đảo ngược): mua BĐS, xây dựng, vay dài hạn → cần phân tích kỹ
- Two-way door (dễ đảo ngược): đặt cọc có hoàn, thuê trước khi mua, khảo sát → nên move fast
- Script: `risk_classifier.py` — classify decision + recommend analysis depth

**TALEB-BARBELL.md** — Asymmetric risk cho BĐS:
- Downside bounded? (mất tối đa bao nhiêu? có leverage risk?)
- Upside convex? (nếu đúng, gain có asymmetric lớn hơn loss?)
- Fragile vs antifragile: BĐS cho thuê (antifragile — benefit from inflation qua rental) vs đất nền speculative (fragile — pure price bet)
- Rule: "Khi downside unbounded (leverage cao), không đầu tư. Khi upside convex + downside bounded, xem xét."

**PREMORTEM.md** — Structured failure analysis:
1. Giả sử 2 năm sau, quyết định này thất bại. Mô tả chi tiết.
2. Brainstorm 5-7 nguyên nhân thất bại
3. Rate mỗi nguyên nhân theo probability × impact
4. Identify top 3 risks
5. Cho mỗi risk: có mitigation plan cụ thể không? Nếu không → red flag

**REGRET-MINIMIZATION.md** — Bezos framework adapted:
- "60 tuổi nhìn lại, sẽ regret điều gì hơn: mua mà lỗ, hay không mua mà giá tăng?"
- Quantify regret: regret of commission (hành động sai) vs regret of omission (bỏ lỡ)
- BĐS insight: regret of omission thường mạnh hơn cho primary residence, regret of commission mạnh hơn cho speculative investment

---

## 5. Tech Stack & Constraints

### 5.1 Runtime Environment

| Platform | Support | Network | Package Install |
|----------|---------|---------|----------------|
| Claude Code CLI | ✅ Primary | Full access | Local only |
| Claude Desktop App | ✅ | Full access | Local only |
| Claude.ai (Pro/Max) | ✅ | Varies by settings | Pre-installed only |
| Claude API | ⚠️ v2 | No network | Pre-installed only |

### 5.2 Dependencies

Tất cả scripts dùng Python stdlib hoặc pre-installed packages:

- `json`, `csv`, `math`, `random`, `statistics` — stdlib
- `datetime`, `pathlib`, `sqlite3` — stdlib
- `numpy` — Monte Carlo simulation (pre-installed trong Claude Code)
- Không dùng external API calls trong scripts — web research qua Claude's native web_search tool

### 5.3 Data Storage

```
.spice_re/
├── config.json              # User profile, preferences
├── decisions.db             # SQLite — decision archive
├── debates/                 # Debate transcripts
│   └── [date]-[topic].md
└── market_cache/            # Cached research data
    └── [location]-[date].json
```

---

## 6. User Flows

### 6.1 Flow: "Có nên mua căn hộ này không?"

```
User: "Tôi đang cân nhắc mua căn hộ 2PN ở Đà Nẵng, giá 2.8 tỷ,
       gần biển Mỹ Khê. Tôi có 1.5 tỷ cash, vay 1.3 tỷ.
       Mục đích cho thuê + nghỉ dưỡng."

→ [deciding-real-estate triggers]

Step 1 — Perception:
  - Intent: MUA
  - Property: căn hộ 2PN, Đà Nẵng, gần Mỹ Khê, 2.8 tỷ
  - Finance: 1.5 tỷ cash, 1.3 tỷ vay (~46% LTV)
  - Purpose: cho thuê + nghỉ dưỡng (mixed)
  - Missing: diện tích? Tên dự án? Lãi suất vay? Thu nhập hiện tại?
  → Hỏi user 3 câu bổ sung

Step 2 — State Model:
  [Build structured state từ user answers]

Step 3 — Analysis:
  → [analyzing-re-biases]: Detect familiarity bias (Đà Nẵng = hometown?)
  → [applying-re-frameworks]: Mixed purpose → EV + Regret Minimization
  → [researching-re-market]: Comparable căn hộ Mỹ Khê, rental yield data

Step 4 — Simulation:
  → [simulating-re-scenarios]: Monte Carlo 5 năm, DCF từ rental income

Step 5 — Decision:
  → [debating-re-decisions]: 5 personas debate
  → Generate Decision Card

Step 6 — Output:
  Decision Card + 3 next steps + confidence level
  + "Set reminder 6 tháng sau để review"
```

### 6.2 Flow: "Nên bán đất bây giờ hay giữ?"

```
User: "Tôi có miếng đất 100m2 ở Hòa Xuân, mua 2021 giá 3.2 tỷ,
       hiện tại thị trường khoảng 2.6 tỷ. Nên bán hay giữ?"

→ [deciding-real-estate triggers]

Step 3 — Analysis:
  → [analyzing-re-biases]:
    ⚠️ ANCHORING: Neo vào giá mua 3.2 tỷ
    ⚠️ LOSS AVERSION: Không muốn realize loss 600tr
    ⚠️ SUNK COST: "Đã chờ 5 năm rồi"
    ⚠️ DISPOSITION EFFECT: Giữ loser quá lâu

  → [applying-re-frameworks]:
    Prospect Theory: "Nếu bạn KHÔNG có miếng đất này,
    bạn có bỏ 2.6 tỷ mua ở giá hiện tại không?"
    Opportunity Cost: 2.6 tỷ × 6% (gửi bank) = 156tr/năm
    vs đất tăng từ 2.6 → 3.2 tỷ cần ~23% gain = bao lâu?
```

### 6.3 Flow: "So sánh 3 căn hộ, nên chọn căn nào?"

```
User: "So sánh 3 căn hộ:
       A: Quận 2, 3.5 tỷ, 75m2, cho thuê 15tr/tháng
       B: Quận 7, 3.2 tỷ, 80m2, cho thuê 13tr/tháng  
       C: Thủ Đức, 2.8 tỷ, 70m2, cho thuê 10tr/tháng"

→ [deciding-real-estate] + [simulating-re-scenarios]

  → Tính cho mỗi căn: Cap rate, Net yield, Price/sqm, Rental yield
  → Sensitivity analysis: lãi suất tăng 2% ảnh hưởng thế nào?
  → Decision Matrix: weighted scoring (ROI 40%, location 25%, 
    liquidity 20%, appreciation potential 15%)
  → Output: Ranked comparison + Decision Card
```

### 6.4 Flow: Nhà đầu tư dòng tiền đánh giá BĐS cho thuê

```
User: "Tôi đang xem 1 căn hộ 2PN ở Quận 7, giá 3.2 tỷ, cho thuê 
       khoảng 13tr/tháng. Tôi muốn mua để cho thuê lấy dòng tiền, 
       vay 50%. Đây có phải deal tốt không?"

→ [deciding-real-estate triggers]
→ [analyzing-re-biases]: Check anchoring vào giá thuê rao (13tr thực tế có thể chỉ 11-12tr)

→ [researching-re-market — Tool 2 Rental Market Scanner]:
  - Web search: "cho thuê căn hộ 2PN Quận 7 giá 2025 2026"
  - Kết quả: rental range 11-15tr, median 12.5tr, vacancy ~1.5 tháng/năm

→ [researching-re-market — Tool 8 Cash Flow Verification]:
  - Phí quản lý: 8,000 VNĐ/m² × 70m² = 560k/tháng
  - Thuế cho thuê: 12.5tr × 7% = 875k/tháng (khoán)
  - Bảo trì: 3.2 tỷ × 1.5% / 12 = 4tr/tháng
  - Khấu hao nội thất: 200tr / 60 tháng = 3.3tr/tháng
  - Debt service: 1.6 tỷ × 9% / 12 = 12tr/tháng

→ [simulating-re-scenarios — Cash Flow Pro-forma]:
  Gross Rent: 12.5tr/tháng (median, không phải max)
  Vacancy: 12.5tr × 1.5/12 = -1.56tr/tháng (annualized)
  Effective Gross: 10.94tr/tháng
  OPEX: -(560k + 875k + 4tr + 3.3tr) = -8.74tr/tháng
  NOI: 2.2tr/tháng
  Debt Service: -12tr/tháng
  ⚠️ Monthly Cash Flow: -9.8tr/tháng (NEGATIVE!)
  
  DSCR = 2.2tr × 12 / (12tr × 12) = 0.18 → 🔴 RED FLAG

→ [debating-re-decisions]:
  Cash Flow Investor: "DSCR 0.18 — deal này negative cash flow nặng. 
    Mỗi tháng bạn bù 9.8tr. Đây không phải đầu tư dòng tiền, đây 
    là đặt cược vào capital gain. Nếu muốn cash flow, hoặc giảm giá 
    mua xuống 2.2 tỷ, hoặc tìm BĐS yield cao hơn (nhà trọ, phòng 
    cho thuê mini apartment)."
  
  Veteran: "Quận 7 location premium, capital gain 5-7%/năm. 
    Negative cash flow 9.8tr/tháng = 118tr/năm = 3.7% trên vốn 1.6 tỷ. 
    Nếu giá tăng >3.7%/năm, vẫn lời tổng thể."
  
  Risk Analyst: "Negative cash flow + leverage 50% = double risk. 
    Nếu lãi suất tăng 2%, debt service = 14.7tr → cash flow -12.5tr/tháng."

→ Output: Decision Card với confidence LOW (35%)
  Đề xuất: "Phân tích cho thấy deal này KHÔNG phù hợp cho mục tiêu 
  dòng tiền. Xem xét: (1) giảm leverage, (2) tìm BĐS yield cao hơn, 
  hoặc (3) chấp nhận đây là capital gain play."
```

### 6.5 Flow: Location Intelligence — Khảo sát khu vực trước khi quyết định

```
User: "Tôi đang xem xét mua đất ở Điện Bàn, Quảng Nam, gần Đà Nẵng. 
       Giúp tôi research khu vực này."

→ [researching-re-market triggers — full 8-tool scan]

Tool 1 — Comparable:
  → Search: "giá đất Điện Bàn Quảng Nam 2026"
  → Output: Price range, transaction volume, trend 12 tháng

Tool 2 — Rental:
  → Search: "cho thuê nhà Điện Bàn", "rental yield Điện Bàn"
  → Output: Rental market gần như không có (red flag cho cash flow investor)

Tool 3 — Infrastructure:
  → Search: "quy hoạch Điện Bàn 2026", "cao tốc Đà Nẵng Quảng Nam",
            "KCN Điện Bàn mới"
  → Output: Infrastructure Score, timeline dự án hạ tầng

Tool 4 — Legal:
  → Search: "quy hoạch sử dụng đất Điện Bàn", "đất thổ cư Điện Bàn",
            "tranh chấp đất Điện Bàn"
  → Output: Zoning status, legal risk flags

Tool 5 — Demand:
  → Search: "dân số Điện Bàn tăng trưởng", "FDI Quảng Nam 2026",
            "KCN Điện Nam Điện Ngọc"
  → Output: Demand Score, drivers (FDI, KCN, urbanization spillover từ ĐN)

Tool 6 — Market Cycle:
  → Search: "thị trường BĐS Điện Bàn 2026 nhận định", "tồn kho đất nền Quảng Nam"
  → Output: Cycle phase assessment

Tool 7 — Supply:
  → Search: "dự án mới Điện Bàn 2026", "phân lô bán nền Điện Bàn"
  → Output: Supply pipeline, absorption rate

Tool 8 — Cash Flow:
  → Skipped (đất nền không có rental income)
  → Flag: "Đất nền = pure capital gain play, không có dòng tiền"

→ Output: Location Intelligence Report
  ┌─────────────────────────────────────┐
  │ 📍 Location Report: Điện Bàn, QNam │
  ├─────────────────────────────────────┤
  │ Price range: X-Y tỷ/100m²          │
  │ Infrastructure Score: 6/10         │
  │ Demand Score: 7/10                 │
  │ Legal Status: ⚠️ Check zoning      │
  │ Market Cycle: Early Markup         │
  │ Supply Risk: Moderate              │
  │ Cash Flow: N/A (đất nền)           │
  │ Rental Yield: N/A                  │
  ├─────────────────────────────────────┤
  │ Key drivers: KCN spillover, hạ tầng│
  │ Key risks: oversupply, pháp lý     │
  └─────────────────────────────────────┘
```

---

## 7. Roadmap

### Phase 1 — MVP (4 tuần)
- [ ] deciding-real-estate: cognitive loop orchestrator + Decision Card
- [ ] analyzing-re-biases: 12 biases + detection logic
- [ ] applying-re-frameworks: Bayesian, EV, Prospect Theory (prompt-based, chưa cần scripts)
- [ ] Cash flow investor persona: formulas + bias profile + workflow integration
- [ ] Cài đặt trên Claude Code CLI (`.claude/skills/`)
- [ ] 5 test cases thực tế (mua căn hộ, bán đất, mua đất nền, mua nhà phố, giữ hay bán)
- [ ] 2 test cases dòng tiền (căn hộ cho thuê negative cash flow, nhà trọ positive cash flow)

### Phase 2 — Quantitative + Location Intelligence (4 tuần)
- [ ] simulating-re-scenarios: Monte Carlo, DCF, sensitivity scripts
- [ ] researching-re-market: 8-tool Location Intelligence Toolkit
- [ ] Scripts: `monte_carlo.py`, `dcf_calculator.py`, `ev_calculator.py`
- [ ] Scripts dòng tiền: `cashflow_proforma.py`, `rental_yield_calc.py`
- [ ] Scripts location: `location_scorer.py`, `supply_demand_ratio.py`, `cycle_detector.py`
- [ ] SOURCES-VN.md: bảng data sources chi tiết với access method
- [ ] LOCATION-CHECKLIST.md + CASHFLOW-VERIFICATION.md
- [ ] Decision archive (SQLite)

### Phase 3 — Debate + Polish (3 tuần)
- [ ] debating-re-decisions: 5 personas (bao gồm Cash Flow Investor) + debate protocol
- [ ] Bezos reversibility + Taleb barbell + Pre-mortem + Regret minimization
- [ ] Reflection loop: track outcomes, calibration logging
- [ ] EXAMPLES.md với 10+ real scenarios (bao gồm 3 cash flow scenarios)

### Phase 4 — Ecosystem (ongoing)
- [ ] Claude API deployment (Skills API /v1/skills upload)
- [ ] Claude.ai zip upload cho Pro/Max users
- [ ] Community contribution: thêm personas, market sources cho các tỉnh
- [ ] Location Intelligence mở rộng: thêm sources cho HCM, Hà Nội, Bình Dương, Long An
- [ ] MCP server option cho external data feeds (batdongsan API nếu có)
- [ ] Publish lên GitHub dưới MIT license

---

## 8. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Bias detection accuracy | ≥80% precision | Manual review 50 test cases |
| Decision Card completeness | 100% fields filled | Automated check |
| User follows recommended next steps | ≥60% | Self-reported in reflection |
| Prediction accuracy (12-month) | Track, no target yet | Outcome logging |
| Context window efficiency | <5k tokens per skill trigger | Token counting |
| Skill trigger accuracy | ≥90% correct skill selected | 100 diverse prompts test |
| Cash flow projection accuracy | ≤15% deviation vs actual NOI after 12 months | User reports actual vs projected |
| Location Intelligence coverage | 8/8 tools produce actionable output | Test across 10 locations |
| DSCR alert accuracy | 100% flag khi DSCR <1.0 | Automated in `cashflow_proforma.py` |
| Negative cash flow detection | 100% catch trước khi recommend mua | Test 20 negative CF scenarios |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| User treats output as financial advice | Legal liability | Mandatory disclaimer trên mọi Decision Card |
| Overconfident recommendations | User loss | Confidence scoring + explicit uncertainty ranges |
| Vietnam market data outdated | Wrong analysis | Timestamp all data, prompt user to verify |
| Context window overflow với nhiều skills | Poor performance | Progressive disclosure + max 2 skills per turn |
| Monte Carlo assumptions unrealistic | Misleading projections | Expose all assumptions, let user adjust |
| Claude API surface: no network | Cannot research market | Graceful fallback — ask user to provide data |
| Rental yield dùng giá rao thay vì giá thực | Overestimate cash flow | Default dùng median, discount 10-15% từ listing price |
| OPEX underestimate (quên chi phí ẩn) | False positive cash flow | CASHFLOW-VERIFICATION.md checklist bắt buộc, vacancy buffer ≥2 tháng |
| Location data bias (chỉ có positive news) | Miss hidden risks | Tool 4 (Legal) + Tool 7 (Supply) chủ động tìm negative signals |
| Web search trả về content cũ/SEO spam | Wrong market assessment | Cross-reference ≥3 sources, prefer CBRE/Savills/JLL reports |

---

## 10. References

### Academic
- Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk
- Beracha, E. & Skiba, H. (2014). Real Estate Investment Decision Making in Behavioral Finance
- Northcraft, G.B. & Neale, M.A. (1987). Experts, Amateurs, and Real Estate: An Anchoring-and-Adjustment Perspective
- Ali et al. (2020). Overconfidence and anchoring in real estate valuators
- Taleb, N.N. (2012). Antifragile: Things That Gain from Disorder
- Behavioural Insights Team (2025). AI can help us make (mostly) better decisions

### Technical
- Anthropic Agent Skills Overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Anthropic Agent Skills Best Practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Spice Decision Runtime: https://github.com/Dyalwayshappy/Spice
- Multi-Viewpoint Debates: https://github.com/openclaw/skills/blob/main/skills/latentfreedom/multi-viewpoint-debates/SKILL.md

# SpiceRE — Trợ lý Phân tích Bất Động Sản Dòng Tiền

Agent Skill cho Claude Code CLI giúp phân tích quyết định đầu tư bất động sản dòng tiền tại Việt Nam. Phát hiện bias tâm lý, tính toán cash flow thực tế, mô phỏng Monte Carlo, và tranh luận đa góc nhìn — tất cả trong một quy trình có cấu trúc.

## Tính năng chính

**Vòng lặp nhận thức 6 bước:**

| Bước | Tên | Mô tả |
|------|-----|-------|
| 1 | Perception | Nhận diện ý định (mua/bán/giữ/so sánh), trích xuất thông tin BĐS |
| 2 | State Modeling | Xây dựng mô hình người dùng/BĐS/thị trường/ràng buộc |
| 3 | Analysis | Phát hiện 12 bias tâm lý + chọn framework phân tích + nghiên cứu thị trường |
| 4 | Simulation | Monte Carlo, DCF, Cash flow pro-forma, Bayesian updating |
| 5 | Decision | Tranh luận 5 personas + tạo Decision Card |
| 6 | Reflection | Lưu trữ quyết định, so sánh với lịch sử |

**Phát hiện bias tâm lý:**
- 12 bias BĐS đặc thù: anchoring, loss aversion, herding, disposition effect, sunk cost, overconfidence, familiarity, confirmation, recency, status quo, endowment effect, framing
- Mỗi bias có marker phát hiện bằng tiếng Việt
- Trình bày dưới dạng câu hỏi: *"Bạn có đang neo vào giá mua 3.2 tỷ?"*

**Phân tích định lượng:**
- `cashflow_proforma.py` — Pro-forma dòng tiền 10 năm với OPEX thực tế Việt Nam, cảnh báo DSCR < 1.0
- `monte_carlo.py` — Mô phỏng giá BĐS (GBM, 1000 iterations, P10-P90)
- `dcf_calculator.py` — NPV, IRR, cash-on-cash return, equity multiple
- `bayesian_updater.py` — Cập nhật xác suất khi có bằng chứng mới

**Tranh luận đa góc nhìn:**
- 5 personas: Nhà đầu tư kỳ cựu, Nhà đầu tư dòng tiền, Chuyên gia rủi ro, Người dùng cuối, Người phản biện
- Xác định tension points (điểm bất đồng) giữa các personas
- Tổng hợp: tensions tiết lộ rủi ro ẩn và giả định chưa kiểm chứng

**Output:** Decision Card tiếng Việt với confidence scoring (Low/Medium/High) + disclaimer bắt buộc

## Cài đặt

### Yêu cầu
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (hỗ trợ Agent Skills)
- Python 3.8+
- numpy

### Bước 1: Clone repo

```bash
git clone https://github.com/abc-elearning/spice-real-estate.git
cd spice-real-estate
```

### Bước 2: Sync skill vào Claude Code

```bash
bash bin/sync-skill.sh
```

### Bước 3: Setup Python environment

```bash
cd .claude/skills/spice-re/deciding-real-estate
python3 -m venv .venv
.venv/bin/pip install numpy
```

### Bước 4: Kiểm tra

```bash
.venv/bin/python3 scripts/test_all.py
# Expected: 14/14 passed
```

## Cách sử dụng

### Sử dụng với Claude Code CLI

Mở Claude Code CLI trong thư mục project. Skill sẽ tự động trigger khi bạn hỏi về BĐS:

```
> Tôi đang cân nhắc mua căn hộ 2PN ở Quận 7, giá 3.2 tỷ,
  cho thuê 13tr/tháng. Tôi có 1.6 tỷ cash, vay 1.6 tỷ lãi 9%.
  Mục đích cho thuê lấy dòng tiền. Có nên mua không?
```

Claude sẽ chạy qua 6 bước cognitive loop và output Decision Card.

### Ví dụ kịch bản

**Kịch bản 1: Mua căn hộ cho thuê (Cash flow dương)**
```
> Căn hộ 2PN Quận 7, 2.8 tỷ, cho thuê 15tr/tháng, 70m², vay 40% lãi 9%
```
→ DSCR green, positive cash flow, Decision Card với confidence Medium-High

**Kịch bản 2: Phát hiện cash flow âm**
```
> Căn hộ 2PN Quận 7, 3.2 tỷ, cho thuê 13tr/tháng, 70m², vay 50% lãi 9%
```
→ DSCR RED FLAG (< 1.0), Cash Flow Investor persona cảnh báo mạnh, confidence Low

**Kịch bản 3: Bán hay giữ — phát hiện loss aversion**
```
> Tôi có miếng đất 100m² ở Hòa Xuân, mua 2021 giá 3.2 tỷ, hiện tại 2.6 tỷ.
  Nên bán hay giữ?
```
→ Phát hiện 3 bias (anchoring, loss aversion, disposition effect), Prospect Theory reframe: *"Nếu không sở hữu, bạn có mua ở 2.6 tỷ không?"*

Xem thêm ví dụ chi tiết tại [`skill/EXAMPLES.md`](skill/EXAMPLES.md)

## Sử dụng scripts độc lập

Các scripts có thể chạy trực tiếp qua CLI:

### Cash flow pro-forma
```bash
cd .claude/skills/spice-re/deciding-real-estate
.venv/bin/python3 scripts/cashflow_proforma.py \
  --price 3200000000 \
  --rent 13000000 \
  --area 70 \
  --loan 1600000000 \
  --interest 0.09
```

### Monte Carlo mô phỏng giá
```bash
.venv/bin/python3 scripts/monte_carlo.py \
  --price 3200000000 \
  --growth 0.05 \
  --std 0.08 \
  --years 5 \
  --sims 1000 \
  --seed 42
```

### DCF (NPV, IRR)
```bash
.venv/bin/python3 scripts/dcf_calculator.py \
  --monthly_rent 13000000 \
  --growth 0.03 \
  --opex_ratio 0.4 \
  --discount 0.1 \
  --years 10 \
  --initial 3200000000 \
  --loan 1600000000 \
  --rate 0.09
```

### Bayesian updating
```bash
.venv/bin/python3 scripts/bayesian_updater.py \
  --prior 0.4 \
  --evidence_strength strong \
  --evidence_direction positive
```

Tất cả scripts output JSON. Ví dụ output `cashflow_proforma.py`:
```json
{
  "status": "success",
  "monthly_cf": -6460000,
  "annual_coc": -0.048,
  "dscr": 0.46,
  "dscr_flag": "red",
  "warning": "DSCR < 1.0 — negative cash flow",
  "year_by_year": [...]
}
```

## Cấu trúc thư mục

```
spice-real-estate/
├── skill/                          # SOURCE OF TRUTH — edit ở đây
│   ├── SKILL.md                    # Entry point: cognitive loop 6 bước
│   ├── FORMULAS.md                 # 17 công thức tài chính + OPEX checklist
│   ├── BIASES.md                   # 12 bias tâm lý + marker phát hiện
│   ├── PERSONAS.md                 # 5 debate personas
│   ├── DECISION-CARD.md            # Template Decision Card (tiếng Việt)
│   ├── SOURCES-VN.md               # 16 nguồn dữ liệu thị trường VN
│   ├── EXAMPLES.md                 # 3 kịch bản ví dụ
│   └── scripts/
│       ├── utils.py                # Shared: JSON output + validation
│       ├── monte_carlo.py          # Mô phỏng giá (GBM, numpy)
│       ├── dcf_calculator.py       # NPV, IRR, cash-on-cash
│       ├── cashflow_proforma.py    # Pro-forma 10 năm + DSCR
│       ├── bayesian_updater.py     # Cập nhật xác suất Bayesian
│       └── test_all.py             # 14 automated tests
├── bin/
│   └── sync-skill.sh              # Sync: skill/ → .claude/skills/
├── docs/
│   └── PRD_SpiceRE.md             # PRD gốc (tài liệu tham khảo)
├── .claude/
│   └── skills/spice-re/deciding-real-estate/  # Runtime copy (Claude Code đọc từ đây)
├── .spice_re/decisions/            # Lưu trữ Decision Cards (gitignored)
├── CLAUDE.md                       # Hướng dẫn cho Claude
└── README.md                       # File này
```

## Quy trình phát triển

```
1. Edit files trong skill/
2. Sync: bash bin/sync-skill.sh
3. Test: cd .claude/skills/spice-re/deciding-real-estate && .venv/bin/python3 scripts/test_all.py
4. Commit & push
```

**Tại sao 2 bản copy?**
- `skill/` là source of truth — edit, review, commit ở đây
- `.claude/skills/` là runtime copy — Claude Code Agent Skills đọc từ đây
- Thư mục `.claude/` có thể bị xóa bởi tools — `skill/` đảm bảo không mất code
- `bin/sync-skill.sh` đồng bộ 1 lệnh

## Công nghệ

| Thành phần | Công nghệ |
|-----------|-----------|
| Platform | Claude Code CLI (Anthropic Agent Skills) |
| Language | Python 3.8+ (stdlib + numpy) |
| Architecture | 3-level progressive disclosure (Level 1: metadata, Level 2: SKILL.md <5k tokens, Level 3: reference files + scripts) |
| Data storage | Markdown files (v1) |
| Testing | Custom test_all.py (subprocess-based, 14 test cases) |
| Sync | rsync via bin/sync-skill.sh |

## Các công thức chính

| Công thức | Ý nghĩa | Ngưỡng VN |
|-----------|---------|-----------|
| Net Rental Yield | (Rent - OPEX) / Price | > 5% = tốt |
| DSCR | NOI / Debt Service | < 1.0 = RED FLAG, ≥ 1.3 = healthy |
| Cash-on-Cash | Annual CF / Equity | > 8% = target |
| Cap Rate | NOI / Property Value | > 5% = attractive |
| GRM | Price / Annual Gross Rent | < 12 = attractive |

Xem đầy đủ 17 công thức tại [`skill/FORMULAS.md`](skill/FORMULAS.md)

## Lưu ý quan trọng

SpiceRE là công cụ **hỗ trợ phân tích**, không phải tư vấn đầu tư chuyên nghiệp. Output luôn kèm:
- Confidence level (Low/Medium/High với %)
- Khuyến nghị dạng "Phân tích cho thấy..." (không phải "Bạn nên...")
- Disclaimer pháp lý bắt buộc trên mọi Decision Card

**Tham vấn chuyên gia tài chính và pháp lý trước khi ra quyết định.**

## Roadmap

- [x] v1: Cognitive loop + 4 scripts + bias detection + debate + Decision Card
- [ ] v2: Location Intelligence toolkit (8 tools), SQLite database, reflection loop
- [ ] v3: Claude Desktop/Claude.ai deployment, multi-region support

## License

MIT

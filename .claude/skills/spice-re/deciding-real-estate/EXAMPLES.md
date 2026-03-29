# Ví dụ Thực tế — SpiceRE Decision Advisor

3 kịch bản minh hoạ full cognitive loop: từ nhận diện ý định → phát hiện bias → mô phỏng số liệu → tranh luận đa chiều → Decision Card.

---

## Kịch bản 1: Mua căn hộ cho thuê — Cash flow DƯƠNG

**Input:** "Mình đang xem căn hộ 2PN Quận 7, giá 2.8 tỷ, cho thuê được 15 triệu/tháng, diện tích 70m². Dự định vay 40% lãi suất 9%. Nên mua không?"

### Step 1: Perception

```
Intent: BUY | Property: Căn hộ 2PN Q7, 2.8 tỷ, 70m², thuê 15tr/th | Gaps: legal_status, risk_tolerance
```

Thuộc tính trích xuất: price=2,800,000,000 VND, rent=15,000,000/th, area=70m², loan=40% (1,120,000,000), interest=9%.

### Step 2: State Modeling

**User Profile:** Equity ~1.68 tỷ, có khả năng vay 1.12 tỷ, mục đích đầu tư cho thuê.

**Property Model:** Giá/m² = 40 triệu/m² (nằm trong khoảng trung bình Q7). Gross yield = 15×12/2800 = 6.4%. Legal: [TBD — cần xác minh sổ hồng].

**Market Context:** Lãi suất cho vay 9% (mức trung bình 2024-2025), thị trường Q7 ổn định, thanh khoản khá.

### Step 3: Analysis

**Bias scan:** Không phát hiện bias rõ ràng. User hỏi trung tính "nên mua không?" — không có anchoring hay confirmation bias.

**Framework:** BUY + cash flow focused → DCF + Cash-on-Cash + DSCR stress test.

### Step 4: Simulation

```bash
.venv/bin/python3 scripts/cashflow_proforma.py \
  --price 2800000000 --rent 15000000 --area 70 \
  --loan 1120000000 --interest 0.09
```

**Kết quả chính (Year 1):**

| Chỉ số | Giá trị |
|--------|---------|
| Gross Rent | 180,000,000/năm |
| Vacancy (12.5%) | -22,500,000 |
| Effective Gross | 157,500,000 |
| OPEX (mgmt + tax + maintenance) | ~65,850,000 |
| NOI | ~91,650,000 |
| Debt Service | 100,800,000 |
| Net Cash Flow | ~-9,150,000/năm (~-762,500/th) |
| DSCR | ~0.91 |

> Lưu ý: Kịch bản mẫu — kết quả thực tế tuỳ thuộc vacancy rate và OPEX thực tế. Với vacancy thấp hơn (1 tháng thay vì 1.5 tháng), DSCR có thể vượt 1.0.

Stress test lãi suất +2% (11%): DSCR giảm xuống ~0.74 → RED FLAG.

### Step 5: Decision — Trích đoạn tranh luận

| Persona | Quan điểm | Lập luận |
|---------|-----------|----------|
| Nhà đầu tư kỳ cựu | Mua có điều kiện | Gross yield 6.4% khá tốt cho Q7, nhưng net yield mỏng. Nên đàm phán giá xuống 2.5-2.6 tỷ |
| Nhà đầu tư dòng tiền | Cân nhắc kỹ | DSCR sát 1.0, rủi ro nếu vacancy tăng. Cần đảm bảo vacancy < 1 tháng/năm |
| Chuyên gia rủi ro | Thận trọng | Leverage 40% ở lãi 9% tạo áp lực. Stress test +2% fail. Buffer tài chính cần >= 6 tháng |
| Người dùng cuối | Trung lập | Vị trí Q7 dễ cho thuê, nhưng cạnh tranh cao |
| Người phản biện | Xem xét lại | Tại sao không gửi tiết kiệm 7% risk-free thay vì chịu rủi ro BĐS? |

**Tension chính:** Nhà đầu tư kỳ cựu vs Chuyên gia rủi ro — leverage level có chấp nhận được không khi DSCR sát ngưỡng.

### Decision Card (trích)

```
📋 Decision Card: Mua căn hộ 2PN Quận 7 cho thuê

Ngày: 2026-03-29  |  Confidence: Medium (55%)

Đề xuất: Phân tích cho thấy căn hộ có gross yield hấp dẫn (6.4%) nhưng
net cash flow mỏng do OPEX thực tế cao hơn kỳ vọng. Độ tin cậy trung bình —
phân tích nghiêng về MUA nếu đàm phán được giá tốt hơn hoặc giảm LTV xuống 30%.

Bước tiếp theo:
1. Xác minh pháp lý (sổ hồng, quy hoạch) — trong 1 tuần
2. Khảo sát giá thuê thực tế 5+ căn tương đương — trong 1 tuần
3. Đàm phán giá xuống 2.5-2.6 tỷ — trong 2 tuần
```

---

## Kịch bản 2: Mua căn hộ — Cash flow ÂM (phát hiện)

**Input:** "Mình muốn mua căn 2PN Quận 7 giá 3.2 tỷ, cho thuê 13 triệu/tháng, 70m², vay 50% lãi 9%."

### Step 1: Perception

```
Intent: BUY | Property: Căn hộ 2PN Q7, 3.2 tỷ, 70m², thuê 13tr/th | Gaps: legal_status
```

### Step 2: State Modeling

**Property Model:** Giá/m² = 45.7 triệu (cao hơn trung bình Q7). Gross yield = 13×12/3200 = 4.9%. LTV = 50%.

### Step 3: Analysis

**Bias scan:** Có thể có anchoring — gross yield 4.9% "trông ổn" nhưng chưa tính OPEX đầy đủ.

**Framework:** BUY + cash flow → DCF + DSCR.

### Step 4: Simulation — RED FLAG

```bash
.venv/bin/python3 scripts/cashflow_proforma.py \
  --price 3200000000 --rent 13000000 --area 70 \
  --loan 1600000000 --interest 0.09
```

**Kết quả Year 1:**

| Chỉ số | Giá trị | Cảnh báo |
|--------|---------|----------|
| Gross Rent | 156,000,000/năm | |
| Effective Gross (sau vacancy) | 136,500,000 | |
| Total OPEX | ~67,050,000 | |
| NOI | ~69,450,000 | |
| Debt Service | 144,000,000 | |
| **Net Cash Flow** | **-74,550,000/năm** | **CASH FLOW ÂM** |
| **DSCR** | **~0.48** | **RED FLAG** |

**Phân tích:** Gross yield 4.9% trông chấp nhận được, nhưng sau khi trừ:
- Vacancy 12.5%
- Phí quản lý 8.4 triệu/năm
- Thuế 10% EGI = 13.65 triệu
- Bảo trì 1.5% = 48 triệu

...NOI chỉ còn ~69.5 triệu, trong khi debt service 144 triệu → thiếu hụt ~6.2 triệu/tháng.

**Key insight:** Gross yield 4.9% KHÔNG ĐỦ để cover OPEX + debt service khi LTV 50% và lãi 9%. Cần gross yield >= 7% hoặc LTV <= 30%.

### Step 5: Decision

| Persona | Quan điểm | Lập luận |
|---------|-----------|----------|
| Nhà đầu tư dòng tiền | **KHÔNG MUA** | DSCR 0.48 — phải bù lỗ 6.2tr/tháng. Đây là deal âm tiền rõ ràng |
| Chuyên gia rủi ro | **KHÔNG MUA** | Stress test: nếu lãi tăng 11% → thiếu hụt 8.9tr/tháng. Không có buffer |
| Người phản biện | Tại sao deal này? | Với 1.6 tỷ equity, gửi tiết kiệm 7% = 112tr/năm risk-free. Deal này mất 74.5tr/năm |

### Decision Card (trích)

```
📋 Decision Card: Mua căn hộ 2PN Quận 7

Ngày: 2026-03-29  |  Confidence: Low (25%)

Đề xuất: Phân tích cho thấy deal này tạo cash flow âm đáng kể (-6.2tr/tháng).
DSCR 0.48 nằm sâu dưới ngưỡng an toàn (1.3). Độ tin cậy thấp — khuyến nghị
KHÔNG tiến hành trừ khi: (1) đàm phán giá xuống < 2.5 tỷ, (2) giảm LTV xuống 30%,
hoặc (3) có kế hoạch capital gain rõ ràng để bù lỗ dòng tiền.

Thông tin cần bổ sung:
- Kế hoạch tăng giá thuê (renovation, furnished?)
- Dữ liệu capital gain khu vực 3-5 năm gần nhất
- Khả năng tài chính bù lỗ hàng tháng trong bao lâu
```

---

## Kịch bản 3: Bán hay giữ — Phát hiện Loss Aversion

**Input:** "Mình có miếng đất 100m² ở Hòa Xuân, Đà Nẵng, mua năm 2021 giá 3.2 tỷ, giờ thị trường chỉ còn 2.6 tỷ. Mình không muốn bán lỗ. Giữ tiếp hay bán?"

### Step 1: Perception

```
Intent: SELL/HOLD | Property: Đất 100m² Hòa Xuân, mua 3.2 tỷ (2021), hiện 2.6 tỷ | Gaps: mục đích sử dụng, tình hình tài chính
```

### Step 2: State Modeling

**Property Model:** Mua 32 triệu/m² (2021), hiện 26 triệu/m² (-18.75%). Lỗ chưa hiện thực hoá: 600 triệu.

**Market Context:** Thị trường đất Đà Nẵng giai đoạn markdown (2022-2025). Thanh khoản thấp. Chưa có tín hiệu phục hồi rõ ràng.

### Step 3: Analysis — Phát hiện 3 Bias

**Bias 1 — Anchoring (Neo giá):**
> "Bạn có đang bị neo vào giá mua 3.2 tỷ? Giá mua năm 2021 là giá đỉnh thị trường — không phản ánh giá trị hiện tại. Thử nghĩ: giá trị thực sự là giá mà thị trường sẵn sàng trả HÔM NAY."

**Bias 2 — Loss Aversion (Sợ lỗ):**
> "Bạn nói 'không muốn bán lỗ' — đây là dấu hiệu loss aversion. Theo Prospect Theory, con người cảm nhận nỗi đau mất mát gấp 2.5× niềm vui lời lãi. Thử nghĩ: khoản lỗ 600 triệu đã xảy ra rồi dù bạn bán hay không."

**Bias 3 — Disposition Effect (Hiệu ứng bán sớm/giữ lâu):**
> "Bạn có xu hướng giữ tài sản lỗ (hy vọng hồi giá) và bán tài sản lời (chốt lãi sớm). Thử nghĩ: quyết định giữ hay bán nên dựa trên triển vọng TƯƠNG LAI, không phải giá mua QUÁ KHỨ."

**Framework:** SELL/HOLD → Prospect Theory + Regret Minimization + Opportunity Cost.

### Step 4: Prospect Theory Reframe

**Câu hỏi then chốt:**
> "Nếu bạn KHÔNG sở hữu miếng đất này, và có 2.6 tỷ tiền mặt, bạn có MUA nó ở giá 2.6 tỷ không?"

Nếu câu trả lời là "Không" → đó là tín hiệu nên bán.

**Opportunity Cost Analysis:**

| Phương án | Giá trị sau 3 năm | Giả định |
|-----------|-------------------|----------|
| Giữ đất | 2.6 tỷ × (1 + g)³ | g = ? (có thể -5% đến +10%) |
| Bán, gửi tiết kiệm 6% | 2.6 tỷ × 1.06³ = 3.096 tỷ | Chắc chắn, risk-free |
| Bán, đầu tư khác | Tuỳ phương án | Cần đánh giá riêng |

**Chi phí cơ hội của việc GIỮ:** 2.6 tỷ × 6% = 156 triệu/năm. Mỗi năm giữ đất mà không tăng giá, bạn mất 156 triệu chi phí cơ hội.

**Để hoà vốn (về lại 3.2 tỷ):** Đất cần tăng ~23% từ 2.6 tỷ → ~7.2%/năm trong 3 năm. Trong bối cảnh thị trường Đà Nẵng hiện tại, mức tăng này KHÔNG CÓ CƠ SỞ DỮ LIỆU hỗ trợ.

### Step 5: Decision

| Persona | Quan điểm | Lập luận |
|---------|-----------|----------|
| Nhà đầu tư kỳ cựu | Bán | Sunk cost. Thị trường markdown. Cơ hội tái phân bổ vốn tốt hơn |
| Nhà đầu tư dòng tiền | Bán | Đất không sinh dòng tiền. 156tr/năm opportunity cost |
| Chuyên gia rủi ro | Bán | Thanh khoản đất Đà Nẵng thấp. Giá có thể giảm thêm 10-15% |
| Người dùng cuối | Giữ nếu có kế hoạch xây | Chỉ giữ nếu có mục đích sử dụng cụ thể trong 2-3 năm |
| Người phản biện | Giữ nếu tin vào Đà Nẵng dài hạn | Nếu infrastructure phát triển, đất Hòa Xuân có thể phục hồi 5-7 năm |

**Tension chính:** 4/5 personas thiên về BÁN. Người phản biện đưa ra case duy nhất — đầu tư dài hạn 5-7 năm nếu tin vào quy hoạch Đà Nẵng. Nhưng chi phí cơ hội là 156tr/năm × 5 = 780 triệu.

### Decision Card (trích)

```
📋 Decision Card: Bán hay giữ đất Hòa Xuân

Ngày: 2026-03-29  |  Confidence: Medium (60%)

Cảnh báo Bias:
| Bias | Mức ảnh hưởng | Cách giảm thiểu |
|------|---------------|-----------------|
| Anchoring (neo giá 3.2 tỷ) | Cao | Đánh giá dựa trên giá thị trường hiện tại 2.6 tỷ |
| Loss Aversion (sợ bán lỗ) | Cao | Khoản lỗ đã xảy ra — quyết định dựa trên tương lai |
| Disposition Effect | Trung bình | Hỏi: "Nếu có 2.6 tỷ cash, có mua đất này không?" |

Đề xuất: Phân tích cho thấy việc GIỮ đất có chi phí cơ hội 156tr/năm và
cần tăng giá 7.2%/năm chỉ để hoà vốn — mức khó đạt trong thị trường hiện tại.
Độ tin cậy trung bình — phân tích nghiêng về BÁN và tái phân bổ vốn,
nhưng cần xác minh: (1) quy hoạch khu vực, (2) dự án hạ tầng gần.

Bước tiếp theo:
1. Kiểm tra quy hoạch chi tiết Hòa Xuân — trong 1 tuần
2. Lấy báo giá từ 3 môi giới để xác nhận giá thị trường — trong 1 tuần
3. Nếu bán: tìm 2-3 phương án tái đầu tư 2.6 tỷ — trong 2 tuần
```

---

> **Lưu ý:** Đây là các ví dụ minh hoạ cách hệ thống hoạt động. Số liệu trong ví dụ dựa trên giả định mẫu — kết quả thực tế sẽ khác tuỳ theo tham số đầu vào cụ thể. Tham vấn chuyên gia tài chính và pháp lý trước khi ra quyết định đầu tư.

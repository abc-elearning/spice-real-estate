# FORMULAS.md — RE Financial Formulas Reference

> Level 3 resource. Loaded on demand during Analysis step of the cognitive loop.

---

## 1. Yield Metrics

### Cap Rate (Capitalization Rate)

```
Cap Rate = NOI / Property Value
```

- **Interpretation:** Tỷ suất lợi nhuận nếu mua hoàn toàn bằng tiền mặt (không vay).
- **Thresholds (Vietnam):**
  - < 3% = thấp (đặc trưng căn hộ cao cấp nội thành HCM/HN)
  - 3-5% = trung bình
  - 5-8% = tốt (mini apartment, nhà trọ, BĐS vùng ven)
  - \> 8% = kiểm tra lại — có thể rủi ro ẩn hoặc thiếu chi phí
- **Lưu ý:** Cap rate KHÔNG tính leverage. Dùng Cash-on-Cash khi có vay.

### Gross Rental Yield

```
Gross Rental Yield = Annual Gross Rent / Purchase Price
```

- **Interpretation:** Tỷ suất thuê thô — chưa trừ chi phí. Dùng để sàng lọc nhanh.
- **Thresholds (Vietnam):**
  - < 3% = yield thấp (thường là mua để lãi vốn, không phải dòng tiền)
  - 3-5% = trung bình cho căn hộ nội thành
  - 5-7% = tốt
  - \> 7% = rất tốt — cần xác minh giá thuê thực tế, không phải giá rao
- **Cảnh báo:** KHÔNG dùng gross yield để ra quyết định. Luôn tính net yield.

### Net Rental Yield

```
Net Rental Yield = (Annual Gross Rent - Annual Operating Expenses) / Purchase Price
```

- **Interpretation:** Tỷ suất thuê ròng — phản ánh thu nhập thực sau chi phí vận hành.
- **Thresholds (Vietnam):**
  - < 2% = kém hơn gửi ngân hàng
  - 2-4% = marginal — cân nhắc kỹ effort quản lý vs alternatives
  - 4-6% = tốt cho căn hộ, chấp nhận được
  - \> 6% = rất tốt — phổ biến ở nhà trọ, phòng cho thuê
- **So sánh:** Luôn so net yield với lãi suất tiết kiệm ngân hàng (thường 5-6% tại VN). Nếu net yield < bank rate, BĐS đó không xứng đáng effort quản lý cho mục tiêu dòng tiền.

---

## 2. Cash Flow Metrics

### Monthly Cash Flow

```
Monthly Cash Flow = Gross Rent - Vacancy Allowance - OPEX - Debt Service - CapEx Reserve
```

- **Interpretation:** Dòng tiền ròng thực tế mỗi tháng sau mọi chi phí.
- **Thresholds:**
  - Negative = BĐS "ăn" tiền — mỗi tháng phải bù thêm
  - 0 = hòa vốn vận hành
  - Positive = tạo thu nhập thụ động
- **Quan trọng:** Phải tính THỰC TẾ, không lý thuyết. Dùng CASHFLOW-VERIFICATION checklist bên dưới.

### Effective Gross Income (EGI)

```
Effective Gross Income = Gross Potential Rent × (1 - Vacancy Rate) + Other Income
```

- **Interpretation:** Thu nhập thuê thực tế sau khi trừ khoảng trống. Other Income bao gồm phí parking, quảng cáo, v.v.

### Net Operating Income (NOI)

```
NOI = Effective Gross Income - Operating Expenses
```

- **Interpretation:** Thu nhập ròng từ vận hành BĐS, TRƯỚC khi trừ chi phí vay.
- **Lưu ý:** NOI không bao gồm debt service, CapEx lớn, hoặc thuế thu nhập cá nhân. Là chỉ số chuẩn để so sánh BĐS với nhau.

### Cash-on-Cash Return (CoC)

```
Cash-on-Cash Return = Annual Pre-tax Cash Flow / Total Cash Invested
```

- **Total Cash Invested** = Down payment + Closing costs + Renovation + Furnishing
- **Interpretation:** Tỷ suất sinh lời trên vốn bỏ ra, tính leverage.
- **Thresholds (Vietnam):**
  - < 5% = kém — gửi bank tốt hơn
  - 5-8% = trung bình
  - 8-12% = tốt
  - \> 12% = rất tốt — kiểm tra lại chi phí đã đủ chưa
- **Target cho nhà đầu tư dòng tiền VN:** >= 8% (sau khi trừ MỌI chi phí thực tế)

### Operating Expense Ratio (OER)

```
Operating Expense Ratio = Operating Expenses / Effective Gross Income
```

- **Interpretation:** Bao nhiêu % thu nhập thuê bị ăn bởi chi phí vận hành.
- **Thresholds:**
  - < 30% = hiệu quả (thường là BĐS đơn giản, ít dịch vụ)
  - 30-40% = bình thường cho căn hộ
  - \> 40% = điều tra cấu trúc chi phí — phí quản lý, bảo trì bất thường?
  - \> 50% = red flag — margin quá mỏng, dễ bị negative cash flow

---

## 3. Risk & Leverage Metrics

### Debt Service Coverage Ratio (DSCR)

```
DSCR = NOI / Annual Debt Service
```

- **Annual Debt Service** = Tổng trả gốc + lãi trong năm
- **Interpretation:** NOI đủ trả nợ bao nhiêu lần.
- **Thresholds:**
  - < 1.0 = **negative cash flow** (RED FLAG) — NOI không đủ trả nợ
  - 1.0-1.2 = fragile — không có buffer, bất kỳ biến động nào cũng gây negative
  - 1.3-1.5 = healthy — có buffer cho vacancy/chi phí phát sinh
  - \> 1.5 = strong — chịu được stress test
- **Minimum cho nhà đầu tư dòng tiền:** DSCR >= 1.3
- **Stress test:** Tính DSCR khi lãi suất +2% và vacancy tăng gấp đôi. Vẫn >= 1.0?

### Loan-to-Value (LTV)

```
LTV = Loan Amount / Property Value
```

- **Interpretation:** Mức độ leverage — vay bao nhiêu % giá trị BĐS.
- **Thresholds (Vietnam):**
  - < 50% = conservative — rủi ro thấp
  - 50-60% = moderate
  - 60-70% = aggressive
  - \> 70% = **high leverage risk** — nếu giá giảm 30%, có thể underwater
- **Lưu ý VN:** Ngân hàng VN thường cho vay tối đa 70% giá trị BĐS, kỳ hạn 15-25 năm. Lãi suất ưu đãi 1-3 năm đầu, sau đó thả nổi (thường +3-4% so với lãi suất huy động).

### Vacancy Rate

```
Vacancy Rate = Vacant Months / 12
```

- **Interpretation:** Tỷ lệ thời gian BĐS không có người thuê trong năm.
- **Assumptions (Vietnam):**
  - Căn hộ nội thành: 1-1.5 tháng/năm (vacancy rate 8-12%)
  - Căn hộ vùng ven: 1.5-2 tháng/năm (12-17%)
  - Nhà trọ/phòng cho thuê: 1-2 tháng/năm (tùy khu vực)
  - BĐS du lịch (biển): 3-5 tháng/năm (seasonal)
  - Condotel: 4-6 tháng/năm (oversupply risk)
- **Rule:** Luôn dùng max(market average, 2 tháng/năm) để tính conservative.

### CapEx Reserve

```
CapEx Reserve = 1-2% × Property Value / Year
```

- **Interpretation:** Quỹ dự phòng cho sửa chữa lớn (thay máy lạnh, sơn lại, thay nội thất).
- **Thresholds (Vietnam):**
  - BĐS mới (< 5 năm): 1% giá trị/năm
  - BĐS cũ (5-15 năm): 1.5% giá trị/năm
  - BĐS cũ (> 15 năm): 2% giá trị/năm hoặc cao hơn
- **Lưu ý:** Nhiều nhà đầu tư VN BỎ QUA khoản này. Đây là sai lầm phổ biến khiến net yield thực tế thấp hơn nhiều so với dự tính.

### Break-even Occupancy

```
Break-even Occupancy = (Operating Expenses + Debt Service) / Gross Potential Rent
```

- **Interpretation:** Tỷ lệ lấp đầy tối thiểu để hòa vốn.
- **Thresholds:**
  - < 75% = an toàn — buffer lớn cho vacancy
  - 75-85% = theo dõi — margin mỏng
  - \> 85% = **risky** — gần như phải lấp đầy 100% mới hòa vốn
- **Dùng khi:** Đánh giá rủi ro BĐS cho thuê, đặc biệt BĐS du lịch/condotel.

---

## 4. Valuation & Investment Metrics

### Gross Rent Multiplier (GRM)

```
GRM = Property Price / Annual Gross Rent
```

- **Interpretation:** Bao nhiêu năm thuê để hoàn vốn (thô, chưa tính chi phí).
- **Thresholds (Vietnam):**
  - < 12 = attractive cho cash flow
  - 12-15 = fair
  - 15-20 = expensive cho cash flow, có thể OK nếu kỳ vọng lãi vốn
  - \> 20 = overvalued cho mục tiêu dòng tiền
- **Lưu ý:** GRM dùng gross rent, nên chỉ để sàng lọc nhanh. Luôn tính net metrics.

### Price-to-Rent Ratio

```
Price-to-Rent Ratio = Median Home Price / Median Annual Rent
```

- **Interpretation:** Nên mua hay thuê? So sánh chi phí sở hữu vs thuê.
- **Thresholds:**
  - < 15 = có lợi khi mua (ở)
  - 15-20 = neutral
  - \> 20 = overvalued — thuê có thể hợp lý hơn mua để ở
- **Dùng khi:** Tư vấn người mua nhà lần đầu (mua vs thuê).

### Net Present Value (NPV)

```
NPV = Σ [CFt / (1 + r)^t] - Initial Investment
```

- **CFt** = Cash flow tại năm t (bao gồm cả terminal value ở năm cuối)
- **r** = Discount rate (thường dùng WACC hoặc required rate of return)
- **Interpretation:**
  - NPV > 0 = đầu tư tạo giá trị (tốt)
  - NPV = 0 = hòa vốn theo required return
  - NPV < 0 = không đạt required return (xem xét lại)
- **Discount rate cho VN:** Thường 10-15% (risk-free rate ~5-6% + RE risk premium 5-9%)

### Internal Rate of Return (IRR)

```
IRR = rate r where NPV = 0
```

- **Interpretation:** Tỷ suất sinh lời nội bộ — rate of return thực sự của đầu tư.
- **Thresholds (Vietnam):**
  - < 8% = kém hơn alternatives an toàn
  - 8-12% = chấp nhận được
  - 12-18% = tốt
  - \> 18% = rất tốt — kiểm tra assumptions có realistic không
- **Lưu ý:** IRR nhạy cảm với terminal value (giá bán cuối kỳ). Luôn chạy sensitivity analysis trên growth rate.

### Break-even Horizon (Mua vs Thuê)

```
Break-even Horizon = Transaction Costs / (Monthly Ownership Cost - Monthly Rent)
```

- **Transaction Costs** = Thuế, phí công chứng, phí môi giới, phí sang tên (~2-5% giá BĐS tại VN)
- **Interpretation:** Bao nhiêu tháng thì mua sẽ rẻ hơn thuê (hoặc ngược lại).
- **Dùng khi:** Tư vấn mua vs thuê cho người mua nhà lần đầu.
- **Lưu ý:** Nếu horizon > 5 năm và user không chắc ở lâu, thuê có thể tốt hơn.

---

## 5. CASHFLOW-VERIFICATION — Vietnam OPEX Reality Check

> **Bắt buộc** chạy checklist này khi phân tích BĐS cho nhà đầu tư dòng tiền. Mục đích: đảm bảo không bỏ sót chi phí ẩn khiến cash flow dự tính sai lệch.

### 5.1 OPEX Items Checklist

| # | Khoản chi phí | Phạm vi VN (typical) | Cách tính | Ghi chú |
|---|--------------|----------------------|-----------|---------|
| 1 | **Phí quản lý tòa nhà** | 5,000-15,000 VND/m2/tháng | Diện tích × đơn giá × 12 | Cao hơn ở chung cư cao cấp, thấp hơn ở nhà trọ tự quản |
| 2 | **Phí dịch vụ** (condotel/serviced apt) | 80,000-200,000 VND/m2/tháng | Diện tích × đơn giá × 12 | Chỉ áp dụng nếu condotel/serviced apartment |
| 3 | **Thuế cho thuê** | 10% gross rent (5% VAT + 5% TNCN) hoặc 7% (khoán cá nhân) | Gross rent × tax rate × 12 | Cá nhân cho thuê dưới 100tr/năm: miễn VAT, chỉ 5% TNCN |
| 4 | **Chi phí bảo trì** | 1-2% giá trị BĐS/năm | Property value × 1-2% | BĐS mới: 1%, cũ: 1.5-2%. Nhiều NĐT bỏ qua khoản này |
| 5 | **Khấu hao nội thất** (furnished) | 150-300tr / 5-7 năm | Giá nội thất / 60-84 tháng | Chỉ nếu cho thuê furnished. Nội thất giảm giá trị nhanh |
| 6 | **Commission môi giới cho thuê** | 1 tháng tiền thuê/năm | Gross rent × 1 tháng / 12 | Mỗi lần tìm khách mới. Giảm nếu tự quản lý |
| 7 | **Vacancy allowance** | 1.5-2 tháng/năm | Gross rent × (vacancy months / 12) | Luôn dùng max(market average, 2 tháng/năm) |
| 8 | **CapEx reserve** | 1-2% giá trị BĐS/năm | Property value × 1-2% / 12 | Sửa chữa lớn: máy lạnh, nội thất, sơn, chống thấm |
| 9 | **Bảo hiểm** (tùy chọn) | 0.1-0.3% giá trị BĐS/năm | Property value × rate | Ít phổ biến ở VN nhưng nên có cho BĐS lớn |
| 10 | **Chi phí quản lý từ xa** (nếu có) | 8-15% gross rent | Gross rent × rate | Nếu thuê bên thứ 3 quản lý (property management) |

### 5.2 Verification Process

1. **List tất cả OPEX items** — chạy qua bảng trên, đánh dấu khoản nào áp dụng
2. **Dùng giá thuê MEDIAN, không MAX** — lấy từ comparable rentals, không phải giá rao
3. **Stress test:**
   - Lãi suất tăng +2-3%: debt service tăng bao nhiêu? Vẫn positive cash flow?
   - Vacancy tăng gấp đôi: cash flow còn positive không?
   - Giá thuê giảm 15%: DSCR còn >= 1.0 không?
4. **So sánh với alternatives:**
   - Net yield vs lãi suất tiết kiệm ngân hàng (5-6%)
   - CoC return vs cổ phiếu cổ tức (~7-10%)
   - Có xứng đáng effort quản lý không?
5. **Red flags:**
   - DSCR < 1.0 = negative cash flow, không phù hợp mục tiêu dòng tiền
   - Break-even occupancy > 85% = quá rủi ro
   - OER > 40% = chi phí vận hành quá cao
   - Net yield < bank deposit rate = effort quản lý không xứng đáng

### 5.3 Pro-forma Cash Flow Template (10 năm)

```
Năm 1:
  Gross Rent:                  [A] = Monthly rent × 12
  - Vacancy:                   [B] = A × vacancy rate
  = Effective Gross Income:    [C] = A - B
  - Operating Expenses:        [D] = Tổng OPEX từ bảng trên
  = NOI:                       [E] = C - D
  - Debt Service:              [F] = (Gốc + Lãi) × 12
  = Pre-tax Cash Flow:         [G] = E - F
  - CapEx Reserve:             [H] = Property value × 1-2%
  = Net Cash Flow:             [I] = G - H

Năm 2-10:
  Rental growth: +3-5%/năm (conservative cho VN)
  OPEX growth: +5-7%/năm (inflation VN)
  Debt service: fixed hoặc thả nổi (tính cả 2 scenario)
  Terminal value: Property value × (1 + appreciation)^n

Key outputs:
  - Monthly Cash Flow mỗi năm
  - Cumulative Cash Flow
  - Cash-on-Cash Return mỗi năm
  - DSCR mỗi năm
  - 10-year IRR (bao gồm terminal value)
  - NPV tại discount rate 10-12%
```

### 5.4 Quick Sanity Checks

- **"Giá thuê 13tr/tháng" → thực tế bao nhiêu?** Giá rao thường cao hơn giá thực 10-20%. Dùng median comparable, không max.
- **"Phí quản lý thấp lắm"** → kiểm tra phí quản lý tòa nhà thực tế. Chung cư cao cấp có thể 12,000-18,000 VND/m2.
- **"Không cần CapEx"** → mọi BĐS đều cần CapEx. Máy lạnh hỏng, chống thấm, sơn lại — trung bình 1-2% giá trị/năm.
- **"Vacancy 0"** → không thực tế. Luôn tính ít nhất 1.5 tháng/năm.
- **"Lãi suất ưu đãi 7%"** → chỉ 1-3 năm đầu. Sau đó thả nổi, thường 9-12%. Tính pro-forma với lãi suất post-ưu đãi.

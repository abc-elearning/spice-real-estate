# Decision Card Template

> Template chuẩn cho output quyết định BĐS. Tất cả nội dung bằng tiếng Việt. Điền đầy đủ mọi section — KHÔNG được bỏ trống.

---

```markdown
## 📋 Decision Card: [Tên quyết định]

**Ngày:** [YYYY-MM-DD]  |  **Confidence:** [Low/Medium/High] ([X]%)

---

### Tình huống

[1-2 câu tóm tắt quyết định cần ra: mua/bán/giữ/cho thuê cái gì, ở đâu, với ngân sách/giá bao nhiêu, mục đích gì]

---

### Phân tích theo framework

- **Framework được dùng:** [Tên framework — VD: Bayesian Update, Expected Value, DCF, Regret Minimization, Pre-mortem, Taleb Barbell]
- **Lý do chọn framework này:** [1 câu — tại sao framework này phù hợp với tình huống]
- **Kết quả chính:**
  - [Finding 1 — kết quả quan trọng nhất]
  - [Finding 2]
  - [Finding 3]

---

### Cảnh báo Bias

| Bias phát hiện | Mức ảnh hưởng | Cách giảm thiểu |
|----------------|---------------|-----------------|
| [VD: Anchoring — bám vào giá rao ban đầu] | [Cao/Trung bình/Thấp] | [VD: So sánh với 5+ comparable giao dịch thực] |
| [VD: Confirmation bias — chỉ tìm info ủng hộ mua] | [Cao/Trung bình/Thấp] | [VD: Yêu cầu Contrarian persona steelman case không mua] |
| [VD: Sunk cost — đã tốn thời gian tìm hiểu nên muốn mua cho xong] | [Cao/Trung bình/Thấp] | [VD: Đánh giá deal như thể mới thấy lần đầu] |

---

### Kịch bản (Scenarios)

| Kịch bản | Xác suất | ROI (5 năm) | NPV | Mô tả ngắn |
|-----------|----------|-------------|-----|-------------|
| Bi quan (P10) | [X]% | [X]% | [X VNĐ] | [1 câu — worst case hợp lý] |
| Cơ sở (P50) | [X]% | [X]% | [X VNĐ] | [1 câu — most likely case] |
| Lạc quan (P90) | [X]% | [X]% | [X VNĐ] | [1 câu — best case hợp lý] |

**Biến số nhạy cảm nhất:** [VD: lãi suất vay (+2% → ROI giảm X%), giá thuê (-15% → cash flow âm), vacancy rate]

---

### Tóm tắt Tranh luận

| Persona | Quan điểm | Lập luận chính |
|---------|-----------|----------------|
| Nhà đầu tư kỳ cựu | [Mua/Bán/Giữ] | [1 câu — góc nhìn ROI, timing, comparable] |
| Nhà đầu tư dòng tiền | [Mua/Bán/Giữ] | [1 câu — góc nhìn cash flow, DSCR, net yield] |
| Chuyên gia rủi ro | [Mua/Bán/Giữ] | [1 câu — góc nhìn downside, stress test, liquidity] |
| Người dùng cuối | [Mua/Bán/Giữ] | [1 câu — góc nhìn livability, personal fit] |
| Người phản biện | [Quan điểm ngược] | [1 câu — challenge assumption mạnh nhất] |

**Tensions chính:**
- [Tension 1 — VD: Veteran vs Risk Analyst về leverage level]
- [Tension 2 — VD: Cash Flow vs End User về loại BĐS]

**Tensions reveal:** [1-2 câu — tranh luận cho thấy điều gì về ưu tiên thực sự và rủi ro bị bỏ qua]

---

### Đề xuất

Phân tích cho thấy [tóm tắt kết luận — KHÔNG BAO GIỜ nói "nên mua" hoặc "nên bán" tuyệt đối]. Confidence: [X]%.

[Nếu confidence < 40%: "Độ tin cậy thấp — khuyến nghị thu thập thêm thông tin: [liệt kê cụ thể thông tin cần bổ sung]"]

[Nếu confidence 40-70%: "Độ tin cậy trung bình — phân tích nghiêng về [hướng] nhưng [yếu tố chưa chắc chắn]"]

[Nếu confidence > 70%: "Độ tin cậy cao — các indicators đồng thuận [hướng], rủi ro chính còn lại là [X]"]

---

### Bước tiếp theo

1. **[Action cụ thể]** — [timeline, VD: trong 1 tuần]
2. **[Action cụ thể]** — [timeline, VD: trong 2 tuần]
3. **[Action cụ thể]** — [timeline, VD: trong 1 tháng]

---

### ⚠️ Lưu ý quan trọng

Đây là phân tích hỗ trợ quyết định dựa trên dữ liệu và frameworks khoa học, **không phải tư vấn đầu tư hoặc tư vấn tài chính**. Mọi quyết định mua bán bất động sản cuối cùng thuộc về người dùng. Khuyến nghị tham vấn chuyên gia tài chính và pháp lý trước khi thực hiện giao dịch. Dữ liệu thị trường có thể không phản ánh đầy đủ điều kiện thực tế tại thời điểm quyết định.
```

---

## Hướng dẫn sử dụng

### Confidence scoring

| Level | % | Khi nào |
|-------|---|---------|
| Low | <40% | Thiếu data quan trọng, personas bất đồng sâu sắc, assumptions chưa verify |
| Medium | 40-70% | Data đủ nhưng có uncertainty lớn, 3-4 personas đồng thuận |
| High | >70% | Data đầy đủ, stress test pass, đa số personas đồng thuận, risks đã identify |

### Nguyên tắc viết Đề xuất

- LUÔN frame là "phân tích cho thấy..." — không bao giờ "bạn nên..."
- LUÔN kèm confidence % cụ thể
- LUÔN nêu rủi ro chính còn lại
- Nếu confidence < 40%, ưu tiên khuyến nghị thu thập thêm thông tin thay vì đưa kết luận

### Nguyên tắc viết Kịch bản

- P10 = 10th percentile (chỉ 10% khả năng tệ hơn) — worst case HỢP LÝ, không phải apocalypse
- P50 = median — trường hợp most likely
- P90 = 90th percentile (chỉ 10% khả năng tốt hơn) — best case HỢP LÝ, không phải lottery
- Tổng xác suất 3 kịch bản phải = 100% (thường: P10 20-30%, P50 40-60%, P90 20-30%)

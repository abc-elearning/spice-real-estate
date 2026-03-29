# BIASES.md — RE Cognitive Bias Detection Reference

> Level 3 resource. Loaded on demand during Analysis step (analyzing-re-biases) of the cognitive loop.
> Detection method: Scan user input for Vietnamese linguistic markers, flag potential biases, present reframed perspective.

---

## 1. Anchoring (Neo giá) — Severity: HIGH

**Mô tả:** Neo quyết định vào một con số tham chiếu (giá mua ban đầu, giá rao, giá hàng xóm) thay vì đánh giá theo giá trị thị trường hiện tại. Trong BĐS, anchoring đặc biệt mạnh vì giá mua thường gắn với ký ức và cảm xúc.

**Ví dụ VN:** "Đất tôi mua 2 tỷ, giờ rao 3 tỷ nhưng thị trường chỉ trả 2.5 tỷ" — người bán neo vào giá rao 3 tỷ, từ chối bán 2.5 tỷ dù đó là giá thị trường hợp lý.

**Detection markers (>=4):**
- "tôi mua giá..." / "giá gốc là..." / "hồi đó mua..."
- "rao giá..." / "giá rao là..." / "đăng bán..."
- "nhà bên cạnh bán được..." / "hàng xóm bán..."
- "giá đất khu này phải..." / "giá hợp lý phải là..."
- "không thể bán dưới..." / "ít nhất phải được..."

**Reframed question:**
> "Nếu bạn KHÔNG sở hữu BĐS này và có số tiền tương đương, bạn có mua nó ở giá hiện tại không? Giá bạn đã mua không còn liên quan — thị trường không quan tâm bạn mua giá nào."

---

## 2. Loss Aversion (Sợ lỗ) — Severity: HIGH

**Mô tả:** Nỗi đau mất mát lớn gấp 2-2.5 lần niềm vui từ lợi nhuận tương đương (Prospect Theory, Kahneman & Tversky 1979). Trong BĐS: không chịu bán lỗ dù fundamentals đã thay đổi, giữ BĐS lỗ ngày càng sâu.

**Ví dụ VN:** Giữ đất vùng ven đã mất quy hoạch đường lớn, giá giảm 40% so với peak. Không cut loss vì "bán là chấp nhận mất tiền". Trong khi tiền đó có thể chuyển sang BĐS khác sinh lời.

**Detection markers (>=4):**
- "bán lỗ thì..." / "không thể bán lỗ" / "lỗ nặng quá"
- "chờ giá lên rồi bán" / "chờ phục hồi" / "thị trường sẽ quay lại"
- "giữ thêm vài năm" / "chờ quy hoạch" / "để đó không mất gì"
- "đã lỡ rồi" / "bán giờ thì uổng" / "mất trắng"
- "tiền đã bỏ ra rồi" / "không lẽ bỏ"

**Reframed question:**
> "Giả sử bạn KHÔNG sở hữu BĐS này và có số tiền bằng giá trị hiện tại của nó. Bạn có dùng tiền đó mua chính BĐS này không? Nếu không, bạn đang giữ nó chỉ vì sợ chấp nhận lỗ — đó là loss aversion."

---

## 3. Sunk Cost (Chi phí chìm) — Severity: MEDIUM

**Mô tả:** Ra quyết định dựa trên tiền/công sức đã bỏ ra (không thể thu hồi) thay vì triển vọng tương lai. Trong BĐS: "đã bỏ 500 triệu renovate nên phải bán ít nhất X".

**Ví dụ VN:** Đã đổ 500 triệu sửa chữa căn nhà cũ, giờ thị trường chỉ trả thêm 200 triệu so với giá chưa sửa. Từ chối bán vì "phải thu hồi tiền sửa chữa". 300 triệu kia đã mất — quyết định nên dựa trên giá trị hiện tại.

**Detection markers:**
- "đã bỏ ra..." / "đã đầu tư vào..." / "tốn ... sửa chữa rồi"
- "phải bán ít nhất..." / "phải thu hồi..." / "phải lấy lại vốn"
- "đã renovate / sửa / nâng cấp rồi"

**Reframed question:**
> "Tiền đã bỏ ra sửa chữa không thể lấy lại — đó là sunk cost. Câu hỏi đúng là: với giá thị trường HIỆN TẠI, giữ hay bán có lợi hơn cho 5 năm tới? Tiền sửa chữa đã mất bất kể bạn bán hay giữ."

---

## 4. Herding (Tâm lý bầy đàn) — Severity: HIGH

**Mô tả:** Mua/bán theo đám đông thay vì phân tích độc lập. FOMO (Fear Of Missing Out) khi thị trường nóng. Trong BĐS VN, herding đặc biệt mạnh khi "sốt đất" — mọi người đổ xô mua đất nền vùng ven.

**Ví dụ VN:** Sốt đất nền vùng ven — "anh Tư mua lời 30%, chị Ba cũng mua, ai cũng mua" → FOMO mua đất nền không có pháp lý rõ ràng, khi sốt hạ mất 50% giá trị.

**Detection markers (>=4):**
- "mọi người đang mua..." / "ai cũng mua" / "nhiều người đã mua"
- "sốt đất" / "thị trường đang nóng" / "không mua bây giờ thì trễ"
- "anh/chị/bạn tôi mua lời..." / "người quen mới mua..."
- "khu này đang lên" / "sắp có dự án lớn" / "nghe nói sắp có..."
- "nếu không mua giờ thì..." / "cơ hội cuối" / "sắp hết hàng"

**Reframed question:**
> "Nếu KHÔNG AI KHÁC đang mua khu vực này, bạn vẫn mua chứ? Phân tích fundamentals: quy hoạch có chính thức không? Pháp lý rõ ràng không? Giá so với comparable có hợp lý không? Đám đông thường đúng ở giữa trend nhưng sai ở đỉnh."

---

## 5. Overconfidence (Quá tự tin) — Severity: MEDIUM

**Mô tả:** Đánh giá quá cao khả năng phán đoán của bản thân, đặc biệt sau vài lần thành công. Trong BĐS: "tôi đầu tư 10 năm, chưa bao giờ sai" — bỏ qua yếu tố may mắn và thị trường thuận lợi.

**Ví dụ VN:** Nhà đầu tư mua đất vùng ven 2015-2019 lời lớn nhờ sóng tăng chung, kết luận "mình giỏi chọn đất". Bỏ qua fact: giai đoạn đó hầu hết đất đều tăng. Năm 2022-2023 mua tiếp theo cùng strategy, lỗ nặng.

**Detection markers:**
- "tôi đầu tư ... năm rồi" / "kinh nghiệm ... năm"
- "chưa bao giờ sai" / "lần nào cũng lời" / "tôi biết khu này"
- "không cần phân tích" / "tin tôi đi" / "tôi rành lắm"

**Reframed question:**
> "Trong những lần bạn lời, bao nhiêu % là do chọn đúng BĐS, bao nhiêu % là do thị trường lên chung? Nếu thay BĐS bạn mua bằng bất kỳ BĐS nào cùng khu vực, kết quả có khác không? Hãy tách skill khỏi luck."

---

## 6. Familiarity (Thiên kiến quen thuộc) — Severity: MEDIUM

**Mô tả:** Ưu tiên BĐS gần nhà, khu vực quen thuộc, hoặc loại BĐS đã mua trước — bỏ qua cơ hội tốt hơn ở khu vực không biết. Home bias trong đầu tư BĐS.

**Ví dụ VN:** Sống ở Quận 7, chỉ tìm mua BĐS Quận 7 dù yield khu vực này chỉ 3%. Bỏ qua nhà trọ Thủ Đức yield 7% vì "không biết khu đó".

**Detection markers:**
- "tôi chỉ mua khu..." / "tôi quen khu này"
- "khu khác tôi không biết" / "không rành khu đó"
- "gần nhà tôi" / "tôi ở đây lâu rồi" / "khu này tôi hiểu"

**Reframed question:**
> "Nếu mục tiêu là tối ưu yield/ROI, bạn có nên giới hạn chỉ ở khu vực quen không? Research khu vực mới mất 2-3 tuần. Cơ hội bỏ lỡ có thể là hàng trăm triệu. Hãy để data dẫn đường, không phải comfort zone."

---

## 7. Confirmation Bias (Thiên kiến xác nhận) — Severity: MEDIUM

**Mô tả:** Chỉ tìm kiếm thông tin ủng hộ quyết định đã có trong đầu, bỏ qua hoặc discount thông tin ngược lại. Trong BĐS: Google "tại sao nên mua đất X" thay vì "rủi ro đất X".

**Ví dụ VN:** Đã quyết định mua căn hộ tại dự án Y, chỉ đọc review tốt trên Facebook group developer, bỏ qua complaint về chậm tiến độ, chất lượng xây dựng kém trên các forum độc lập.

**Detection markers:**
- "tôi đã tìm hiểu kỹ rồi" / "đọc nhiều rồi"
- "ai cũng nói tốt" / "review tốt lắm" / "mọi người khen"
- "chỉ có vài người chê" / "người chê là không hiểu"

**Reframed question:**
> "Bạn đã chủ động tìm kiếm LÝ DO KHÔNG NÊN mua BĐS này chưa? Hãy dành 30 phút search '[tên dự án] vấn đề', '[khu vực] rủi ro', '[developer] khiếu nại'. Nếu sau đó vẫn muốn mua, quyết định sẽ chắc chắn hơn."

---

## 8. Recency Bias (Thiên kiến gần đây) — Severity: MEDIUM

**Mô tả:** Đặt trọng số quá lớn vào xu hướng giá gần nhất, extrapolate ngắn hạn thành dài hạn. Trong BĐS: "3 tháng qua tăng 20%, sẽ tiếp tục tăng".

**Ví dụ VN:** BĐS Quận 9 (TP. Thủ Đức) tăng 30% trong 6 tháng cuối 2020 nhờ announcement metro. Nhiều người mua vào đỉnh, kỳ vọng tăng tiếp. Thực tế: giá đi ngang hoặc giảm 2-3 năm sau.

**Detection markers:**
- "mấy tháng qua tăng..." / "vừa rồi tăng..." / "gần đây lên giá"
- "xu hướng đang lên" / "đang tăng nhanh" / "tăng chưa dừng"
- "sẽ tiếp tục tăng" / "còn tăng nữa" / "đà tăng mạnh"

**Reframed question:**
> "Xu hướng 3-6 tháng gần đây có phản ánh giá trị dài hạn không? Hãy xem giá 5-10 năm. BĐS có chu kỳ: tăng nhanh thường theo sau bằng đi ngang hoặc giảm. Bạn đang mua ở đâu trong chu kỳ?"

---

## 9. Status Quo Bias (Thiên kiến hiện trạng) — Severity: LOW

**Mô tả:** Xu hướng không hành động, giữ nguyên hiện trạng dù data cho thấy nên mua hoặc bán. "Để đó, chờ thêm" khi đã có đủ thông tin. Inaction cũng là một quyết định — và có thể là quyết định tồi.

**Ví dụ VN:** Phân tích cho thấy nên bán BĐS A để chuyển sang BĐS B yield cao hơn. Nhưng ngại thủ tục, ngại thay đổi, ngại "nếu bán xong giá lên thì sao" → không làm gì. 3 năm sau, BĐS A tiếp tục giảm, BĐS B tăng 40%.

**Detection markers:**
- "để đó đã" / "chờ thêm" / "chưa vội" / "từ từ"
- "thủ tục phức tạp lắm" / "ngại bán" / "phiền phức"
- "lỡ bán xong giá lên thì sao" / "chờ xem thêm"

**Reframed question:**
> "Không hành động cũng là một quyết định — bạn đang chọn giữ nguyên. Chi phí cơ hội của việc KHÔNG hành động là bao nhiêu? Nếu giữ thêm 3 năm, expected return là bao nhiêu so với alternatives?"

---

## 10. Endowment Effect (Hiệu ứng sở hữu) — Severity: MEDIUM

**Mô tả:** Định giá BĐS mình sở hữu cao hơn giá thị trường — chỉ vì mình sở hữu nó. "Nhà tôi view đẹp, phải hơn thị trường 30%." Buyer không trả premium cho giá trị cảm xúc của bạn.

**Ví dụ VN:** Chủ căn hộ view sông định giá cao hơn 30% so với các căn cùng tầng cùng dự án vì "view nhà tôi đẹp hơn nhiều". Thực tế: premium cho view sông tại VN thường chỉ 5-10%.

**Detection markers:**
- "nhà tôi đặc biệt" / "căn này khác" / "không giống mấy căn khác"
- "view đẹp" / "vị trí đắc địa" / "nội thất xịn"
- "giá này rẻ lắm rồi" / "người khác bán đắt hơn"

**Reframed question:**
> "Nếu bạn là NGƯỜI MUA đang xem căn này, bạn có trả giá bạn đang rao không? Hãy so sánh khách quan với 5-10 comparable cùng khu vực. Premium mà bạn cảm nhận (view, nội thất) thị trường định giá bao nhiêu?"

---

## 11. Framing Effect (Hiệu ứng khung) — Severity: LOW

**Mô tả:** Cách đặt vấn đề (frame) thay đổi quyết định dù nội dung giống nhau. "Mất 500 triệu" vs "tiết kiệm 1 tỷ so với peak" — cùng một con số nhưng tạo cảm xúc khác nhau.

**Ví dụ VN:** Môi giới frame: "Chị tiết kiệm được 800 triệu so với giá peak 2022!" thay vì "Giá hiện tại vẫn cao hơn giá 2019 là 500 triệu." Cùng BĐS, cùng giá, nhưng frame khác tạo cảm giác khác.

**Detection markers:**
- "tiết kiệm được..." / "rẻ hơn ... so với..."
- "giảm từ ... xuống" / "so với peak" / "so với giá cũ"
- "chỉ mất..." / "chỉ tốn thêm..." / "chỉ chênh..."

**Reframed question:**
> "Bỏ qua mọi so sánh với giá quá khứ. Chỉ nhìn giá HIỆN TẠI: BĐS này có đáng giá X tỷ dựa trên comparable hiện tại, yield hiện tại, và fundamentals hiện tại không?"

---

## 12. Disposition Effect (Hiệu ứng bán sớm/giữ lỗ) — Severity: HIGH

**Mô tả:** Bán BĐS đang lời quá sớm (chốt lời nhanh) và giữ BĐS đang lỗ quá lâu (không chịu cut loss). Ngược với logic: nên giữ winner nếu fundamentals tốt, và bán loser nếu fundamentals xấu.

**Ví dụ VN:** Bán căn hộ Quận 2 lời 30% ngay khi có lời, trong khi khu vực này tiếp tục tăng 100% trong 5 năm sau. Đồng thời giữ đất nền Long An lỗ 40%, hy vọng "quay lại giá cũ", trong khi tiền đó có thể đầu tư chỗ khác.

**Detection markers (>=4):**
- "lời rồi, bán chốt lời thôi" / "lời 30% là được rồi" / "chốt lời đi"
- "giữ chờ giá quay lại" / "chờ về giá cũ" / "lỗ thì không bán"
- "bán lời trước đã" / "cầm tiền cho chắc"
- "đang lỗ thì giữ" / "giữ lâu sẽ lên" / "thời gian sẽ giải quyết"
- "bán cái đang lời, giữ cái đang lỗ"

**Reframed question:**
> "Đánh giá từng BĐS INDEPENDENT: fundamentals có tốt không? Khu vực có tiếp tục tăng không? Đừng quyết định bán/giữ dựa trên bạn đang lời hay lỗ — mà dựa trên TRIỂN VỌNG TƯƠNG LAI. Nếu BĐS đang lời vẫn có fundamentals tốt, giữ. Nếu BĐS đang lỗ có fundamentals xấu, cắt lỗ."

---

## Quick Reference: Severity & Priority

| # | Bias | Severity | Markers |
|---|------|----------|---------|
| 1 | Anchoring | HIGH | 5 |
| 2 | Loss Aversion | HIGH | 5 |
| 3 | Sunk Cost | MEDIUM | 3 |
| 4 | Herding | HIGH | 5 |
| 5 | Overconfidence | MEDIUM | 3 |
| 6 | Familiarity | MEDIUM | 3 |
| 7 | Confirmation | MEDIUM | 3 |
| 8 | Recency | MEDIUM | 3 |
| 9 | Status Quo | LOW | 3 |
| 10 | Endowment Effect | MEDIUM | 3 |
| 11 | Framing | LOW | 3 |
| 12 | Disposition Effect | HIGH | 5 |

**Priority biases** (4+ markers, HIGH severity): Anchoring, Loss Aversion, Herding, Disposition Effect — these cause the largest financial damage in RE decisions.

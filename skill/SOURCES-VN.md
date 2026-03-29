# Vietnam Real Estate Data Sources

> Nguồn dữ liệu thị trường BĐS Việt Nam cho web_search và web_fetch. Sử dụng khi cần thu thập market data, comparable, macro indicators.

---

## Bảng nguồn dữ liệu

| # | Category | Source | URL | Data type | Access |
|---|----------|--------|-----|-----------|--------|
| 1 | Listing & comps | batdongsan.com.vn | batdongsan.com.vn | Giá rao, volume giao dịch, phân khúc, cho thuê | web_search |
| 2 | Listing & comps | cafeland.vn | cafeland.vn | Market analysis, giá theo khu vực, xu hướng | web_search |
| 3 | Listing & comps | alonhadat.com.vn | alonhadat.com.vn | Giá thực tế (C2C listings), ít markup môi giới | web_search |
| 4 | Listing & comps | nhadat24h.net | nhadat24h.net | Listings vùng ven, đất nền, tỉnh lẻ | web_search |
| 5 | Rental market | batdongsan.com.vn/cho-thue | batdongsan.com.vn/cho-thue | Rental listings, giá cho thuê theo khu vực | web_search |
| 6 | Rental market | Airbnb, Booking.com | airbnb.com, booking.com | Short-term rental yield, occupancy, seasonal | web_search |
| 7 | Macro — lãi suất | Ngân hàng Nhà nước (SBV) | sbv.gov.vn | Lãi suất điều hành, tín dụng BĐS, chính sách tiền tệ | web_fetch |
| 8 | Macro — kinh tế | Tổng cục Thống kê (GSO) | gso.gov.vn | CPI, GDP, dân số, nhập cư, thu nhập bình quân | web_fetch |
| 9 | Quy hoạch | Sở Xây dựng / Sở TN&MT tỉnh | (varies by province) | Quy hoạch 1/500, pháp lý đất đai, dự án hạ tầng | web_search |
| 10 | Market reports | CBRE Vietnam | cbre.com.vn | Quarterly market overview, giá thuê văn phòng/retail | web_search |
| 11 | Market reports | Savills Vietnam | savills.com.vn | Market pulse, pricing index, phân khúc cao cấp | web_search |
| 12 | Market reports | JLL Vietnam | jll.com.vn | Research & trends, industrial/logistics | web_search |
| 13 | Market reports | Vietnam Report | vietnamreport.net | Top 10 BĐS uy tín, xếp hạng chủ đầu tư | web_search |
| 14 | News & analysis | CafeF | cafef.vn | Tin tức tài chính, phân tích thị trường BĐS | web_search |
| 15 | News & analysis | VnExpress BĐS | vnexpress.net/bat-dong-san | Tin tức thị trường, chính sách, dự án mới | web_search |
| 16 | FDI & industry | Bộ KH&ĐT, VCCI | mpi.gov.vn, vcci.com.vn | FDI theo tỉnh, KCN mới, đầu tư nước ngoài | web_search |

---

## Web Search Query Patterns

Các mẫu query chuẩn cho Claude web_search tool. Thay `[biến]` bằng giá trị cụ thể.

### Comparable — Tìm giá giao dịch

```
"giá [loại BĐS] [khu vực] [năm hiện tại]"
"[khu vực] giao dịch thực tế [năm]"
"[dự án cụ thể] review [năm]"
"giá m2 [khu vực] [quý/năm]"
"[loại BĐS] [khu vực] mở bán giá bao nhiêu"
```

**Ví dụ:**
- `"giá căn hộ Thủ Đức 2026"`
- `"Vinhomes Grand Park giao dịch thực tế 2026"`
- `"giá m2 đất Hòa Xuân Đà Nẵng quý 1 2026"`

### Rental — Tìm giá cho thuê

```
"cho thuê [loại BĐS] [khu vực] giá"
"rental yield [khu vực] [năm]"
"[dự án] cho thuê bao nhiêu [tháng/năm]"
"giá cho thuê [loại BĐS] [khu vực] tháng"
"occupancy rate [khu vực] [năm]"
```

**Ví dụ:**
- `"cho thuê căn hộ 2 phòng ngủ Quận 2 giá 2026"`
- `"rental yield căn hộ Đà Nẵng 2026"`
- `"Vinhomes Ocean Park cho thuê bao nhiêu tháng"`

### Macro — Lãi suất & tín dụng

```
"lãi suất cho vay BĐS [năm]"
"lãi suất ngân hàng mua nhà [năm]"
"tăng trưởng tín dụng BĐS [năm]"
"chính sách tín dụng BĐS ngân hàng nhà nước [năm]"
"CPI Việt Nam [tháng/năm]"
"GDP Việt Nam [quý/năm]"
```

**Ví dụ:**
- `"lãi suất cho vay mua nhà 2026 ngân hàng nào thấp nhất"`
- `"tăng trưởng tín dụng BĐS quý 1 2026"`
- `"CPI Việt Nam tháng 3 2026"`

### Infrastructure — Quy hoạch & hạ tầng

```
"quy hoạch [khu vực/quận] [năm]"
"hạ tầng giao thông [khu vực] mới"
"dự án [đường/cầu/metro] [thành phố] tiến độ"
"[khu vực] quy hoạch sử dụng đất"
"metro [thành phố] [tuyến] khi nào xong"
"cao tốc [tên] tiến độ [năm]"
```

**Ví dụ:**
- `"quy hoạch Thủ Đức 2026 dự án hạ tầng"`
- `"metro TP HCM tuyến 1 tiến độ 2026"`
- `"cao tốc Biên Hòa Vũng Tàu tiến độ 2026"`

### Legal — Pháp lý

```
"quy hoạch sử dụng đất [khu vực]"
"[khu vực] đất thổ cư hay nông nghiệp"
"tranh chấp [dự án/khu vực]"
"[chủ đầu tư] pháp lý dự án [năm]"
"sổ đỏ [dự án] đã cấp chưa"
```

### Supply — Nguồn cung

```
"dự án mới [khu vực] [năm]"
"nguồn cung căn hộ [thành phố] [năm]"
"mở bán [khu vực] [năm]"
"tồn kho BĐS [thành phố] [năm]"
"absorption rate [khu vực]"
```

### Population & Demand

```
"dân số [thành phố/quận] tăng trưởng"
"nhập cư [khu vực] [năm]"
"FDI [tỉnh] [năm]"
"KCN mới [tỉnh] [năm]"
"du lịch [thành phố] lượt khách [năm]"
```

### Cash Flow Verification

```
"chi phí quản lý [dự án] tháng"
"phí dịch vụ [dự án/khu vực] /tháng"
"thuế cho thuê BĐS Việt Nam [năm]"
"phí bảo trì chung cư [dự án]"
```

---

## Macro Indicators — Bảng diễn giải

| Indicator | Signal Bullish (thuận lợi) | Signal Bearish (bất lợi) | Cách đọc |
|-----------|---------------------------|--------------------------|----------|
| Lãi suất cho vay BĐS | Giảm / thấp (<8%) | Tăng / cao (>12%) | Lãi suất thấp = chi phí vay rẻ = demand tăng. Lãi suất cao = gánh nặng trả nợ = demand giảm |
| Tăng trưởng tín dụng BĐS | 15-20% YoY (ổn định) | <5% (siết chặt) hoặc >25% (quá nóng, bong bóng) | Tín dụng tăng quá nhanh = rủi ro bong bóng. Tín dụng siết = thanh khoản khó |
| Tồn kho BĐS | Giảm (absorption tốt) | Tăng >20% (oversupply) | Tồn kho cao = áp lực giảm giá, bargaining power cho buyer |
| Giá/Thu nhập (Price-to-Income) | <25x thu nhập năm | >35x thu nhập năm | Ratio cao = BĐS quá đắt so với khả năng chi trả = rủi ro điều chỉnh |
| Rental yield (net) | >5% net | <3% net | Yield thấp = giá quá cao so với rental income hoặc chi phí quá lớn |
| Thanh khoản (Days on Market) | <60 ngày | >180 ngày | DOM cao = thị trường chậm, khó thoát hàng, cần haircut giá |
| GDP growth | >6% | <5% | GDP tăng = thu nhập tăng = demand BĐS tăng |
| CPI | 2-4% (ổn định) | >7% (lạm phát cao) | Lạm phát vừa = BĐS hedge tốt. Lạm phát quá cao = lãi suất sẽ tăng |
| FDI vào tỉnh | Tăng YoY, KCN mới | Giảm, doanh nghiệp rút | FDI = việc làm = demand nhà ở cho công nhân và expat |
| Dân số/nhập cư | Tăng >2%/năm | Giảm hoặc stagnant | Dân số tăng = demand tự nhiên. Đặc biệt quan trọng: Bình Dương, Long An, Đà Nẵng |

---

## Lưu ý khi sử dụng sources

1. **Giá rao ≠ giá giao dịch** — giá trên batdongsan.com.vn thường cao hơn 10-20% so với giá giao dịch thực. Luôn note discount này.
2. **Cross-reference tối thiểu 2 nguồn** — không dựa vào một nguồn duy nhất cho bất kỳ data point nào.
3. **Chú ý ngày publish** — data BĐS cũ hơn 6 tháng có thể không còn chính xác trong thị trường biến động.
4. **Market reports (CBRE, Savills, JLL)** — thường tập trung phân khúc trung-cao cấp và thành phố lớn. Không phản ánh đầy đủ thị trường tỉnh lẻ.
5. **SBV và GSO** — data chính thức nhưng thường chậm 1-2 quý. Bổ sung bằng news analysis cho data gần nhất.
6. **Rental data** — phân biệt gross yield (trước chi phí) và net yield (sau thuế, quản lý, vacancy, bảo trì). Luôn tính net.
7. **Quy hoạch** — thông tin quy hoạch có thể thay đổi. Check nguồn chính thức (Sở Xây dựng) và cross-reference với news.

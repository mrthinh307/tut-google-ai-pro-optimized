# TUT Google AI Pro Optimized

Bộ công cụ tự động hóa kiểm tra offer, đăng ký dùng thử **0 đồng** và **cộng dồn thời hạn gói Google AI Pro (5 TB)** thông qua Android Play Billing (tối ưu cho giả lập **MuMu Player** hoặc thiết bị Android đã root).

---

## 1. Công cụ này hoạt động như thế nào?

Nhiều ưu đãi dùng thử miễn phí của Google One (như `12months-eft`, `6months-eft`, `eft-3months`, …) không hiển thị trực tiếp trên giao diện web hay trong app, nhưng lại tồn tại trong dữ liệu trả về của thư viện **Google Play Billing (`BillingClient`)**.

Thay vì phải chỉnh sửa APK hay cài Xposed, `ultra0.py` hoạt động theo cơ chế **tiêm script runtime (Frida)**:

1. **Chuẩn bị môi trường thiết bị**: Kiểm tra quyền `root`, tắt animation hệ thống (giúp đọc UI nhanh), tắt proxy chặn mạng Play, đẩy `frida-server` và module `BillingClient` (`module_521.apk`) nhúng sẵn vào `/data/local/tmp/`.
2. **Đồng bộ ngữ cảnh tài khoản**: Xác định đúng email Google đang hoạt động trên thiết bị, dọn cache `sku_details.db` / `app_commerce_acquire_cache` và đồng bộ chủ sở hữu gói Google One trong `localappstate.db` của Play Store để tránh lỗi dính cache hoặc nhầm tài khoản.
3. **Đọc trạng thái gói hiện tại (khi cộng dồn `--stack`)**:
   - Đọc `purchaseToken` còn hiệu lực của đúng tài khoản từ `library.db` (hoặc lấy trực tiếp từ `queryPurchases` của Play Billing).
   - Nếu gói đang ở trạng thái **Đã hủy gia hạn (`autoRenewing = false`)**, script tự mở trang Subscriptions trên Play Store để thử bấm **Resubscribe / Đăng ký lại** trước khi cộng dồn.
4. **Mượn tiến trình Google One để gọi Play Billing**:
   - Inject JavaScript vào tiến trình `com.google.android.apps.subscriptions.red` (Google One) bằng **Frida 16.5.9**.
   - Dùng `DexClassLoader` nạp `module_521.apk`, khởi tạo `BillingClient`, truy vấn SKU (`queryProductDetails`) để lấy `offerToken` của gói miễn phí mục tiêu.
   - Khi chạy chế độ cộng dồn (`--stack`), script truyền `oldPurchaseToken` kèm `SubscriptionUpdateParams` với `prorationMode = 5` (`CHARGE_FULL_PRICE`) để **quy đổi và nối tiếp thời gian dùng thử còn lại** thay vì thay thế mất ngày cũ.
5. **Kiểm tra an toàn trước khi xác nhận thanh toán**:
   - Khi hộp thoại thanh toán Google Play hiện lên, script đọc giao diện qua `uiautomator`.
   - **Chỉ bấm `Subscribe / Đăng ký`** khi xác nhận là gói dùng thử miễn phí / giá `0` (và không phải gói 1 tháng thông thường).
   - Nếu xuất hiện hộp thoại `Error` hoặc thông báo không đủ điều kiện, script tự đóng hộp thoại, dọn cache và trả về mã lỗi (`exit code != 0`) để luồng tự động chuyển sang bước tiếp theo.
6. **Lưu báo cáo**: Kết quả từng lần chạy được lưu dưới dạng JSON trong thư mục `ultra0-report/`.

---

## 2. Cấu trúc thư mục

| File / Thư mục                  | Chức năng                                                                                                                 |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| `Cai_dat_moi_truong.bat`        | Cài đặt nhanh môi trường trên Windows (gọi `setup_env.py`)                                                                |
| `0_Kiem_tra_moi_truong.bat`     | Kiểm tra thiết bị Android/giả lập, root, `frida-server`, module Billing và Play Store                                     |
| `1_Xem_danh_sach_offer.bat`     | Liệt kê tất cả offer & token hiện có của tài khoản (chỉ đọc, không mở thanh toán)                                         |
| `2_Pro_12_thang_Buoc_1.bat`     | Bước 1: Đăng ký gói Pro 5TB **12 tháng** (`--plan pro12`)                                                                 |
| `3_Pro_Them_6_thang_Buoc_2.bat` | Bước 2: Cộng dồn thêm **6 tháng** (`--stack --plan pro6`)                                                                 |
| `4_Pro_Them_6_thang_Buoc_3.bat` | Bước 3: Cộng dồn thêm **6 tháng** nữa (`--stack --plan pro6b`)                                                            |
| `5_Pro_Du_phong_6_thang.bat`    | Dự phòng: Cộng dồn thêm **6 tháng** (`--stack --plan pro6c`)                                                              |
| `6_Pro_3_thang_eft.bat`         | Gói **3 tháng** (`--stack --plan pro3`)                                                                                   |
| `7_Auto_Chay_2_den_6.bat`       | Chạy tự động lần lượt từ file `2` đến `6`; gặp lỗi tự nhảy bước tiếp theo, xong lượt đầu sẽ random cho đến khi thành công |
| `ultra0.py`                     | Script lõi thực thi toàn bộ quy trình ADB, đồng bộ tài khoản, Frida inject và auto UI                                     |
| `setup_env.py`                  | Script kiểm tra Python, cài `frida==16.5.9`, tìm/tải `adb` và kết nối giả lập                                             |
| `query_sku.py`                  | Công cụ CLI tra cứu nhanh toàn bộ offer của bất kỳ SKU nào                                                                |
| `requirements.txt`              | Khai báo thư viện Python (`frida>=16.0`, khuyến nghị `16.5.9`)                                                            |
| `Huong_dan_su_dung.txt`         | Ghi chú hướng dẫn gốc kèm theo repo                                                                                       |
| `ultra0-report/`                | Thư mục lưu file JSON báo cáo kết quả theo từng tài khoản                                                                 |

---

## 3. Chuẩn bị trước khi chạy

### Trên máy tính (Windows)

- **Python 3.10 trở lên** (tối thiểu 3.9).
- **Frida phiên bản `16.5.9`** _(bắt buộc dùng nhánh `16.x`; bản `17.x` đã bỏ Java bridge nên không chạy được — `setup_env.py` sẽ tự hạ cấp giúp bạn)_.
- **ADB** (dùng sẵn ADB của MuMu Player, trong `PATH`, hoặc để `setup_env.py` tự tải `platform-tools`).

### Trên giả lập MuMu / điện thoại Android

1. Thiết bị đã bật **Root** và bật **Gỡ lỗi USB / ADB Debugging**.
2. Đã cài sẵn **Google Play Store** và **Google One** (`com.google.android.apps.subscriptions.red`).
3. Đã đăng nhập tài khoản Google cần dùng trên thiết bị.
4. Tài khoản đã gắn sẵn **phương thức thanh toán** (khuyến nghị dùng thẻ có hạn mức thấp để tránh bị trừ nhầm nếu quên hủy).
5. Play Store mở được bình thường (không bị chặn mạng/proxy).

---

## 4. Hướng dẫn sử dụng từng bước (cho người mới)

### Bước 1: Cài đặt môi trường một chạm

Bấm đúp file **`Cai_dat_moi_truong.bat`** (hoặc chạy `python setup_env.py`). Script sẽ tự động:

- Kiểm tra phiên bản Python.
- Cài `frida==16.5.9`.
- Tìm `adb.exe` (tự nhận diện thư mục cài MuMu hoặc tải `platform-tools` từ Google).
- Kết nối tới các cổng ADB phổ biến của giả lập (`16384`, `7555`, `16416`, `21503`, `62001`).
- Chạy `ultra0.py --check` để kiểm tra toàn bộ hệ thống.

### Bước 2: Kiểm tra môi trường & xem offer (không rủi ro)

1. Bấm đúp **`0_Kiem_tra_moi_truong.bat`** → Đảm bảo mọi mục kiểm tra đều báo đạt (`✅`).
2. Bấm đúp **`1_Xem_danh_sach_offer.bat`** → Liệt kê các offer khả dụng trên tài khoản đang đăng nhập mà **không mở trang thanh toán**.

### Bước 3: Mở gói & cộng dồn thời hạn

Bạn có thể chọn **chạy từng bước thủ công** hoặc **chạy tự động**:

#### Cách A — Chạy từng bước thủ công (khuyên dùng để hiểu rõ từng giai đoạn)

Chạy lần lượt theo thứ tự:

1. **`2_Pro_12_thang_Buoc_1.bat`** → Mở gói 12 tháng đầu tiên (`pro12`).
2. **`3_Pro_Them_6_thang_Buoc_2.bat`** → Cộng dồn thêm 6 tháng (`pro6`, tổng ~18 tháng).
3. **`4_Pro_Them_6_thang_Buoc_3.bat`** → Cộng dồn thêm 6 tháng (`pro6b`, tổng ~24 tháng).
4. **`5_Pro_Du_phong_6_thang.bat`** → Cộng dồn thêm 6 tháng dự phòng (`pro6c`).
5. **`6_Pro_3_thang_eft.bat`** → Thử thêm gói 3 tháng (`pro3`).

> **Cách nhận biết trang thanh toán cộng dồn ĐÚNG:**
>
> - Hôm nay: **`0`** (ví dụ `Hôm nay JP¥0` / `US$0`).
> - Có dòng quy đổi thời gian từ gói hiện tại (ví dụ: _`546 ngày (bao gồm 364 ngày được quy đổi từ thời gian còn lại của gói hiện tại của bạn)`_).
> - **Ngày bắt đầu tính phí** được dời về tương lai (12 → 18 → 24 tháng sau).
>
> Nếu thấy **ngày bắt đầu = ngày hết hạn cũ và hôm nay trừ tiền ngay**, tuyệt đối không bấm đăng ký; kiểm tra lại xem gói hiện tại có đang ở trạng thái **Active (tự gia hạn bật)** và có bật cờ `--stack` hay chưa.

#### Cách B — Chạy luồng tự động

Bấm đúp **`7_Auto_Chay_2_den_6.bat`**:

- Đặt biến `AUTO_FLOW=1` để các file `.bat` con không dừng `pause` giữa chừng.
- Tự động chạy tuần tự từ file `2` → `6`.
- Nếu gặp hộp thoại `Error` hoặc không đủ điều kiện, script đóng bước hiện tại và tự chuyển sang file tiếp theo.
- Nếu chạy hết 1 lượt chưa thành công, script chuyển sang chế độ thử ngẫu nhiên (`RANDOM`) cho tới khi một file báo thành công (`exit code 0`), hoặc bạn bấm `Ctrl + C` để dừng.

---

## 5. Bảng các gói (`--plan`) và SKU tương ứng

| Tham số `--plan`      | File `.bat` tương ứng           | SKU trên Play Billing                       | Offer ưu tiên         | Ghi chú                                                    |
| :-------------------- | :------------------------------ | :------------------------------------------ | :-------------------- | :--------------------------------------------------------- |
| `pro12`               | `2_Pro_12_thang_Buoc_1.bat`     | `g1.2tb.ai.subs_variant`                    | `12months-eft`        | Gói 12 tháng (bước 1)                                      |
| `pro6`                | `3_Pro_Them_6_thang_Buoc_2.bat` | `g1.2tb.ai.subs_variant`                    | `6months-eft`         | Cộng dồn +6 tháng (bước 2)                                 |
| `pro6b`               | `4_Pro_Them_6_thang_Buoc_3.bat` | `g1.2tb.ai.subs_variant`                    | `6months-eft-2`       | Cộng dồn +6 tháng (bước 3)                                 |
| `pro6c`               | `5_Pro_Du_phong_6_thang.bat`    | `g1.2tb.ai.subs_variant`                    | `6months-eft-ss-2026` | Cộng dồn +6 tháng dự phòng                                 |
| `pro3`                | `6_Pro_3_thang_eft.bat`         | `g1.2tb.ai.3months_eft`                     | `eft-3months`         | Gói 3 tháng                                                |
| `5x` / `20x` / `auto` | _(CLI)_                         | `g1.play.20tb`, `g1.play.ai.pro`, `g1.30tb` | Tự chọn dài nhất      | Gói Ultra cũ (thường không còn offer cho tài khoản thường) |

---

## 6. Sử dụng nâng cao qua dòng lệnh (CLI)

### Lệnh `ultra0.py`

```bash
# Kiểm tra môi trường
python ultra0.py --check

# Liệt kê offer của tài khoản hiện tại trên thiết bị (không mua)
python ultra0.py --account "current@device" --no-add --force --list --plan pro12

# Chạy 1 tài khoản đang đăng nhập sẵn trên thiết bị
python ultra0.py --account "current@device" --no-add --force --plan pro12
python ultra0.py --account "current@device" --no-add --force --stack --plan pro6

# Chạy chỉ định email (email:password:totp)
python ultra0.py --account "user@gmail.com:matkhau:2FAKEY" --plan pro12

# Chạy hàng loạt từ file danh sách (mỗi dòng: email----password----recovery----totp)
python ultra0.py accounts.txt --plan pro12
```

**Các tham số chính của `ultra0.py`:**

- `--check`: Tự kiểm tra kết nối ADB, root, Frida, module Billing và Play Store.
- `--list`: Chỉ tra và in danh sách offer, không mở trang thanh toán.
- `--plan {auto,5x,20x,pro12,pro6,pro6b,pro6c,pro3}`: Chọn gói/offer cần xử lý.
- `--stack`: Bật chế độ nâng cấp cộng dồn dựa trên `purchaseToken` hiện tại.
- `--old-token <token>`: Truyền thủ công `purchaseToken` cũ khi dùng kèm `--stack`.
- `--mode <1..5>`: Chọn `prorationMode` khi nâng cấp (mặc định khi stack là `5` = `CHARGE_FULL_PRICE`).
- `--no-add`: Bỏ qua bước tự thêm tài khoản Google (dùng tài khoản đã đăng nhập sẵn).
- `--no-switch`: Không tự chuyển tài khoản trong Play Store, chỉ kiểm tra có đúng tài khoản hay không.
- `--force`: Bỏ qua bước kiểm tra tài khoản trên UI Play Store.
- `--serial <id>`: Chỉ định ADB serial nếu máy đang kết nối nhiều thiết bị/giả lập.

### Tra cứu SKU tùy ý với `query_sku.py`

Yêu cầu đã bật `frida-server` (hoặc forward cổng `27042`) và Google One đang mở:

```bash
python query_sku.py g1.2tb.ai.subs_variant g1.2tb.ai.3months_eft
```

---

## 7. Lưu ý quan trọng & Xử lý sự cố

- **Luôn giữ gói ở trạng thái Active trong lúc cộng dồn**: Gói đã hủy (`Canceled` / `autoRenewing=false`) sẽ không cộng dồn được bằng `SubscriptionUpdateParams`. Hãy cộng dồn xong toàn bộ các bước rồi mới hủy gia hạn. Sau khi hủy, quyền lợi vẫn giữ nguyên đến hết ngày hết hạn.
- **Kẹt ở bước `connecting`**: Play Store chưa chạy hoặc bị treo; hãy mở thủ công Play Store trên giả lập hoặc khởi động lại giả lập.
- **Lỗi `Bạn đã đăng ký` / `ITEM_UNAVAILABLE`**: Tài khoản đã có gói ở trạng thái xung đột (thường do chưa bật `--stack`, dính cache `sku_details.db`, hoặc gói cũ đang bị `Canceled`). Script bản mới đã tự động dọn cache, đồng bộ tài khoản và thử Resubscribe, nhưng nếu vẫn lỗi nhiều lần liên tiếp thì nên nghỉ ~24 giờ để tránh kiểm soát rủi ro (risk control).
- **Lỗi `Không kết nối được với Internet`**: Mạng giả lập chập chờn hoặc vướng proxy cũ; đợi vài giây rồi thử lại hoặc khởi động lại giả lập.
- **Nhớ hủy gói trước ngày gia hạn**: Sau khi hoàn tất cộng dồn, kiểm tra lại tại `https://play.google.com/store/account/subscriptions` để xác nhận ngày thanh toán tiếp theo và hủy tự gia hạn nếu không muốn bị trừ tiền khi hết hạn dùng thử.

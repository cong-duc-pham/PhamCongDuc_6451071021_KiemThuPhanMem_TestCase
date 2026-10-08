# BÁO CÁO THỰC HÀNH KIỂM THỬ WEB UI TỰ ĐỘNG: SELENIUM & POM (PYTHON)

**Môn học:** Kiểm thử phần mềm  
**Bộ môn:** Công nghệ Thông tin - Trường Đại học Giao thông Vận tải Phân hiệu tại TP.HCM  
**Sinh viên thực hiện:** Phạm Công Đức  
**Mã số sinh viên (MSV):** 6451071021  
**Website mục tiêu:** [https://vanphongdientu.utc.edu.vn/](https://vanphongdientu.utc.edu.vn/)

---

## 1. CẤU TRÚC THƯ MỤC DỰ ÁN

Mô hình thiết kế tách riêng Page Objects và Test Scripts, tích hợp Allure Report và ánh xạ đầy đủ 27 Test Cases tự động từ file đặc tả Excel:

```text
PhamCongDuc_6451071021/
|-- base/
|   |-- __init__.py
|   |-- base_test.py                    # Khởi tạo WebDriver, timeout, cấu hình Headless, đính kèm ảnh Allure khi thất bại
|
|-- pages/                              # Các Page Objects
|   |-- __init__.py
|   |-- base_page.py                    # Lớp cơ sở: wait, click, js_click, type, get_text
|   |-- login_page.py                   # Trang Đăng nhập UTC
|   |-- home_page.py                    # Trang sau khi đăng nhập thành công
|   |-- forgot_password_page.py         # Trang Quên mật khẩu và Captcha
|
|-- tests/                              # Toàn bộ 27 kịch bản kiểm thử E2E ánh xạ trực tiếp từ file Excel
|   |-- __init__.py
|   |-- test_login_e2e.py               # 12 ca kiểm thử Đăng nhập (TC_LOG_01 -> TC_LOG_12, TC_SSO_01)
|   |-- test_forgot_password_e2e.py     # 7 ca kiểm thử Quên mật khẩu & Captcha (TC_FP_01 -> TC_FP_08)
|   |-- test_security_and_ui_e2e.py     # 8 ca kiểm thử Bảo mật & Giao diện (TC_SEC_01 -> 06, TC_UI_01 -> 03)
|
|-- reports/                            # Thư mục xuất báo cáo kiểm thử
|   |-- report.html                     # Báo cáo HTML tiêu chuẩn (pytest-html)
|   |-- allure-results/                 # Dữ liệu kết quả Allure dạng JSON
|   |-- allure-report/                  # Báo cáo Allure HTML tương tác hoàn chỉnh
|
|-- tools/                              # Công cụ hỗ trợ
|   |-- allure-2.32.0/                  # Bộ Allure Commandline phục vụ xuất báo cáo
|
|-- build/
|   |-- screenshots/                    # Ảnh chụp tự động khi có kiểm thử thất bại
|
|-- conftest.py                         # Cấu hình PyTest hooks và fixtures
|-- pytest.ini                          # Cấu hình PyTest testpaths, report và alluredir
|-- requirements.txt                    # Danh sách thư viện phụ thuộc
|-- run_tests.py                        # Script thực thi kiểm thử và tự động biên dịch Allure Report
|-- TestCases_VanPhongDienTu_UTC.xlsx      # Bảng đặc tả 37 Test Cases dạng Excel
└── TestCases_VanPhongDienTu_UTC.md        # Báo cáo đặc tả Test Cases dạng Markdown
```

---

## 2. DANH MỤC 27 CA KIỂM THỬ TỰ ĐỘNG ÁNH XẠ TỪ FILE EXCEL

### 2.1. Phân hệ Đăng nhập hệ thống (`test_login_e2e.py` - 12 ca)
- **TC_LOG_01:** Đăng nhập thành công với thông tin hợp lệ
- **TC_LOG_02:** Đăng nhập thất bại khi nhập sai Mật khẩu
- **TC_LOG_03:** Đăng nhập thất bại khi Tên đăng nhập không tồn tại
- **TC_LOG_04:** Để trống cả Tên đăng nhập và Mật khẩu
- **TC_LOG_05:** Để trống Tên đăng nhập, chỉ nhập Mật khẩu
- **TC_LOG_06:** Nhập Tên đăng nhập, để trống Mật khẩu
- **TC_LOG_07:** Tên đăng nhập có khoảng trắng ở đầu hoặc cuối
- **TC_LOG_08:** Tính phân biệt chữ hoa/thường của Mật khẩu
- **TC_LOG_09:** Kiểm tra tính năng 'Giữ tôi luôn đăng nhập'
- **TC_LOG_10 (FAILED - Báo cáo lỗi):** Kiểm tra cơ chế tự động tạm khóa tài khoản sau khi đăng nhập sai nhiều lần (Kỳ vọng có thông báo tạm khóa để chống brute force; Thực tế website UTC không khóa và chỉ báo sai mật khẩu -> Phát hiện lỗi và tự động chụp ảnh màn hình)
- **TC_LOG_11:** Ẩn ký tự trường Mật khẩu (Password Masking)
- **TC_LOG_12:** Đăng nhập bằng cách nhấn phím Enter
- **TC_SSO_01:** Kiểm tra cấu hình liên kết Google OAuth 2.0 (Email UTC)

### 2.2. Phân hệ Lấy lại mật khẩu (`test_forgot_password_e2e.py` - 7 ca)
- **TC_FP_01:** Chuyển hướng đến trang 'Lấy lại mật khẩu' qua liên kết
- **TC_FP_03:** Gửi yêu cầu với mã Captcha sai
- **TC_FP_04:** Để trống ô Mã bảo mật Captcha
- **TC_FP_05:** Để trống ô Địa chỉ Email
- **TC_FP_06:** Để trống cả Captcha và Email khi submit
- **TC_FP_07:** Kiểm tra liên kết 'Trở lại đăng nhập?'
- **TC_FP_08:** Kiểm tra hiển thị hình ảnh Captcha bảo mật và Logo

### 2.3. Phân hệ Bảo mật & Giao diện (`test_security_and_ui_e2e.py` - 8 ca)
- **TC_SEC_01:** Phòng chống tấn công SQL Injection tại ô Tên đăng nhập
- **TC_SEC_02:** Phòng chống tấn công SQL Injection tại ô Mật khẩu
- **TC_SEC_03:** Phòng chống mã độc Cross-Site Scripting (XSS)
- **TC_SEC_05:** Chặn truy cập trực tiếp URL nội bộ khi chưa xác thực
- **TC_SEC_06:** Kiểm tra bảo mật giao thức kết nối HTTPS
- **TC_UI_01:** Kiểm tra hiển thị banner, slogan và bản quyền footer
- **TC_UI_02:** Kiểm tra liên kết 'Trung tâm trợ giúp' mở đúng tab mới
- **TC_UI_03:** Kiểm tra liên kết 'Ý kiến phản hồi' sử dụng giao thức mailto

---

## 3. HƯỚNG DẪN THỰC THI KIỂM THỬ

### 3.1. Chạy toàn bộ 27 ca kiểm thử tự động
```powershell
python run_tests.py
```

### 3.2. Chạy mở trực tiếp giao diện trình duyệt (Headed Mode)
Nếu muốn quan sát Chrome thao tác trực quan trên màn hình máy tính:
```powershell
$env:HEADED="true"; python run_tests.py
```

### 3.3. Chạy theo từng nhóm kiểm thử riêng biệt
```powershell
# Chỉ chạy nhóm Đăng nhập (12 ca)
pytest tests/test_login_e2e.py -v

# Chỉ chạy nhóm Quên mật khẩu (7 ca)
pytest tests/test_forgot_password_e2e.py -v

# Chỉ chạy nhóm Bảo mật & Giao diện (8 ca)
pytest tests/test_security_and_ui_e2e.py -v
```

---

## 4. XEM BÁO CÁO KẾT QUẢ KIỂM THỬ

### 4.1. Xem Allure Report tương tác
Mở giao diện Allure Report trên trình duyệt:
```powershell
python run_tests.py --allure
```
Hoặc:
```powershell
.\tools\allure-2.32.0\bin\allure.bat open reports\allure-report
```

### 4.2. Xem Báo cáo HTML tiêu chuẩn
Mở trực tiếp file:  
[reports/report.html](file:///c:/CongDuc/Ki_I_nam_IV\KiemThuPhanMem\PhamCongDuc_6451071021\reports\report.html)

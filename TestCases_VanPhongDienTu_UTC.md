# BÁO CÁO THIẾT KẾ TEST CASE: VĂN PHÒNG ĐIỆN TỬ UTC
**URL Hệ thống:** [https://vanphongdientu.utc.edu.vn/](https://vanphongdientu.utc.edu.vn/)  
**Môn học:** Kiểm thử phần mềm (Software Testing)  
**Sinh viên thực hiện:** Phạm Công Đức  
**Mã sinh viên:** 6451071021  
**Trường:** Đại học Giao thông Vận tải (UTC)

---

## 1. TỔNG QUAN HỆ THỐNG VÀ PHẠM VI KIỂM THỬ

### 1.1. Khảo sát thực tế hệ thống
Cổng thông tin **Văn phòng điện tử Trường Đại học Giao thông Vận tải** (`https://vanphongdientu.utc.edu.vn/`) là hệ thống phục vụ công tác điều hành, quản trị văn bản và xử lý công việc trực tuyến dành cho Cán bộ, Giảng viên và Sinh viên UTC.

Khi người dùng chưa đăng nhập, hệ thống tự động kiểm tra trạng thái phiên và chuyển hướng (redirect) về trang đăng nhập với cơ chế bảo mật:
- URL chuyển hướng: `https://vanphongdientu.utc.edu.vn/Login?r={URL_gốc}`
- Phương thức gửi dữ liệu form: `POST /Login`
- Thư viện client: jQuery, CSS thuần tối ưu hóa tốc độ tải.

### 1.2. Các thành phần giao diện & chức năng chính
1. **Form Đăng nhập nội bộ (`/Login`)**:
   - Trường `username` (Tên đăng nhập): `type="text"`, `placeholder="Tên đăng nhập"`
   - Trường `userpwd` (Mật khẩu): `type="password"`, `placeholder="Mật khẩu"`
   - Checkbox `persistent`: `value="1"`, nhãn *"Giữ tôi luôn đăng nhập"*
   - Nút submit: `value="Đăng nhập"`
2. **Đăng nhập liên kết Single Sign-On (Google OAuth 2.0)**:
   - Nút *"Đăng nhập bằng e-mail UTC"* liên kết tới OAuth endpoint của Google Accounts với client ID trường cấp và callback domain về hệ thống.
3. **Form Lấy lại mật khẩu (`/Login/GetPass`)**:
   - Mã Captcha: Sinh động qua endpoint `/login/index/captcha`
   - Trường `captcha` (Mã bảo mật): `type="text"`, `placeholder="Mã bảo mật"`
   - Trường `email` (Địa chỉ Email): `type="text"`, `placeholder="Địa chỉ Email"`
   - Nút submit: `value="Cập nhật"`
   - Liên kết điều hướng *"Trở lại đăng nhập?"*
4. **Các liên kết phụ trợ & Chân trang (Footer)**:
   - Trung tâm trợ giúp: `http://hotrokythuat.utc.edu.vn` (mở tab mới)
   - Ý kiến phản hồi: `mailto:hotrokythuat@utc.edu.vn`
   - Bản quyền nhà trường: `Trường ĐH Giao Thông Vận Tải © 2026`

---

## 2. KỸ THUẬT THIẾT KẾ TEST CASE ÁP DỤNG

1. **Phân vùng tương đương (Equivalence Partitioning - EP):** Phân chia tập dữ liệu đầu vào thành các lớp hợp lệ (Valid Partition) và không hợp lệ (Invalid Partition) cho Tên đăng nhập, Mật khẩu, Email và Captcha.
2. **Phân tích giá trị biên (Boundary Value Analysis - BVA):** Kiểm tra giới hạn độ dài chuỗi ký tự, các ký tự trắng đầu/cuối chuỗi (trim spaces).
3. **Bảng quyết định (Decision Table):** Kết hợp các trường hợp nhập đúng/sai giữa Username và Password; Email và Captcha.
4. **Đoán lỗi & Kiểm thử bảo mật (Error Guessing & Security Testing):**
   - Kiểm tra phòng chống tấn công SQL Injection (`' OR 1=1 --`).
   - Kiểm tra phòng chống Cross-Site Scripting (XSS).
   - Kiểm tra phòng chống Brute Force (dò quét mật khẩu).
   - Kiểm tra xác thực miền email Google OAuth (`@utc.edu.vn` vs `@gmail.com`).
   - Kiểm tra an toàn Cookie & Giao thức HTTPS.

---

## 3. DANH SÁCH CHI TIẾT CÁC CA KIỂM THỬ (TEST CASES SPECIFICATION)

### PHÂN HỆ 1: ĐĂNG NHẬP BẰNG TÀI KHOẢN NỘI BỘ (FORM LOGIN)

| Mã TC | Tiêu đề ca kiểm thử | Điều kiện tiên quyết | Các bước thực hiện | Dữ liệu thử nghiệm (Test Data) | Kết quả mong đợi (Expected Result) | Loại KT | Mức độ ưu tiên |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_LOG_01** | Đăng nhập thành công với thông tin hợp lệ | Tài khoản đang kích hoạt trong hệ thống. Đang ở trang `/Login` | 1. Nhập Username hợp lệ<br>2. Nhập Password chính xác<br>3. Bấm nút "Đăng nhập" | `username: 'gv_utc'`<br>`userpwd: 'ValidPass123@'` | Đăng nhập thành công, hệ thống điều hướng vào Dashboard nội bộ, tạo phiên làm việc (Session). | Functional | **High** |
| **TC_LOG_02** | Đăng nhập thất bại khi nhập sai Mật khẩu | Tài khoản người dùng tồn tại. Đang ở trang `/Login` | 1. Nhập Username hợp lệ<br>2. Nhập sai Mật khẩu<br>3. Bấm nút "Đăng nhập" | `username: 'gv_utc'`<br>`userpwd: 'SaiMatKhau999'` | Từ chối đăng nhập. Hiển thị thông báo: *"Tên đăng nhập hoặc mật khẩu không chính xác"*. | Functional | **High** |
| **TC_LOG_03** | Đăng nhập thất bại khi Tên đăng nhập không tồn tại | Đang ở trang `/Login` | 1. Nhập Username không có trong CSDL<br>2. Nhập mật khẩu bất kỳ<br>3. Bấm nút "Đăng nhập" | `username: 'user_khongtontai'`<br>`userpwd: 'Matkhau123'` | Từ chối đăng nhập. Hiển thị thông báo lỗi chung, không để lộ thông tin tài khoản tồn tại hay không. | Functional | **High** |
| **TC_LOG_04** | Để trống cả Tên đăng nhập và Mật khẩu | Đang ở trang `/Login` | 1. Bỏ trống cả 2 ô<br>2. Bấm nút "Đăng nhập" | `username: ''`<br>`userpwd: ''` | Hệ thống chặn submit form hoặc hiển thị thông báo yêu cầu nhập đầy đủ thông tin. | Validation | **Medium** |
| **TC_LOG_05** | Để trống Tên đăng nhập, chỉ nhập Mật khẩu | Đang ở trang `/Login` | 1. Để trống ô Tên đăng nhập<br>2. Nhập Mật khẩu<br>3. Bấm "Đăng nhập" | `username: ''`<br>`userpwd: 'ValidPass123@'` | Báo lỗi yêu cầu nhập Tên đăng nhập. Con trỏ tự động trỏ vào ô Tên đăng nhập. | Validation | **Medium** |
| **TC_LOG_06** | Nhập Tên đăng nhập, để trống Mật khẩu | Đang ở trang `/Login` | 1. Nhập Tên đăng nhập<br>2. Để trống ô Mật khẩu<br>3. Bấm "Đăng nhập" | `username: 'gv_utc'`<br>`userpwd: ''` | Báo lỗi yêu cầu nhập Mật khẩu. Con trỏ tự động trỏ vào ô Mật khẩu. | Validation | **Medium** |
| **TC_LOG_07** | Tên đăng nhập có khoảng trắng ở đầu/cuối | Tài khoản 'gv_utc' tồn tại | 1. Nhập Username có khoảng trắng dư thừa<br>2. Nhập đúng Password<br>3. Bấm "Đăng nhập" | `username: '  gv_utc  '`<br>`userpwd: 'ValidPass123@'` | Hệ thống tự động cắt bỏ (trim) khoảng trắng và đăng nhập thành công. | Usability | **Low** |
| **TC_LOG_08** | Tính phân biệt chữ hoa/thường của Mật khẩu | Mật khẩu tài khoản là 'Password123' | 1. Nhập đúng Username<br>2. Nhập mật khẩu toàn chữ thường<br>3. Bấm "Đăng nhập" | `username: 'gv_utc'`<br>`userpwd: 'password123'` | Đăng nhập thất bại do mật khẩu bắt buộc phân biệt chữ hoa và chữ thường (Case-sensitive). | Security | **High** |
| **TC_LOG_09** | Chức năng "Giữ tôi luôn đăng nhập" (Remember me) | Đang ở trang `/Login` | 1. Nhập thông tin đăng nhập đúng<br>2. Tích chọn checkbox "Giữ tôi luôn đăng nhập"<br>3. Đăng nhập thành công<br>4. Đóng trình duyệt và mở lại | `persistent = 1` | Phiên làm việc được lưu trong Cookie dài hạn, mở lại website không cần đăng nhập lại. | Functional | **Medium** |
| **TC_LOG_10** | Đăng nhập KHÔNG tích chọn "Giữ tôi luôn đăng nhập" | Đang ở trang `/Login` | 1. Đăng nhập đúng không tích chọn persistent<br>2. Đóng toàn bộ tab và trình duyệt<br>3. Mở lại trang | `persistent = 0` | Session kết thúc khi đóng trình duyệt. Khi mở lại website bắt buộc phải đăng nhập lại. | Functional | **Medium** |
| **TC_LOG_11** | Kiểm tra ẩn ký tự trường Mật khẩu (Password Masking) | Đang ở trang `/Login` | 1. Nhập ký tự vào ô Mật khẩu<br>2. Quan sát hiển thị trên màn hình | `userpwd: 'Secret123'` | Ký tự hiển thị dưới dạng dấu chấm tròn (•), thuộc tính thẻ input là `type="password"`. | UI / Security | **High** |
| **TC_LOG_12** | Đăng nhập bằng cách nhấn phím Enter | Đang ở trang `/Login` | 1. Nhập đúng Username và Password<br>2. Nhấn phím Enter từ bàn phím | Phím Enter | Form tự động submit và đăng nhập thành công mà không cần click chuột vào nút "Đăng nhập". | Usability | **Medium** |

---

### PHÂN HỆ 2: ĐĂNG NHẬP LIÊN KẾT EMAIL TRƯỜNG (GOOGLE OAUTH 2.0 SSO)

| Mã TC | Tiêu đề ca kiểm thử | Điều kiện tiên quyết | Các bước thực hiện | Dữ liệu thử nghiệm (Test Data) | Kết quả mong đợi (Expected Result) | Loại KT | Mức độ ưu tiên |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_SSO_01** | Đăng nhập thành công với Email Google cấp bởi trường UTC | Có tài khoản email `@utc.edu.vn` hoạt động | 1. Nhấp nút "Đăng nhập bằng e-mail UTC"<br>2. Tại Google SSO, đăng nhập email UTC<br>3. Cho phép quyền xác thực | `Email: gv_khoa@utc.edu.vn`<br>`Google Password hợp lệ` | Xác thực Google thành công, callback redirect về hệ thống và đăng nhập thẳng vào trang làm việc. | Functional | **High** |
| **TC_SSO_02** | Từ chối đăng nhập với Email Google cá nhân ngoài trường | Đang tại trang đăng nhập Google | 1. Bấm nút "Đăng nhập bằng e-mail UTC"<br>2. Đăng nhập bằng Gmail thông thường (`@gmail.com`) | `Email: user_canhan@gmail.com` | Hệ thống từ chối đăng nhập, cảnh báo: *"Vui lòng sử dụng địa chỉ email do Trường cấp (@utc.edu.vn)"*. | Security | **High** |
| **TC_SSO_03** | Người dùng bấm Hủy quyền tại trang Google SSO | Đang tại trang cấp quyền Google | 1. Bấm "Đăng nhập bằng e-mail UTC"<br>2. Nhấn nút "Hủy / Cancel" trên giao diện Google | Người dùng hủy thao tác | Điều hướng an toàn về lại trang `/Login`, không phát sinh lỗi mã nguồn (HTTP 500 error). | Exception | **Medium** |
| **TC_SSO_04** | Email UTC hợp lệ nhưng chưa được kích hoạt quyền văn phòng điện tử | Tài khoản sinh viên/nhân sự chưa phân quyền | 1. Đăng nhập bằng email UTC chưa cấp tài khoản văn phòng điện tử | `Email: sv_chua_kich_hoat@utc.edu.vn` | Hệ thống thông báo tài khoản chưa được cấp quyền sử dụng Văn phòng điện tử và hướng dẫn liên hệ quản trị. | Authorization | **Medium** |

---

### PHÂN HỆ 3: LẤY LẠI MẬT KHẨU (`/Login/GetPass`)

| Mã TC | Tiêu đề ca kiểm thử | Điều kiện tiên quyết | Các bước thực hiện | Dữ liệu thử nghiệm (Test Data) | Kết quả mong đợi (Expected Result) | Loại KT | Mức độ ưu tiên |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_FP_01** | Điều hướng đến trang Lấy lại mật khẩu | Đang ở trang `/Login` | 1. Nhấp chuột vào link "Bạn quên mật khẩu đăng nhập ?" | Link: `/Login/GetPass` | Chuyển hướng thành công tới `/Login/GetPass`, hiển thị tiêu đề "Lấy lại mật khẩu" và form nhập liệu. | Navigation | **High** |
| **TC_FP_02** | Gửi yêu cầu lấy lại mật khẩu thành công | Email đã đăng ký trong hệ thống | 1. Nhập chính xác mã Captcha trên ảnh<br>2. Nhập Email hợp lệ<br>3. Bấm nút "Cập nhật" | `captcha: [mã đúng trên ảnh]`<br>`email: 'gv_abc@utc.edu.vn'` | Gửi thành công yêu cầu. Hệ thống thông báo đã gửi liên kết đặt lại mật khẩu về hộp thư người dùng. | Functional | **High** |
| **TC_FP_03** | Nhập sai mã Captcha bảo mật | Đang ở `/Login/GetPass` | 1. Nhập sai mã Captcha<br>2. Nhập Email đúng<br>3. Bấm "Cập nhật" | `captcha: '000000'` (sai)<br>`email: 'gv_abc@utc.edu.vn'` | Báo lỗi: *"Mã bảo mật không chính xác"*. Tự động tạo ảnh Captcha mới để chống spam. | Security | **High** |
| **TC_FP_04** | Nhập Email không tồn tại trong hệ thống | Đang ở `/Login/GetPass` | 1. Nhập Captcha đúng<br>2. Nhập email không có trong hệ thống<br>3. Bấm "Cập nhật" | `captcha: đúng`<br>`email: 'khongtontai@utc.edu.vn'` | Thông báo lỗi email không tồn tại trên hệ thống. | Negative | **Medium** |
| **TC_FP_05** | Để trống trường Mã bảo mật (Captcha) | Đang ở `/Login/GetPass` | 1. Bỏ trống ô Mã bảo mật<br>2. Nhập Email hợp lệ<br>3. Bấm "Cập nhật" | `captcha: ''`<br>`email: 'gv_abc@utc.edu.vn'` | Báo lỗi yêu cầu nhập mã bảo mật. Không gửi request. | Validation | **Medium** |
| **TC_FP_06** | Để trống trường Địa chỉ Email | Đang ở `/Login/GetPass` | 1. Nhập đúng Captcha<br>2. Bỏ trống ô Email<br>3. Bấm "Cập nhật" | `captcha: đúng`<br>`email: ''` | Báo lỗi yêu cầu nhập địa chỉ Email. | Validation | **Medium** |
| **TC_FP_07** | Nhập Email sai cú pháp định dạng | Đang ở `/Login/GetPass` | 1. Nhập Captcha đúng<br>2. Nhập email thiếu `@`, thiếu tên miền<br>3. Bấm "Cập nhật" | `email: 'dinhdang_sai.utc'` | Hệ thống cảnh báo định dạng địa chỉ Email không đúng chuẩn. | Validation | **Medium** |
| **TC_FP_08** | Kiểm tra liên kết "Trở lại đăng nhập?" | Đang ở `/Login/GetPass` | 1. Nhấp vào liên kết "Trở lại đăng nhập?" | Link: `/Login` | Điều hướng quay trở về trang đăng nhập `/Login`. | Navigation | **Low** |
| **TC_FP_09** | Kiểm tra làm mới ảnh Captcha khi tải lại trang | Đang ở `/Login/GetPass` | 1. Quan sát mã Captcha hiện thời<br>2. Nhấn phím F5 reload lại trang | Reload Page | Mã Captcha cũ bị vô hiệu hóa, sinh ra hình ảnh mã Captcha mới. | Functional | **Medium** |

---

### PHÂN HỆ 4: KIỂM THỬ BẢO MẬT & PHI CHỨC NĂNG (SECURITY & NON-FUNCTIONAL)

| Mã TC | Tiêu đề ca kiểm thử | Điều kiện tiên quyết | Các bước thực hiện | Dữ liệu thử nghiệm (Test Data) | Kết quả mong đợi (Expected Result) | Loại KT | Mức độ ưu tiên |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_SEC_01** | Phòng chống tấn công SQL Injection tại ô Tên đăng nhập | Đang ở trang `/Login` | 1. Nhập chuỗi khai thác SQLi vào ô Username<br>2. Nhập Password bất kỳ<br>3. Bấm "Đăng nhập" | `username: ' OR '1'='1 --`<br>`userpwd: 'test'` | Hệ thống lọc dữ liệu an toàn (sử dụng Prepared Statement), từ chối đăng nhập, không trả về mã lỗi SQL hay crash DB. | Security | **High** |
| **TC_SEC_02** | Phòng chống tấn công SQL Injection tại ô Mật khẩu | Đang ở trang `/Login` | 1. Nhập username tồn tại (vd: `admin`)<br>2. Nhập chuỗi SQLi vào ô Password<br>3. Bấm "Đăng nhập" | `username: 'admin'`<br>`userpwd: ' OR '1'='1` | Hệ thống mã hóa hash mật khẩu, kiểm tra chính xác, từ chối đăng nhập trái phép. | Security | **High** |
| **TC_SEC_03** | Phòng chống Cross-Site Scripting (XSS) | Đang ở trang `/Login` và `/Login/GetPass` | 1. Chèn thẻ script HTML vào ô Tên đăng nhập và Email<br>2. Bấm submit form | Payload: `<script>alert('XSS')</script>` | Mã Javascript không bị thực thi trên trình duyệt, dữ liệu hiển thị (nếu có) được escape mã HTML an toàn. | Security | **High** |
| **TC_SEC_04** | Kiểm tra chống dò mật khẩu liên tục (Brute Force) | Đang ở trang `/Login` | 1. Cố ý nhập sai mật khẩu liên tiếp 5-10 lần trong thời gian ngắn cho cùng 1 tài khoản | Nhập sai liên tục 5-10 lần | Hệ thống kích hoạt cơ chế khóa tạm thời tài khoản hoặc yêu cầu nhập Captcha/Rate limiting để ngăn bot. | Security | **High** |
| **TC_SEC_05** | Chặn truy cập trực tiếp URL nội bộ khi chưa xác thực | Chưa đăng nhập hệ thống | 1. Mở tab trình duyệt ẩn danh<br>2. Truy cập thẳng URL trang chủ `https://vanphongdientu.utc.edu.vn/` | URL trang chủ | Bị chặn và chuyển hướng ngay về `/Login?r=...`. Không xem được bất kỳ nội dung nghiệp vụ nội bộ nào. | Security | **High** |
| **TC_SEC_06** | Kiểm tra mã hóa kết nối HTTPS và thuộc tính Cookie | Mở website | 1. Kiểm tra chứng chỉ SSL trên URL bar<br>2. Kiểm tra cờ bảo mật Cookie trong tab Application (F12) | Giao thức HTTPS | Chứng chỉ bảo mật SSL còn hạn, Cookie phiên được đánh dấu cờ `HttpOnly` (chống lộ cookie qua JS) và `Secure`. | Security | **High** |
| **TC_SEC_07** | Kiểm tra nút Back trình duyệt sau khi đăng xuất | Vừa thao tác Đăng xuất khỏi hệ thống | 1. Bấm nút Back trên trình duyệt để quay lại trang làm việc trước | Nút Back trình duyệt | Hệ thống không hiển thị dữ liệu đã lưu trong cache (áp dụng `Cache-Control: no-store`), tự động yêu cầu đăng nhập lại. | Usability / Security | **Medium** |

---

### PHÂN HỆ 5: GIAO DIỆN & TƯƠNG THÍCH (UI/UX & COMPATIBILITY)

| Mã TC | Tiêu đề ca kiểm thử | Điều kiện tiên quyết | Các bước thực hiện | Dữ liệu thử nghiệm (Test Data) | Kết quả mong đợi (Expected Result) | Loại KT | Mức độ ưu tiên |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC_UI_01** | Kiểm tra bố cục, hình ảnh và tiêu đề trang | Mở trang `/Login` | 1. Quan sát banner trái, logo trường, form đăng nhập phải<br>2. Kiểm tra lỗi font chữ tiếng Việt | Giao diện chuẩn 1920x1080 | Hiển thị đầy đủ hình ảnh, font chữ Unicode tiếng Việt hiển thị chính xác không bị lỗi ký tự (? hoặc ô vuông), bố cục hài hòa. | UI | **Medium** |
| **TC_UI_02** | Kiểm tra liên kết "Trung tâm trợ giúp" | Mở trang `/Login` | 1. Cuộn xuống chân trang<br>2. Bấm vào liên kết "Trung tâm trợ giúp" | Link: `http://hotrokythuat.utc.edu.vn` | Mở trang Hỗ trợ kỹ thuật UTC trên tab mới (`target="_blank"`). | Navigation | **Low** |
| **TC_UI_03** | Kiểm tra liên kết "Ý kiến phản hồi" | Mở trang `/Login` | 1. Bấm vào liên kết "Ý kiến phản hồi" tại chân trang | Link: `mailto:hotrokythuat@utc.edu.vn` | Kích hoạt phần mềm gửi email trên máy tính với địa chỉ người nhận điền sẵn là `hotrokythuat@utc.edu.vn`. | Usability | **Low** |
| **TC_UI_04** | Kiểm tra khả năng tương thích trên các trình duyệt | Cài đặt Chrome, Edge, Firefox | 1. Mở trang trên Chrome, Edge, Firefox<br>2. Kiểm tra tính năng nhập liệu và submit | Các trình duyệt phổ biến | Hoạt động đồng nhất, giao diện không bị xô lệch trên các engine trình duyệt khác nhau (Blink, Gecko). | Compatibility | **Medium** |
| **TC_UI_05** | Kiểm tra hiển thị thích ứng trên di động (Responsive) | Bật Device Mode (F12) kích thước 375x812 | 1. Xem màn hình ở tỷ lệ màn hình điện thoại<br>2. Thử nghiệm thao tác chạm và gõ phím | Viewport di động | Giao diện tự động co giãn vừa vặn, không bị vỡ khung hay xuất hiện thanh cuộn ngang gây khó thao tác. | Responsive | **Medium** |

---

## 4. MA TRẬN TRUY XUẤT YÊU CẦU (TRACEABILITY MATRIX)

| Phân hệ / Yêu cầu chức năng | Mã Test Case bao phủ | Mức độ bao phủ (Coverage) |
| :--- | :--- | :---: |
| **Đăng nhập form thường** | TC_LOG_01 đến TC_LOG_12 | 100% |
| **Đăng nhập Google SSO (Email UTC)** | TC_SSO_01 đến TC_SSO_04 | 100% |
| **Quên mật khẩu & Captcha** | TC_FP_01 đến TC_FP_09 | 100% |
| **Bảo mật hệ thống (SQLi, XSS, Brute force, Session)** | TC_SEC_01 đến TC_SEC_07 | 100% |
| **Giao diện người dùng & Tương thích** | TC_UI_01 đến TC_UI_05 | 100% |

---

## 5. TÀI NGUYÊN FILE TRONG DỰ ÁN

- File kịch bản Test Case định dạng bảng Excel hoàn chỉnh:  
  👉 [TestCases_VanPhongDienTu_UTC.xlsx](file:///c:/CongDuc/Ki_I_nam_IV/KiemThuPhanMem/PhamCongDuc_6451071021/TestCases_VanPhongDienTu_UTC.xlsx)
- File tài liệu chi tiết định dạng Markdown:  
  👉 [TestCases_VanPhongDienTu_UTC.md](file:///c:/CongDuc/Ki_I_nam_IV/KiemThuPhanMem/PhamCongDuc_6451071021/TestCases_VanPhongDienTu_UTC.md)
- Script Python tái tạo file Excel:  
  👉 [generate_testcases_excel.py](file:///c:/CongDuc/Ki_I_nam_IV/KiemThuPhanMem/PhamCongDuc_6451071021/generate_testcases_excel.py)

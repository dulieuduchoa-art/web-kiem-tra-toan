# Ứng Dụng Web Kiểm Tra Trực Tuyến Môn Toán THPT (Khối 10 & Khối 12)

> **Chuẩn Cấu Trúc Đề Thi Tốt Nghiệp THPT Mới của Bộ Giáo Dục & Đào Tạo**  
> Tích hợp công thức toán học sắc nét với KaTeX, giám sát rời tab chống gian lận, chấm điểm lũy tiến và xuất file Excel (.xlsx) chuyên nghiệp.

---

## 🌟 1. Tính Năng Nổi Bật

### 📐 Ma Trận Đề Thi Chuẩn Bộ GD&ĐT (22 câu = 10 điểm) sắp xếp từ Dễ đến Khó:
- **Phần I – 12 câu Trắc nghiệm 4 lựa chọn (A, B, C, D):** 0,25 điểm/câu = **3,0 điểm**.
- **Phần II – 4 câu Trắc nghiệm Đúng / Sai:** 1,0 điểm/câu = **4,0 điểm**.
  - Mỗi câu gồm 4 ý $a, b, c, d$.
  - **Chấm lũy tiến chuẩn Bộ GD&ĐT:**
    - Đúng 1 ý: **0,10 điểm**
    - Đúng 2 ý: **0,25 điểm**
    - Đúng 3 ý: **0,50 điểm**
    - Đúng 4 ý: **1,00 điểm**
- **Phần III – 6 câu Trả lời ngắn:** 0,5 điểm/câu = **3,0 điểm**.
  - Học sinh nhập số kết quả vào ô.
  - **Hệ thống tự động chấp nhận cả dấu chấm `.` và dấu phẩy `,`** cho số thập phân (ví dụ: `3.5` hoặc `3,5`, `-0.44` hoặc `-0,44`).

---

### 👨‍🏫 2. Khu Vực Giáo Viên (Teacher Portal)
- **Mật khẩu truy cập mặc định:** `123456` (có thể đổi mật khẩu bất kỳ lúc nào).
- **Tạo đề kiểm tra mới linh hoạt với 2 phương thức chính:**
  1. **Chọn bài học từ thư mục `Kho_SGK_SBT`:**
     - Chia 2 khối: **Lớp 10** và **Lớp 12**.
     - Đầy đủ **4 bộ sách giáo khoa:**
       - *Kết nối tri thức với cuộc sống*
       - *Chân trời sáng tạo*
       - *Cùng khám phá*
       - *Cánh diều*
     - Hỗ trợ 1-click tự động tạo đề chuẩn 22 câu Bộ GD&ĐT theo từng bài học.
     - Tích hợp liên kết mở và xem trực tiếp các file sách PDF từ thư mục `Kho_SGK_SBT`.
  2. **Nhập / Dán nội dung đề thi (Text / Word / LaTeX):**
     - Trình phân tích cú pháp thông minh tự bóc tách Phần I, Phần II, Phần III, đáp án và lời giải.
     - Nút "Nạp đề mẫu" giúp giáo viên làm quen định dạng trong 1 giây.
- **Cài đặt đề thi:**
  - Thời gian làm bài (phút): 15p, 45p, 50p, 90p...
  - Bật / tắt tính năng **trộn thứ tự câu hỏi**.
  - Bật / tắt tính năng **trộn thứ tự phương án A, B, C, D** trong Phần I.
  - **Xem trước (Preview):** Xem toàn bộ đề thi trực quan với công thức KaTeX trước khi xuất bản.
- **Xuất bản đề thi & Chia sẻ:**
  - Tự động tạo link bài thi riêng biệt cho học sinh (ví dụ: `http://localhost:8000/exam/cb854991`).
  - Nút sao chép liên kết 1 chạm để gửi qua Zalo, Messenger, Google Classroom...
- **Bảng tổng hợp kết quả & Giám sát học sinh:**
  - Bộ lọc kết quả theo từng **Lớp** (ví dụ: *Tất cả các lớp*, *10A1*, *12A1*, *12A2*...).
  - Tìm kiếm nhanh học sinh theo tên.
  - Các cột dữ liệu: STT, Họ và tên, Lớp, Điểm Phần I, Điểm Phần II, Điểm Phần III, Tổng điểm, Thời gian làm bài, **Số lần rời màn hình** (Cảnh báo đỏ nếu học sinh chuyển tab/gian lận), Thời gian nộp bài.
  - **Nút "Xuất file Excel (.xlsx)":** Tạo file bảng điểm Excel mẫu chuẩn nhà trường với đường viền, màu sắc chuyên nghiệp, xếp loại học lực và khối thống kê phổ điểm (Giỏi, Khá, Trung bình, Yếu).

---

### 👨‍🎓 3. Khu Vực Học Sinh (Student Exam Room)
- **Truy cập dễ dàng qua đường link:**
  - Nhập **Họ và tên** và **Lớp** trước khi bắt đầu.
- **Giao diện làm bài hiện đại, tối ưu cho cả Điện thoại & Máy tính:**
  - Thiết kế phân chia 3 phần rõ ràng với thẻ màu trực quan.
  - **Đồng hồ đếm ngược (Sticky Timer):** Cảnh báo chuyển màu vàng cam khi còn dưới 5 phút, nhấp nháy đỏ khi còn 1 phút.
  - **Tự động thu bài và nộp:** Khi hết giờ, bài làm tự động gửi lên máy chủ, không bị mất bài.
  - **Bảng danh sách câu hỏi (Palette 1 - 22):**
    - Chuyển màu khi đã hoàn thành (Xám: chưa làm, Xanh: đã làm).
    - Bấm vào số câu để cuộn mượt ngay đến câu đó.
    - Trên điện thoại: Có nút mở ngăn kéo bảng câu hỏi nhanh gọn.
  - **Hệ thống chống gian lận (Anti-cheat):**
    - Giám sát sự kiện chuyển tab, thu nhỏ trình duyệt (`visibilitychange` / `window blur`).
    - Hiển thị bảng cảnh báo vi phạm trực tiếp trên màn hình và tự động cộng dồn số lần vi phạm để báo cáo cho giáo viên.
  - **Tự động lưu tạm thời (LocalStorage):** Chống mất bài làm khi lỡ bấm tải lại trang hoặc rớt mạng.
- **Chấm điểm tức thì sau khi nộp:**
  - Hiển thị ngay tổng điểm / 10.0 và chi tiết điểm từng phần.
  - So sánh chi tiết từng câu: Đáp án học sinh chọn vs Đáp án đúng.
  - **Lời giải chi tiết bài bản:** Trình bày từng bước giải toán kèm công thức KaTeX sắc nét giúp học sinh tự sửa sai và nắm chắc kiến thức.

---

## 🚀 4. Hướng Dẫn Khởi Chạy

### Cách 1: Khởi chạy nhanh bằng File Batch (Khuyên Dùng Trên Windows)
Click đúp chuột vào file:
```
run.bat
```

### Cách 2: Khởi chạy bằng dòng lệnh
Mở Terminal / PowerShell tại thư mục `d:\Web_KiemTra_Toan` và chạy:
```powershell
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 5. Địa Chỉ Truy Cập

| Khu Vực | Địa Chỉ URL | Ghi Chú |
|---|---|---|
| **Cổng Học Sinh / Trang Chủ** | `http://localhost:8000/` | Xem danh sách đề hoặc nhập mã đề thi |
| **Khu Vực Giáo Viên** | `http://localhost:8000/teacher` | Mật khẩu mặc định: `123456` |
| **Phòng Thi Học Sinh** | `http://localhost:8000/exam/{mã_đề}` | Ví dụ: `http://localhost:8000/exam/cb854991` |

---

## 📁 6. Cấu Trúc Mã Nguồn

```
d:\Web_KiemTra_Toan\
├── server.py              # FastAPI Web Backend & Hệ thống API
├── database.py            # Quản lý cơ sở dữ liệu SQLite & Thuật toán chấm điểm Bộ GD&ĐT
├── curriculum_data.py     # Dữ liệu ma trận 22 câu cho 4 bộ sách (KNTT, CTST, CKP, CD) Lớp 10 & 12
├── excel_exporter.py      # Bộ tạo file Excel (.xlsx) chuẩn bảng điểm bằng openpyxl
├── parser_utils.py        # Bộ phân tích đề thi từ văn bản dán tự do / LaTeX
├── Kho_SGK_SBT/           # Thư mục lưu trữ các file sách PDF (Khối 10 & Khối 12)
├── templates/             # Giao diện HTML hiện đại
│   ├── index.html         # Trang chủ / Cổng tra cứu đề thi
│   ├── teacher.html       # Trang quản trị giáo viên
│   ├── exam.html          # Phòng làm bài thi học sinh
│   └── result.html        # Trang xem kết quả chi tiết & Lời giải
├── static/                # Tài nguyên giao diện
│   ├── css/style.css      # CSS phong cách Glassmorphism, Responsive & Tinh chỉnh KaTeX
│   └── js/
│       ├── app.js         # Tiện ích chung (Render KaTeX, Toast, Copy link)
│       ├── teacher.js     # Logic khu vực giáo viên (Tạo đề, Lọc lớp, Xuất Excel)
│       └── student.js     # Logic làm bài (Đồng hồ, Giám sát gian lận, Tự động nộp)
├── run.bat                # File khởi chạy 1 chạm cho Windows
├── push_to_github.bat     # File tự động đẩy code lên GitHub để xuất bản
├── requirements.txt       # Danh sách thư viện Python cần thiết
├── render.yaml            # Cấu hình tự động cho Render
├── Procfile               # Lệnh khởi chạy Web Service
├── vercel.json            # Cấu hình Serverless cho Vercel
├── .vercelignore          # Bỏ qua tài nguyên nặng khi đẩy lên Vercel
└── verify_app.py          # Script kiểm thử tự động toàn diện
```

---

## ☁️ 7. Triển Khai Lên Mạng Miễn Phí (Lưu Dữ Liệu Vĩnh Viễn Không Bị Mất)

1. **Tạo Cơ Sở Dữ Liệu Trực Tuyến Miễn Phí (Neon.tech - 30 giây):**
   - Truy cập [neon.tech](https://neon.tech) -> Đăng nhập bằng Google/GitHub -> Bấm **Create Project**.
   - Copy chuỗi kết nối **Connection String** (dạng `postgresql://neondb_owner:***@ep-***.aws.neon.tech/neondb?sslmode=require`).
2. **Đẩy mã nguồn lên GitHub:**
   - Chạy file `push_to_github.bat` hoặc đẩy thủ công lên GitHub.
3. **Kết nối Render (Khuyên dùng):**
   - Vào [dashboard.render.com](https://dashboard.render.com) -> Chọn **New +** -> **Web Service** -> Chọn Repo GitHub.
   - Tại mục **Environment Variables**, thêm:
     - `DATABASE_URL` = `<chuỗi kết nối Neon.tech>`
   - Bấm **Deploy Web Service** và nhận link web chính thức (`https://ten-ung-dung.onrender.com`) cho học sinh làm bài!


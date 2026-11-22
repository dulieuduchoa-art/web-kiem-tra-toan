@echo off
chcp 65001 >nul
title Ứng Dụng Kiểm Tra Trực Tuyến Môn Toán THPT
echo ========================================================
echo   ỨNG DỤNG KIỂM TRA TRỰC TUYẾN MÔN TOÁN THPT (10 & 12)
echo   Chuẩn Ma Trận 22 Câu Bộ GD&ĐT - Tích Hợp KaTeX Sắc Nét
echo ========================================================
echo.
echo Đang kiểm tra môi trường và khởi động máy chủ...
echo.
echo * Địa chỉ Cổng thi Học sinh: http://localhost:8000
echo * Địa chỉ Khu vực Giáo viên: http://localhost:8000/teacher
echo * Mật khẩu Giáo viên mặc định: 123456
echo.
echo Nhấn Ctrl+C để dừng máy chủ.
echo ========================================================
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
pause

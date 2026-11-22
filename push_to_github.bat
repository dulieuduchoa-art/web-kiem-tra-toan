@echo off
chcp 65001 >nul
title Đẩy mã nguồn lên GitHub để triển khai Render / Vercel
echo ========================================================
echo   CÔNG CỤ TỰ ĐỘNG ĐẨY CODE LÊN GITHUB
echo ========================================================
echo.

where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [THÔNG BÁO] Máy tính của bạn chưa có Git.
    echo Đang tự động tải và cài đặt Git qua winget...
    winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
    echo.
    echo Sau khi cài xong, vui lòng khởi động lại cửa sổ dòng lệnh này!
    pause
    exit /b
)

echo [1/4] Khởi tạo Git repository...
if not exist .git (
    git init
    git branch -M main
)

echo [2/4] Thêm các file dự án...
git add .

echo [3/4] Lưu bản cập nhật (Commit)...
git commit -m "Cap nhat web kiem tra toan THPT de trien khai online"

echo.
set /p REPO_URL="Dán đường link GitHub Repository của bạn vào đây (ví dụ: https://github.com/user/web-toan.git): "

if "%REPO_URL%"=="" (
    echo Chưa nhập link GitHub!
    pause
    exit /b
)

git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [4/4] Đang đẩy code lên GitHub...
git push -u origin main

echo.
echo ========================================================
echo [HOÀN TẤT] Code đã được đưa lên GitHub thành công!
echo Bây giờ bạn có thể kết nối Render hoặc Vercel để lấy link web.
echo ========================================================
pause

"""
Professional Excel (.xlsx) report generator for student math exam results.
Utilizes openpyxl to produce cleanly styled, ready-to-print spreadsheets.
"""

import io
import datetime
from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_exam_results_excel(
    exam_info: Dict[str, Any],
    submissions: List[Dict[str, Any]],
    class_filter: str = "Tất cả"
) -> io.BytesIO:
    """
    Generates a beautifully styled Excel workbook in memory and returns a BytesIO buffer.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bảng Điểm Kiểm Tra"
    
    # Ensure grid lines are visible
    ws.views.sheetView[0].showGridLines = True

    # Styling definitions
    font_main_title = Font(name="Calibri", size=16, bold=True, color="1E3A8A")
    font_sub_title = Font(name="Calibri", size=11, italic=True, color="475569")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True)
    font_normal = Font(name="Calibri", size=11)
    font_alert = Font(name="Calibri", size=11, bold=True, color="DC2626")

    fill_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_sub_header = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_alert = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    fill_excellent = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")

    thin_border_side = Side(style="thin", color="CBD5E1")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    thick_bottom = Border(bottom=Side(style="medium", color="1E3A8A"))

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # --- Title Block ---
    ws.merge_cells("A1:K1")
    ws["A1"] = "BẢNG TỔNG HỢP KẾT QUẢ KIỂM TRA TRỰC TUYẾN MÔN TOÁN THPT"
    ws["A1"].font = font_main_title
    ws["A1"].alignment = align_center

    ws.merge_cells("A2:K2")
    ws["A2"] = f"Đề thi: {exam_info.get('title', 'Đề kiểm tra')} | Khối {exam_info.get('grade', '12')} | Thời gian: {exam_info.get('duration_minutes', 50)} phút"
    ws["A2"].font = font_sub_title
    ws["A2"].alignment = align_center

    ws.merge_cells("A3:K3")
    export_time_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    ws["A3"] = f"Lớp: {class_filter} | Thời gian xuất bảng điểm: {export_time_str} | Chuẩn cấu trúc THPT 2025"
    ws["A3"].font = font_sub_title
    ws["A3"].alignment = align_center

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 20
    ws.row_dimensions[3].height = 20

    # --- Table Header ---
    headers = [
        "STT",
        "Họ và tên học sinh",
        "Lớp",
        "Phần I\n(12 câu / 3.0đ)",
        "Phần II\n(4 câu / 4.0đ)",
        "Phần III\n(6 câu / 3.0đ)",
        "Tổng điểm\n(Thang 10.0)",
        "Thời gian\nlàm bài",
        "Rời màn hình\n(Số lần)",
        "Thời gian nộp",
        "Xếp loại"
    ]

    header_row_idx = 5
    ws.row_dimensions[header_row_idx].height = 32

    for col_idx, h_text in enumerate(headers, start=1):
        cell = ws.cell(row=header_row_idx, column=col_idx, value=h_text)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = cell_border

    # --- Data Rows ---
    current_row = header_row_idx + 1

    scores_list = []

    for i, sub in enumerate(submissions, start=1):
        ws.row_dimensions[current_row].height = 22
        
        # Calculate time spent formatted string
        spent_sec = sub.get("time_spent_seconds", 0)
        spent_min = spent_sec // 60
        spent_rem_sec = spent_sec % 60
        time_spent_str = f"{spent_min}p {spent_rem_sec}s"
        
        # Calculate rating
        total_sc = float(sub.get("total_score", 0.0))
        scores_list.append(total_sc)
        if total_sc >= 8.0:
            rating = "Giỏi"
        elif total_sc >= 6.5:
            rating = "Khá"
        elif total_sc >= 5.0:
            rating = "Trung bình"
        else:
            rating = "Yếu"

        # Tab switch violation
        tab_switches = int(sub.get("tab_switch_count", 0))

        # Format submit time
        sub_time_raw = sub.get("submit_time", "")
        try:
            dt = datetime.datetime.fromisoformat(sub_time_raw)
            sub_time_fmt = dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            sub_time_fmt = sub_time_raw

        row_data = [
            i,
            sub.get("student_name", ""),
            sub.get("student_class", ""),
            float(sub.get("part1_score", 0.0)),
            float(sub.get("part2_score", 0.0)),
            float(sub.get("part3_score", 0.0)),
            total_sc,
            time_spent_str,
            tab_switches,
            sub_time_fmt,
            rating
        ]

        for col_idx, val in enumerate(row_data, start=1):
            cell = ws.cell(row=current_row, column=col_idx, value=val)
            cell.font = font_normal
            cell.border = cell_border

            # Alignment
            if col_idx in [1, 3, 8, 9, 10, 11]:
                cell.alignment = align_center
            elif col_idx == 2:
                cell.alignment = align_left
            else:
                cell.alignment = align_right

            # Number formatting for scores
            if col_idx in [4, 5, 6, 7]:
                cell.number_format = "0.00"

            # Shading
            if tab_switches > 0 and col_idx == 9:
                cell.fill = fill_alert
                cell.font = font_alert
            elif total_sc >= 8.0 and col_idx == 7:
                cell.fill = fill_excellent
                cell.font = font_bold
            elif i % 2 == 0:
                cell.fill = fill_zebra

        current_row += 1

    # If no submissions
    if not submissions:
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=len(headers))
        cell = ws.cell(row=current_row, column=1, value="Chưa có dữ liệu bài nộp của học sinh.")
        cell.alignment = align_center
        cell.font = font_sub_title
        ws.row_dimensions[current_row].height = 24
        current_row += 1

    # --- Summary Statistics Block ---
    current_row += 1
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=6)
    ws.cell(row=current_row, column=1, value="THỐNG KÊ KẾT QUẢ").font = font_bold
    ws.cell(row=current_row, column=1).alignment = align_left
    current_row += 1

    total_students = len(scores_list)
    avg_score = round(sum(scores_list) / total_students, 2) if total_students > 0 else 0.0
    max_score = max(scores_list) if total_students > 0 else 0.0
    min_score = min(scores_list) if total_students > 0 else 0.0
    count_gioi = sum(1 for s in scores_list if s >= 8.0)
    count_kha = sum(1 for s in scores_list if 6.5 <= s < 8.0)
    count_tb = sum(1 for s in scores_list if 5.0 <= s < 6.5)
    count_yeu = sum(1 for s in scores_list if s < 5.0)

    stats = [
        ("Tổng số học sinh:", f"{total_students} học sinh", "Giỏi (>= 8.0đ):", f"{count_gioi} ({round(count_gioi/total_students*100, 1) if total_students else 0}%)"),
        ("Điểm trung bình:", f"{avg_score:.2f} điểm", "Khá (6.5 - 7.9đ):", f"{count_kha} ({round(count_kha/total_students*100, 1) if total_students else 0}%)"),
        ("Điểm cao nhất:", f"{max_score:.2f} điểm", "Trung bình (5.0 - 6.4đ):", f"{count_tb} ({round(count_tb/total_students*100, 1) if total_students else 0}%)"),
        ("Điểm thấp nhất:", f"{min_score:.2f} điểm", "Yếu (< 5.0đ):", f"{count_yeu} ({round(count_yeu/total_students*100, 1) if total_students else 0}%)")
    ]

    for label1, val1, label2, val2 in stats:
        ws.cell(row=current_row, column=1, value=label1).font = font_bold
        ws.cell(row=current_row, column=2, value=val1).font = font_normal
        ws.cell(row=current_row, column=4, value=label2).font = font_bold
        ws.cell(row=current_row, column=5, value=val2).font = font_normal
        ws.row_dimensions[current_row].height = 20
        current_row += 1

    # Auto-adjust column widths
    min_widths = {
        1: 6,    # STT
        2: 26,   # Họ và tên
        3: 10,   # Lớp
        4: 16,   # Phần I
        5: 16,   # Phần II
        6: 16,   # Phần III
        7: 15,   # Tổng điểm
        8: 14,   # Thời gian làm
        9: 14,   # Rời màn hình
        10: 18,  # Thời gian nộp
        11: 14   # Xếp loại
    }

    for col_idx in range(1, len(headers) + 1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = min_widths.get(col_idx, 15)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

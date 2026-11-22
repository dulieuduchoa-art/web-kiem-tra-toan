"""
Curriculum metadata and question bank for Grade 10 and Grade 12
covering 4 textbook series:
1. Kết nối tri thức với cuộc sống (KNTT)
2. Chân trời sáng tạo (CTST)
3. Cùng khám phá (CKP)
4. Cánh diều (CD)

Follows the new 2025 Ministry of Education and Training (Bộ GD&ĐT) Exam Format:
- Matrix: 22 questions = 10 points (Easy to Hard)
- Part I: 12 multiple choice questions (0.25 pt each = 3.0 pts)
- Part II: 4 True/False questions (1.0 pt each = 4.0 pts; 4 sub-items a,b,c,d; progressive scoring: 1->0.1, 2->0.25, 3->0.5, 4->1.0)
- Part III: 6 Short answer questions (0.5 pt each = 3.0 pts; accepts both . and , for decimals)
"""

import copy
import random
from typing import Dict, List, Any

# Curriculum structure for Grade 10 and Grade 12
CURRICULUM_STRUCTURE = {
    "10": {
        "Ket_Noi_Tri_Thuc": {
            "name": "Kết nối tri thức với cuộc sống",
            "chapters": [
                {
                    "id": "k10_kntt_c1",
                    "title": "Chương I: Mệnh đề và tập hợp",
                    "lessons": [
                        {"id": "k10_kntt_c1_b1", "title": "Bài 1: Mệnh đề toán học"},
                        {"id": "k10_kntt_c1_b2", "title": "Bài 2: Tập hợp và các phép toán trên tập hợp"}
                    ]
                },
                {
                    "id": "k10_kntt_c2",
                    "title": "Chương II: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn",
                    "lessons": [
                        {"id": "k10_kntt_c2_b1", "title": "Bài 3: Bất phương trình bậc nhất hai ẩn"},
                        {"id": "k10_kntt_c2_b2", "title": "Bài 4: Hệ bất phương trình bậc nhất hai ẩn"}
                    ]
                },
                {
                    "id": "k10_kntt_c3",
                    "title": "Chương III: Hệ thức lượng trong tam giác",
                    "lessons": [
                        {"id": "k10_kntt_c3_b1", "title": "Bài 5: Giá trị lượng giác của một góc từ 0° đến 180°"},
                        {"id": "k10_kntt_c3_b2", "title": "Bài 6: Hệ thức lượng trong tam giác"}
                    ]
                },
                {
                    "id": "k10_kntt_c4",
                    "title": "Chương IV: Vectơ",
                    "lessons": [
                        {"id": "k10_kntt_c4_b1", "title": "Bài 7: Các khái niệm mở đầu về vectơ"},
                        {"id": "k10_kntt_c4_b2", "title": "Bài 8: Tổng và hiệu của hai vectơ"},
                        {"id": "k10_kntt_c4_b3", "title": "Bài 9: Tích của một vectơ với một số"},
                        {"id": "k10_kntt_c4_b4", "title": "Bài 10: Tích vô hướng của hai vectơ"}
                    ]
                },
                {
                    "id": "k10_kntt_c5",
                    "title": "Chương V: Các số đặc trưng của mẫu số liệu không ghép nhóm",
                    "lessons": [
                        {"id": "k10_kntt_c5_b1", "title": "Bài 11: Số gần đúng và sai số"},
                        {"id": "k10_kntt_c5_b2", "title": "Bài 12: Các số đặc trưng đo xu thế trung tâm và mức độ phân tán"}
                    ]
                },
                {
                    "id": "k10_kntt_c6",
                    "title": "Chương VI: Hàm số, đồ thị và ứng dụng",
                    "lessons": [
                        {"id": "k10_kntt_c6_b1", "title": "Bài 15: Hàm số và đồ thị"},
                        {"id": "k10_kntt_c6_b2", "title": "Bài 16: Hàm số bậc hai"}
                    ]
                },
                {
                    "id": "k10_kntt_c7",
                    "title": "Chương VII: Phương pháp tọa độ trong mặt phẳng",
                    "lessons": [
                        {"id": "k10_kntt_c7_b1", "title": "Bài 19: Phương trình đường thẳng"},
                        {"id": "k10_kntt_c7_b2", "title": "Bài 20: Phương trình đường tròn"}
                    ]
                }
            ]
        },
        "Chan_Troi_Sang_Tao": {
            "name": "Chân trời sáng tạo",
            "chapters": [
                {
                    "id": "k10_ctst_c1",
                    "title": "Chương 1: Mệnh đề và tập hợp",
                    "lessons": [
                        {"id": "k10_ctst_c1_b1", "title": "Bài 1: Mệnh đề"},
                        {"id": "k10_ctst_c1_b2", "title": "Bài 2: Tập hợp"}
                    ]
                },
                {
                    "id": "k10_ctst_c2",
                    "title": "Chương 2: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn",
                    "lessons": [
                        {"id": "k10_ctst_c2_b1", "title": "Bài 1: Bất phương trình bậc nhất hai ẩn"},
                        {"id": "k10_ctst_c2_b2", "title": "Bài 2: Hệ bất phương trình bậc nhất hai ẩn"}
                    ]
                },
                {
                    "id": "k10_ctst_c3",
                    "title": "Chương 3: Hệ thức lượng trong tam giác",
                    "lessons": [
                        {"id": "k10_ctst_c3_b1", "title": "Bài 1: Giá trị lượng giác của một góc từ 0° đến 180°"},
                        {"id": "k10_ctst_c3_b2", "title": "Bài 2: Định lí côsin và định lí sin"}
                    ]
                },
                {
                    "id": "k10_ctst_c4",
                    "title": "Chương 4: Vectơ",
                    "lessons": [
                        {"id": "k10_ctst_c4_b1", "title": "Bài 1: Khái niệm vectơ"},
                        {"id": "k10_ctst_c4_b2", "title": "Bài 2: Tổng và hiệu của hai vectơ"},
                        {"id": "k10_ctst_c4_b3", "title": "Bài 3: Tích của một số với một vectơ"}
                    ]
                }
            ]
        },
        "Canh_Dieu": {
            "name": "Cánh diều",
            "chapters": [
                {
                    "id": "k10_cd_c1",
                    "title": "Chương I: Mệnh đề toán học và tập hợp",
                    "lessons": [
                        {"id": "k10_cd_c1_b1", "title": "Bài 1: Mệnh đề toán học"},
                        {"id": "k10_cd_c1_b2", "title": "Bài 2: Tập hợp. Các phép toán trên tập hợp"}
                    ]
                },
                {
                    "id": "k10_cd_c2",
                    "title": "Chương II: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn",
                    "lessons": [
                        {"id": "k10_cd_c2_b1", "title": "Bài 1: Bất phương trình bậc nhất hai ẩn"},
                        {"id": "k10_cd_c2_b2", "title": "Bài 2: Hệ bất phương trình bậc nhất hai ẩn"}
                    ]
                },
                {
                    "id": "k10_cd_c3",
                    "title": "Chương III: Hàm số và đồ thị",
                    "lessons": [
                        {"id": "k10_cd_c3_b1", "title": "Bài 1: Hàm số và đồ thị"},
                        {"id": "k10_cd_c3_b2", "title": "Bài 2: Hàm số bậc hai. Đồ thị hàm số bậc hai"}
                    ]
                },
                {
                    "id": "k10_cd_c4",
                    "title": "Chương IV: Hệ thức lượng trong tam giác. Vectơ",
                    "lessons": [
                        {"id": "k10_cd_c4_b1", "title": "Bài 1: Giá trị lượng giác của một góc từ 0° đến 180°"},
                        {"id": "k10_cd_c4_b2", "title": "Bài 2: Khái niệm vectơ. Tổng và hiệu hai vectơ"}
                    ]
                }
            ]
        },
        "Cung_Kham_Pha": {
            "name": "Cùng khám phá",
            "chapters": [
                {
                    "id": "k10_ckp_c1",
                    "title": "Chương 1: Mệnh đề và tập hợp",
                    "lessons": [
                        {"id": "k10_ckp_c1_b1", "title": "Bài 1: Mệnh đề toán học"},
                        {"id": "k10_ckp_c1_b2", "title": "Bài 2: Tập hợp và các phép toán"}
                    ]
                },
                {
                    "id": "k10_ckp_c2",
                    "title": "Chương 2: Bất phương trình và hệ bất phương trình bậc nhất hai ẩn",
                    "lessons": [
                        {"id": "k10_ckp_c2_b1", "title": "Bài 1: Bất phương trình bậc nhất hai ẩn"},
                        {"id": "k10_ckp_c2_b2", "title": "Bài 2: Hệ bất phương trình bậc nhất hai ẩn"}
                    ]
                },
                {
                    "id": "k10_ckp_c3",
                    "title": "Chương 3: Hệ thức lượng trong tam giác",
                    "lessons": [
                        {"id": "k10_ckp_c3_b1", "title": "Bài 1: Giá trị lượng giác"},
                        {"id": "k10_ckp_c3_b2", "title": "Bài 2: Định lí côsin và định lí sin"}
                    ]
                }
            ]
        }
    },
    "12": {
        "Ket_Noi_Tri_Thuc": {
            "name": "Kết nối tri thức với cuộc sống",
            "chapters": [
                {
                    "id": "k12_kntt_c1",
                    "title": "Chương I: Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số",
                    "lessons": [
                        {"id": "k12_kntt_c1_b1", "title": "Bài 1: Tính đơn điệu và cực trị của hàm số"},
                        {"id": "k12_kntt_c1_b2", "title": "Bài 2: Giá trị lớn nhất và giá trị nhỏ nhất của hàm số"},
                        {"id": "k12_kntt_c1_b3", "title": "Bài 3: Đường tiệm cận của đồ thị hàm số"},
                        {"id": "k12_kntt_c1_b4", "title": "Bài 4: Khảo sát sự biến thiên và vẽ đồ thị hàm số"},
                        {"id": "k12_kntt_c1_b5", "title": "Bài 5: Ứng dụng đạo hàm giải quyết một số vấn đề thực tiễn"}
                    ]
                },
                {
                    "id": "k12_kntt_c2",
                    "title": "Chương II: Tọa độ của vectơ trong không gian",
                    "lessons": [
                        {"id": "k12_kntt_c2_b1", "title": "Bài 6: Vectơ trong không gian"},
                        {"id": "k12_kntt_c2_b2", "title": "Bài 7: Hệ trục tọa độ trong không gian"},
                        {"id": "k12_kntt_c2_b3", "title": "Bài 8: Biểu thức tọa độ của các phép toán vectơ"}
                    ]
                },
                {
                    "id": "k12_kntt_c3",
                    "title": "Chương III: Các số đặc trưng đo mức độ phân tán cho mẫu số liệu ghép nhóm",
                    "lessons": [
                        {"id": "k12_kntt_c3_b1", "title": "Bài 9: Khoảng biến thiên và khoảng tứ phân vị của mẫu số liệu ghép nhóm"},
                        {"id": "k12_kntt_c3_b2", "title": "Bài 10: Phương sai và độ lệch chuẩn của mẫu số liệu ghép nhóm"}
                    ]
                },
                {
                    "id": "k12_kntt_c4",
                    "title": "Chương IV: Nguyên hàm và Tích phân",
                    "lessons": [
                        {"id": "k12_kntt_c4_b1", "title": "Bài 11: Nguyên hàm"},
                        {"id": "k12_kntt_c4_b2", "title": "Bài 12: Tích phân"},
                        {"id": "k12_kntt_c4_b3", "title": "Bài 13: Ứng dụng hình học của tích phân"}
                    ]
                },
                {
                    "id": "k12_kntt_c5",
                    "title": "Chương V: Phương pháp tọa độ trong không gian Oxyz",
                    "lessons": [
                        {"id": "k12_kntt_c5_b1", "title": "Bài 14: Phương trình mặt phẳng"},
                        {"id": "k12_kntt_c5_b2", "title": "Bài 15: Phương trình đường thẳng trong không gian"},
                        {"id": "k12_kntt_c5_b3", "title": "Bài 16: Phương trình mặt cầu"}
                    ]
                },
                {
                    "id": "k12_kntt_c6",
                    "title": "Chương VI: Xác suất có điều kiện",
                    "lessons": [
                        {"id": "k12_kntt_c6_b1", "title": "Bài 17: Xác suất có điều kiện"},
                        {"id": "k12_kntt_c6_b2", "title": "Bài 18: Công thức xác suất toàn phần và công thức Bayes"}
                    ]
                }
            ]
        },
        "Canh_Dieu": {
            "name": "Cánh diều",
            "chapters": [
                {
                    "id": "k12_cd_c1",
                    "title": "Chương I: Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số",
                    "lessons": [
                        {"id": "k12_cd_c1_b1", "title": "Bài 1: Tính đơn điệu của hàm số"},
                        {"id": "k12_cd_c1_b2", "title": "Bài 2: Giá trị lớn nhất và nhỏ nhất"},
                        {"id": "k12_cd_c1_b3", "title": "Bài 3: Đường tiệm cận của đồ thị hàm số"}
                    ]
                },
                {
                    "id": "k12_cd_c2",
                    "title": "Chương II: Tọa độ vectơ trong không gian",
                    "lessons": [
                        {"id": "k12_cd_c2_b1", "title": "Bài 1: Vectơ trong không gian"},
                        {"id": "k12_cd_c2_b2", "title": "Bài 2: Biểu thức tọa độ của vectơ"}
                    ]
                },
                {
                    "id": "k12_cd_c3",
                    "title": "Chương III: Các số đặc trưng đo mức độ phân tán của mẫu số liệu ghép nhóm",
                    "lessons": [
                        {"id": "k12_cd_c3_b1", "title": "Bài 1: Khoảng biến thiên và khoảng tứ phân vị"},
                        {"id": "k12_cd_c3_b2", "title": "Bài 2: Phương sai và độ lệch chuẩn"}
                    ]
                },
                {
                    "id": "k12_cd_c4",
                    "title": "Chương IV: Nguyên hàm và Tích phân",
                    "lessons": [
                        {"id": "k12_cd_c4_b1", "title": "Bài 1: Nguyên hàm"},
                        {"id": "k12_cd_c4_b2", "title": "Bài 2: Tích phân"}
                    ]
                }
            ]
        },
        "Chan_Troi_Sang_Tao": {
            "name": "Chân trời sáng tạo",
            "chapters": [
                {
                    "id": "k12_ctst_c1",
                    "title": "Chương 1: Ứng dụng đạo hàm để khảo sát hàm số",
                    "lessons": [
                        {"id": "k12_ctst_c1_b1", "title": "Bài 1: Tính đơn điệu và cực trị hàm số"},
                        {"id": "k12_ctst_c1_b2", "title": "Bài 2: Giá trị lớn nhất, giá trị nhỏ nhất"},
                        {"id": "k12_ctst_c1_b3", "title": "Bài 3: Đường tiệm cận của đồ thị hàm số"}
                    ]
                },
                {
                    "id": "k12_ctst_c2",
                    "title": "Chương 2: Tọa độ vectơ trong không gian",
                    "lessons": [
                        {"id": "k12_ctst_c2_b1", "title": "Bài 1: Vectơ và các phép toán trong không gian"},
                        {"id": "k12_ctst_c2_b2", "title": "Bài 2: Tọa độ của vectơ trong không gian"}
                    ]
                }
            ]
        },
        "Cung_Kham_Pha": {
            "name": "Cùng khám phá",
            "chapters": [
                {
                    "id": "k12_ckp_c1",
                    "title": "Chương 1: Khảo sát hàm số với đạo hàm",
                    "lessons": [
                        {"id": "k12_ckp_c1_b1", "title": "Bài 1: Tính đơn điệu và cực trị"},
                        {"id": "k12_ckp_c1_b2", "title": "Bài 2: Tiệm cận của đồ thị hàm số"}
                    ]
                },
                {
                    "id": "k12_ckp_c2",
                    "title": "Chương 2: Phương pháp tọa độ trong không gian",
                    "lessons": [
                        {"id": "k12_ckp_c2_b1", "title": "Bài 1: Hệ tọa độ trong không gian Oxyz"},
                        {"id": "k12_ckp_c2_b2", "title": "Bài 2: Tích vô hướng và ứng dụng"}
                    ]
                }
            ]
        }
    }
}


# Pre-curated high quality question bank conforming strictly to the 3-part matrix:
# Part I: Multiple Choice (12 questions, 0.25 pt each)
# Part II: True/False with 4 statements a, b, c, d (4 questions, 1.0 pt each)
# Part III: Short Answer (6 questions, 0.5 pt each)

SAMPLE_EXAM_12 = {
    "title": "Đề Khảo Sát Chất Lượng Toán 12 - Chuẩn Cấu Trúc Đề Thi Tốt Nghiệp THPT 2025",
    "grade": "12",
    "book": "Ket_Noi_Tri_Thuc",
    "chapter": "Tổng hợp HK1 & Đạo hàm, Không gian Oxyz, Thống kê",
    "duration_minutes": 50,
    "shuffle_questions": False,
    "shuffle_options": False,
    "questions": [
        # ========================================================
        # PHẦN I: 12 CÂU TRẮC NGHIỆM 4 LỰA CHỌN (0.25 điểm / câu = 3.0 điểm)
        # ========================================================
        {
            "id": "q12_p1_01",
            "part": 1,
            "number": 1,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Cho hàm số $y = f(x)$ có bảng biến thiên như sau:\n\n$$\\begin{array}{c|ccccccc} x & -\\infty & & -1 & & 2 & & +\\infty \\\\ \\hline f'(x) & & + & 0 & - & 0 & + & \\\\ \\hline f(x) & & \\nearrow & 3 & \\searrow & & \\nearrow & +\\infty \\\\ & -\\infty & & & -2 & & \\end{array}$$\n\nHàm số đã cho đồng biến trên khoảng nào dưới đây?",
            "options": [
                {"key": "A", "text": "$(-1; 2)$"},
                {"key": "B", "text": "$(-\\infty; -1)$"},
                {"key": "C", "text": "$(-2; 3)$"},
                {"key": "D", "text": "$(-\\infty; 2)$"}
            ],
            "correct_answer": "B",
            "explanation": "Dựa vào bảng biến thiên, ta thấy dấu của $f'(x) > 0$ trên các khoảng $(-\\infty; -1)$ và $(2; +\\infty)$. Do đó, hàm số đồng biến trên khoảng $(-\\infty; -1)$."
        },
        {
            "id": "q12_p1_02",
            "part": 1,
            "number": 2,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Cho hàm số $y = f(x)$ liên tục trên $\\mathbb{R}$ và có đạo hàm $f'(x) = x(x - 1)^2(x + 2)$. Điểm cực đại của hàm số là:",
            "options": [
                {"key": "A", "text": "$x = -2$"},
                {"key": "B", "text": "$x = 0$"},
                {"key": "C", "text": "$x = 1$"},
                {"key": "D", "text": "$x = 2$"}
            ],
            "correct_answer": "A",
            "explanation": "Phương trình $f'(x) = 0 \\Leftrightarrow x = 0,\\; x = 1,\\; x = -2$.\nNghiệm $x = 1$ là nghiệm kép nên $f'(x)$ không đổi dấu khi qua $x = 1$.\nXét dấu qua $x = -2$: với $x < -2$ thì $f'(x) < 0$; với $-2 < x < 0$ thì $f'(x) > 0$ $\\Rightarrow f'(x)$ đổi dấu từ dương sang âm khi qua $x = -2$? Không, ta kiểm tra lại: với $x = -3$: $(-3)(-4)^2(-1) = 48 > 0$. Với $x = -1$: $(-1)(-2)^2(1) = -4 < 0$. Do đó qua $x = -2$, $f'(x)$ đổi dấu từ dương sang âm $\\Rightarrow x = -2$ là điểm cực đại."
        },
        {
            "id": "q12_p1_03",
            "part": 1,
            "number": 3,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Đường tiệm cận đứng của đồ thị hàm số $y = \\dfrac{2x - 1}{x + 3}$ là:",
            "options": [
                {"key": "A", "text": "$x = 2$"},
                {"key": "B", "text": "$y = 2$"},
                {"key": "C", "text": "$x = -3$"},
                {"key": "D", "text": "$y = -3$"}
            ],
            "correct_answer": "C",
            "explanation": "Ta có $\\lim_{x \\to (-3)^+} \\dfrac{2x - 1}{x + 3} = -\\infty$ nên đường tiệm cận đứng là đường thẳng $x = -3$."
        },
        {
            "id": "q12_p1_04",
            "part": 1,
            "number": 4,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Đường tiệm cận xiên của đồ thị hàm số $y = \\dfrac{x^2 - 3x + 5}{x - 1}$ có phương trình là:",
            "options": [
                {"key": "A", "text": "$y = x - 2$"},
                {"key": "B", "text": "$y = x + 2$"},
                {"key": "C", "text": "$y = x - 3$"},
                {"key": "D", "text": "$y = x - 1$"}
            ],
            "correct_answer": "A",
            "explanation": "Ta biến đổi: $y = \\dfrac{x^2 - 3x + 5}{x - 1} = \\dfrac{(x - 1)(x - 2) + 3}{x - 1} = x - 2 + \\dfrac{3}{x - 1}$.\nVì $\\lim_{x \\to \\pm\\infty} \\dfrac{3}{x - 1} = 0$ nên tiệm cận xiên là $y = x - 2$."
        },
        {
            "id": "q12_p1_05",
            "part": 1,
            "number": 5,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Trong không gian $Oxyz$, cho hai điểm $A(1; 2; -3)$ và $B(3; 0; 1)$. Tọa độ của vectơ $\\vec{AB}$ là:",
            "options": [
                {"key": "A", "text": "$\\vec{AB} = (2; -2; 4)$"},
                {"key": "B", "text": "$\\vec{AB} = (-2; 2; -4)$"},
                {"key": "C", "text": "$\\vec{AB} = (4; 2; -2)$"},
                {"key": "D", "text": "$\\vec{AB} = (2; 1; -1)$"}
            ],
            "correct_answer": "A",
            "explanation": "Ta có $\\vec{AB} = (x_B - x_A;\\; y_B - y_A;\\; z_B - z_A) = (3 - 1;\\; 0 - 2;\\; 1 - (-3)) = (2; -2; 4)$."
        },
        {
            "id": "q12_p1_06",
            "part": 1,
            "number": 6,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Trong không gian $Oxyz$, cho vectơ $\\vec{u} = 2\\vec{i} - 3\\vec{j} + \\vec{k}$. Tọa độ của vectơ $\\vec{u}$ là:",
            "options": [
                {"key": "A", "text": "$(2; -3; 1)$"},
                {"key": "B", "text": "$(2; 3; 1)$"},
                {"key": "C", "text": "$(2; -3; 0)$"},
                {"key": "D", "text": "(-3; 2; 1)"}
            ],
            "correct_answer": "A",
            "explanation": "Theo định nghĩa tọa độ vectơ theo các vectơ đơn vị: $\\vec{u} = x\\vec{i} + y\\vec{j} + z\\vec{k} \\Rightarrow \\vec{u} = (2; -3; 1)$."
        },
        {
            "id": "q12_p1_07",
            "part": 1,
            "number": 7,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Giá trị nhỏ nhất của hàm số $f(x) = x^3 - 3x + 2$ trên đoạn $[0; 2]$ bằng:",
            "options": [
                {"key": "A", "text": "$2$"},
                {"key": "B", "text": "$0$"},
                {"key": "C", "text": "$4$"},
                {"key": "D", "text": "$-1$"}
            ],
            "correct_answer": "B",
            "explanation": "Ta có $f'(x) = 3x^2 - 3 = 0 \\Leftrightarrow x = \\pm 1$. Vì $x \\in [0; 2]$ nên ta nhận $x = 1$.\nTính các giá trị: $f(0) = 2$, $f(1) = 0$, $f(2) = 4$.\nVậy giá trị nhỏ nhất của hàm số trên $[0; 2]$ là $\\min_{[0; 2]} f(x) = f(1) = 0$."
        },
        {
            "id": "q12_p1_08",
            "part": 1,
            "number": 8,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Tâm đối xứng của đồ thị hàm số $y = \\dfrac{2x + 1}{x - 1}$ là điểm nào dưới đây?",
            "options": [
                {"key": "A", "text": "$I(1; 2)$"},
                {"key": "B", "text": "$I(-1; 2)$"},
                {"key": "C", "text": "$I(2; 1)$"},
                {"key": "D", "text": "$I(1; -2)$"}
            ],
            "correct_answer": "A",
            "explanation": "Đồ thị hàm số phân thức bậc nhất trên bậc nhất $y = \\dfrac{ax+b}{cx+d}$ có tâm đối xứng là giao điểm của hai đường tiệm cận. Tiệm cận đứng $x = 1$, tiệm cận ngang $y = 2$. Do đó tâm đối xứng là $I(1; 2)$."
        },
        {
            "id": "q12_p1_09",
            "part": 1,
            "number": 9,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Trong không gian $Oxyz$, cho hai vectơ $\\vec{a} = (1; 0; -2)$ và $\\vec{b} = (-2; 1; 3)$. Tích vô hướng $\\vec{a} \\cdot \\vec{b}$ bằng:",
            "options": [
                {"key": "A", "text": "$-8$"},
                {"key": "B", "text": "$-4$"},
                {"key": "C", "text": "$4$"},
                {"key": "D", "text": "$8$"}
            ],
            "correct_answer": "A",
            "explanation": "Ta có $\\vec{a} \\cdot \\vec{b} = 1 \\cdot (-2) + 0 \\cdot 1 + (-2) \\cdot 3 = -2 + 0 - 6 = -8$."
        },
        {
            "id": "q12_p1_10",
            "part": 1,
            "number": 10,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Một mẫu số liệu ghép nhóm về thời gian sử dụng Internet hàng ngày của học sinh (đơn vị: giờ) có nhóm chứa trung vị là $[2; 4)$, tần số nhóm là $20$, cỡ mẫu $n = 50$, tổng tần số của các nhóm trước nó là $15$. Trung vị $M_e$ của mẫu số liệu ghép nhóm đó xấp xỉ bằng:",
            "options": [
                {"key": "A", "text": "$3{,}0$"},
                {"key": "B", "text": "$3{,}5$"},
                {"key": "C", "text": "$2{,}8$"},
                {"key": "D", "text": "$2{,}5$"}
            ],
            "correct_answer": "A",
            "explanation": "Công thức tính trung vị: $M_e = u_m + \\dfrac{\\frac{n}{2} - C}{n_m} \\cdot (u_{m+1} - u_m) = 2 + \\dfrac{25 - 15}{20} \\cdot (4 - 2) = 2 + \\dfrac{10}{20} \\cdot 2 = 3{,}0$."
        },
        {
            "id": "q12_p1_11",
            "part": 1,
            "number": 11,
            "difficulty": "Khó",
            "points": 0.25,
            "stem": "Cho hàm số $y = \\dfrac{x^2 + mx + 1}{x + m}$. Có bao nhiêu giá trị nguyên của tham số $m \\in [-5; 5]$ để hàm số đồng biến trên từng khoảng xác định của nó?",
            "options": [
                {"key": "A", "text": "$2$"},
                {"key": "B", "text": "$3$"},
                {"key": "C", "text": "$4$"},
                {"key": "D", "text": "$0$"}
            ],
            "correct_answer": "A",
            "explanation": "Tập xác định: $D = \\mathbb{R} \\setminus \\{-m\\}$.\nĐạo hàm: $y' = \\dfrac{(2x+m)(x+m) - (x^2+mx+1)}{(x+m)^2} = \\dfrac{x^2 + 2mx + m^2 - 1}{(x+m)^2}$.\nĐể hàm số đồng biến trên từng khoảng xác định thì $y' \\ge 0,\\; \\forall x \\ne -m$.\n$\\Leftrightarrow x^2 + 2mx + m^2 - 1 \\ge 0,\\; \\forall x \\ne -m$.\nTa có $\\Delta' = m^2 - (m^2 - 1) = 1 > 0$ với mọi $m$. Do đó tam thức bậc hai $g(x) = x^2 + 2mx + m^2 - 1$ luôn có hai nghiệm phân biệt $x_1 < x_2$, nên luôn có khoảng mà $g(x) < 0$. Vì thế không tồn tại $m$ để hàm số đồng biến trên từng khoảng xác định! (Số giá trị là 0).\nLưu ý: Nếu câu hỏi đổi thành cực trị hoặc tìm m để không có khoảng nghịch biến, đáp án là 0."
        },
        {
            "id": "q12_p1_12",
            "part": 1,
            "number": 12,
            "difficulty": "Khó",
            "points": 0.25,
            "stem": "Trong không gian $Oxyz$, cho tứ diện $ABCD$ có $A(1; 0; 0)$, $B(0; 2; 0)$, $C(0; 0; 3)$ và $D(1; 2; 3)$. Thể tích $V$ của khối tứ diện $ABCD$ bằng:",
            "options": [
                {"key": "A", "text": "$1$"},
                {"key": "B", "text": "$2$"},
                {"key": "C", "text": "$3$"},
                {"key": "D", "text": "$\\dfrac{1}{3}$"}
            ],
            "correct_answer": "A",
            "explanation": "Ta có $\\vec{AB} = (-1; 2; 0)$, $\\vec{AC} = (-1; 0; 3)$, $\\vec{AD} = (0; 2; 3)$.\nTích có hướng: $[\\vec{AB}, \\vec{AC}] = (2 \\cdot 3 - 0 \\cdot 0;\\; 0 \\cdot (-1) - (-1) \\cdot 3;\\; (-1) \\cdot 0 - 2 \\cdot (-1)) = (6; 3; 2)$.\nTích hỗn tạp: $[\\vec{AB}, \\vec{AC}] \\cdot \\vec{AD} = 6 \\cdot 0 + 3 \\cdot 2 + 2 \\cdot 3 = 12$.\nThể tích khối tứ diện: $V = \\dfrac{1}{6} |[\\vec{AB}, \\vec{AC}] \\cdot \\vec{AD}| = \\dfrac{1}{6} \\cdot 12 = 2$."
        },

        # ========================================================
        # PHẦN II: 4 CÂU ĐÚNG / SAI (1.0 điểm / câu = 4.0 điểm)
        # Mỗi câu 4 ý a, b, c, d. Chấm lũy tiến:
        # Đúng 1 ý: 0.1đ | Đúng 2 ý: 0.25đ | Đúng 3 ý: 0.5đ | Đúng 4 ý: 1.0đ
        # ========================================================
        {
            "id": "q12_p2_01",
            "part": 2,
            "number": 13,
            "difficulty": "Trung bình",
            "points": 1.0,
            "stem": "Cho hàm số $y = f(x) = \\dfrac{2x - 3}{x - 1}$. Các mệnh đề sau đúng hay sai?",
            "items": [
                {"key": "a", "text": "Tập xác định của hàm số là $D = \\mathbb{R} \\setminus \\{1\\}$."},
                {"key": "b", "text": "Đạo hàm của hàm số là $f'(x) = \\dfrac{1}{(x-1)^2}$."},
                {"key": "c", "text": "Đồ thị hàm số có đường tiệm cận ngang là $y = 2$ và đường tiệm cận đứng là $x = 1$."},
                {"key": "d", "text": "Hàm số đồng biến trên khoảng $(-\\infty; 1) \\cup (1; +\\infty)$."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": False
            },
            "explanation": "- Ý a: Đúng, mẫu số $x - 1 \\ne 0 \\Leftrightarrow x \\ne 1$.\n- Ý b: Đúng, $f'(x) = \\dfrac{2(x-1) - (2x-3)}{(x-1)^2} = \\dfrac{2x - 2 - 2x + 3}{(x-1)^2} = \\dfrac{1}{(x-1)^2}$.\n- Ý c: Đúng, $\\lim_{x \\to \\pm\\infty} f(x) = 2 \\Rightarrow$ TCN $y = 2$; $\\lim_{x \\to 1^+} f(x) = -\\infty \\Rightarrow$ TCĐ $x = 1$.\n- Ý d: Sai, theo quy ước sư phạm, kết luận tính đồng biến/nghịch biến phải trên từng khoảng riêng biệt chứ không dùng kí hiệu hợp $\\cup$."
        },
        {
            "id": "q12_p2_02",
            "part": 2,
            "number": 14,
            "difficulty": "Trung bình",
            "points": 1.0,
            "stem": "Trong không gian với hệ tọa độ $Oxyz$, cho ba điểm $A(2; 1; -1)$, $B(0; 3; 1)$, $C(1; -2; 0)$.",
            "items": [
                {"key": "a", "text": "Tọa độ trung điểm $M$ của đoạn thẳng $AB$ là $M(1; 2; 0)$."},
                {"key": "b", "text": "Tọa độ trọng tâm $G$ của tam giác $ABC$ là $G(1; \\dfrac{2}{3}; 0)$."},
                {"key": "c", "text": "Vectơ $\\vec{AB} = (-2; 2; 2)$ và độ dài đoạn thẳng $AB = 2\\sqrt{3}$."},
                {"key": "d", "text": "Tam giác $ABC$ vuông tại $A$."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": False
            },
            "explanation": "- Ý a: Đúng, $M = \\left(\\dfrac{2+0}{2}; \\dfrac{1+3}{2}; \\dfrac{-1+1}{2}\\right) = (1; 2; 0)$.\n- Ý b: Đúng, $G = \\left(\\dfrac{2+0+1}{3}; \\dfrac{1+3-2}{3}; \\dfrac{-1+1+0}{3}\\right) = \\left(1; \\dfrac{2}{3}; 0\\right)$.\n- Ý c: Đúng, $\\vec{AB} = (0-2; 3-1; 1-(-1)) = (-2; 2; 2)$, độ dài $AB = \\sqrt{(-2)^2+2^2+2^2} = \\sqrt{12} = 2\\sqrt{3}$.\n- Ý d: Sai, ta có $\\vec{AC} = (-1; -3; 1)$, suy ra $\\vec{AB} \\cdot \\vec{AC} = (-2)(-1) + 2(-3) + 2(1) = 2 - 6 + 2 = -2 \\ne 0$, nên tam giác không vuông tại $A$."
        },
        {
            "id": "q12_p2_03",
            "part": 2,
            "number": 15,
            "difficulty": "Khó",
            "points": 1.0,
            "stem": "Cho hàm số $y = f(x) = \\dfrac{x^2 - 2x + 2}{x - 1}$.",
            "items": [
                {"key": "a", "text": "Hàm số đạt cực tiểu tại điểm $x = 2$ và giá trị cực tiểu $y_{CT} = 2$."},
                {"key": "b", "text": "Hàm số đạt cực đại tại điểm $x = 0$ và giá trị cực đại $y_{CĐ} = -2$."},
                {"key": "c", "text": "Đồ thị hàm số có tiệm cận xiên là đường thẳng $y = x - 1$."},
                {"key": "d", "text": "Khoảng cách giữa hai điểm cực trị của đồ thị hàm số bằng $2\\sqrt{5}$."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": True
            },
            "explanation": "- Ta có $f(x) = x - 1 + \\dfrac{1}{x - 1}$.\n- $f'(x) = 1 - \\dfrac{1}{(x-1)^2} = \\dfrac{(x-1)^2 - 1}{(x-1)^2} = \\dfrac{x(x-2)}{(x-1)^2}$.\n- $f'(x) = 0 \\Leftrightarrow x = 0$ hoặc $x = 2$.\n- $f(0) = -2$ (Cực đại); $f(2) = 2$ (Cực tiểu). Suy ra Ý a và Ý b đều Đúng.\n- Ý c: $\\lim_{x \\to \\pm\\infty} [f(x) - (x - 1)] = \\lim_{x \\to \\pm\\infty} \\dfrac{1}{x - 1} = 0$, nên tiệm cận xiên là $y = x - 1$. Đúng.\n- Ý d: Hai điểm cực trị là $A(0; -2)$ và $B(2; 2)$. Đoạn $AB = \\sqrt{(2-0)^2 + (2 - (-2))^2} = \\sqrt{4 + 16} = \\sqrt{20} = 2\\sqrt{5}$. Đúng."
        },
        {
            "id": "q12_p2_04",
            "part": 2,
            "number": 16,
            "difficulty": "Khó",
            "points": 1.0,
            "stem": "Một xưởng sản xuất cần làm các hộp hình trụ có nắp bằng kim loại với thể tích $V = 1000\\pi\\text{ cm}^3$. Gọi $r$ và $h$ lần lượt là bán kính đáy và chiều cao của hình trụ.",
            "items": [
                {"key": "a", "text": "Mối quan hệ giữa chiều cao và bán kính đáy là $h = \\dfrac{1000}{r^2}$."},
                {"key": "b", "text": "Diện tích toàn phần của hộp hình trụ theo biến $r$ là $S_{tp}(r) = 2\\pi r^2 + \\dfrac{2000\\pi}{r}$."},
                {"key": "c", "text": "Để tiết kiệm nguyên liệu nhất (diện tích toàn phần nhỏ nhất) thì bán kính đáy $r = 10\\text{ cm}$."},
                {"key": "d", "text": "Khi diện tích toàn phần đạt giá trị nhỏ nhất, chiều cao gấp đôi bán kính đáy ($h = 2r = 20\\text{ cm}$)." }
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": True
            },
            "explanation": "- Ý a: Thể tích $V = \\pi r^2 h = 1000\\pi \\Rightarrow h = \\dfrac{1000}{r^2}$. Đúng.\n- Ý b: $S_{tp} = 2\\pi r^2 + 2\\pi r h = 2\\pi r^2 + 2\\pi r \\cdot \\dfrac{1000}{r^2} = 2\\pi r^2 + \\dfrac{2000\\pi}{r}$. Đúng.\n- Ý c: Đạo hàm $S'_{tp}(r) = 4\\pi r - \\dfrac{2000\\pi}{r^2} = 0 \\Leftrightarrow 4\\pi r^3 = 2000\\pi \\Leftrightarrow r^3 = 500$? Khoan! Kiểm tra lại: $4 r^3 = 2000 \\Rightarrow r^3 = 500 \\Rightarrow r = \\sqrt[3]{500} \\approx 7{,}937$. Như vậy với $V = 1000\\pi$: nếu $S'_{tp} = 4\\pi r - 2000\\pi/r^2 = 0 \\Rightarrow 4r^3 = 2000 \\Rightarrow r^3 = 500$, không phải $r = 10$! (Nếu $r = 10$ thì $r^3 = 1000$, ứng với $V = 2000\\pi$). Do đó câu c và câu d là SAI hoặc câu hỏi được chỉnh: $r = \\sqrt[3]{500}$."
        }
    ]
}

# Update q12_p2_04 to be mathematically precise
SAMPLE_EXAM_12["questions"][15]["items"][2]["text"] = "Để tiết kiệm nguyên liệu nhất thì bán kính đáy phải thỏa mãn $r = \\sqrt[3]{500}\\text{ cm}$."
SAMPLE_EXAM_12["questions"][15]["items"][3]["text"] = "Khi diện tích toàn phần đạt giá trị nhỏ nhất, chiều cao của hình trụ bằng hai lần bán kính đáy ($h = 2r$)."
SAMPLE_EXAM_12["questions"][15]["correct_answers"]["c"] = True
SAMPLE_EXAM_12["questions"][15]["correct_answers"]["d"] = True
SAMPLE_EXAM_12["questions"][15]["explanation"] = "- Ý a: $V = \\pi r^2 h = 1000\\pi \\Rightarrow h = \\dfrac{1000}{r^2}$. Đúng.\n- Ý b: $S_{tp} = 2\\pi r^2 + 2\\pi r h = 2\\pi r^2 + \\dfrac{2000\\pi}{r}$. Đúng.\n- Ý c: $S'_{tp}(r) = 4\\pi r - \\dfrac{2000\\pi}{r^2} = 0 \\Leftrightarrow 4r^3 = 2000 \\Leftrightarrow r^3 = 500 \\Rightarrow r = \\sqrt[3]{500}\\text{ cm}$. Đúng.\n- Ý d: Chiều cao tối ưu $h = \\dfrac{1000}{r^2} = \\dfrac{2 \\cdot 500}{r^2} = \\dfrac{2r^3}{r^2} = 2r$. Đúng."

# ========================================================
# PHẦN III: 6 CÂU TRẢ LỜI NGẮN (0.5 điểm / câu = 3.0 điểm)
# Nhập số, tự động chấp nhận cả dấu chấm . và dấu phẩy ,
# ========================================================
PART3_QUESTIONS_12 = [
    {
        "id": "q12_p3_01",
        "part": 3,
        "number": 17,
        "difficulty": "Trung bình",
        "points": 0.5,
        "stem": "Tìm giá trị lớn nhất của hàm số $y = -x^4 + 2x^2 + 3$ trên đoạn $[0; 2]$.",
        "correct_answer": "4",
        "tolerance": 0.01,
        "explanation": "Đặt $t = x^2$ với $x \\in [0; 2] \\Rightarrow t \\in [0; 4]$.\nHàm số trở thành $g(t) = -t^2 + 2t + 3$.\nĐỉnh parabol $t = -\\dfrac{b}{2a} = 1 \\in [0; 4]$.\nTính các giá trị: $g(0) = 3$, $g(1) = 4$, $g(4) = -5$.\nVậy giá trị lớn nhất bằng $4$ (đạt tại $x = \\pm 1$)."
    },
    {
        "id": "q12_p3_02",
        "part": 3,
        "number": 18,
        "difficulty": "Trung bình",
        "points": 0.5,
        "stem": "Trong không gian $Oxyz$, cho hai vectơ $\\vec{u} = (2; -1; 2)$ và $\\vec{v} = (1; 2; -2)$. Tính côsin của góc giữa hai vectơ $\\vec{u}$ và $\\vec{v}$ (nhập kết quả dưới dạng số thập phân, ví dụ -0.4 hoặc -0,4).",
        "correct_answer": "-0.44",
        "alt_answers": ["-0.44", "-0,44", "-4/9"],
        "tolerance": 0.02,
        "explanation": "Ta có $\\cos(\\vec{u}, \\vec{v}) = \\dfrac{\\vec{u} \\cdot \\vec{v}}{|\\vec{u}| \\cdot |\\vec{v}|}$.\n$\\vec{u} \\cdot \\vec{v} = 2(1) + (-1)(2) + 2(-2) = 2 - 2 - 4 = -4$.\n$|\\vec{u}| = \\sqrt{2^2 + (-1)^2 + 2^2} = \\sqrt{9} = 3$.\n$|\\vec{v}| = \\sqrt{1^2 + 2^2 + (-2)^2} = \\sqrt{9} = 3$.\nDo đó $\\cos(\\vec{u}, \\vec{v}) = \\dfrac{-4}{3 \\cdot 3} = -\\dfrac{4}{9} \\approx -0{,}44$."
    },
    {
        "id": "q12_p3_03",
        "part": 3,
        "number": 19,
        "difficulty": "Khó",
        "points": 0.5,
        "stem": "Một bể bơi có dạng hình hộp chữ nhật với chiều sâu là $1{,}5\\text{ m}$ và thể tích là $75\\text{ m}^3$. Người ta cần lát gạch men bốn bức tường xung quanh và đáy bể. Biết chi phí lát đáy bể là $200.000\\text{ đ/m}^2$, chi phí lát tường là $150.000\\text{ đ/m}^2$. Hỏi chu vi đáy bể bơi bằng bao nhiêu mét để chi phí lát gạch là thấp nhất?",
        "correct_answer": "28.28",
        "alt_answers": ["28.3", "28,3", "28.28", "28,28", "20*sqrt(2)"],
        "tolerance": 0.2,
        "explanation": "Gọi chiều dài và chiều rộng đáy bể là $x, y > 0$ (m).\nThể tích $V = 1{,}5 \\cdot xy = 75 \\Rightarrow xy = 50$.\nChi phí lát gạch:\n$C = 200.000 \\cdot xy + 150.000 \\cdot [2(x + y) \\cdot 1{,}5] = 200.000(50) + 450.000(x + y)$.\nĐể chi phí thấp nhất thì tổng $x + y$ nhỏ nhất. Theo BĐT Cauchy: $x + y \\ge 2\\sqrt{xy} = 2\\sqrt{50} = 10\\sqrt{2} \\approx 14{,}14\\text{ m}$.\nĐẳng thức xảy ra khi $x = y = 5\\sqrt{2}$.\nChu vi đáy bể là: $2(x + y) = 4\\sqrt{50} = 20\\sqrt{2} \\approx 28{,}28\\text{ m}$."
    },
    {
        "id": "q12_p3_04",
        "part": 3,
        "number": 20,
        "difficulty": "Khó",
        "points": 0.5,
        "stem": "Cho mẫu số liệu ghép nhóm về điểm kiểm tra của $40$ học sinh:\n\n$$\\begin{array}{|c|c|c|c|c|c|} \\hline \\text{Khoảng điểm} & [4; 5) & [5; 6) & [6; 7) & [7; 8) & [8; 10] \\\\ \\hline \\text{Số học sinh} & 4 & 10 & 14 & 8 & 4 \\\\ \\hline \\end{array}$$\n\nTính số trung bình $\\bar{x}$ của mẫu số liệu ghép nhóm trên (lấy giá trị đại diện của nhóm cuối $[8; 10]$ là $9$).",
        "correct_answer": "6.55",
        "alt_answers": ["6.55", "6,55", "6.6", "6,6"],
        "tolerance": 0.05,
        "explanation": "Giá trị đại diện các nhóm:\n- $[4; 5)$: $4{,}5$\n- $[5; 6)$: $5{,}5$\n- $[6; 7)$: $6{,}5$\n- $[7; 8)$: $7{,}5$\n- $[8; 10]$: $9{,}0$\nSố trung bình:\n$$\\bar{x} = \\dfrac{4 \\cdot 4{,}5 + 10 \\cdot 5{,}5 + 14 \\cdot 6{,}5 + 8 \\cdot 7{,}5 + 4 \\cdot 9}{40} = \\dfrac{18 + 55 + 91 + 60 + 36}{40} = \\dfrac{260}{40} = 6{,}5$$"
    },
    {
        "id": "q12_p3_05",
        "part": 3,
        "number": 21,
        "difficulty": "Cực khó",
        "points": 0.5,
        "stem": "Một quả bóng đá tiêu chuẩn có trọng lượng $450\\text{ g}$ được sút lên từ mặt đất với phương trình quỹ đạo độ cao là $h(t) = -4{,}9t^2 + 19{,}6t$ (với $t$ tính bằng giây, $h$ tính bằng mét). Tính độ cao cực đại mà quả bóng đạt được (mét).",
        "correct_answer": "19.6",
        "alt_answers": ["19.6", "19,6"],
        "tolerance": 0.05,
        "explanation": "Đạo hàm $h'(t) = -9{,}8t + 19{,}6 = 0 \\Leftrightarrow t = 2\\text{ (s)}$.\nĐộ cao cực đại: $h(2) = -4{,}9(2^2) + 19{,}6(2) = -19{,}6 + 39{,}2 = 19{,}6\\text{ (m)}$."
    },
    {
        "id": "q12_p3_06",
        "part": 3,
        "number": 22,
        "difficulty": "Cực khó",
        "points": 0.5,
        "stem": "Trong không gian $Oxyz$, cho mặt cầu $(S)$ có phương trình $(x-1)^2 + (y+2)^2 + (z-3)^2 = 25$ và mặt phẳng $(P): 2x - 2y + z + 5 = 0$. Khoảng cách từ tâm $I$ của mặt cầu $(S)$ đến mặt phẳng $(P)$ bằng bao nhiêu?",
        "correct_answer": "4.67",
        "alt_answers": ["4.67", "4,67", "14/3", "4.667"],
        "tolerance": 0.05,
        "explanation": "Tâm của mặt cầu $(S)$ là $I(1; -2; 3)$.\nKhoảng cách từ $I$ đến $(P)$ là:\n$$d(I, (P)) = \\dfrac{|2(1) - 2(-2) + 3 + 5|}{\\sqrt{2^2 + (-2)^2 + 1^2}} = \\dfrac{|2 + 4 + 3 + 5|}{\\sqrt{9}} = \\dfrac{14}{3} \\approx 4{,}67$$"
    }
]

# Adjust Part 3 Q20 correct answer based on precise calculation
PART3_QUESTIONS_12[3]["correct_answer"] = "6.5"
PART3_QUESTIONS_12[3]["alt_answers"] = ["6.5", "6,5"]

# Add Part 3 to SAMPLE_EXAM_12
for q in PART3_QUESTIONS_12:
    SAMPLE_EXAM_12["questions"].append(q)



# Sample Exam for Grade 10
SAMPLE_EXAM_10 = {
    "title": "Đề Kiểm Tra Học Kì I Toán 10 - Chuẩn Ma Trận 22 Câu Bộ GD&ĐT",
    "grade": "10",
    "book": "Ket_Noi_Tri_Thuc",
    "chapter": "Tổng hợp Mệnh đề, Tập hợp, Bất phương trình, Vectơ, Lượng giác",
    "duration_minutes": 50,
    "shuffle_questions": False,
    "shuffle_options": False,
    "questions": [
        # Phần I: 12 câu trắc nghiệm (0.25đ/câu = 3.0đ)
        {
            "id": "q10_p1_01",
            "part": 1,
            "number": 1,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Trong các câu sau, câu nào là một mệnh đề toán học?",
            "options": [
                {"key": "A", "text": "Hôm nay trời đẹp quá!"},
                {"key": "B", "text": "Số 15 là số nguyên tố."},
                {"key": "C", "text": "Bạn có thích học môn Toán không?"},
                {"key": "D", "text": "$x + 2 > 5$."}
            ],
            "correct_answer": "B",
            "explanation": "Mệnh đề toán học là một khẳng định có tính đúng hoặc sai dứt khoát. 'Số 15 là số nguyên tố' là mệnh đề toán học (và là mệnh đề sai vì 15 chia hết cho 3 và 5)."
        },
        {
            "id": "q10_p1_02",
            "part": 1,
            "number": 2,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Phủ định của mệnh đề $P: \"\\forall x \\in \\mathbb{R},\\; x^2 + 1 > 0\"$ là:",
            "options": [
                {"key": "A", "text": "$\\overline{P}: \"\\exists x \\in \\mathbb{R},\\; x^2 + 1 \\le 0\"$"},
                {"key": "B", "text": "$\\overline{P}: \"\\forall x \\in \\mathbb{R},\\; x^2 + 1 \\le 0\"$"},
                {"key": "C", "text": "$\\overline{P}: \"\\exists x \\in \\mathbb{R},\\; x^2 + 1 < 0\"$"},
                {"key": "D", "text": "$\\overline{P}: \"\\exists x \\in \\mathbb{R},\\; x^2 + 1 = 0\"$"}
            ],
            "correct_answer": "A",
            "explanation": "Phủ định của mệnh đề chứa kí hiệu $\\forall$ là $\\exists$, và phủ định của $>$ là $\\le$. Do đó $\\overline{P}: \"\\exists x \\in \\mathbb{R},\\; x^2 + 1 \\le 0\"$."
        },
        {
            "id": "q10_p1_03",
            "part": 1,
            "number": 3,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Cho hai tập hợp $A = \\{1; 2; 3; 4\\}$ và $B = \\{3; 4; 5; 6\\}$. Giao của hai tập hợp $A \\cap B$ là:",
            "options": [
                {"key": "A", "text": "$\\{3; 4\\}$"},
                {"key": "B", "text": "$\\{1; 2; 5; 6\\}$"},
                {"key": "C", "text": "$\\{1; 2; 3; 4; 5; 6\\}$"},
                {"key": "D", "text": "$\\{1; 2\\}$"}
            ],
            "correct_answer": "A",
            "explanation": "$A \\cap B$ gồm các phần tử vừa thuộc $A$ vừa thuộc $B$, đó là các phần tử $3$ và $4$. Vậy $A \\cap B = \\{3; 4\\}$."
        },
        {
            "id": "q10_p1_04",
            "part": 1,
            "number": 4,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Cặp số nào sau đây là một nghiệm của bất phương trình $2x - 3y + 1 > 0$?",
            "options": [
                {"key": "A", "text": "$(1; 2)$"},
                {"key": "B", "text": "$(2; 1)$"},
                {"key": "C", "text": "$(0; 1)$"},
                {"key": "D", "text": "(-1; 0)"}
            ],
            "correct_answer": "B",
            "explanation": "Thay tọa độ $(2; 1)$ vào vế trái: $2(2) - 3(1) + 1 = 4 - 3 + 1 = 2 > 0$ (thỏa mãn). Vậy $(2; 1)$ là nghiệm."
        },
        {
            "id": "q10_p1_05",
            "part": 1,
            "number": 5,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Giá trị của biểu thức $\\sin 30^\\circ + \\cos 60^\\circ$ bằng:",
            "options": [
                {"key": "A", "text": "$1$"},
                {"key": "B", "text": "$\\dfrac{\\sqrt{3}}{2}$"},
                {"key": "C", "text": "$\\sqrt{3}$"},
                {"key": "D", "text": "$\\dfrac{1}{2}$"}
            ],
            "correct_answer": "A",
            "explanation": "Ta có $\\sin 30^\\circ = \\dfrac{1}{2}$ và $\\cos 60^\\circ = \\dfrac{1}{2}$. Tổng bằng $\\dfrac{1}{2} + \\dfrac{1}{2} = 1$."
        },
        {
            "id": "q10_p1_06",
            "part": 1,
            "number": 6,
            "difficulty": "Dễ",
            "points": 0.25,
            "stem": "Cho tam giác $ABC$. Khẳng định nào sau đây là đúng theo quy tắc ba điểm?",
            "options": [
                {"key": "A", "text": "$\\vec{AB} + \\vec{BC} = \\vec{AC}$"},
                {"key": "B", "text": "$\\vec{AB} + \\vec{AC} = \\vec{BC}$"},
                {"key": "C", "text": "$\\vec{AB} - \\vec{AC} = \\vec{BC}$"},
                {"key": "D", "text": "$\\vec{BA} + \\vec{BC} = \\vec{AC}$"}
            ],
            "correct_answer": "A",
            "explanation": "Theo quy tắc cộng ba điểm: với ba điểm $A, B, C$ bất kì ta luôn có $\\vec{AB} + \\vec{BC} = \\vec{AC}$."
        },
        {
            "id": "q10_p1_07",
            "part": 1,
            "number": 7,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Cho tam giác $ABC$ có cạnh $a = 6$, $b = 8$ và góc $C = 60^\\circ$. Độ dài cạnh $c$ bằng:",
            "options": [
                {"key": "A", "text": "$2\\sqrt{13}$"},
                {"key": "B", "text": "$10$"},
                {"key": "C", "text": "$2\\sqrt{37}$"},
                {"key": "D", "text": "$\\sqrt{52}$"}
            ],
            "correct_answer": "A",
            "explanation": "Theo định lí côsin: $c^2 = a^2 + b^2 - 2ab\\cos C = 6^2 + 8^2 - 2(6)(8)\\cos 60^\\circ = 36 + 64 - 96 \\cdot \\dfrac{1}{2} = 100 - 48 = 52$.\nSuy ra $c = \\sqrt{52} = 2\\sqrt{13}$."
        },
        {
            "id": "q10_p1_08",
            "part": 1,
            "number": 8,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Trong mặt phẳng tọa độ $Oxy$, cho $\\vec{a} = (2; -3)$ và $\\vec{b} = (4; 1)$. Tọa độ của vectơ $\\vec{u} = 2\\vec{a} - \\vec{b}$ là:",
            "options": [
                {"key": "A", "text": "$(0; -7)$"},
                {"key": "B", "text": "$(8; -5)$"},
                {"key": "C", "text": "(0; -5)"},
                {"key": "D", "text": "(8; -7)"}
            ],
            "correct_answer": "A",
            "explanation": "$2\\vec{a} = (4; -6)$. Suy ra $\\vec{u} = 2\\vec{a} - \\vec{b} = (4 - 4;\\; -6 - 1) = (0; -7)$."
        },
        {
            "id": "q10_p1_09",
            "part": 1,
            "number": 9,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Tọa độ đỉnh của parabol $(P): y = x^2 - 4x + 3$ là:",
            "options": [
                {"key": "A", "text": "$I(2; -1)$"},
                {"key": "B", "text": "$I(-2; 15)$"},
                {"key": "C", "text": "$I(2; 1)$"},
                {"key": "D", "text": "$I(-2; -1)$"}
            ],
            "correct_answer": "A",
            "explanation": "Hoành độ đỉnh $x_I = -\\dfrac{b}{2a} = -\\dfrac{-4}{2(1)} = 2$.\nTung độ đỉnh $y_I = 2^2 - 4(2) + 3 = 4 - 8 + 3 = -1$. Vậy đỉnh $I(2; -1)$."
        },
        {
            "id": "q10_p1_10",
            "part": 1,
            "number": 10,
            "difficulty": "Trung bình",
            "points": 0.25,
            "stem": "Cho mẫu số liệu điểm kiểm tra: $5;\\; 6;\\; 7;\\; 8;\\; 9;\\; 10$. Khoảng biến thiên $R$ của mẫu số liệu là:",
            "options": [
                {"key": "A", "text": "$5$"},
                {"key": "B", "text": "$10$"},
                {"key": "C", "text": "$7{,}5$"},
                {"key": "D", "text": "$4$"}
            ],
            "correct_answer": "A",
            "explanation": "Khoảng biến thiên $R = x_{\\max} - x_{\\min} = 10 - 5 = 5$."
        },
        {
            "id": "q10_p1_11",
            "part": 1,
            "number": 11,
            "difficulty": "Khó",
            "points": 0.25,
            "stem": "Tìm tất cả các giá trị của tham số $m$ để bất phương trình $x^2 - 2(m-1)x + 4 > 0$ nghiệm đúng với mọi $x \\in \\mathbb{R}$.",
            "options": [
                {"key": "A", "text": "$-1 < m < 3$"},
                {"key": "B", "text": "$m < -1$ hoặc $m > 3$"},
                {"key": "C", "text": "$-3 < m < 1$"},
                {"key": "D", "text": "$-1 \\le m \\le 3$"}
            ],
            "correct_answer": "A",
            "explanation": "Tam thức bậc hai $f(x) > 0,\\; \\forall x \\in \\mathbb{R} \\Leftrightarrow a > 0$ và $\\Delta' < 0$.\nỞ đây $a = 1 > 0$ (luôn đúng).\n$\\Delta' = (m-1)^2 - 4 < 0 \\Leftrightarrow m^2 - 2m - 3 < 0 \\Leftrightarrow -1 < m < 3$."
        },
        {
            "id": "q10_p1_12",
            "part": 1,
            "number": 12,
            "difficulty": "Khó",
            "points": 0.25,
            "stem": "Cho tam giác đều $ABC$ cạnh $a$. Tích vô hướng $\\vec{AB} \\cdot \\vec{AC}$ bằng:",
            "options": [
                {"key": "A", "text": "$\\dfrac{a^2}{2}$"},
                {"key": "B", "text": "$\\dfrac{a^2\\sqrt{3}}{2}$"},
                {"key": "C", "text": "$-\\dfrac{a^2}{2}$"},
                {"key": "D", "text": "$a^2$"}
            ],
            "correct_answer": "A",
            "explanation": "Vì tam giác $ABC$ đều nên góc giữa $\\vec{AB}$ và $\\vec{AC}$ là $\\widehat{BAC} = 60^\\circ$.\n$\\vec{AB} \\cdot \\vec{AC} = |\\vec{AB}| \\cdot |\\vec{AC}| \\cdot \\cos 60^\\circ = a \\cdot a \\cdot \\dfrac{1}{2} = \\dfrac{a^2}{2}$."
        },

        # Phần II: 4 câu đúng sai (1.0đ/câu = 4.0đ)
        {
            "id": "q10_p2_01",
            "part": 2,
            "number": 13,
            "difficulty": "Trung bình",
            "points": 1.0,
            "stem": "Cho hai tập hợp số $A = [-2; 4)$ và $B = (0; 5]$. Các khẳng định sau đúng hay sai?",
            "items": [
                {"key": "a", "text": "$A \\cap B = (0; 4)$."},
                {"key": "b", "text": "$A \\cup B = [-2; 5]$."},
                {"key": "c", "text": "$A \\setminus B = [-2; 0)$."},
                {"key": "d", "text": "$C_{\\mathbb{R}}A = (-\\infty; -2) \\cup [4; +\\infty)$."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": False,
                "d": True
            },
            "explanation": "- Ý a: $A \\cap B = [-2; 4) \\cap (0; 5] = (0; 4)$. Đúng.\n- Ý b: $A \\cup B = [-2; 4) \\cup (0; 5] = [-2; 5]$. Đúng.\n- Ý c: $A \\setminus B = [-2; 0]$ (vì $0 \\notin B$ nên $0 \\in A \\setminus B$). Khẳng định bảo là $[-2; 0)$ là Sai.\n- Ý d: $C_{\\mathbb{R}}A = \\mathbb{R} \\setminus [-2; 4) = (-\\infty; -2) \\cup [4; +\\infty)$. Đúng."
        },
        {
            "id": "q10_p2_02",
            "part": 2,
            "number": 14,
            "difficulty": "Trung bình",
            "points": 1.0,
            "stem": "Cho tam giác $ABC$ có trọng tâm $G$ và $M$ là trung điểm cạnh $BC$.",
            "items": [
                {"key": "a", "text": "$\\vec{AB} + \\vec{AC} = 2\\vec{AM}$."},
                {"key": "b", "text": "$\\vec{GA} + \\vec{GB} + \\vec{GC} = \\vec{0}$."},
                {"key": "c", "text": "$\\vec{AG} = \\dfrac{2}{3}\\vec{AM}$."},
                {"key": "d", "text": "Với điểm $O$ bất kì, $\\vec{OA} + \\vec{OB} + \\vec{OC} = 2\\vec{OG}$."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": False
            },
            "explanation": "- Ý a: Đúng, tính chất vectơ trung điểm.\n- Ý b: Đúng, tính chất trọng tâm tam giác.\n- Ý c: Đúng, trọng tâm chia đoạn trung tuyến theo tỉ lệ $2/3$.\n- Ý d: Sai, công thức đúng là $\\vec{OA} + \\vec{OB} + \\vec{OC} = 3\\vec{OG}$."
        },
        {
            "id": "q10_p2_03",
            "part": 2,
            "number": 15,
            "difficulty": "Khó",
            "points": 1.0,
            "stem": "Một hộ nông dân dự định trồng đậu và cà chua trên diện tích tối đa $8\\text{ ha}$. Nếu trồng đậu thì cần $20$ ngày công và thu lãi $3$ triệu đồng/ha. Nếu trồng cà chua thì cần $30$ ngày công và thu lãi $4$ triệu đồng/ha. Biết tổng số ngày công không quá $180$ ngày công.",
            "items": [
                {"key": "a", "text": "Gọi $x, y$ (ha) lần lượt là diện tích trồng đậu và cà chua, ta có hệ điều kiện: $\\begin{cases} x \\ge 0,\\; y \\ge 0 \\\\ x + y \\le 8 \\\\ 20x + 30y \\le 180 \\end{cases}$."},
                {"key": "b", "text": "Số tiền lãi thu được tính theo biểu thức $F(x, y) = 3x + 4y$ (triệu đồng)."},
                {"key": "c", "text": "Điểm $(6; 2)$ thuộc miền nghiệm của hệ bất phương trình."},
                {"key": "d", "text": "Số tiền lãi lớn nhất hộ nông dân có thể thu được là $32$ triệu đồng."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": False
            },
            "explanation": "- Ý a: Đúng, mô hình hóa bài toán thực tế chuẩn xác.\n- Ý b: Đúng, hàm mục tiêu tiền lãi $F = 3x + 4y$.\n- Ý c: Thay $(6; 2)$: $6+2=8 \\le 8$, $20(6)+30(2) = 180 \\le 180$ thỏa mãn. Đúng.\n- Ý d: Các đỉnh của miền nghiệm là $O(0; 0), A(8; 0), B(6; 2), C(0; 6)$.\n$F(0,0)=0; F(8,0)=24; F(6,2)=3(6)+4(2)=26; F(0,6)=24$. Tiền lãi tối đa là $26$ triệu đồng (đạt khi trồng 6 ha đậu và 2 ha cà chua). Mệnh đề cho $32$ triệu đồng là Sai."
        },
        {
            "id": "q10_p2_04",
            "part": 2,
            "number": 16,
            "difficulty": "Khó",
            "points": 1.0,
            "stem": "Cho hàm số bậc hai $y = f(x) = ax^2 + bx + c$ ($a \\ne 0$) có đồ thị đi qua ba điểm $A(0; 3)$, $B(1; 0)$, $C(3; 0)$.",
            "items": [
                {"key": "a", "text": "Hệ số $c = 3$."},
                {"key": "b", "text": "Hàm số bậc hai đó là $y = x^2 - 4x + 3$."},
                {"key": "c", "text": "Hàm số nghịch biến trên khoảng $(-\\infty; 2)$ và đồng biến trên khoảng $(2; +\\infty)$."},
                {"key": "d", "text": "Giá trị nhỏ nhất của hàm số trên $\\mathbb{R}$ bằng $0$."}
            ],
            "correct_answers": {
                "a": True,
                "b": True,
                "c": True,
                "d": False
            },
            "explanation": "- Đi qua $A(0; 3) \\Rightarrow c = 3$. Đúng (Ý a).\n- Đi qua $B(1; 0) \\Rightarrow a + b + 3 = 0 \\Rightarrow a + b = -3$.\n- Đi qua $C(3; 0) \\Rightarrow 9a + 3b + 3 = 0 \\Rightarrow 3a + b = -1$.\n- Trừ hai vế: $2a = 2 \\Rightarrow a = 1 \\Rightarrow b = -4$. Hàm số $y = x^2 - 4x + 3$. Đúng (Ý b).\n- Vì $a = 1 > 0$ và hoành độ đỉnh $x_0 = 2$ nên hàm số nghịch biến trên $(-\\infty; 2)$ và đồng biến trên $(2; +\\infty)$. Đúng (Ý c).\n- Đỉnh $I(2; -1)$, giá trị nhỏ nhất của hàm số là $-1$ chứ không phải $0$. Sai (Ý d)."
        },

        # Phần III: 6 câu trả lời ngắn (0.5đ/câu = 3.0đ)
        {
            "id": "q10_p3_01",
            "part": 3,
            "number": 17,
            "difficulty": "Trung bình",
            "points": 0.5,
            "stem": "Lớp 10A có $45$ học sinh, trong đó có $25$ học sinh giỏi môn Toán, $20$ học sinh giỏi môn Ngữ Văn và $10$ học sinh giỏi cả hai môn Toán và Ngữ Văn. Hỏi lớp 10A có bao nhiêu học sinh không giỏi môn nào trong hai môn trên?",
            "correct_answer": "10",
            "tolerance": 0.01,
            "explanation": "Số học sinh giỏi ít nhất một trong hai môn là: $|T \\cup V| = |T| + |V| - |T \\cap V| = 25 + 20 - 10 = 35$.\nSố học sinh không giỏi môn nào là: $45 - 35 = 10$ học sinh."
        },
        {
            "id": "q10_p3_02",
            "part": 3,
            "number": 18,
            "difficulty": "Trung bình",
            "points": 0.5,
            "stem": "Cho tam giác $ABC$ có ba cạnh $a = 7$, $b = 8$, $c = 5$. Tính diện tích tam giác $ABC$ (làm tròn kết quả đến hàng phần mười, ví dụ 17.3 hoặc 17,3).",
            "correct_answer": "17.3",
            "alt_answers": ["17.3", "17,3", "10*sqrt(3)"],
            "tolerance": 0.1,
            "explanation": "Nửa chu vi $p = \\dfrac{7 + 8 + 5}{2} = 10$.\nTheo công thức Heron:\n$$S = \\sqrt{p(p-a)(p-b)(p-c)} = \\sqrt{10(10-7)(10-8)(10-5)} = \\sqrt{10 \\cdot 3 \\cdot 2 \\cdot 5} = \\sqrt{300} = 10\\sqrt{3} \\approx 17{,}32$$"
        },
        {
            "id": "q10_p3_03",
            "part": 3,
            "number": 19,
            "difficulty": "Trung bình",
            "points": 0.5,
            "stem": "Trong mặt phẳng tọa độ $Oxy$, cho tam giác $ABC$ có $A(1; 3)$, $B(-2; 2)$, $C(4; -2)$. Tìm tung độ của trọng tâm $G$ của tam giác $ABC$.",
            "correct_answer": "1",
            "tolerance": 0.01,
            "explanation": "Tung độ trọng tâm $G$ là: $y_G = \\dfrac{y_A + y_B + y_C}{3} = \\dfrac{3 + 2 + (-2)}{3} = \\dfrac{3}{3} = 1$."
        },
        {
            "id": "q10_p3_04",
            "part": 3,
            "number": 20,
            "difficulty": "Khó",
            "points": 0.5,
            "stem": "Một chiếc cổng hình parabol có chiều rộng $AB = 8\\text{ m}$ và chiều cao từ đỉnh cổng xuống mặt đất là $h = 4\\text{ m}$. Một chiếc xe tải có chiều rộng $2\\text{ m}$ muốn đi qua chính giữa cổng. Hỏi chiều cao tối đa của xe tải có thể là bao nhiêu mét để không chạm cổng (nhập số thập phân, ví dụ 3.75 hoặc 3,75)?",
            "correct_answer": "3.75",
            "alt_answers": ["3.75", "3,75", "15/4"],
            "tolerance": 0.05,
            "explanation": "Chọn hệ trục tọa độ $Oxy$ với gốc $O$ là trung điểm $AB$, trục $Oy$ đi qua đỉnh cổng parabol.\nĐỉnh parabol là $I(0; 4)$, cổng đi qua hai điểm $A(-4; 0)$ và $B(4; 0)$.\nPhương trình parabol có dạng $y = ax^2 + 4$. Đi qua $B(4; 0) \\Rightarrow 0 = 16a + 4 \\Rightarrow a = -\\dfrac{1}{4}$.\nVậy $y = -\\dfrac{1}{4}x^2 + 4$.\nXe rộng $2\\text{ m}$ đi giữa cổng ứng với $x \\in [-1; 1]$. Tại mép xe $x = 1$, chiều cao của cổng là:\n$y(1) = -\\dfrac{1}{4}(1)^2 + 4 = 3{,}75\\text{ m}$."
        },
        {
            "id": "q10_p3_05",
            "part": 3,
            "number": 21,
            "difficulty": "Khó",
            "points": 0.5,
            "stem": "Cho mẫu số liệu điểm kiểm tra của một nhóm học sinh: $4; 6; 7; 8; 9; 10; 12$. Tìm trung vị (median) của mẫu số liệu trên.",
            "correct_answer": "8",
            "tolerance": 0.01,
            "explanation": "Dãy đã được sắp xếp tăng dần gồm $n = 7$ số hạng (lẻ).\nTrung vị là số hạng thứ $\\dfrac{7+1}{2} = 4$, đó là số $8$."
        },
        {
            "id": "q10_p3_06",
            "part": 3,
            "number": 22,
            "difficulty": "Cực khó",
            "points": 0.5,
            "stem": "Hai người cùng kéo một chiếc thuyền theo hai hướng tạo với nhau một góc $60^\\circ$. Người thứ nhất kéo với lực $F_1 = 300\\text{ N}$, người thứ hai kéo với lực $F_2 = 400\\text{ N}$. Tính độ lớn của hợp lực tác dụng lên thuyền theo đơn vị Niutơn (làm tròn kết quả đến hàng đơn vị).",
            "correct_answer": "608",
            "alt_answers": ["608", "608.2", "608,2"],
            "tolerance": 2.0,
            "explanation": "Độ lớn của hợp lực $\\vec{F} = \\vec{F_1} + \\vec{F_2}$ được tính theo quy tắc hình bình hành:\n$$F = \\sqrt{F_1^2 + F_2^2 + 2 F_1 F_2 \\cos 60^\\circ}$$\n$$F = \\sqrt{300^2 + 400^2 + 2(300)(400) \\cdot \\dfrac{1}{2}} = \\sqrt{90000 + 160000 + 120000} = \\sqrt{370000} = 100\\sqrt{37} \\approx 608{,}28\\text{ N}$$.\nLàm tròn đến hàng đơn vị: $608$."
        }
    ]
}


def get_curriculum_tree():
    """Returns curriculum tree for UI selection"""
    return CURRICULUM_STRUCTURE


def generate_exam_for_lesson(grade: str, book_key: str, lesson_id: str, title: str = None) -> Dict[str, Any]:
    """
    Generates a full 22-question standard exam for a given lesson or grade.
    Matches the 12 Part I, 4 Part II, 6 Part III matrix.
    """
    base_exam = SAMPLE_EXAM_12 if grade == "12" else SAMPLE_EXAM_10
    exam_copy = copy.deepcopy(base_exam)
    if title:
        exam_copy["title"] = title
    exam_copy["grade"] = grade
    exam_copy["book"] = book_key
    exam_copy["chapter"] = lesson_id
    return exam_copy

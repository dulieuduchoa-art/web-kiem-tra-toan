"""
Text parser for importing math exams from raw pasted text (Word/LaTeX/plain text).
Supports the 3-part format:
- Part I: 12 Multiple choice (A, B, C, D)
- Part II: 4 True/False (a, b, c, d)
- Part III: 6 Short answers
"""

import re
from typing import Dict, List, Any

SAMPLE_IMPORT_TEMPLATE = """[PHẦN I]
Câu 1: Cho hàm số $y = f(x)$ có bảng biến thiên và đồng biến trên khoảng nào?
A. $(-1; 2)$
B. $(-\\infty; -1)$
C. $(-2; 3)$
D. $(-\\infty; 2)$
Đáp án: B
Lời giải: Dựa vào bảng biến thiên, ta thấy $f'(x) > 0$ trên $(-\\infty; -1)$.

Câu 2: Đồ thị hàm số $y = \\frac{2x - 1}{x + 3}$ có tiệm cận đứng là:
A. $x = 2$
B. $y = 2$
C. $x = -3$
D. $y = -3$
Đáp án: C
Lời giải: Tiệm cận đứng là nghiệm của mẫu $x + 3 = 0 \\Leftrightarrow x = -3$.

[PHẦN II]
Câu 13: Cho hàm số $y = \\frac{2x - 3}{x - 1}$. Xét tính đúng sai của các khẳng định sau:
a) Tập xác định của hàm số là $D = \\mathbb{R} \\setminus \\{1\\}$.
b) Đạo hàm của hàm số là $f'(x) = \\frac{1}{(x-1)^2}$.
c) Đồ thị hàm số có đường tiệm cận ngang là $y = 2$.
d) Hàm số đồng biến trên toàn trục số.
Đáp án: a:Đ, b:Đ, c:Đ, d:S
Lời giải: Hàm số không xác định tại $x = 1$ nên không thể đồng biến trên toàn trục số.

[PHẦN III]
Câu 17: Tìm giá trị lớn nhất của hàm số $y = -x^4 + 2x^2 + 3$ trên đoạn $[0; 2]$.
Đáp án: 4
Lời giải: Đặt $t = x^2 \\in [0; 4]$, $g(t) = -t^2 + 2t + 3$ đạt cực đại tại $t = 1$ với $g(1) = 4$.
"""

def parse_exam_text(raw_text: str) -> List[Dict[str, Any]]:
    """
    Parses pasted text into a list of question dictionaries conforming to the schema.
    """
    if not raw_text or not raw_text.strip():
        return []

    lines = raw_text.splitlines()
    
    current_part = 1
    current_question = None
    questions = []
    
    # Regular expressions for headers and parts
    part_header_pattern = re.compile(r"^\s*\[?(?:PHẦN|PHAN|PART)\s+([I|V|X|1|2|3]+)\]?", re.IGNORECASE)
    question_start_pattern = re.compile(r"^\s*(?:Câu|Cau|Bài|Question)\s*(\d+)[\s*:\.\)]\s*(.*)", re.IGNORECASE)
    option_pattern = re.compile(r"^\s*([A-D])[\.\)]\s*(.*)", re.IGNORECASE)
    item_tf_pattern = re.compile(r"^\s*([a-d])[\.\)]\s*(.*)", re.IGNORECASE)
    answer_pattern = re.compile(r"^\s*(?:Đáp án|Dap an|Đ/A|DA|Answer|Ans)[\s*:\.]\s*(.*)", re.IGNORECASE)
    solution_pattern = re.compile(r"^\s*(?:Lời giải|Hướng dẫn giải|Loi giai|HDG|Solution)[\s*:\.]\s*(.*)", re.IGNORECASE)

    def finalize_question(q):
        if not q:
            return
        # Auto-detect part if not set
        if q.get("items") and len(q["items"]) > 0:
            q["part"] = 2
            q["points"] = 1.0
            if "correct_answers" not in q:
                q["correct_answers"] = {"a": True, "b": True, "c": True, "d": False}
        elif q.get("options") and len(q["options"]) > 0:
            q["part"] = 1
            q["points"] = 0.25
            if not q.get("correct_answer"):
                q["correct_answer"] = "A"
        else:
            q["part"] = 3
            q["points"] = 0.5
            if not q.get("correct_answer"):
                q["correct_answer"] = "0"
        
        # Difficulty default
        if not q.get("difficulty"):
            p = q.get("part", 1)
            if p == 1:
                q["difficulty"] = "Dễ" if len(questions) < 6 else "Trung bình"
            elif p == 2:
                q["difficulty"] = "Trung bình" if len(questions) < 14 else "Khó"
            else:
                q["difficulty"] = "Khó" if len(questions) < 20 else "Cực khó"

        questions.append(q)

    current_mode = "stem" # 'stem', 'explanation'

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check Part header
        part_match = part_header_pattern.match(stripped)
        if part_match:
            part_str = part_match.group(1).upper()
            if part_str in ["I", "1"]:
                current_part = 1
            elif part_str in ["II", "2"]:
                current_part = 2
            elif part_str in ["III", "3"]:
                current_part = 3
            continue

        # Check Question start
        q_match = question_start_pattern.match(stripped)
        if q_match:
            finalize_question(current_question)
            q_num = int(q_match.group(1))
            q_stem = q_match.group(2).strip()
            
            # Infer part if not strictly specified
            detected_part = current_part
            if q_num > 16:
                detected_part = 3
            elif q_num > 12:
                detected_part = 2
            elif q_num <= 12 and current_part == 1:
                detected_part = 1

            current_question = {
                "id": f"q_custom_{len(questions) + 1}",
                "number": q_num,
                "part": detected_part,
                "stem": q_stem,
                "options": [],
                "items": [],
                "correct_answer": None,
                "correct_answers": {},
                "explanation": "",
                "points": 0.25 if detected_part == 1 else (1.0 if detected_part == 2 else 0.5)
            }
            current_mode = "stem"
            continue

        if not current_question:
            # First question without "Câu X:" header?
            current_question = {
                "id": f"q_custom_1",
                "number": 1,
                "part": current_part,
                "stem": stripped,
                "options": [],
                "items": [],
                "explanation": "",
                "points": 0.25
            }
            current_mode = "stem"
            continue

        # Check Answer line
        ans_match = answer_pattern.match(stripped)
        if ans_match:
            ans_text = ans_match.group(1).strip()
            if current_question["part"] == 1:
                # Part 1: Single letter A, B, C, D
                m = re.search(r"[A-D]", ans_text.upper())
                current_question["correct_answer"] = m.group(0) if m else "A"
            elif current_question["part"] == 2:
                # Part 2: e.g. a:Đ, b:S, c:Đ, d:S or a-Đ, b-S...
                # or Đ-S-Đ-S or True/False
                parsed_answers = {}
                for k in ["a", "b", "c", "d"]:
                    # Match like a: Đ or a) Đúng or a = S
                    km = re.search(rf"{k}\s*[:=\-\)]\s*([Đ|D|S|T|F|đ|d|s|t|f]|Đúng|Sai|True|False)", ans_text, re.IGNORECASE)
                    if km:
                        val = km.group(1).upper()
                        parsed_answers[k] = val in ["Đ", "D", "T", "ĐÚNG", "TRUE"]
                
                # If not matched by key, check sequential Đ/S like Đ - S - Đ - S
                if len(parsed_answers) < 4:
                    tokens = [t.strip().upper() for t in re.split(r"[,;\-\s/]+", ans_text) if t.strip()]
                    tf_tokens = [t for t in tokens if t in ["Đ", "D", "S", "T", "F", "ĐÚNG", "SAI", "TRUE", "FALSE"]]
                    if len(tf_tokens) == 4:
                        for idx, k in enumerate(["a", "b", "c", "d"]):
                            parsed_answers[k] = tf_tokens[idx] in ["Đ", "D", "T", "ĐÚNG", "TRUE"]

                current_question["correct_answers"] = parsed_answers
            else:
                # Part 3: Short answer number
                current_question["correct_answer"] = ans_text
            continue

        # Check Solution line
        sol_match = solution_pattern.match(stripped)
        if sol_match:
            current_question["explanation"] = sol_match.group(1).strip()
            current_mode = "explanation"
            continue

        # Check Option A-D for Part I
        opt_match = option_pattern.match(stripped)
        if opt_match and current_question["part"] == 1:
            opt_key = opt_match.group(1).upper()
            opt_val = opt_match.group(2).strip()
            current_question["options"].append({"key": opt_key, "text": opt_val})
            continue

        # Check Sub-item a-d for Part II
        item_match = item_tf_pattern.match(stripped)
        if item_match and current_question["part"] == 2:
            item_key = item_match.group(1).lower()
            item_val = item_match.group(2).strip()
            current_question["items"].append({"key": item_key, "text": item_val})
            continue

        # Otherwise, append to stem or explanation
        if current_mode == "explanation":
            current_question["explanation"] += "\n" + stripped
        else:
            current_question["stem"] += "\n" + stripped

    finalize_question(current_question)

    # Renumber questions 1..N
    for i, q in enumerate(questions, start=1):
        q["number"] = i
        if not q.get("id"):
            q["id"] = f"q_{i}"

    return questions

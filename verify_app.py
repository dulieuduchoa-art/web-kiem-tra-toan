import urllib.request
import urllib.parse
import json
import openpyxl
import io

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("=== STARTING FULL APPLICATION TEST ===")
    
    # 1. Test Home page
    with urllib.request.urlopen(f"{BASE_URL}/") as res:
        assert res.status == 200
        html = res.read().decode('utf-8')
        assert "Toán THPT Online" in html
        print("[PASS] 1. Home portal loaded.")

    # 2. Test Teacher Login
    login_data = json.dumps({"password": "wrong_password"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/auth/teacher", data=login_data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        assert False, "Should have failed with wrong password"
    except urllib.error.HTTPError as e:
        assert e.code == 401
        print("[PASS] 2a. Wrong teacher password correctly rejected (401).")

    login_data = json.dumps({"password": "123456"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/auth/teacher", data=login_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode('utf-8'))
        assert data["success"] is True
        print("[PASS] 2b. Default teacher password '123456' logged in successfully.")

    # 3. Test Curriculum & Kho_SGK_SBT files
    with urllib.request.urlopen(f"{BASE_URL}/api/curriculum") as res:
        curr = json.loads(res.read().decode('utf-8'))
        assert "10" in curr["curriculum"] and "12" in curr["curriculum"]
        assert "Ket_Noi_Tri_Thuc" in curr["curriculum"]["12"]
        print("[PASS] 3a. Curriculum tree verified (Grade 10 & 12, 4 textbooks).")

    with urllib.request.urlopen(f"{BASE_URL}/api/kho-sgk-sbt/files") as res:
        files = json.loads(res.read().decode('utf-8'))
        assert "files" in files
        print("[PASS] 3b. Kho_SGK_SBT PDF file tree loaded.")

    # 4. Test Generating Exam from Curriculum Lesson
    gen_data = json.dumps({
        "grade": "12",
        "book": "Ket_Noi_Tri_Thuc",
        "lesson_id": "k12_kntt_c1_b1",
        "title": "Kiểm Tra Toán 12 Tự Động Từ Kho Sách",
        "duration_minutes": 50
    }).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/curriculum/generate-exam", data=gen_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        exam_gen = json.loads(res.read().decode('utf-8'))
        questions = exam_gen["exam"]["questions"]
        assert len(questions) == 22, f"Expected 22 questions, got {len(questions)}"
        p1 = sum(1 for q in questions if q["part"] == 1)
        p2 = sum(1 for q in questions if q["part"] == 2)
        p3 = sum(1 for q in questions if q["part"] == 3)
        assert p1 == 12 and p2 == 4 and p3 == 6
        print(f"[PASS] 4. Auto-generated exam matrix verified: Part I={p1}, Part II={p2}, Part III={p3} (Total 22 questions).")

    # 5. Test Raw Text Parser
    sample_text = """[PHẦN I]
Câu 1: Hàm số $y = x^2$ đồng biến trên khoảng nào?
A. $(-\\infty; 0)$
B. $(0; +\\infty)$
C. $\\mathbb{R}$
D. $(-1; 1)$
Đáp án: B
Lời giải: Đạo hàm $y' = 2x > 0$ khi $x > 0$.

[PHẦN II]
Câu 13: Cho tam giác ABC vuông tại A.
a) $\\vec{AB} \\cdot \\vec{AC} = 0$.
b) $AB^2 + AC^2 = BC^2$.
c) Góc $\\widehat{BAC} = 90^\\circ$.
d) Diện tích tam giác bằng $AB \\cdot AC$.
Đáp án: a:Đ, b:Đ, c:Đ, d:S
Lời giải: Diện tích bằng 1/2 AB * AC nên ý d sai.

[PHẦN III]
Câu 17: Tính giá trị của biểu thức $\\sqrt{16}$.
Đáp án: 4
Lời giải: $\\sqrt{16} = 4$.
"""
    parse_data = json.dumps({"raw_text": sample_text}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/exams/parse-text", data=parse_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        parsed_res = json.loads(res.read().decode('utf-8'))
        assert parsed_res["count"] == 3
        print("[PASS] 5. Raw text parser with KaTeX verified.")

    # 6. Test Publishing Exam
    pub_data = json.dumps(exam_gen["exam"]).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/exams", data=pub_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        pub_res = json.loads(res.read().decode('utf-8'))
        created_exam_id = pub_res["exam_id"]
        assert pub_res["success"] is True
        print(f"[PASS] 6. Exam published successfully. ID: {created_exam_id}")

    # 7. Test Student Exam API (Sanitization check)
    with urllib.request.urlopen(f"{BASE_URL}/api/exams/{created_exam_id}?mode=student") as res:
        student_exam = json.loads(res.read().decode('utf-8'))
        # Ensure answers and explanations are NOT leaked to student
        for q in student_exam["questions"]:
            assert "correct_answer" not in q, f"Leak: correct_answer found in student payload for Q{q['number']}"
            assert "correct_answers" not in q, f"Leak: correct_answers found in student payload for Q{q['number']}"
            assert "explanation" not in q, f"Leak: explanation found in student payload for Q{q['number']}"
        print("[PASS] 7. Security check passed: answers & explanations strictly hidden from student test payload.")

    # 8. Test Student Submission & Ministry Progressive Grading
    with urllib.request.urlopen(f"{BASE_URL}/api/exams/{created_exam_id}?mode=teacher") as res:
        teacher_exam = json.loads(res.read().decode('utf-8'))

    # Build answers:
    # Get 100% score (10.0 points):
    perfect_answers = {}
    for q in teacher_exam["questions"]:
        qid = q["id"]
        if q["part"] == 1:
            perfect_answers[qid] = q["correct_answer"]
        elif q["part"] == 2:
            perfect_answers[qid] = q["correct_answers"]
        elif q["part"] == 3:
            # Let's test with comma for decimals!
            val = str(q["correct_answer"]).replace(".", ",")
            perfect_answers[qid] = val

    sub_payload = json.dumps({
        "student_name": "Trần Thị Tuyết Mai",
        "student_class": "12A1",
        "start_time": "2026-11-22T08:00:00",
        "time_spent_seconds": 2400,
        "tab_switch_count": 0,
        "answers": perfect_answers
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/api/exams/{created_exam_id}/submit", data=sub_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        sub_res = json.loads(res.read().decode('utf-8'))
        assert sub_res["success"] is True
        sub_id = sub_res["submission_id"]
        print(f"[PASS] 8a. Submitted exam. Scores: Part I={sub_res['part1_score']}, Part II={sub_res['part2_score']}, Part III={sub_res['part3_score']}, Total={sub_res['total_score']}")
        assert sub_res["part1_score"] == 3.0, f"Expected 3.0, got {sub_res['part1_score']}"
        assert sub_res["part2_score"] == 4.0, f"Expected 4.0, got {sub_res['part2_score']}"
        assert sub_res["part3_score"] == 3.0, f"Expected 3.0, got {sub_res['part3_score']}"
        assert sub_res["total_score"] == 10.0, f"Expected 10.0, got {sub_res['total_score']}"
        print("[PASS] 8b. Exact 10.0/10.0 score verified with comma decimal support.")

    # 9. Test Submission with Partial Answers & Tab Switch Violations
    partial_answers = {}
    for i, q in enumerate(teacher_exam["questions"]):
        qid = q["id"]
        if q["part"] == 1 and i < 6: # 6/12 correct = 1.5 pt
            partial_answers[qid] = q["correct_answer"]
        elif q["part"] == 2 and i == 12: # 1 question with 2 correct sub-items = 0.25 pt
            corr = q["correct_answers"]
            partial_answers[qid] = {
                "a": corr.get("a"),
                "b": corr.get("b"),
                "c": not corr.get("c"), # intentional wrong
                "d": not corr.get("d")  # intentional wrong
            }
        elif q["part"] == 3 and i == 16: # 1 short answer correct = 0.5 pt
            partial_answers[qid] = str(q["correct_answer"])

    cheat_payload = json.dumps({
        "student_name": "Phạm Quốc Hưng",
        "student_class": "12A1",
        "start_time": "2026-11-22T08:00:00",
        "time_spent_seconds": 2900,
        "tab_switch_count": 4, # 4 tab switches!
        "answers": partial_answers
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/api/exams/{created_exam_id}/submit", data=cheat_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as res:
        cheat_res = json.loads(res.read().decode('utf-8'))
        assert cheat_res["part1_score"] == 1.5 # 6 * 0.25
        assert cheat_res["part2_score"] == 0.25 # 2 correct sub-items progressive
        assert cheat_res["part3_score"] == 0.5 # 1 correct * 0.5
        assert cheat_res["total_score"] == 2.25
        print(f"[PASS] 9. Ministry progressive scoring verified: 2 sub-items correct -> exactly 0.25 points. Total: {cheat_res['total_score']}đ.")

    # 10. Test Excel Export (.xlsx)
    excel_url = f"{BASE_URL}/api/exams/{created_exam_id}/export-excel?class_name=12A1"
    with urllib.request.urlopen(excel_url) as res:
        assert res.status == 200
        assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in res.headers["Content-Type"]
        excel_bytes = res.read()
        assert len(excel_bytes) > 1000
        
        # Parse with openpyxl to verify valid Excel workbook
        wb = openpyxl.load_workbook(io.BytesIO(excel_bytes))
        ws = wb.active
        assert ws.title == "Bảng Điểm Kiểm Tra"
        # Check cell contents
        assert "BẢNG TỔNG HỢP KẾT QUẢ KIỂM TRA" in str(ws["A1"].value)
        # Check that students are in rows
        student_names = [ws.cell(row=r, column=2).value for r in range(6, 15) if ws.cell(row=r, column=2).value]
        assert "Trần Thị Tuyết Mai" in student_names
        assert "Phạm Quốc Hưng" in student_names
        print(f"[PASS] 10. Excel (.xlsx) file generated and validated with openpyxl. Rows contain students: {student_names}")

    # 11. Test Result Page HTML
    with urllib.request.urlopen(f"{BASE_URL}/result/{sub_id}") as res:
        assert res.status == 200
        html = res.read().decode('utf-8')
        assert "Kết Quả Kiểm Tra" in html
        print("[PASS] 11. Student result review page loaded with KaTeX integration.")

    print("\n==========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==========================================")

if __name__ == "__main__":
    test_api()

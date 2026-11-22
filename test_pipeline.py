import database
import curriculum_data
import parser_utils

database.init_db()
print("DB initialized.")

parsed = parser_utils.parse_exam_text(parser_utils.SAMPLE_IMPORT_TEMPLATE)
print("Parsed questions count:", len(parsed))
for q in parsed:
    ans = q.get("correct_answer") or q.get("correct_answers")
    print(f"Q{q['number']} (Part {q['part']}): {q['stem'][:35]}... -> {ans}")

# Seed sample exams
id_12 = database.save_exam(curriculum_data.SAMPLE_EXAM_12)
print("Saved Grade 12 exam ID:", id_12)
id_10 = database.save_exam(curriculum_data.SAMPLE_EXAM_10)
print("Saved Grade 10 exam ID:", id_10)

exam12 = database.get_exam(id_12)
print("Exam 12 questions count:", len(exam12["questions"]))

# Test grading
sample_answers = {
    "q12_p1_01": "B",
    "q12_p1_02": "A",
    "q12_p2_01": {"a": True, "b": True, "c": True, "d": False},
    "q12_p3_01": "4",
    "q12_p3_05": "19,6" # testing comma!
}
graded = database.grade_submission(exam12, sample_answers)
print("Graded result:")
print("  Part I  :", graded["part1_score"], "/ 3.0")
print("  Part II :", graded["part2_score"], "/ 4.0")
print("  Part III:", graded["part3_score"], "/ 3.0")
print("  TOTAL   :", graded["total_score"], "/ 10.0")

# Test excel exporter
import excel_exporter
sample_submissions = [
    {
        "id": "sub_1",
        "student_name": "Nguyễn Văn An",
        "student_class": "12A1",
        "time_spent_seconds": 2450,
        "tab_switch_count": 0,
        "part1_score": 2.75,
        "part2_score": 3.25,
        "part3_score": 2.5,
        "total_score": 8.5,
        "submit_time": "2026-11-22T10:15:00"
    },
    {
        "id": "sub_2",
        "student_name": "Trần Thị Bích",
        "student_class": "12A1",
        "time_spent_seconds": 2800,
        "tab_switch_count": 2,
        "part1_score": 2.25,
        "part2_score": 2.5,
        "part3_score": 1.5,
        "total_score": 6.25,
        "submit_time": "2026-11-22T10:20:00"
    }
]
excel_buf = excel_exporter.generate_exam_results_excel(exam12, sample_submissions, "12A1")
print("Excel generated successfully! Size:", len(excel_buf.getvalue()), "bytes")

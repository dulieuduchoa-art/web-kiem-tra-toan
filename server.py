"""
FastAPI Main Application Server for Online Math Examination System.
Supports Grade 10 & Grade 12, 4 Textbooks, KaTeX Rendering, and Ministry of Education 3-Part Exam Structure.
"""

import os
import json
import io
import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import quote

from fastapi import FastAPI, HTTPException, Request, Depends, Query, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel

import database
import curriculum_data
import parser_utils
import excel_exporter

app = FastAPI(title="Ứng Dụng Kiểm Tra Trực Tuyến Môn Toán THPT")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
BOOKS_DIR = os.path.join(BASE_DIR, "Kho_SGK_SBT")

# Mount static files
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount Kho_SGK_SBT for direct book downloads/viewing
if os.path.exists(BOOKS_DIR):
    app.mount("/kho_sach", StaticFiles(directory=BOOKS_DIR), name="kho_sach")

# Initialize database on startup and seed initial exams if empty
@app.on_event("startup")
def startup_event():
    database.init_db()
    existing = database.list_exams()
    if not existing:
        print("Seeding initial 22-question standard exams for Grade 12 and Grade 10...")
        exam12_id = database.save_exam(curriculum_data.SAMPLE_EXAM_12)
        exam10_id = database.save_exam(curriculum_data.SAMPLE_EXAM_10)
        
        # Add sample student submissions so teacher dashboard has rich data on first launch
        sub1 = {
            "exam_id": exam12_id,
            "student_name": "Nguyễn Hoàng Nam",
            "student_class": "12A1",
            "start_time": (datetime.datetime.now() - datetime.timedelta(minutes=45)).isoformat(),
            "submit_time": datetime.datetime.now().isoformat(),
            "time_spent_seconds": 2480,
            "tab_switch_count": 0,
            "part1_score": 2.75,
            "part2_score": 3.25,
            "part3_score": 2.50,
            "total_score": 8.50,
            "answers": {},
            "details": []
        }
        sub2 = {
            "exam_id": exam12_id,
            "student_name": "Lê Thị Mai Anh",
            "student_class": "12A1",
            "start_time": (datetime.datetime.now() - datetime.timedelta(minutes=40)).isoformat(),
            "submit_time": datetime.datetime.now().isoformat(),
            "time_spent_seconds": 2350,
            "tab_switch_count": 3,
            "part1_score": 2.25,
            "part2_score": 2.50,
            "part3_score": 1.50,
            "total_score": 6.25,
            "answers": {},
            "details": []
        }
        sub3 = {
            "exam_id": exam12_id,
            "student_name": "Trần Quốc Bảo",
            "student_class": "12A2",
            "start_time": (datetime.datetime.now() - datetime.timedelta(minutes=50)).isoformat(),
            "submit_time": datetime.datetime.now().isoformat(),
            "time_spent_seconds": 2890,
            "tab_switch_count": 1,
            "part1_score": 3.00,
            "part2_score": 3.50,
            "part3_score": 3.00,
            "total_score": 9.50,
            "answers": {},
            "details": []
        }
        database.save_submission(sub1)
        database.save_submission(sub2)
        database.save_submission(sub3)
        print("Database seeded successfully.")


# ========================================================
# PYDANTIC SCHEMAS
# ========================================================

class TeacherLoginRequest(BaseModel):
    password: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class TextParseRequest(BaseModel):
    raw_text: str

class GenerateExamRequest(BaseModel):
    grade: str
    book: str
    lesson_id: str
    title: Optional[str] = None
    duration_minutes: Optional[int] = 50

class SubmitExamRequest(BaseModel):
    student_name: str
    student_class: str
    start_time: Optional[str] = None
    time_spent_seconds: int = 0
    tab_switch_count: int = 0
    answers: Dict[str, Any]


# ========================================================
# API ROUTES: AUTH & SETTINGS
# ========================================================

@app.post("/api/auth/teacher")
def teacher_login(req: TeacherLoginRequest):
    if database.verify_teacher_password(req.password):
        return {"success": True, "token": "teacher_auth_token_ok", "message": "Đăng nhập thành công!"}
    raise HTTPException(status_code=401, detail="Mật khẩu giáo viên không chính xác! (Mặc định: 123456)")

@app.post("/api/auth/change-password")
def change_password(req: ChangePasswordRequest):
    if database.change_teacher_password(req.old_password, req.new_password):
        return {"success": True, "message": "Đổi mật khẩu thành công!"}
    raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác!")


# ========================================================
# API ROUTES: CURRICULUM & KHO_SGK_SBT
# ========================================================

@app.get("/api/curriculum")
def get_curriculum():
    return {
        "curriculum": curriculum_data.get_curriculum_tree(),
        "books_info": {
            "Ket_Noi_Tri_Thuc": "Kết nối tri thức với cuộc sống",
            "Chan_Troi_Sang_Tao": "Chân trời sáng tạo",
            "Cung_Kham_Pha": "Cùng khám phá",
            "Canh_Dieu": "Cánh diều"
        }
    }

@app.get("/api/kho-sgk-sbt/files")
def get_sgk_files():
    """Lists actual PDF files physically present in Kho_SGK_SBT"""
    files_tree = {}
    base_dir = "Kho_SGK_SBT"
    if os.path.exists(base_dir):
        for grade_dir in os.listdir(base_dir):
            grade_path = os.path.join(base_dir, grade_dir)
            if os.path.isdir(grade_path):
                files_tree[grade_dir] = {}
                for book_dir in os.listdir(grade_path):
                    book_path = os.path.join(grade_path, book_dir)
                    if os.path.isdir(book_path):
                        pdf_files = []
                        for f in os.listdir(book_path):
                            if f.lower().endswith(".pdf"):
                                f_path = os.path.join(book_path, f)
                                pdf_files.append({
                                    "filename": f,
                                    "size_mb": round(os.path.getsize(f_path) / (1024 * 1024), 2),
                                    "url": f"/kho_sach/{grade_dir}/{book_dir}/{quote(f)}"
                                })
                        files_tree[grade_dir][book_dir] = pdf_files
    return {"files": files_tree}

@app.post("/api/curriculum/generate-exam")
def generate_curriculum_exam(req: GenerateExamRequest):
    """Assembles a standard 22-question exam from a chosen lesson in Kho_SGK_SBT"""
    exam = curriculum_data.generate_exam_for_lesson(
        grade=req.grade,
        book_key=req.book,
        lesson_id=req.lesson_id,
        title=req.title
    )
    if req.duration_minutes:
        exam["duration_minutes"] = req.duration_minutes
    return {"exam": exam}


# ========================================================
# API ROUTES: EXAMS & IMPORT
# ========================================================

@app.post("/api/exams/parse-text")
def parse_text_endpoint(req: TextParseRequest):
    """Parses raw pasted exam text into structured questions"""
    questions = parser_utils.parse_exam_text(req.raw_text)
    return {
        "success": True,
        "count": len(questions),
        "questions": questions
    }

@app.get("/api/exams/sample-template")
def get_sample_template():
    return {"template": parser_utils.SAMPLE_IMPORT_TEMPLATE}

@app.post("/api/exams")
def create_exam_endpoint(exam_data: Dict[str, Any]):
    """Creates or updates an exam"""
    # Matrix validation: check standard structure
    questions = exam_data.get("questions", [])
    if not questions:
        raise HTTPException(status_code=400, detail="Đề thi phải có ít nhất 1 câu hỏi!")
    
    # Check parts
    p1 = sum(1 for q in questions if q.get("part") == 1)
    p2 = sum(1 for q in questions if q.get("part") == 2)
    p3 = sum(1 for q in questions if q.get("part") == 3)
    
    exam_id = database.save_exam(exam_data)
    return {
        "success": True, 
        "exam_id": exam_id, 
        "message": f"Đã xuất bản đề thi thành công! ({p1} câu Phần I, {p2} câu Phần II, {p3} câu Phần III - Tổng {len(questions)} câu)"
    }

@app.get("/api/exams")
def list_exams_endpoint():
    return {"exams": database.list_exams()}

@app.get("/api/exams/{exam_id}")
def get_exam_endpoint(exam_id: str, mode: Optional[str] = "student"):
    """
    Returns exam. If mode == 'student', sanitizes correct answers and explanations.
    If mode == 'teacher', returns full keys and explanations.
    """
    for_student = (mode != "teacher")
    exam = database.get_exam(exam_id, for_student=for_student)
    if not exam:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề thi!")
    return exam

@app.delete("/api/exams/{exam_id}")
def delete_exam_endpoint(exam_id: str):
    if database.delete_exam(exam_id):
        return {"success": True, "message": "Đã xóa đề thi thành công!"}
    raise HTTPException(status_code=404, detail="Không tìm thấy đề thi để xóa!")


# ========================================================
# API ROUTES: SUBMISSIONS & GRADING
# ========================================================

@app.post("/api/exams/{exam_id}/submit")
def submit_exam_endpoint(exam_id: str, req: SubmitExamRequest):
    exam = database.get_exam(exam_id, for_student=False)
    if not exam:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề thi!")

    if not req.student_name.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập Họ và tên!")
    if not req.student_class.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập Lớp!")

    # Grade submission using Ministry of Education progressive formula
    graded = database.grade_submission(exam, req.answers)

    sub_data = {
        "exam_id": exam_id,
        "student_name": req.student_name.strip(),
        "student_class": req.student_class.strip().upper(),
        "start_time": req.start_time,
        "submit_time": datetime.datetime.now().isoformat(),
        "time_spent_seconds": req.time_spent_seconds,
        "tab_switch_count": req.tab_switch_count,
        "part1_score": graded["part1_score"],
        "part2_score": graded["part2_score"],
        "part3_score": graded["part3_score"],
        "total_score": graded["total_score"],
        "answers": req.answers,
        "details": graded["details"]
    }

    sub_id = database.save_submission(sub_data)

    return {
        "success": True,
        "submission_id": sub_id,
        "student_name": req.student_name,
        "student_class": req.student_class,
        "part1_score": graded["part1_score"],
        "part2_score": graded["part2_score"],
        "part3_score": graded["part3_score"],
        "total_score": graded["total_score"],
        "details": graded["details"]
    }

@app.get("/api/submissions/{sub_id}")
def get_submission_endpoint(sub_id: str):
    sub = database.get_submission(sub_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Không tìm thấy kết quả bài thi!")
    return sub

@app.get("/api/exams/{exam_id}/results")
def get_exam_results(exam_id: str, class_name: Optional[str] = None):
    submissions = database.get_submissions_by_exam(exam_id, class_filter=class_name)
    classes = database.get_exam_classes(exam_id)
    return {
        "submissions": submissions,
        "classes": classes
    }

@app.get("/api/exams/{exam_id}/export-excel")
def export_excel(exam_id: str, class_name: Optional[str] = "Tất cả"):
    exam = database.get_exam(exam_id, for_student=False)
    if not exam:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề thi!")

    filter_val = None if (not class_name or class_name.lower() in ["tất cả", "all"]) else class_name
    submissions = database.get_submissions_by_exam(exam_id, class_filter=filter_val)
    
    excel_stream = excel_exporter.generate_exam_results_excel(
        exam_info=exam,
        submissions=submissions,
        class_filter=class_name or "Tất cả"
    )

    # Safe filename without non-ASCII characters in header
    safe_ascii_title = "".join(c for c in exam.get("title", "Bang_Diem") if c.isascii() and (c.isalnum() or c in ("_", "-"))).strip()
    if not safe_ascii_title:
        safe_ascii_title = f"Bang_Diem_Mon_Toan_{exam_id}"
    safe_ascii_title = safe_ascii_title.replace(" ", "_")[:30]
    date_str = datetime.date.today().strftime('%Y%m%d')
    ascii_filename = f"{safe_ascii_title}_{date_str}.xlsx"
    encoded_utf8_filename = quote(f"Bảng_Điểm_{exam.get('title', 'Toan')}_{date_str}.xlsx")

    headers = {
        "Content-Disposition": f'attachment; filename="{ascii_filename}"; filename*=UTF-8\'\'{encoded_utf8_filename}'
    }

    return StreamingResponse(
        excel_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


# ========================================================
# HTML PAGE SERVING ROUTES
# ========================================================

TEMPLATES_DIR = "templates"

def serve_template(template_name: str) -> HTMLResponse:
    path = os.path.join(TEMPLATES_DIR, template_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content=f"<h1>Template {template_name} not found</h1>", status_code=404)

@app.get("/", response_class=HTMLResponse)
def index_page():
    return serve_template("index.html")

@app.get("/teacher", response_class=HTMLResponse)
def teacher_page():
    return serve_template("teacher.html")

@app.get("/exam/{exam_id}", response_class=HTMLResponse)
def exam_page(exam_id: str):
    return serve_template("exam.html")

@app.get("/result/{sub_id}", response_class=HTMLResponse)
def result_page(sub_id: str):
    return serve_template("result.html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)

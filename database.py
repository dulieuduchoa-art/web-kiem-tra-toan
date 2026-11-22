"""
Database management and grading engine for Online Math Exam Application.
Supports both SQLite (local development) and PostgreSQL (Neon / Supabase / Render cloud deployment)
via DATABASE_URL environment variable.
"""

import os
import json
import uuid
import datetime
import math
from typing import Dict, List, Any, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_db_url() -> str:
    url = os.environ.get("DATABASE_URL", "").strip()
    # Normalize postgres:// -> postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    # Ensure SSL is required for remote Postgres services (Neon, Supabase, Render)
    if url.startswith("postgresql://") and "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return url

def is_postgres() -> bool:
    return get_db_url().startswith("postgresql://")

def get_sqlite_path() -> str:
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return "/tmp/math_exams.db"
    return os.path.join(BASE_DIR, "math_exams.db")

PART2_PROGRESSIVE_SCORES = {
    0: 0.0,
    1: 0.1,
    2: 0.25,
    3: 0.5,
    4: 1.0
}

_DB_INITIALIZED = False

def get_connection():
    global _DB_INITIALIZED
    if is_postgres():
        import psycopg2
        import psycopg2.extras
        url = get_db_url()
        conn = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
        if not _DB_INITIALIZED:
            _DB_INITIALIZED = True
            init_db(conn_override=conn)
        return conn
    else:
        import sqlite3
        conn = sqlite3.connect(get_sqlite_path())
        conn.row_factory = sqlite3.Row
        if not _DB_INITIALIZED:
            _DB_INITIALIZED = True
            init_db(conn_override=conn)
        return conn

def run_sql(cursor, query: str, params: tuple = ()):
    """Executes SQL converting ? to %s if on PostgreSQL"""
    if is_postgres():
        pg_query = query.replace("?", "%s")
        cursor.execute(pg_query, params)
    else:
        cursor.execute(query, params)

def init_db(conn_override=None):
    should_close = False
    if conn_override is not None:
        conn = conn_override
    else:
        if is_postgres():
            import psycopg2
            import psycopg2.extras
            url = get_db_url()
            conn = psycopg2.connect(url, cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            import sqlite3
            conn = sqlite3.connect(get_sqlite_path())
            conn.row_factory = sqlite3.Row
        should_close = True

    cursor = conn.cursor()

    # Teacher settings table (default password: 123456)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacher_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Check if default teacher password exists
    run_sql(cursor, "SELECT value FROM teacher_settings WHERE key = ?", ('teacher_password',))
    row = cursor.fetchone()
    if not row:
        run_sql(cursor, "INSERT INTO teacher_settings (key, value) VALUES (?, ?)", ('teacher_password', '123456'))

    # Exams table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            grade TEXT NOT NULL,
            book TEXT NOT NULL,
            chapter TEXT,
            duration_minutes INTEGER NOT NULL DEFAULT 50,
            shuffle_questions INTEGER NOT NULL DEFAULT 0,
            shuffle_options INTEGER NOT NULL DEFAULT 0,
            is_published INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            questions_json TEXT NOT NULL
        )
    """)

    # Submissions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id TEXT PRIMARY KEY,
            exam_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            start_time TEXT,
            submit_time TEXT NOT NULL,
            time_spent_seconds INTEGER NOT NULL DEFAULT 0,
            tab_switch_count INTEGER NOT NULL DEFAULT 0,
            part1_score REAL NOT NULL DEFAULT 0.0,
            part2_score REAL NOT NULL DEFAULT 0.0,
            part3_score REAL NOT NULL DEFAULT 0.0,
            total_score REAL NOT NULL DEFAULT 0.0,
            answers_json TEXT NOT NULL,
            details_json TEXT NOT NULL
        )
    """)

    conn.commit()
    if should_close:
        conn.close()

def verify_teacher_password(password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    run_sql(cursor, "SELECT value FROM teacher_settings WHERE key = ?", ('teacher_password',))
    row = cursor.fetchone()
    conn.close()
    if row and row["value"] == password:
        return True
    return False

def change_teacher_password(old_pw: str, new_pw: str) -> bool:
    if not verify_teacher_password(old_pw):
        return False
    conn = get_connection()
    cursor = conn.cursor()
    run_sql(cursor, "UPDATE teacher_settings SET value = ? WHERE key = ?", (new_pw, 'teacher_password'))
    conn.commit()
    conn.close()
    return True

# --- Exam Operations ---

def save_exam(exam_data: Dict[str, Any]) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    
    exam_id = exam_data.get("id") or str(uuid.uuid4())[:8]
    created_at = exam_data.get("created_at") or datetime.datetime.now().isoformat()
    questions_json = json.dumps(exam_data.get("questions", []), ensure_ascii=False)
    
    # Universal delete-then-insert pattern working on both SQLite and PostgreSQL
    run_sql(cursor, "DELETE FROM exams WHERE id = ?", (exam_id,))
    run_sql(cursor, """
        INSERT INTO exams 
        (id, title, grade, book, chapter, duration_minutes, shuffle_questions, shuffle_options, is_published, created_at, questions_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        exam_id,
        exam_data.get("title", "Đề kiểm tra môn Toán"),
        str(exam_data.get("grade", "12")),
        exam_data.get("book", "Ket_Noi_Tri_Thuc"),
        exam_data.get("chapter", ""),
        int(exam_data.get("duration_minutes", 50)),
        1 if exam_data.get("shuffle_questions") else 0,
        1 if exam_data.get("shuffle_options") else 0,
        1 if exam_data.get("is_published", True) else 0,
        created_at,
        questions_json
    ))
    
    conn.commit()
    conn.close()
    return exam_id

def get_exam(exam_id: str, for_student: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    run_sql(cursor, "SELECT * FROM exams WHERE id = ?", (exam_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    
    exam = dict(row)
    questions = json.loads(exam["questions_json"])
    
    if for_student:
        sanitized_questions = []
        for q in questions:
            sq = {
                "id": q.get("id"),
                "part": q.get("part"),
                "number": q.get("number"),
                "difficulty": q.get("difficulty"),
                "points": q.get("points"),
                "stem": q.get("stem")
            }
            if q.get("part") == 1:
                sq["options"] = q.get("options", [])
            elif q.get("part") == 2:
                sq["items"] = [{"key": it["key"], "text": it["text"]} for it in q.get("items", [])]
            elif q.get("part") == 3:
                sq["placeholder"] = "Nhập số (chấp nhận cả dấu . và ,)"
            sanitized_questions.append(sq)
        exam["questions"] = sanitized_questions
    else:
        exam["questions"] = questions
        
    return exam

def list_exams() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.title, e.grade, e.book, e.chapter, e.duration_minutes, 
               e.shuffle_questions, e.shuffle_options, e.is_published, e.created_at,
               COUNT(s.id) as submission_count, AVG(s.total_score) as avg_score
        FROM exams e
        LEFT JOIN submissions s ON e.id = s.exam_id
        GROUP BY e.id, e.title, e.grade, e.book, e.chapter, e.duration_minutes, 
                 e.shuffle_questions, e.shuffle_options, e.is_published, e.created_at
        ORDER BY e.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        d = dict(r)
        d["avg_score"] = round(float(d["avg_score"]), 2) if d["avg_score"] is not None else 0.0
        result.append(d)
    return result

def delete_exam(exam_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    run_sql(cursor, "DELETE FROM submissions WHERE exam_id = ?", (exam_id,))
    run_sql(cursor, "DELETE FROM exams WHERE id = ?", (exam_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

# --- Grading Logic Engine ---

def parse_number_flexible(val_str: str) -> Optional[float]:
    """
    Parses a string into float accepting both dot (.) and comma (,)
    and handling simple fractions like 1/2 or -4/9.
    """
    if not val_str:
        return None
    cleaned = str(val_str).strip().replace(" ", "").replace(",", ".")
    if not cleaned:
        return None
    try:
        if "/" in cleaned:
            parts = cleaned.split("/")
            if len(parts) == 2 and float(parts[1]) != 0:
                return float(parts[0]) / float(parts[1])
        return float(cleaned)
    except Exception:
        return None

def grade_submission(exam_data: Dict[str, Any], student_answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Grades an exam submission strictly following Ministry of Education rules:
    - Part I: 12 questions * 0.25 = 3.0 pts
    - Part II: 4 questions * 1.0 = 4.0 pts (progressive scoring: 1->0.1, 2->0.25, 3->0.5, 4->1.0)
    - Part III: 6 questions * 0.5 = 3.0 pts (accepts . and ,)
    Total = 10.0 points
    """
    questions = exam_data.get("questions", [])
    
    part1_score = 0.0
    part2_score = 0.0
    part3_score = 0.0
    
    details = []
    
    for q in questions:
        q_id = str(q.get("id"))
        q_num = q.get("number")
        part = q.get("part")
        user_ans = student_answers.get(q_id)
        
        q_detail = {
            "id": q_id,
            "number": q_num,
            "part": part,
            "stem": q.get("stem"),
            "difficulty": q.get("difficulty"),
            "explanation": q.get("explanation", ""),
            "user_answer": user_ans,
            "points_earned": 0.0,
            "max_points": q.get("points", 0.0),
            "is_correct": False
        }
        
        # --- PART I: 4-CHOICE MULTIPLE CHOICE ---
        if part == 1:
            q_detail["options"] = q.get("options", [])
            correct = q.get("correct_answer")
            q_detail["correct_answer"] = correct
            
            if user_ans and str(user_ans).strip().upper() == str(correct).strip().upper():
                q_detail["points_earned"] = 0.25
                q_detail["is_correct"] = True
                part1_score += 0.25
            else:
                q_detail["points_earned"] = 0.0
                q_detail["is_correct"] = False
                
        # --- PART II: TRUE/FALSE (4 STATEMENTS a, b, c, d) ---
        elif part == 2:
            correct_map = q.get("correct_answers", {})
            items = q.get("items", [])
            q_detail["items"] = items
            q_detail["correct_answers"] = correct_map
            
            sub_correct_count = 0
            item_results = {}
            
            for item in items:
                k = item["key"]
                expected = correct_map.get(k)
                user_choice = None
                if isinstance(user_ans, dict):
                    user_val = user_ans.get(k)
                    if user_val is not None:
                        if isinstance(user_val, bool):
                            user_choice = user_val
                        elif str(user_val).strip().lower() in ["true", "dung", "đúng", "d", "đ", "1"]:
                            user_choice = True
                        elif str(user_val).strip().lower() in ["false", "sai", "s", "0"]:
                            user_choice = False
                
                is_sub_correct = (user_choice == expected)
                if is_sub_correct:
                    sub_correct_count += 1
                    
                item_results[k] = {
                    "text": item.get("text"),
                    "user_choice": user_choice,
                    "expected": expected,
                    "is_correct": is_sub_correct
                }
            
            earned = PART2_PROGRESSIVE_SCORES.get(sub_correct_count, 0.0)
            q_detail["sub_correct_count"] = sub_correct_count
            q_detail["item_results"] = item_results
            q_detail["points_earned"] = earned
            q_detail["is_correct"] = (sub_correct_count == 4)
            part2_score += earned
            
        # --- PART III: SHORT ANSWER ---
        elif part == 3:
            expected_raw = str(q.get("correct_answer", "")).strip()
            alt_answers = [str(a).strip() for a in q.get("alt_answers", [])]
            tolerance = q.get("tolerance", 0.01)
            
            q_detail["correct_answer"] = expected_raw
            q_detail["alt_answers"] = alt_answers
            
            is_match = False
            user_str = str(user_ans).strip() if user_ans is not None else ""
            
            if user_str:
                norm_user = user_str.replace(" ", "").replace(",", ".")
                norm_exp = expected_raw.replace(" ", "").replace(",", ".")
                if norm_user.lower() == norm_exp.lower():
                    is_match = True
                else:
                    for alt in alt_answers:
                        norm_alt = alt.replace(" ", "").replace(",", ".")
                        if norm_user.lower() == norm_alt.lower():
                            is_match = True
                            break
                
                if not is_match:
                    user_float = parse_number_flexible(user_str)
                    exp_float = parse_number_flexible(expected_raw)
                    if user_float is not None and exp_float is not None:
                        if abs(user_float - exp_float) <= tolerance:
                            is_match = True
                        else:
                            for alt in alt_answers:
                                alt_float = parse_number_flexible(alt)
                                if alt_float is not None and abs(user_float - alt_float) <= tolerance:
                                    is_match = True
                                    break
            
            if is_match:
                q_detail["points_earned"] = 0.5
                q_detail["is_correct"] = True
                part3_score += 0.5
            else:
                q_detail["points_earned"] = 0.0
                q_detail["is_correct"] = False
                
        details.append(q_detail)
        
    part1_score = round(part1_score, 2)
    part2_score = round(part2_score, 2)
    part3_score = round(part3_score, 2)
    total_score = round(part1_score + part2_score + part3_score, 2)
    
    return {
        "part1_score": part1_score,
        "part2_score": part2_score,
        "part3_score": part3_score,
        "total_score": total_score,
        "details": details
    }

# --- Submission Operations ---

def save_submission(sub_data: Dict[str, Any]) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    
    sub_id = sub_data.get("id") or str(uuid.uuid4())
    submit_time = sub_data.get("submit_time") or datetime.datetime.now().isoformat()
    
    run_sql(cursor, """
        INSERT INTO submissions 
        (id, exam_id, student_name, student_class, start_time, submit_time, 
         time_spent_seconds, tab_switch_count, part1_score, part2_score, part3_score, 
         total_score, answers_json, details_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sub_id,
        sub_data["exam_id"],
        sub_data.get("student_name", "").strip(),
        sub_data.get("student_class", "").strip().upper(),
        sub_data.get("start_time"),
        submit_time,
        int(sub_data.get("time_spent_seconds", 0)),
        int(sub_data.get("tab_switch_count", 0)),
        float(sub_data.get("part1_score", 0.0)),
        float(sub_data.get("part2_score", 0.0)),
        float(sub_data.get("part3_score", 0.0)),
        float(sub_data.get("total_score", 0.0)),
        json.dumps(sub_data.get("answers", {}), ensure_ascii=False),
        json.dumps(sub_data.get("details", []), ensure_ascii=False)
    ))
    
    conn.commit()
    conn.close()
    return sub_id

def get_submission(sub_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    run_sql(cursor, """
        SELECT s.*, e.title as exam_title, e.grade as exam_grade, e.duration_minutes
        FROM submissions s
        JOIN exams e ON s.exam_id = e.id
        WHERE s.id = ?
    """, (sub_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["answers"] = json.loads(d["answers_json"])
    d["details"] = json.loads(d["details_json"])
    return d

def get_submissions_by_exam(exam_id: str, class_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    if class_filter and class_filter.strip() and class_filter.strip().upper() != "ALL":
        run_sql(cursor, """
            SELECT * FROM submissions 
            WHERE exam_id = ? AND student_class = ?
            ORDER BY total_score DESC, submit_time ASC
        """, (exam_id, class_filter.strip().upper()))
    else:
        run_sql(cursor, """
            SELECT * FROM submissions 
            WHERE exam_id = ?
            ORDER BY total_score DESC, submit_time ASC
        """, (exam_id,))
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        d = dict(r)
        d["answers"] = json.loads(d["answers_json"])
        d["details"] = json.loads(d["details_json"])
        result.append(d)
    return result

def get_exam_classes(exam_id: str) -> List[str]:
    conn = get_connection()
    cursor = conn.cursor()
    run_sql(cursor, """
        SELECT DISTINCT student_class FROM submissions 
        WHERE exam_id = ? AND student_class IS NOT NULL AND student_class != ''
        ORDER BY student_class ASC
    """, (exam_id,))
    rows = cursor.fetchall()
    conn.close()
    classes = []
    for r in rows:
        val = r["student_class"] if isinstance(r, dict) or hasattr(r, "__getitem__") else r[0]
        if val:
            classes.append(val)
    return classes

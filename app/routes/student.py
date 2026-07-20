from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Student, Course

router = APIRouter()


# -----------------------------
# Get Student Information
# -----------------------------
@router.get("/student/{student_code}")
def get_student(student_code: str):

    db = SessionLocal()

    student = db.query(Student).filter(
        Student.student_code == student_code
    ).first()

    if not student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = db.query(Course).filter(
        Course.id == student.course_id
    ).first()

    db.close()

    return {
        "id": student.id,
        "student_code": student.student_code,
        "name": student.name,
        "email": student.email,
        "department": student.department,
        "grade": student.grade,
        "course": course.name
    }
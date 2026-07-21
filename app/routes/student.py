from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import StudentResponse

router = APIRouter()


# -----------------------------
# Get Student Information
# -----------------------------
@router.get(
    "/student/{student_code}",
    response_model=StudentResponse,
    summary="Get Student Information",
    description="Returns all information about a student using the student code."
)
def get_student(
    student_code: str,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.student_code == student_code
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": student.id,
        "student_code": student.student_code,
        "name": student.name,
        "email": student.email,
        "department": student.department,
        "grade": student.grade,
        "course": student.course.name
    }
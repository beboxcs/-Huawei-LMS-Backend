from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Student, Course, Module, Progress

router = APIRouter()


@router.get("/leaderboard/{course_name}")
def leaderboard(course_name: str):

    db = SessionLocal()

    # Find the course
    course = db.query(Course).filter(
        Course.name == course_name
    ).first()

    if not course:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # All students in this course
    students = db.query(Student).filter(
        Student.course_id == course.id
    ).all()

    # All modules for this course
    modules = db.query(Module).filter(
        Module.course_id == course.id
    ).all()

    total_modules = len(modules)
    module_ids = [m.id for m in modules]

    leaderboard = []

    for student in students:

        completed = db.query(Progress).filter(
            Progress.student_id == student.id,
            Progress.module_id.in_(module_ids),
            Progress.completed == True
        ).count()

        percentage = 0

        if total_modules > 0:
            percentage = round((completed / total_modules) * 100)

        leaderboard.append({
            "student_code": student.student_code,
            "name": student.name,
            "progress": percentage
        })

    db.close()

    leaderboard.sort(
        key=lambda x: x["progress"],
        reverse=True
    )

    return leaderboard
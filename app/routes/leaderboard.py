from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Course, Progress
from app.schemas import LeaderboardResponse

router = APIRouter()


@router.get(
    "/leaderboard/{course_name}",
    response_model=list[LeaderboardResponse],
    summary="Course Leaderboard",
    description="Ranks students by completion percentage within a Huawei course."
)
def leaderboard(
    course_name: str,
    db: Session = Depends(get_db)
):

    # Find the course
    course = db.query(Course).filter(
        Course.name == course_name
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    students = course.students
    modules = course.modules

    total_modules = len(modules)
    module_ids = [module.id for module in modules]

    leaderboard = []

    for student in students:

        completed = db.query(Progress).filter(
            Progress.student_id == student.id,
            Progress.module_id.in_(module_ids),
            Progress.completed == True
        ).count()

        percentage = 0

        if total_modules > 0:
            percentage = round(
                completed * 100 / total_modules
            )

        leaderboard.append({
            "student_code": student.student_code,
            "name": student.name,
            "progress": percentage
        })

    leaderboard.sort(
        key=lambda student: student["progress"],
        reverse=True
    )

    return leaderboard
from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Course

router = APIRouter()


@router.get("/courses")
def get_courses():

    db = SessionLocal()

    courses = db.query(Course).all()

    db.close()

    return courses


@router.get("/course/{course_id}")
def get_course(course_id: int):

    db = SessionLocal()

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    db.close()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course
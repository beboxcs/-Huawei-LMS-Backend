from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Course, Module

router = APIRouter(
    tags=["Modules"]
)


@router.get(
    "/modules/{course_name}",
    summary="Get Course Modules",
    description="Returns all modules that belong to a Huawei course."
)
def get_modules(
    course_name: str,
    db: Session = Depends(get_db)
):

    # Find the course by its name
    course = db.query(Course).filter(
        Course.name == course_name
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    modules = (
        db.query(Module)
        .filter(Module.course_id == course.id)
        .order_by(Module.module_order)
        .all()
    )

    return [
        {
            "id": module.id,
            "title": module.title,
            "order": module.module_order
        }
        for module in modules
    ]
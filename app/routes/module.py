from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Course
from app.schemas import ModuleResponse

router = APIRouter()


# -----------------------------
# Get Modules of a Course
# -----------------------------
@router.get(
    "/modules/{course_name}",
    response_model=list[ModuleResponse],
    summary="Get Course Modules",
    description="Returns all modules that belong to a Huawei course."
)
def get_modules(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    modules = sorted(
        course.modules,
        key=lambda module: module.module_order
    )

    return [
        {
            "id": module.id,
            "title": module.title,
            "order": module.module_order
        }
        for module in modules
    ]
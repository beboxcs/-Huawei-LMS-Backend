from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Module

router = APIRouter()


@router.get("/course/{course_id}/modules")
def get_modules(course_id: int):

    db = SessionLocal()

    modules = (
        db.query(Module)
        .filter(Module.course_id == course_id)
        .order_by(Module.module_order)
        .all()
    )

    db.close()

    if not modules:
        raise HTTPException(
            status_code=404,
            detail="No modules found for this course"
        )

    return [
        {
            "id": module.id,
            "title": module.title,
            "order": module.module_order
        }
        for module in modules
    ]
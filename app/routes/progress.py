from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student, Module, Progress
from app.schemas import (
    ProgressUpdate,
    ProgressResponse
)

router = APIRouter()


@router.put(
    "/progress",
    summary="Update Student Progress",
    description="Marks a module as completed or incomplete for a student."
)
def update_progress(
    data: ProgressUpdate,
    db: Session = Depends(get_db)
):

    # -------------------------
    # Check student exists
    # -------------------------
    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -------------------------
    # Check module exists
    # -------------------------
    module = db.query(Module).filter(
        Module.id == data.module_id
    ).first()

    if not module:
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

    # -------------------------
    # Check module belongs to student's course
    # -------------------------
    if module.course_id != student.course_id:
        raise HTTPException(
            status_code=400,
            detail="Module does not belong to student's course"
        )

    # -------------------------
    # Update or Create Progress
    # -------------------------
    progress = db.query(Progress).filter(
        Progress.student_id == data.student_id,
        Progress.module_id == data.module_id
    ).first()

    if progress:
        progress.completed = data.completed
    else:
        progress = Progress(
            student_id=data.student_id,
            module_id=data.module_id,
            completed=data.completed
        )
        db.add(progress)

    db.commit()

    return {
        "message": "Progress updated successfully"
    }


@router.get(
    "/progress/{student_code}",
    response_model=list[ProgressResponse],
    summary="Get Student Progress",
    description="Returns all modules in the student's course and whether each one has been completed."
)
def get_progress(
    student_code: str,
    db: Session = Depends(get_db)
):

    # -------------------------
    # Find student
    # -------------------------
    student = db.query(Student).filter(
        Student.student_code == student_code
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # -------------------------
    # Get all modules for student's course
    # -------------------------
    modules = db.query(Module).filter(
        Module.course_id == student.course_id
    ).order_by(
        Module.module_order
    ).all()

    result = []

    for module in modules:

        progress = db.query(Progress).filter(
            Progress.student_id == student.id,
            Progress.module_id == module.id
        ).first()

        result.append(
            ProgressResponse(
                module_id=module.id,
                module_title=module.title,
                completed=progress.completed if progress else False
            )
        )

    return result
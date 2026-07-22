from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student, Module, Progress, Course
from app.schemas import (
    ProgressUpdate,
    ProgressResponse,
    ProgressSummaryResponse
)

router = APIRouter(
    tags=["Progress"]
)


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

    # Find student
    student = db.query(Student).filter(
        Student.student_code == student_code
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Get all modules
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


@router.get(
    "/progress-summary/{student_code}",
    response_model=ProgressSummaryResponse,
    summary="Get Student Progress Summary",
    description="Returns the student's overall course progress."
)
def get_progress_summary(
    student_code: str,
    db: Session = Depends(get_db)
):

    # Find student
    student = db.query(Student).filter(
        Student.student_code == student_code
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Find course
    course = db.query(Course).filter(
        Course.id == student.course_id
    ).first()

    modules = db.query(Module).filter(
        Module.course_id == student.course_id
    ).all()

    total_modules = len(modules)

    module_ids = [module.id for module in modules]

    completed_modules = db.query(Progress).filter(
        Progress.student_id == student.id,
        Progress.module_id.in_(module_ids),
        Progress.completed == True
    ).count()

    progress_percentage = 0

    if total_modules > 0:
        progress_percentage = round(
            (completed_modules / total_modules) * 100
        )

    return ProgressSummaryResponse(
        student=student.name,
        student_code=student.student_code,
        course=course.name,
        completed_modules=completed_modules,
        total_modules=total_modules,
        progress_percentage=progress_percentage
    )
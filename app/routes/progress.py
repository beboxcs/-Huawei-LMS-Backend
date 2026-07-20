from fastapi import APIRouter, HTTPException

from app.database import SessionLocal
from app.models import Progress, Student, Module, Course
from app.schemas import ProgressUpdate

router = APIRouter()


# ---------------------------------
# Update Module Progress
# ---------------------------------
@router.put("/progress")
def update_progress(data: ProgressUpdate):

    db = SessionLocal()

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if not student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    module = db.query(Module).filter(
        Module.id == data.module_id
    ).first()

    if not module:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Module not found"
        )

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
    db.close()

    return {
        "message": "Progress updated successfully"
    }


# ---------------------------------
# Student Progress Percentage
# ---------------------------------
@router.get("/progress/{student_code}")
def get_progress(student_code: str):

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

    if not course:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    modules = db.query(Module).filter(
        Module.course_id == course.id
    ).all()

    total_modules = len(modules)

    module_ids = [module.id for module in modules]

    completed_modules = db.query(Progress).filter(
        Progress.student_id == student.id,
        Progress.module_id.in_(module_ids),
        Progress.completed == True
    ).count()

    percentage = 0

    if total_modules > 0:
        percentage = round((completed_modules / total_modules) * 100)

    db.close()

    return {
        "student": student.name,
        "student_code": student.student_code,
        "course": course.name,
        "completed_modules": completed_modules,
        "total_modules": total_modules,
        "progress_percentage": percentage
    }


# ---------------------------------
# Student Modules
# ---------------------------------
@router.get("/student/{student_code}/modules")
def get_student_modules(student_code: str):

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

    modules = (
        db.query(Module)
        .filter(Module.course_id == student.course_id)
        .order_by(Module.module_order)
        .all()
    )

    result = []

    for module in modules:

        progress = db.query(Progress).filter(
            Progress.student_id == student.id,
            Progress.module_id == module.id
        ).first()

        result.append({
            "id": module.id,
            "title": module.title,
            "order": module.module_order,
            "completed": progress.completed if progress else False
        })

    db.close()

    return result
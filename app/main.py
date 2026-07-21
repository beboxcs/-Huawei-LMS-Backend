from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from app.database import Base, engine
import app.models

from app.exceptions import (
    http_exception_handler,
    generic_exception_handler
)

from app.routes.student import router as student_router
from app.routes.module import router as module_router
from app.routes.progress import router as progress_router
from app.routes.leaderboard import router as leaderboard_router

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Home",
        "description": "General API information."
    },
    {
        "name": "Students",
        "description": "Operations related to Huawei students."
    },
    {
        "name": "Modules",
        "description": "Retrieve Huawei course modules."
    },
    {
        "name": "Progress",
        "description": "Track and update student learning progress."
    },
    {
        "name": "Leaderboard",
        "description": "Rank students based on course completion."
    },
]

app = FastAPI(
    title="Huawei LMS Backend API",
    description="""
Backend API for the Huawei Learning Management System.

## Features

- Student Management
- Huawei Courses
- Course Modules
- Progress Tracking
- Leaderboard
""",
    version="1.0.0",
    openapi_tags=tags_metadata
)

# Register exception handlers
app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.include_router(student_router, tags=["Students"])
app.include_router(module_router, tags=["Modules"])
app.include_router(progress_router, tags=["Progress"])
app.include_router(leaderboard_router, tags=["Leaderboard"])


@app.get(
    "/",
    tags=["Home"],
    summary="API Status"
)
def home():
    return {
        "message": "Huawei LMS Backend is Running!"
    }
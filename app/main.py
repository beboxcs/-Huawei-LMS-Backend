from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routes.student import router as student_router
from app.routes.module import router as module_router
from app.routes.progress import router as progress_router
from app.routes.leaderboard import router as leaderboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Huawei LMS Backend"
)

app.include_router(student_router)
app.include_router(module_router)
app.include_router(progress_router)
app.include_router(leaderboard_router)


@app.get("/")
def home():
    return {
        "message": "Huawei LMS Backend is Running!"
    }
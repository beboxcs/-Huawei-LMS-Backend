from pydantic import BaseModel


# ----------------------------
# Progress Update Request
# ----------------------------
class ProgressUpdate(BaseModel):
    student_id: int
    module_id: int
    completed: bool


# ----------------------------
# Student Response
# ----------------------------
class StudentResponse(BaseModel):
    id: int
    student_code: str
    name: str
    email: str
    department: str
    grade: str
    course: str


# ----------------------------
# Module Response
# ----------------------------
class ModuleResponse(BaseModel):
    id: int
    title: str
    order: int


# ----------------------------
# Progress Response
# ----------------------------
class ProgressResponse(BaseModel):
    student: str
    student_code: str
    course: str
    completed_modules: int
    total_modules: int
    progress_percentage: int


# ----------------------------
# Leaderboard Response
# ----------------------------
class LeaderboardResponse(BaseModel):
    student_code: str
    name: str
    progress: int
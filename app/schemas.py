from pydantic import BaseModel


class ProgressUpdate(BaseModel):
    student_id: int
    module_id: int
    completed: bool
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base


# -----------------------
# Students
# -----------------------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String)
    department = Column(String)
    grade = Column(String)

    # Foreign Key -> Course
    course_id = Column(Integer, ForeignKey("courses.id"))


# -----------------------
# Courses
# -----------------------
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)


# -----------------------
# Modules
# -----------------------
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String)
    module_order = Column(Integer)


# -----------------------
# Progress
# -----------------------
class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    module_id = Column(Integer, ForeignKey("modules.id"))
    completed = Column(Boolean, default=False)
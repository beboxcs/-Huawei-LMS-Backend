from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from app.database import Base


# -----------------------
# Students
# -----------------------
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_code = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False
    )

    department = Column(
        String,
        nullable=False
    )

    grade = Column(
        String,
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True
    )

    # Relationships
    course = relationship(
        "Course",
        back_populates="students"
    )

    progress = relationship(
        "Progress",
        back_populates="student",
        cascade="all, delete"
    )


# -----------------------
# Courses
# -----------------------
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    # Relationships
    students = relationship(
        "Student",
        back_populates="course"
    )

    modules = relationship(
        "Module",
        back_populates="course",
        cascade="all, delete"
    )


# -----------------------
# Modules
# -----------------------
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    module_order = Column(
        Integer,
        nullable=False
    )

    # Relationships
    course = relationship(
        "Course",
        back_populates="modules"
    )

    progress = relationship(
        "Progress",
        back_populates="module",
        cascade="all, delete"
    )


# -----------------------
# Progress
# -----------------------
class Progress(Base):
    __tablename__ = "progress"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "module_id",
            name="unique_student_module"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False,
        index=True
    )

    module_id = Column(
        Integer,
        ForeignKey("modules.id"),
        nullable=False,
        index=True
    )

    completed = Column(
        Boolean,
        nullable=False,
        default=False
    )

    # Relationships
    student = relationship(
        "Student",
        back_populates="progress"
    )

    module = relationship(
        "Module",
        back_populates="progress"
    )
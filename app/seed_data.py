print("Seed script started")

from app.database import Base, engine, SessionLocal
import app.models

from app.models import Student, Course, Module, Progress

# --------------------------------
# Create tables if they don't exist
# --------------------------------
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --------------------------------
# Clear old data
# --------------------------------
db.query(Progress).delete()
db.query(Module).delete()
db.query(Student).delete()
db.query(Course).delete()
db.commit()

# --------------------------------
# Create Courses
# --------------------------------
course_names = [
    ("AI", "Huawei AI"),
    ("WLAN", "Huawei WLAN"),
    ("Security", "Huawei Security"),
    ("Cloud Computing", "Huawei Cloud Computing"),
    ("Cloud Service", "Huawei Cloud Service"),
    ("Storage", "Huawei Storage"),
    ("Big Data", "Huawei Big Data"),
    ("5G", "Huawei 5G"),
    ("Datacom", "Huawei Datacom"),
    ("IoT", "Huawei IoT"),
    ("Intelligent Computing", "Huawei Intelligent Computing"),
]

for name, description in course_names:
    db.add(
        Course(
            name=name,
            description=description
        )
    )

db.commit()

# --------------------------------
# Get Courses
# --------------------------------
courses = db.query(Course).all()

course_map = {
    course.name: course
    for course in courses
}

# --------------------------------
# Sample Students
# --------------------------------
students = [

    Student(
        student_code="20231192",
        name="Osama Sameh Tony",
        email="osama@test.com",
        department="ICT",
        grade="Second Year",
        course_id=course_map["WLAN"].id
    ),

    Student(
        student_code="20231353",
        name="Mariam Sayed",
        email="mariam@test.com",
        department="ICT",
        grade="Second Year",
        course_id=course_map["AI"].id
    )

]

db.add_all(students)
db.commit()

# --------------------------------
# Create Modules
# --------------------------------
module_titles = [
    "Introduction",
    "Basic Concepts",
    "Intermediate",
    "Advanced",
    "Final Assessment"
]

for course in courses:

    for order, title in enumerate(module_titles, start=1):

        db.add(
            Module(
                course_id=course.id,
                title=title,
                module_order=order
            )
        )

db.commit()

print("Sample data created successfully!")

db.close()
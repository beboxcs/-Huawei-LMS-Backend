import pandas as pd

from app.database import SessionLocal
from app.models import Student, Course

db = SessionLocal()

df = pd.read_excel(
    "excel/huawei_students.xlsx",
    header=2,          # Change this if the Excel header row changes
    engine="openpyxl"
)

print(df.columns.tolist())

# Keep track of duplicate student codes inside the Excel file
seen_codes = set()

for _, row in df.iterrows():

    student_code = str(row["Student Code"]).strip()

    # Skip duplicate student codes inside Excel
    if student_code in seen_codes:
        continue

    seen_codes.add(student_code)

    # Find the student's course
    course = db.query(Course).filter(
        Course.name == str(row["Course"]).strip()
    ).first()

    # Skip if course doesn't exist
    if not course:
        print(f"Course not found: {row['Course']}")
        continue

    # Skip if student already exists in database
    existing = db.query(Student).filter(
        Student.student_code == student_code
    ).first()

    if existing:
        continue

    # Create student
    student = Student(
        student_code=student_code,
        name=str(row["Name EN"]).strip(),
        email=str(row["Email"]).strip(),
        department=str(row["Department"]).strip(),
        grade=str(row["Grade"]).strip(),
        course_id=course.id
    )

    db.add(student)

db.commit()
db.close()

print("Students imported successfully!")
# Huawei LMS Backend

Backend API for the Huawei Learning Management System built with FastAPI.

---

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- OpenPyXL
- Pydantic
- python-dotenv

---

## Features

- Student Management
- Huawei Courses
- Course Modules
- Student Progress Tracking
- Leaderboard
- Excel Student Import
- REST API
- Interactive Swagger Documentation

---

## Project Structure

```
Huawei-LMS-Backend/
│
├── app/
│   ├── routes/
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── main.py
│   └── ...
│
├── excel/
├── requirements.txt
├── README.md
├── .env
└── students.db
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/beboxcs/-Huawei-LMS-Backend.git
```

Go to the project folder:

```bash
cd Huawei-LMS-Backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=sqlite:///./students.db
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Students

- GET `/student/{student_code}`

### Modules

- GET `/modules/{course_name}`

### Progress

- GET `/progress/{student_code}`
- PUT `/progress`

### Leaderboard

- GET `/leaderboard/{course_name}`

---

## Database

SQLite

Tables:

- Students
- Courses
- Modules
- Progress

---

## Team

Huawei LMS Development Team

---

## License

This project was developed for educational purposes.
# Huawei LMS Backend

Backend API for the Huawei Learning Management System.

## Technologies

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pandas
- OpenPyXL

## Features

- Import students from Excel
- Manage students
- Manage Huawei courses
- Course modules
- Student progress tracking
- Leaderboard
- REST API

## Installation

1. Clone the repository:

```bash
git clone https://github.com/beboxcs/-Huawei-LMS-Backend.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn app.main:app --reload
```

4. Open the API documentation:

```
http://127.0.0.1:8000/docs
```

## Project Structure

```
Huawei-LMS-Backend/
│
├── app/
│   ├── routes/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   ├── seed_data.py
│   └── import_students.py
│
├── excel/
├── requirements.txt
├── README.md
└── .gitignore
```

## Database

- SQLite
- SQLAlchemy ORM

## Framework

- FastAPI
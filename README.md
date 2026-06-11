# Library Management System

A RESTful Library Management System built using FastAPI, SQLAlchemy, SQLite, and Pydantic. The project provides APIs for managing books, members, borrowing transactions, and returns while demonstrating core backend development concepts such as database relationships, foreign keys, validation, and CRUD operations.

## Features

### Book Management

* Create a new book
* View all books
* View a specific book by ID
* Update book details
* Delete a book
* Search books by title

### Member Management

* Register a new member
* View member details
* Update member information
* Delete a member

### Borrowing System

* Borrow a book
* Automatic due date generation
* Return a borrowed book
* Track book availability
* Prevent borrowing when no copies are available

### Reporting APIs

* View all borrow records
* View currently borrowed books
* View overdue books

## Tech Stack

* FastAPI
* SQLAlchemy ORM
* SQLite
* Pydantic
* Uvicorn

## Database Design

### Books Table

Stores information about books available in the library.

### Members Table

Stores registered library members.

### Borrow Records Table

Stores borrowing transactions including:

* Member ID
* Book ID
* Borrow Date
* Due Date
* Return Date

## Concepts Implemented

### FastAPI

* Route handling
* Path parameters
* Query parameters
* Dependency Injection
* HTTP Exceptions

### Pydantic

* Request validation
* Email validation
* Data schemas

### SQLAlchemy

* ORM Models
* CRUD Operations
* Filtering and Queries
* Foreign Keys
* Relationships using `back_populates`

### Database Relationships

* One Member → Many Borrow Records
* One Book → Many Borrow Records
* Many Borrow Records → One Member
* Many Borrow Records → One Book

## Project Structure

```text
Lib_Management/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Lib_Management
```

Install dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Learning Outcomes

Through this project, I gained hands-on experience with:

* Building REST APIs using FastAPI
* Designing relational databases
* Implementing SQLAlchemy ORM models
* Managing database relationships
* Using foreign keys for data integrity
* Performing CRUD operations
* Designing business logic for borrowing and returning books
* Version control using Git and GitHub

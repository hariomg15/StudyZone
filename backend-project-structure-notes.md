# Backend Project Structure Notes

## StudyZone Backend Structure

This note explains the main backend folders in a simple way.

Backend folders:

- `app/api/`
- `app/core/`
- `app/db/`
- `app/models/`
- `app/schemas/`

These folders help us keep the project clean and organized.

Think like this:

- `api` = where requests come in
- `core` = common backend logic
- `db` = database setup
- `models` = database table design
- `schemas` = request and response structure

---

## 1. `api/` - Routes

### Definition

The `api/` folder contains route files.
A route is a URL path connected to a Python function.

Short definition:

`api/` is the folder where we define endpoints for the frontend or client.

### Why we use it

We use `api/` so all endpoints stay in one logical place.
This makes the project easier to read and maintain.

If we do not separate routes, all endpoints may go into one file and the backend becomes messy.

### In this project

Files:

- `app/api/router.py`
- `app/api/v1/auth.py`
- `app/api/v1/users.py`
- `app/api/v1/courses.py`
- `app/api/v1/enrollements.py`

### Example

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/courses")
def list_courses():
    return [{"title": "Python Basics"}]
```

### Explanation

- `APIRouter()` creates a route group
- `@router.get("/courses")` means this function runs on `GET /courses`
- `list_courses()` returns course data

### StudyZone example

In `auth.py`:

- register user
- login user
- get current user

In `courses.py`:

- create course
- list courses
- search courses
- publish or unpublish course

In `enrollements.py`:

- enroll in a course
- view my enrollments

### Real-life meaning

When the frontend sends a request like:

`GET /api/v1/courses`

the backend checks the matching route in the `api/` folder and runs that function.

### Quick revision

- `api/` contains endpoints
- it handles incoming requests
- routes are grouped by feature
- examples: auth, courses, enrollments

---

## 2. `core/` - Config, Security, Dependencies

### Definition

The `core/` folder contains shared backend logic used in many places.

Short definition:

`core/` stores common settings and reusable logic.

### Why we use it

We use `core/` to avoid repeating code.
It keeps important logic in one place.

If we do not use `core/`, then config, auth logic, and dependency logic may get repeated in many files.

### In this project

Files:

- `app/core/config.py`
- `app/core/security.py`
- `app/core/dependecies.py`

### A. `config.py`

This file stores app settings.

Example:

```python
class Settings(BaseSettings):
    app_name: str = "study zone"
    debug: bool = True
    database_url: str
    secret_key: str
```

### Meaning

- `app_name` = project name
- `debug` = show SQL and debug information
- `database_url` = database connection string
- `secret_key` = key used for JWT token signing

### Why config is useful

We do not hardcode everything in random files.
Settings stay in one place and can also come from `.env`.

### B. `security.py`

This file handles password hashing and JWT token creation.

Example:

```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

```python
def create_access_token(data: dict) -> str:
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
```

### Meaning

- plain password should not be stored directly
- we store hashed password
- JWT token is created after login

### C. `dependecies.py`

This file contains reusable dependencies.

Example:

```python
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
```

### Meaning

- create DB session
- give it to route
- close it after request ends

Other dependency examples:

- `get_current_user`
- `require_teacher`
- `require_admin`

These are used for authentication and authorization.

### Important words

`Authentication`:
checking who the user is

`Authorization`:
checking what the user is allowed to do

`Dependency`:
a helper function that another function needs

### Quick revision

- `core/` stores shared logic
- `config.py` handles settings
- `security.py` handles password and JWT
- `dependecies.py` handles DB and current user logic

---

## 3. `db/` - Engine, Session, Base

### Definition

The `db/` folder contains database setup code.

Short definition:

`db/` connects the backend to the database.

### Why we use it

Database connection code should stay separate from route logic.
This keeps the app clean and reusable.

### In this project

Files:

- `app/db/session.py`
- `app/db/base.py`

### A. Engine

The engine is the main connection layer between SQLAlchemy and the database.

Example:

```python
engine = create_engine(DATABASE_URL, echo=settings.debug, **engine_kwargs)
```

### Meaning

- `create_engine(...)` prepares the database connection
- `DATABASE_URL` tells SQLAlchemy where the database is
- `echo=True` shows SQL queries in logs

### B. Session

A session is used to talk to the database during one request.

Example:

```python
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### What is a session?

A session is like a temporary working area for database operations.

With a session, we can:

- add data
- read data
- update data
- delete data
- commit changes

### Why session is needed

Without a session, routes cannot properly interact with the database.

### C. Base

Example:

```python
Base = declarative_base()
```

### Meaning

`Base` is the parent class for all SQLAlchemy models.

Example:

```python
class User(Base):
    __tablename__ = "users"
```

This means `User` is a database model linked to a table.

### Important words

`Engine`:
database connection setup

`SessionLocal`:
a factory that creates database sessions

`yield`:
it gives a value for use now, and cleanup can happen later

`declarative_base`:
SQLAlchemy base class for models

### Quick revision

- `engine` connects SQLAlchemy to DB
- `session` performs DB work
- `Base` is parent for models
- `get_db()` usually gives a session to routes

---

## 4. `models/` - SQLAlchemy Entities

### Definition

The `models/` folder contains SQLAlchemy  classes.
model
Short definition:

`models/` defines database tables in Python code.

### Why we use it

Instead of writing raw SQL everywhere, we define Python classes for tables.
This makes database work easier and more readable.

### What is SQLAlchemy?

SQLAlchemy is a Python library used to work with databases.

Short definition:

SQLAlchemy helps Python code talk to the database.

It is used for:

- creating models
- making database queries
- inserting data
- updating data
- deleting data
- handling relationships between tables

In this project, SQLAlchemy is the main database tool.

### What is ORM?

ORM means `Object Relational Mapping`.

Short definition:

ORM means we use Python classes and objects to work with database tables.

Simple meaning:

- database table becomes a Python class
- row becomes an object
- column becomes a class attribute

So instead of writing raw SQL like this:

```sql
SELECT * FROM users;
```

we can write Python like this:

```python
db.query(User).all()
```

That is the power of ORM.

### Why ORM is useful

ORM is useful because:

- code becomes easier to read
- Python developers can work faster
- table relationships become easier to manage
- less raw SQL is needed in everyday code

If we do not use ORM, then we must manually write many SQL queries and handle more low-level database logic.

### In this project

Files:

- `app/models/user.py`
- `app/models/course.py`
- `app/models/enrollment.py`

### Where SQLAlchemy is created in this project

SQLAlchemy setup starts in the `db/` folder.

In `app/db/base.py`:

```python
Base = declarative_base()
```

This `Base` is used as the parent class for all models.

In `app/db/session.py`:

```python
engine = create_engine(DATABASE_URL, echo=settings.debug, **engine_kwargs)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

This creates:

- `engine` for database connection
- `Sessionlocal` for database sessions

### Where SQLAlchemy models are created

Models are created in:

- `app/models/user.py`
- `app/models/course.py`
- `app/models/enrollment.py`

Example:

```python
class User(Base):
    __tablename__ = "users"
```

This means:

- `User` is a SQLAlchemy model
- it is linked to the `users` table

### Where SQLAlchemy is used

SQLAlchemy is used mostly inside route files and dependency files.

Examples:

In `app/core/dependecies.py`:

```python
db = Sessionlocal()
```

This creates a DB session.

In routes:

```python
user = db.query(User).filter(User.email == user_data.email).first()
```

```python
db.add(new_course)
db.commit()
db.refresh(new_course)
```

These are SQLAlchemy operations.

### Common SQLAlchemy operations in this project

- `db.query(Model)` = read data
- `.filter(...)` = add condition
- `.first()` = get first result
- `.all()` = get all results
- `db.add(obj)` = add new row
- `db.commit()` = save changes
- `db.refresh(obj)` = get updated object from DB
- `db.delete(obj)` = delete row

### SQLAlchemy example from StudyZone

```python
course = db.query(Course).filter(Course.id == course_id).first()
```

Meaning:

- go to `courses` table
- find row where `id == course_id`
- return first matching course

Another example:

```python
new_user = User(
    name=user_data.name,
    email=user_data.email,
    password=hashed_password
)
db.add(new_user)
db.commit()
db.refresh(new_user)
```

Meaning:

- create Python object
- add it to session
- save it in database
- refresh it to get final DB values like `id`

### Example: User model

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
```

### Meaning

- `User` is a model class
- `users` is the table name
- `id`, `name`, `email` are table columns

### Example: Course model

```python
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

### Meaning

- one course belongs to one teacher
- `teacher_id` connects course to user table

### Relationship example

```python
teacher = relationship("User", back_populates="courses")
```

### Meaning

This links two models together.

Examples in project:

- one teacher has many courses
- one course has many sections
- one section has many lectures
- one student has many enrollments

### What is an entity?

An entity means a real object in the system.

Examples:

- user
- course
- section
- lecture
- note
- enrollment

### Quick revision

- models define database tables
- model fields become columns
- relationships connect tables
- SQLAlchemy lets us work with Python classes instead of raw SQL
- ORM means Python objects are mapped to database tables
- SQLAlchemy is created in `db/` and used in routes, dependencies, and models

---

## 5. `schemas/` - Request and Response Validation

### Definition

The `schemas/` folder contains Pydantic models used for validating request data and formatting response data.

Short definition:

`schemas/` defines what data should come in and what data should go out.

### Why we use it

We use schemas to make sure the API receives valid data.
They also control what data is returned to the client.

If we do not use schemas:

- invalid data may enter the system
- response format may become inconsistent
- security problems may happen if extra fields are returned

### In this project

Files:

- `app/schemas/user.py`
- `app/schemas/course.py`
- `app/schemas/content.py`
- `app/schemas/enrollment.py`
- `app/schemas/dashboard.py`

### Example: request schema

```python
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
```

### Meaning

This schema says that when a user registers:

- `name` must be a string
- `email` must be a valid email
- `password` must be a string

### Example: response schema

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True
```

### Meaning

This controls the response sent back to the client.
Notice that password is not returned.

That is very important.

### What is validation?

Validation means checking if input data is correct before using it.

Example:

- email should be valid
- title should not be empty
- price should be a number

### Example from course schema

```python
class CourseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    price: float | None = None
```

### Meaning

- `title` must have at least 2 characters
- `description` can be empty
- `price` can be a float or empty

### Quick revision

- schemas validate request data
- schemas shape response data
- they improve safety and consistency
- Pydantic is used here

---

## Simple Full Flow Example

Let us connect all folders in one example.

### Example: Create a course

Step 1:
Frontend sends request to route in `api/`

```python
@router.post("/", response_model=CourseResponse)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
```

Step 2:
`schemas/` validates `course_data`

- title must be valid
- price must follow rules

Step 3:
`core/dependecies.py` gives:

- DB session
- current logged-in teacher

Step 4:
`models/` creates a `Course` object

```python
new_course = Course(
    title=course_data.title,
    description=course_data.description,
    teacher_id=current_user.id
)
```

Step 5:
`db/` session saves data

```python
db.add(new_course)
db.commit()
db.refresh(new_course)
```

Step 6:
response goes back using response schema

This is how all folders work together.

---

## Easy Interview Notes

### What is `api/`?

It contains route files and endpoint logic.

### What is `core/`?

It contains shared logic like settings, security, and dependencies.

### What is `db/`?

It contains database connection setup, sessions, and base class.

### What is `models/`?

It contains SQLAlchemy classes that represent database tables.

### What is `schemas/`?

It contains Pydantic models for request validation and response formatting.

---

## Common Confusions

### Model vs Schema

`Model`:
used for database tables

`Schema`:
used for request and response data

### Session vs Engine

`Engine`:
connects to database

`Session`:
does actual read and write work

### Authentication vs Authorization

`Authentication`:
who are you?

`Authorization`:
what are you allowed to do?

---

## One-Line Memory Tricks

- `api` = endpoints live here
- `core` = common logic center
- `db` = database connection tools
- `models` = database table classes
- `schemas` = input and output rules

---

## Final Summary Table

| Folder | Main Purpose | Simple Meaning |
|---|---|---|
| `api/` | Routes and endpoints | where requests come in |
| `core/` | Shared app logic | config, security, dependencies |
| `db/` | Database setup | engine, session, base |
| `models/` | Database tables | SQLAlchemy classes |
| `schemas/` | Validation and response format | input/output structure |

---

## Quick Revision Page

- `api/` handles routes
- `core/` stores reusable logic
- `db/` connects backend to database
- `models/` define tables and relationships
- `schemas/` validate request and shape response
- routes use schemas, dependencies, models, and DB session together

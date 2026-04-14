# Backend Revision Notes

## 1. Pydantic Schemas

### What is a schema?

A schema is a data shape.
It tells the backend what data should come in and what data should go out.

In this project, schemas are inside `app/schemas/`.

### Request schema vs Response schema

`Request schema`:
used for input data coming from client

Example:

```python
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
```

This means:

- user must send `name`
- user must send valid `email`
- user must send `password`

`Response schema`:
used for output data sent back to client

Example:

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
```

This is good because password is not returned.

### BaseModel

`BaseModel` is the main Pydantic class.
We inherit from it to create schemas.

Example:

```python
from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    price: float
```

### Field

`Field` adds rules to a field.

Example:

```python
title: str = Field(..., min_length=2, max_length=255)
```

Meaning:

- `...` means required
- `min_length=2` means title cannot be too short
- `max_length=255` means title cannot be too long

### Validation

Validation means checking input before using it.

Examples from this project:

- `min_length`
- `max_length`
- `EmailStr`

### EmailStr

`EmailStr` checks that the input looks like a real email.

Example:

```python
email: EmailStr
```

If someone sends `abc`, validation fails.

### `from_attributes = True`

This tells Pydantic that it can read data from ORM objects like SQLAlchemy models.

Example:

```python
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
```

Without this, returning SQLAlchemy objects directly may fail.

### Simple example

```python
class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
```

This means:

- email must be valid
- password must be at least 6 characters

### Interview points

- Schema = data structure for input/output
- `BaseModel` is the base class for Pydantic schemas
- `Field` adds rules and metadata
- `EmailStr` validates email format
- `from_attributes = True` helps convert ORM model to response schema

---

## 2. Authentication

### What is authentication?

Authentication means checking who the user is.

Simple question:
Is this user really logged in?

### Register flow

In this project:

1. user sends name, email, password
2. backend checks if email already exists
3. password is hashed
4. user is saved in DB
5. response is returned

### Login flow

1. user sends email and password
2. backend finds user by email
3. backend verifies password
4. if correct, JWT token is created
5. token is returned to client

### Password hashing

Hashing means converting plain password into a secure unreadable value.

Example:

```python
hashed_password = hash_password(user_data.password)
```

Why needed:

- do not store plain passwords
- improves security

### Password verify

When user logs in, entered password is checked against hashed password.

Example:

```python
verify_password(user_data.password, user.password)
```

### JWT token creation

JWT is a signed token used for authentication.

Example:

```python
access_token = create_access_token(data={"sub": user.email})
```

### `sub` claim

`sub` means subject.
It usually stores the main identity of the user.

In this project, `sub` stores the user's email.

Why email?

- email is unique
- easy to query user by email

### Token expiry

Token expiry means token is valid only for a limited time.

Example:

```python
expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
```

Why needed:

- improves security
- old tokens should not live forever

### Bearer token flow

Client sends token in header like this:

```text
Authorization: Bearer <token>
```

Backend reads this token and verifies it.

### Simple example

```python
@router.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
```

This route:

- gets login data
- finds user
- verifies password
- returns token

### Interview points

- Authentication checks identity
- Register stores hashed password
- Login verifies password and returns token
- JWT token contains user identity
- `sub` is used for main user identity

---

## 3. Authorization

### What is authorization?

Authorization means checking what the user is allowed to do.

Simple question:
User is logged in, but does this user have permission?

### Current user extraction from token

In this project, backend:

1. reads bearer token
2. decodes JWT
3. gets `sub`
4. finds user in database
5. returns current user object

### Role-based access

Roles in this project:

- `student`
- `teacher`
- `admin`

### Protected endpoints

Protected endpoint means an endpoint that needs login or permission.

Example:

- create course
- publish course
- admin stats

### `require_teacher`

This dependency allows only teacher or admin.

Use case:

- create course
- manage content

### `require_admin`

This dependency allows only admin.

Use case:

- admin stats endpoint

### Simple example

```python
def require_teacher(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(status_code=403, detail="You do not have permission")
    return current_user
```

### Interview points

- Authentication = who are you
- Authorization = what can you do
- Token is used to find current user
- Role-based access is implemented using dependencies
- `require_teacher` and `require_admin` protect routes

---

## 4. Database + SQLAlchemy

### What is SQLAlchemy?

SQLAlchemy is a Python library used to work with databases.

It helps us:

- define tables
- query data
- insert data
- update data
- delete data

### What is ORM?

ORM means Object Relational Mapping.

Simple meaning:

- table -> Python class
- row -> Python object
- column -> class field

### `create_engine`

This creates the database connection setup.

Example:

```python
engine = create_engine(DATABASE_URL, echo=settings.debug, **engine_kwargs)
```

### `sessionmaker`

This creates session factory.

Example:

```python
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### `declarative_base`

This creates the base class for all models.

Example:

```python
Base = declarative_base()
```

### `Column`

`Column` defines a database field.

Example:

```python
id = Column(Integer, primary_key=True, index=True)
```

### `ForeignKey`

`ForeignKey` connects one table to another.

Example:

```python
teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

Meaning:
course belongs to one user as teacher

### `relationship`

`relationship` connects models at Python level.

Example:

```python
teacher = relationship("User", back_populates="courses")
```

### Common DB operations

`query`:
read data

```python
db.query(User)
```

`filter`:
apply condition

```python
.filter(User.email == user_data.email)
```

`first`:
get first row

```python
.first()
```

`all`:
get all rows

```python
.all()
```

`commit`:
save changes

```python
db.commit()
```

`refresh`:
reload object from DB after commit

```python
db.refresh(new_user)
```

### Simple example

```python
new_course = Course(title="Python", teacher_id=1)
db.add(new_course)
db.commit()
db.refresh(new_course)
```

### Interview points

- SQLAlchemy is the DB library
- ORM maps tables to Python classes
- engine connects to DB
- session does DB work
- models define tables

---

## 5. Database Relationships

### In this project

#### One teacher -> many courses

One teacher can create many courses.

```python
courses = relationship("Course", back_populates="teacher")
```

#### One student -> many enrollments

One student can enroll in many courses.

#### One course -> many sections

Each course can have many sections.

#### One section -> many lectures/notes

Each section can contain many lectures and many notes.

#### Many students <-> many courses via Enrollment

This is many-to-many relation.

One student can enroll in many courses.
One course can have many students.

This is handled by `Enrollment` table.

### Why Enrollment table is separate

Because many-to-many relation usually needs a middle table.

Also, enrollment table can store extra fields like:

- enrollment date

### Interview points

- `ForeignKey` links tables
- `relationship` links Python models
- `Enrollment` is the bridge table
- many-to-many needs separate table

---

## 6. Loading Strategies

### `joinedload`

`joinedload` loads related data using SQL join.

Example:


```python
db.query(Course).options(joinedload(Course.teacher)).all()
```

Why used:

- fetch course and teacher together
- reduce extra queries

### `selectinload`

`selectinload` loads related data using separate optimized queries.

Example:

```python
db.query(Course).options(
    selectinload(Course.sections).selectinload(Section.lectures)
)
```

Why used:

- useful for nested collections
- often better for one-to-many lists

### Why eager loading is used

Eager loading means loading related data early.

Why needed:

- avoids many extra DB queries
- improves performance
- prevents N+1 query problem

### Interview points

- `joinedload` uses join
- `selectinload` uses separate select queries
- eager loading improves performance
- used when related data is definitely needed

---

## 7. Business Logic

### Free vs Paid course

If course is free:

- price should be `0.0`
- student can enroll without payment

If course is paid:

- student should not access content without payment or enrollment rule

### Published vs Unpublished course

Published course:

- visible to students

Unpublished course:

- only owner teacher or admin can see/manage it

### Who can create/update/delete/publish course

- teacher can manage own courses
- admin can manage all courses
- student cannot create or manage courses

### Who can access course content

- everyone can access free course content if rules allow
- paid course content is restricted
- teacher/admin can access based on ownership and role
- enrolled student can access enrolled course content

### Enrollment restriction logic

- only student can enroll
- course must exist
- course must be published
- free course can enroll directly
- duplicate enrollment is blocked

### Interview points

- business logic means real app rules
- role decides who can do what
- publication status controls visibility
- free/paid flag controls access

---

## 8. Migrations

### Why Alembic?

Alembic is used for database migrations.

Migration means controlled database schema change over time.

Why not only `create_all`?

- `create_all` is basic
- it does not track schema history properly
- Alembic supports versioned schema changes

### Initial migration

Initial migration creates first version of tables.

In this project:

- users
- courses
- sections
- lectures
- notes
- enrollments

### Enum type migration

This project also creates `userrole` enum in PostgreSQL.

Why needed:

- role field uses enum values
- DB should know allowed values

### Schema versioning

Schema versioning means keeping track of DB structure changes over time.

Benefits:

- easier team work
- safe DB updates
- rollback support

### Interview points

- Alembic manages schema changes
- migrations are version-controlled DB changes
- initial migration sets up tables
- enum migration supports role enum in DB

---

## 9. Environment Config

### `.env`

`.env` file stores environment variables.

These are settings kept outside code.

### `DATABASE_URL`

This tells the app which database to connect to.

Example:

```text
postgresql://postgres:password@localhost:5432/studyzone_db
```

### `SECRET_KEY`

Used to sign JWT tokens.

Why important:

- token security depends on it

### `teacher_signup_code`

Used as a protected internal code for teacher/admin related access logic.

### `access_token_expire_minutes`

Defines how long token stays valid.

### Interview points

- env config keeps secrets outside code
- `DATABASE_URL` connects DB
- `SECRET_KEY` signs token
- token expiry improves security

---

## 10. Deployment Basics

### Dockerfile

Dockerfile tells Docker how to build app image.

Example use:

- install Python
- copy code
- install requirements
- run uvicorn

### `docker-compose.yml`

This file runs multiple services together.

In this project:

- `db` service for PostgreSQL
- `app` service for FastAPI backend

### Running app with uvicorn

Uvicorn is ASGI server used to run FastAPI app.

Example:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Meaning:

- `app.main` = file path
- `app` = FastAPI app object

### Interview points

- Dockerfile builds app container
- docker-compose manages multi-container setup
- uvicorn runs FastAPI app

---

## 11. Backend Entities

### User

File: `app/models/user.py`

Important fields:

- `id`
- `name`
- `email`
- `password`
- `is_active`
- `role`

### Course

File: `app/models/course.py`

Important fields:

- `title`
- `description`
- `price`
- `is_free`
- `is_published`
- `teacher_id`

### Section

Important fields:

- `title`
- `order_num`
- `course_id`

### Lecture

Important fields:

- `title`
- `video_url`
- `duration`
- `is_preview`
- `order_num`

### Note

Important fields:

- `title`
- `pdf_url`

### Enrollment

File: `app/models/enrollment.py`

Important fields:

- `user_id`
- `course_id`
- unique enrollment constraint

### Why unique constraint?

It prevents same student from enrolling in same course again and again.

---

## 12. API Modules Used

### Auth routes

File: `app/api/v1/auth.py`

Used for:

- register
- login
- current user

### User/Admin stats

File: `app/api/v1/users.py`

Used for:

- admin statistics

### Courses/Content

File: `app/api/v1/courses.py`

Used for:

- course CRUD
- publish/unpublish
- sections
- lectures
- notes
- course content access

### Enrollments

File: `app/api/v1/enrollements.py`

Used for:

- enroll in course
- my enrollments
- course enrollments

### Main router

File: `app/api/router.py`

Used for:

- combining all routers

---

## 13. Recruiter Questions with Short Answers

### Why FastAPI instead of Django or Express?

FastAPI is simple, fast, uses Python type hints, gives automatic validation, and creates API docs automatically.

### What is `Depends`?

`Depends` is FastAPI dependency injection system. It gives reusable things like DB session or current user to routes.

### What is JWT? How is it different from session auth?

JWT is a signed token stored on client side. Session auth usually stores session data on server side.

### Why not store plain text passwords?

If DB leaks, all user passwords become visible. Hashing protects them.

### Explain `hash_password` and `verify_password`.

`hash_password` converts plain password into secure hash. `verify_password` checks user input against stored hash.

### Why store email in `sub` claim?

Because email is unique and easy to use for user lookup.

### What does `HTTPBearer` do?

It reads bearer token from `Authorization` header.

### How did you implement role-based access?

Using dependencies like `get_current_user`, `require_teacher`, and `require_admin`.

### Why use `joinedload` and `selectinload`?

To load related data efficiently and reduce extra queries.

### Difference between `relationship` and `ForeignKey`?

`ForeignKey` creates link in DB table. `relationship` creates easy object access in Python code.

### Why separate `Enrollment` table?

Because student-course is many-to-many relation and it also stores enrollment-specific data.

### How did you prevent duplicate enrollment?

By checking existing enrollment in code and also using unique constraint in DB.

### Purpose of `UniqueConstraint`?

It ensures one student cannot enroll in the same course twice.

### Why Alembic instead of `create_all`?

Alembic tracks schema changes over time and supports proper DB migration flow.

### Difference between Pydantic schema and SQLAlchemy model?

Schema handles input/output validation. Model handles database table structure.

### Where does request validation happen?

In Pydantic schemas before route logic runs fully.

### What is unpublished course visibility logic?

Students should not see unpublished courses. Only owner teacher or admin can access them.

### What is paid course access logic?

Paid course content is restricted unless access rules like enrollment/payment are satisfied.

### What is CORS?

CORS controls which frontend origins can call backend APIs from browser.

### Why use environment variables?

To keep config and secrets outside source code.

### Why Dockerize the project?

To make setup and deployment consistent across systems.

### If you scale this project, what will you improve?

- better payment system
- pagination
- caching
- background jobs
- stricter permissions
- better logging and tests

---

## 14. Quick Final Revision

- Pydantic schemas validate input and shape output
- Authentication checks identity
- Authorization checks permission
- SQLAlchemy handles DB through ORM
- relationships connect tables and models
- eager loading improves query performance
- business logic controls real app rules
- Alembic manages DB changes
- `.env` stores config
- Docker and uvicorn help run and deploy app


# StudyZone

StudyZone is a full-stack coaching platform built with FastAPI, PostgreSQL, and React. It supports student authentication, teacher course management, enrollments, protected course content, and an admin stats dashboard.

## Live Project

- Frontend: https://studyzone-frontend-wzzo.onrender.com/
- Backend API (local by default): `http://127.0.0.1:8000`
- API docs (local): `http://127.0.0.1:8000/docs`

## Core Features

- JWT-based login and registration
- Role-based flows for students, teachers, and admins
- Course creation, editing, publishing, and unpublishing
- Free course enrollments for students
- Nested course content with sections, lectures, and notes
- My Courses page for enrolled students
- Teacher dashboard for managing created courses
- Admin dashboard with platform statistics

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL
- Frontend: React, Vite, React Router, Axios
- Auth: JWT
- Deployment: Render
- Containerization: Docker, Docker Compose

## Project Structure

```text
studyzone/
|-- app/                  FastAPI backend
|   |-- api/              Route modules
|   |-- core/             Settings, auth, dependencies
|   |-- db/               Database setup
|   |-- models/           SQLAlchemy models
|   `-- schemas/          Pydantic schemas
|-- alembic/              Database migrations
|-- frontend/             React frontend
|   |-- public/
|   `-- src/
|-- Dockerfile
|-- docker-compose.yml
|-- requirements.txt
`-- README.md
```

## Backend Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/studyzone_db
SECRET_KEY=replace_with_a_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
TEACHER_SIGNUP_CODE=replace_with_your_code
```

4. Start PostgreSQL locally, or run Docker Compose:

```bash
docker-compose up --build
```

5. Run migrations:

```bash
alembic upgrade head
```

6. Start the backend server if you are not using Docker:

```bash
uvicorn app.main:app --reload
```

## Frontend Setup

1. Move into the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create a frontend env file if needed:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

4. Start the frontend:

```bash
npm run dev
```

## Main Routes

- `/` course listing page
- `/login` login page
- `/signup` student signup page
- `/my-courses` enrolled student courses
- `/teacher` teacher dashboard
- `/teacher/create-course` create course page
- `/admin` admin dashboard

## Important Notes

- Do not commit `.env` or any secret keys to GitHub.
- Rotate any secrets immediately if they were pushed earlier.
- The admin dashboard requires an admin user plus the `X-Admin-Access-Code` header value configured in the backend environment.

## Possible Improvements

- Add tests for backend routes and frontend flows
- Add payment support for paid courses
- Tighten CORS configuration for production
- Add CI/CD and deployment notes for backend

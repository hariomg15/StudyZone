<div align="center">
  <img src="./frontend/public/brand/studyzone-logo.jpeg" alt="StudyZone logo" width="120" />
  <h1>StudyZone</h1>
  <p><strong>Learn with structure.</strong> A full-stack coaching platform by Prince Jaiswal built with FastAPI, PostgreSQL, and React.</p>
  <p>
    <a href="https://studyzone-frontend-wzzo.onrender.com/">Live Frontend</a> |
    <a href="http://127.0.0.1:8000/docs">Local API Docs</a>
  </p>
</div>

## Overview

StudyZone is a role-based learning platform where students can discover and enroll in courses, teachers can create and manage course content, and admins can monitor platform-level stats. The project combines a FastAPI backend with a React frontend and is designed to feel clean, simple, and deployment-ready.

## Highlights

- Student signup, login, and enrolled course access
- Teacher dashboard for course creation and management
- Admin dashboard with protected platform stats
- Course publishing flow with free and premium labels
- Structured course content with sections, lectures, and notes
- Full-stack setup with Docker, Alembic, PostgreSQL, and Vite

## Live Demo

- Frontend: https://studyzone-frontend-wzzo.onrender.com/
- Backend API local base URL: `http://127.0.0.1:8000`
- API docs local URL: `http://127.0.0.1:8000/docs`

## UI Snapshot Notes

The current UI includes these polished screens:

- Signup page with founder intro card and student onboarding flow
- Login page with a focused access panel and feature callouts
- Course library page with search, pricing labels, and clean cards
- Course detail page with status, teacher info, and quick actions

## Core Features

### Authentication and Roles

- JWT-based login and protected routes
- Student self-signup flow
- Teacher and admin access handled through managed accounts
- Admin stats guarded by an extra access-code header

### Course Platform

- Browse published courses
- Search courses by title
- Create, update, publish, and unpublish courses
- Add sections, lectures, and PDF notes
- Access free content through enrollment

### Dashboards

- Student view for enrolled courses
- Teacher workspace for managing created courses
- Admin dashboard for total users, courses, and enrollments

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL
- Frontend: React, Vite, React Router, Axios
- Authentication: JWT
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
2. Install backend dependencies.

```bash
pip install -r requirements.txt
```

3. Create a root `.env` file.

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/studyzone_db
SECRET_KEY=replace_with_a_secure_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
TEACHER_SIGNUP_CODE=replace_with_your_code
```

4. Start PostgreSQL locally or use Docker Compose.

```bash
docker-compose up --build
```

5. Run database migrations.

```bash
alembic upgrade head
```

6. Start the backend server if you are not using Docker.

```bash
uvicorn app.main:app --reload
```

## Frontend Setup

1. Open the frontend folder.

```bash
cd frontend
```

2. Install frontend dependencies.

```bash
npm install
```

3. Add frontend environment config if needed.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

4. Start the frontend app.

```bash
npm run dev
```

## Main Routes

- `/` browse published courses
- `/login` sign in page
- `/signup` student registration page
- `/my-courses` enrolled student courses
- `/teacher` teacher dashboard
- `/teacher/create-course` create course page
- `/teacher/courses/:id` manage a specific course
- `/admin` admin dashboard

## Security Notes

- Never commit `.env` or secrets to GitHub
- Rotate any secrets immediately if they were exposed earlier
- The admin dashboard requires an admin account and the `X-Admin-Access-Code` header

## Future Improvements

- Payment integration for premium courses
- Automated testing for backend and frontend flows
- Production CORS tightening
- CI/CD pipeline and backend deployment notes

## Author

Built by Prince Jaiswal.

# 🚀 LMS Backend (Coaching Platform API)

A production-ready Learning Management System (LMS) backend built using FastAPI, PostgreSQL, and JWT authentication.
This project demonstrates real-world backend architecture with role-based access, course management, enrollment system, and protected content delivery.

---

## 🌐 Live Demo

* 🔗 API Docs: https://your-backend-link.onrender.com/docs
* 🔗 GitHub Repo: https://github.com/your-username/your-repo

---

## ✨ Features

### 🔐 Authentication & Authorization

* JWT-based authentication (Login/Register)
* Role-based access control (Student, Teacher, Admin)

### 📚 Course Management

* Teachers can create, update, delete courses
* Publish / Unpublish courses
* Course search functionality

### 🎓 Enrollment System

* Students can enroll in courses
* Prevent duplicate enrollments
* Access control for enrolled users only

### 📂 Course Content System

* Sections → Lectures → Notes structure
* Only enrolled users can access content
* Preview lectures support

### 👨‍🏫 Teacher Features

* View own created courses
* Manage course content
* View enrolled students

### 📊 Admin Dashboard

* Total users, courses, enrollments
* Platform statistics API

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT
* **Migration:** Alembic
* **Containerization:** Docker
* **API Testing:** Swagger UI

---

## 🏗️ Project Structure

```bash
app/
│
├── api/            # Routes (Auth, Courses, Enrollments)
├── core/           # Config, Security, Dependencies
├── db/             # Database connection
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
│
alembic/            # Database migrations
Dockerfile
docker-compose.yml
requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run with Docker

```bash
docker-compose up --build
```

---

### 4️⃣ Run migrations

```bash
alembic upgrade head
```

---

### 5️⃣ Access API

```text
http://localhost:8000/docs
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/lms_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🧠 Key Learnings

* Built scalable backend architecture
* Implemented JWT authentication securely
* Designed relational database with multiple entities
* Applied role-based authorization
* Containerized application using Docker
* Managed database migrations using Alembic

---

## 🎯 Future Improvements

* Frontend (React + Tailwind)
* Payment integration (Stripe/Razorpay)
* Advanced search & filtering
* Unit testing
* Pagination

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

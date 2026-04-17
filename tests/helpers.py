from tests.conftest import TestingSessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password


def register_student(client, name="Hari", email="hari@example.com", password="secret123"):
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "role": "student",
    }
    return client.post("/api/v1/auth/register", json=payload)


def login_user(client, email="hari@example.com", password="secret123"):
    payload = {
        "email": email,
        "password": password,
    }
    return client.post("/api/v1/auth/login", json=payload)


def create_user_directly(email, password="secret123", role=UserRole.teacher, name="User"):
    db = TestingSessionLocal()
    try:
        user = User(
            name=name,
            email=email,
            password=hash_password(password),
            role=role,
            is_active=True,
        )
        db.add(user)
        db.commit()
    finally:
        db.close()


def create_teacher_directly(client, email="teacher@example.com", password="secret123", name="Teacher"):
    create_user_directly(email=email, password=password, role=UserRole.teacher, name=name)
    login_response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password,
    })
    return login_response.json()["access_token"]


def create_admin_directly(client, email="admin@example.com", password="secret123", name="Admin"):
    create_user_directly(email=email, password=password, role=UserRole.admin, name=name)
    login_response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password,
    })
    return login_response.json()["access_token"]


def create_course_as_teacher(
    client,
    token,
    title="Math Course",
    is_free=True,
    is_published=True,
    price=0,
    description="A sample course",
):
    payload = {
        "title": title,
        "description": description,
        "price": price,
        "is_free": is_free,
        "thumbnail": None,
        "is_published": is_published,
    }

    return client.post(
        "/api/v1/courses/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

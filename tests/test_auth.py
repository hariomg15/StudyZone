def test_register_user_success(client):
    payload = {
        "name": "Hari",
        "email": "hari@example.com",
        "password": "secret123",
        "role": "student"
    }

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Hari"
    assert data["email"] == "hari@example.com"
    assert data["role"] == "student"


def test_register_duplicate_email_fails(client):
    payload = {
        "name": "Hari",
        "email": "hari@example.com",
        "password": "secret123",
        "role": "student"
    }

    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_teacher_role_fails(client):
    payload = {
        "name": "Prince",
        "email": "teacher@example.com",
        "password": "secret123",
        "role": "teacher"
    }

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Teacher and admin accounts are created internally only"


def test_login_success(client):
    register_payload = {
        "name": "Hari",
        "email": "hari@example.com",
        "password": "secret123",
        "role": "student"
    }

    login_payload = {
        "email": "hari@example.com",
        "password": "secret123"
    }

    client.post("/api/v1/auth/register", json=register_payload)
    response = client.post("/api/v1/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password_fails(client):
    register_payload = {
        "name": "Hari",
        "email": "hari@example.com",
        "password": "secret123",
        "role": "student"
    }

    wrong_login_payload = {
        "email": "hari@example.com",
        "password": "wrongpassword"
    }

    client.post("/api/v1/auth/register", json=register_payload)
    response = client.post("/api/v1/auth/login", json=wrong_login_payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_unknown_email_fails(client):
    payload = {
        "email": "unknown@example.com",
        "password": "secret123"
    }

    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

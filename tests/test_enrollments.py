from tests.helpers import (
    create_course_as_teacher,
    create_teacher_directly,
    login_user,
    register_student,
)


def test_student_can_enroll_in_free_published_course(client):
    register_student(client)
    student_token = login_user(client).json()["access_token"]

    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(client, teacher_token, is_free=True, is_published=True, price=0)
    course_id = course_response.json()["id"]

    response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 201
    assert response.json()["course_id"] == course_id


def test_duplicate_enrollment_fails(client):
    register_student(client)
    student_token = login_user(client).json()["access_token"]

    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(client, teacher_token, is_free=True, is_published=True, price=0)
    course_id = course_response.json()["id"]

    client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You are already enrolled in this course."


def test_student_cannot_enroll_in_paid_course(client):
    register_student(client)
    student_token = login_user(client).json()["access_token"]

    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(client, teacher_token, is_free=False, is_published=True, price=799)
    course_id = course_response.json()["id"]

    response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "This is not free course. Please complete payment to access it."


def test_student_cannot_enroll_in_unpublished_course(client):
    register_student(client)
    student_token = login_user(client).json()["access_token"]

    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(client, teacher_token, is_free=True, is_published=False, price=0)
    course_id = course_response.json()["id"]

    response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot enroll in an unpublished course"


def test_non_student_cannot_enroll(client):
    teacher_token = create_teacher_directly(client, email="teacher2@example.com")
    course_response = create_course_as_teacher(client, teacher_token, is_free=True, is_published=True, price=0)
    course_id = course_response.json()["id"]

    response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only students can enroll in courses."

from tests.helpers import create_admin_directly, create_course_as_teacher, create_teacher_directly, login_user, register_student


def test_student_cannot_create_course(client):
    register_student(client)
    student_token = login_user(client).json()["access_token"]

    response = client.post(
        "/api/v1/courses/",
        json={
            "title": "Unauthorized Course",
            "description": "Should fail",
            "price": 0,
            "is_free": True,
            "thumbnail": None,
            "is_published": False,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert response.status_code == 403


def test_teacher_cannot_access_admin_stats(client):
    teacher_token = create_teacher_directly(client)

    response = client.get(
        "/api/v1/users/admin/stats",
        headers={
            "Authorization": f"Bearer {teacher_token}",
            "X-Admin-Access-Code": "StudyZone1825",
        },
    )

    assert response.status_code == 403


def test_teacher_cannot_publish_another_teachers_course(client):
    teacher_one_token = create_teacher_directly(client, email="teacher1@example.com", name="Teacher One")
    teacher_two_token = create_teacher_directly(client, email="teacher2@example.com", name="Teacher Two")
    course_response = create_course_as_teacher(
        client,
        teacher_one_token,
        title="Owner Course",
        is_free=True,
        is_published=False,
        price=0,
    )
    course_id = course_response.json()["id"]

    response = client.patch(
        f"/api/v1/courses/{course_id}/publish",
        headers={"Authorization": f"Bearer {teacher_two_token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to publish this course"


def test_admin_can_publish_any_course(client):
    teacher_token = create_teacher_directly(client, email="teacher3@example.com", name="Teacher Three")
    course_response = create_course_as_teacher(
        client,
        teacher_token,
        title="Admin Publish Course",
        is_free=True,
        is_published=False,
        price=0,
    )
    course_id = course_response.json()["id"]
    admin_token = create_admin_directly(client)

    response = client.patch(
        f"/api/v1/courses/{course_id}/publish",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["is_published"] is True

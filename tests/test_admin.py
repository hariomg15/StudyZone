from tests.helpers import create_admin_directly, create_course_as_teacher, create_teacher_directly, register_student, login_user


def test_admin_stats_success_with_valid_header(client):
    register_student(client)
    login_user(client)
    teacher_token = create_teacher_directly(client)
    create_course_as_teacher(client, teacher_token, title="Admin Course", is_free=True, is_published=True, price=0)
    admin_token = create_admin_directly(client)

    response = client.get(
        "/api/v1/users/admin/stats",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "X-Admin-Access-Code": "StudyZone1825",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] >= 2
    assert data["total_courses"] == 1


def test_admin_stats_fail_with_wrong_access_code(client):
    admin_token = create_admin_directly(client)

    response = client.get(
        "/api/v1/users/admin/stats",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "X-Admin-Access-Code": "WrongCode",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid admin access code"

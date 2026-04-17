from tests.helpers import create_teacher_directly, create_course_as_teacher, register_student, login_user


def test_teacher_can_create_course(client):
    teacher_token = create_teacher_directly(client)

    response = create_course_as_teacher(
        client,
        teacher_token,
        title="Physics",
        is_free=True,
        is_published=False,
        price=0,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Physics"
    assert data["is_free"] is True
    assert data["is_published"] is False


def test_list_courses_shows_only_published_to_public(client):
    teacher_token = create_teacher_directly(client)
    create_course_as_teacher(client, teacher_token, title="Published", is_free=True, is_published=True, price=0)
    create_course_as_teacher(client, teacher_token, title="Draft", is_free=True, is_published=False, price=0)

    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    data = response.json()
    titles = [course["title"] for course in data]
    assert "Published" in titles
    assert "Draft" not in titles


def test_teacher_sees_all_courses_including_unpublished(client):
    teacher_token = create_teacher_directly(client)
    create_course_as_teacher(client, teacher_token, title="Published", is_free=True, is_published=True, price=0)
    create_course_as_teacher(client, teacher_token, title="Draft", is_free=True, is_published=False, price=0)

    response = client.get(
        "/api/v1/courses/",
        headers={"Authorization": f"Bearer {teacher_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    titles = [course["title"] for course in data]
    assert "Published" in titles
    assert "Draft" in titles


def test_public_cannot_view_unpublished_course_detail(client):
    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(
        client,
        teacher_token,
        title="Private Course",
        is_free=True,
        is_published=False,
        price=0,
    )
    course_id = course_response.json()["id"]

    response = client.get(f"/api/v1/courses/{course_id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Course is not published"


def test_teacher_can_publish_course(client):
    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(
        client,
        teacher_token,
        title="Draft Course",
        is_free=True,
        is_published=False,
        price=0,
    )
    course_id = course_response.json()["id"]

    response = client.patch(
        f"/api/v1/courses/{course_id}/publish",
        headers={"Authorization": f"Bearer {teacher_token}"},
    )

    assert response.status_code == 200
    assert response.json()["is_published"] is True


def test_teacher_can_update_own_course(client):
    teacher_token = create_teacher_directly(client)
    course_response = create_course_as_teacher(
        client,
        teacher_token,
        title="Old Title",
        is_free=True,
        is_published=False,
        price=0,
    )
    course_id = course_response.json()["id"]

    response = client.put(
        f"/api/v1/courses/{course_id}",
        json={"title": "New Title"},
        headers={"Authorization": f"Bearer {teacher_token}"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_course_list_supports_pagination(client):
    teacher_token = create_teacher_directly(client)
    create_course_as_teacher(client, teacher_token, title="Course 1", is_free=True, is_published=True, price=0)
    create_course_as_teacher(client, teacher_token, title="Course 2", is_free=True, is_published=True, price=0)
    create_course_as_teacher(client, teacher_token, title="Course 3", is_free=True, is_published=True, price=0)

    response = client.get("/api/v1/courses/?skip=1&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_search_courses_supports_query_and_pagination(client):
    teacher_token = create_teacher_directly(client)
    create_course_as_teacher(client, teacher_token, title="Mathematics", is_free=True, is_published=True, price=0)
    create_course_as_teacher(client, teacher_token, title="Math Advanced", is_free=True, is_published=True, price=0)
    create_course_as_teacher(client, teacher_token, title="Biology", is_free=True, is_published=True, price=0)

    response = client.get("/api/v1/courses/search?q=Math&skip=0&limit=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Math" in data[0]["title"]

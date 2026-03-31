import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";
import { getUser } from "../utils/auth";

function TeacherDashboard() {
  const user = getUser();
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const endpoint = user?.role === "admin" ? "/courses" : "/courses/my/created";
        const res = await api.get(endpoint);
        setCourses(res.data);
      } catch (requestError) {
        setError(requestError?.response?.data?.detail || "Failed to load courses");
      }
    };

    fetchCourses();
  }, [user?.role]);

  const publishedCount = courses.filter((course) => course.is_published).length;

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">{user?.role === "admin" ? "Course Control" : "Teacher Space"}</span>
          <h2>{user?.role === "admin" ? "See every course from one place" : "Manage your teaching workflow"}</h2>
          <p>
            Create new courses, open a course workspace, publish when ready, and keep sections,
            lectures, and notes organized.
          </p>
        </div>

        <div className="hero-badge">
          <strong>{courses.length}</strong>
          <span>{publishedCount} published</span>
        </div>
      </div>

      <div className="dashboard-toolbar">
        <Link to="/teacher/create-course" className="button">Create Course</Link>
      </div>

      {error && <div className="notice notice--error">{error}</div>}

      <div className="course-grid">
        {courses.map((course) => (
          <article key={course.id} className="course-card">
            <div className="course-card__top">
              <span className="pill">{course.is_published ? "Published" : "Draft"}</span>
              <span className="course-card__price">
                {course.is_free ? "Free" : `Rs ${course.price}`}
              </span>
            </div>
            <h3>{course.title}</h3>
            <p>{course.description || "No description added yet."}</p>
            <div className="meta-row">
              <span>Teacher: {course.teacher?.name || "Unknown"}</span>
            </div>
            <div className="action-row">
              <Link className="button button--small" to={`/teacher/courses/${course.id}`}>
                Manage Course
              </Link>
              <Link className="button button--ghost button--small" to={`/courses/${course.id}`}>
                Preview
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default TeacherDashboard;

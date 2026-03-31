import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import { getUser, isLoggedIn } from "../utils/auth";
import { showToast } from "../utils/toast";

function CourseDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const user = getUser();
  const [course, setCourse] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const res = await api.get(`/courses/${id}`);
        setCourse(res.data);
      } catch (requestError) {
        setError(requestError?.response?.data?.detail || "Failed to load course");
      }
    };

    fetchCourse();
  }, [id]);

  const handleEnroll = async () => {
    if (!course?.is_free) {
      const message = "This is not free course. Please complete payment to access it.";
      setError(message);
      showToast(message, "error");
      return;
    }

    if (!isLoggedIn()) {
      showToast("Please login to unlock this free course.", "info");
      navigate("/login");
      return;
    }

    setBusy(true);
    setError("");

    try {
      await api.post(`/enrollments/${id}`);
      showToast("Free course unlocked successfully.", "success");
      navigate("/my-courses");
    } catch (requestError) {
      const message = requestError?.response?.data?.detail || "Enrollment failed";
      setError(message);
      showToast(message, "error");
      setBusy(false);
    }
  };

  if (error && !course) {
    return <section className="page"><div className="notice notice--error">{error}</div></section>;
  }

  if (!course) {
    return <section className="page"><div className="notice">Loading course...</div></section>;
  }

  const canManage = user?.role === "admin" || (user?.role === "teacher" && user?.id === course.teacher_id);
  const canOpenContent = canManage || course.is_free || user?.role === "student";

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">{course.is_published ? "Published Course" : "Draft Course"}</span>
          <h2>{course.title}</h2>
          <p>{course.description || "No description added yet."}</p>
        </div>

        <div className="hero-badge">
          <strong>{course.is_free ? "Free" : `Rs ${course.price}`}</strong>
          <span>By {course.teacher?.name || "Unknown teacher"}</span>
        </div>
      </div>

      {error && <div className="notice notice--error">{error}</div>}

      <article className="panel-card panel-card--narrow">
        <div className="meta-list">
          <div className="meta-row">
            <span>Status</span>
            <strong>{course.is_published ? "Published" : "Draft"}</strong>
          </div>
          <div className="meta-row">
            <span>Teacher</span>
            <strong>{course.teacher?.name}</strong>
          </div>
          <div className="meta-row">
            <span>Email</span>
            <strong>{course.teacher?.email}</strong>
          </div>
        </div>

        <div className="action-row">
          {canManage ? (
            <Link className="button" to={`/teacher/courses/${course.id}`}>Manage Course</Link>
          ) : (
            <button type="button" className="button" onClick={handleEnroll} disabled={busy}>
              {course.is_free ? "Unlock Free Course" : "Paid Course"}
            </button>
          )}

          {canOpenContent && (
            <Link className="button button--ghost" to={`/courses/${course.id}/content`}>
              Open Content
            </Link>
          )}
        </div>
      </article>
    </section>
  );
}

export default CourseDetail;

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

function MyCourses() {
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMyCourses = async () => {
      try {
        const res = await api.get("/enrollments/my");
        setCourses(res.data);
      } catch (requestError) {
        setError(requestError?.response?.data?.detail || "Failed to load enrolled courses");
      }
    };

    fetchMyCourses();
  }, []);

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">My Learning</span>
          <h2>Your enrolled courses</h2>
          <p>Open course content directly and continue from the latest section whenever you want.</p>
        </div>
        <div className="hero-badge">
          <strong>{courses.length}</strong>
          <span>courses enrolled</span>
        </div>
      </div>

      {error && <div className="notice notice--error">{error}</div>}

      <div className="course-grid">
        {courses.map((item) => (
          <article key={item.id} className="course-card">
            <span className="pill">Enrolled</span>
            <h3>{item.course.title}</h3>
            <p>{item.course.description || "No description added yet."}</p>
            <div className="action-row">
              <Link className="button button--small" to={`/courses/${item.course.id}/content`}>
                Open Content
              </Link>
              <Link className="button button--ghost button--small" to={`/courses/${item.course.id}`}>
                Course Page
              </Link>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default MyCourses;

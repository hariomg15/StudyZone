import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

function Courses() {
  const [courses, setCourses] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCourses = async () => {
      setLoading(true);
      setError("");

      try {
        const endpoint = query.trim() ? `/courses/search?q=${encodeURIComponent(query.trim())}` : "/courses";
        const res = await api.get(endpoint);
        setCourses(res.data);
      } catch (requestError) {
        setError(requestError?.response?.data?.detail || "Failed to load courses");
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, [query]);

  return (
    <section className="page page--courses">
      <div className="page-hero">
        <div>
          <span className="eyebrow">Course Library</span>
          <h2>Learn in a cleaner, calmer workspace</h2>
          <p>
            Browse published courses, check pricing, and jump into detailed course pages.
          </p>
        </div>
        <div className="hero-badge">
          <strong>{courses.length}</strong>
          <span>Courses available</span>
        </div>
      </div>

      <article className="panel-card">
        <div className="panel-card__header">
          <div>
            <span className="eyebrow">Search Courses</span>
            <h3>Find by title</h3>
          </div>
          {loading && <span className="pill">Searching...</span>}
        </div>
        <form className="auth-form" onSubmit={(event) => event.preventDefault()}>
          <input
            type="text"
            placeholder="Search published courses by title"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </form>
        {error && <div className="notice notice--error">{error}</div>}
      </article>

      <div className="course-grid">
        {courses.map((course) => (
          <article key={course.id} className="course-card">
            <div className="course-card__top">
              <span className="pill">{course.is_free ? "Free" : "Premium"}</span>
              <span className="course-card__price">
                {course.is_free ? "Free" : `Rs ${course.price}`}
              </span>
            </div>
            <h3>{course.title}</h3>
            <p>{course.description || "No description added yet."}</p>
            <Link className="button button--small" to={`/courses/${course.id}`}>View Details</Link>
          </article>
        ))}
      </div>

      {!loading && !courses.length && (
        <div className="notice">
          {query.trim() ? "No courses matched your search." : "No courses available yet."}
        </div>
      )}
    </section>
  );
}

export default Courses;

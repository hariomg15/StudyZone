import { useEffect, useState } from "react";
import api from "../api/axios";

const statItems = [
  { key: "total_users", label: "Users" },
  { key: "total_students", label: "Students" },
  { key: "total_teachers", label: "Teachers" },
  { key: "total_admins", label: "Admins" },
  { key: "total_courses", label: "Courses" },
  { key: "total_published_courses", label: "Published" },
  { key: "total_enrollments", label: "Enrollments" },
];

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");
  const [accessCode, setAccessCode] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchStats = async (event) => {
    event?.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await api.get("/users/admin/stats", {
        headers: {
          "X-Admin-Access-Code": accessCode,
        },
      });
      setStats(res.data);
    } catch (requestError) {
      setStats(null);
      setError(requestError?.response?.data?.detail || "Failed to load admin stats");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">Admin Console</span>
          <h2>Platform health in one glance</h2>
          <p>
            This dashboard opens only after logging in with a user whose role is `admin`. Stats are
            shown only after entering the admin access code.
          </p>
        </div>
        <div className="hero-badge">
          <strong>{stats ? stats.total_users : "Admin"}</strong>
          <span>{stats ? "accounts on platform" : "secure access only"}</span>
        </div>
      </div>

      <article className="panel-card panel-card--narrow">
        <div className="panel-card__header">
          <div>
            <span className="eyebrow">Admin Access</span>
            <h3>Enter dashboard passcode</h3>
          </div>
          {loading && <span className="pill">Checking...</span>}
        </div>

        <form className="auth-form" onSubmit={fetchStats}>
          <input
            type="password"
            placeholder="Enter admin access code"
            value={accessCode}
            onChange={(event) => setAccessCode(event.target.value)}
          />
          <button type="submit" className="button">Open Dashboard</button>
        </form>

        {error && <div className="notice notice--error">{error}</div>}
      </article>

      {stats && (
        <div className="stats-grid">
          {statItems.map((item) => (
            <article key={item.key} className="panel-card stat-card">
              <span className="eyebrow">{item.label}</span>
              <h3>{stats[item.key]}</h3>
            </article>
          ))}
        </div>
      )}

      <article className="panel-card panel-card--narrow">
        <div className="panel-card__header">
          <div>
            <span className="eyebrow">Admin Login</span>
            <h3>How to access this page</h3>
          </div>
        </div>
        <div className="stack-list">
          <p>Use the regular login page at `/login`.</p>
          <p>Your user record must have role set to `admin` in the backend database.</p>
          <p>After login, enter the admin access code `StudyZone1825` to view stats.</p>
        </div>
      </article>
    </section>
  );
}

export default AdminDashboard;

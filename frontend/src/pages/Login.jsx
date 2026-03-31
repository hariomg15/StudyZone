import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { saveToken, saveUser } from "../utils/auth";
import { showToast } from "../utils/toast";

function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/auth/login", form);
      saveToken(res.data.access_token);
      const meRes = await api.get("/auth/me");
      saveUser(meRes.data);
      showToast("Login successful. Welcome back to StudyZone.", "success");
      navigate(
        meRes.data.role === "teacher"
          ? "/teacher"
          : meRes.data.role === "admin"
            ? "/admin"
            : "/"
      );
    } catch (error) {
      showToast(error?.response?.data?.detail || "Login failed", "error");
    }
  };

  return (
    <section className="auth-layout">
      <div className="auth-panel auth-panel--intro">
        <span className="eyebrow">StudyZone Access</span>
        <h2>Welcome back to your learning space</h2>
        <p>
          Continue your courses, track progress, and manage your dashboard from one clean place.
        </p>
        <div className="feature-strip">
          <div>
            <strong>Smart</strong>
            <span>Role based flows</span>
          </div>
          <div>
            <strong>Fast</strong>
            <span>Simple JWT login</span>
          </div>
          <div>
            <strong>Clear</strong>
            <span>Student, teacher, and admin views</span>
          </div>
        </div>
      </div>

      <div className="auth-panel auth-panel--form">
        <span className="eyebrow">Login</span>
        <h2>Sign in</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            placeholder="Enter email"
            value={form.email}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Enter password"
            value={form.password}
            onChange={handleChange}
          />
          <button type="submit" className="button">Login</button>
        </form>
      </div>
    </section>
  );
}

export default Login;

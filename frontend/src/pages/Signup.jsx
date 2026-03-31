import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { showToast } from "../utils/toast";

function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "student",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await api.post("/auth/register", form);
      showToast("Signup successful. You can log in now.", "success");
      navigate("/login");
    } catch (error) {
      showToast(error?.response?.data?.detail || "Signup failed", "error");
    }
  };

  return (
    <section className="auth-layout">
      <div className="auth-panel auth-panel--intro auth-panel--warm">
        <span className="eyebrow">Join StudyZone</span>
        <h2>Build your learning profile in minutes</h2>
        <p>
          Student signup is open here. Teacher and admin access are managed privately by Prince
          Jaiswal through database-created accounts.
        </p>
        <div className="founder-card">
          <img src="/brand/prince.jpg" alt="Prince Jaiswal" className="founder-card__image" />
          <div>
            <strong>StudyZone by Prince Jaiswal</strong>
            <span>Founder access manages the admin dashboard and platform controls.</span>
          </div>
        </div>
        <div className="role-cards">
          <div className="role-card">
            <strong>Student</strong>
            <span>Explore courses and open content after enrollment.</span>
          </div>
          <div className="role-card">
            <strong>Teacher</strong>
            <span>Not public signup. Teacher accounts are created internally and then can log in normally.</span>
          </div>
          <div className="role-card">
            <strong>Admin</strong>
            <span>Not public signup. Admin role is created internally and opens the secure dashboard.</span>
          </div>
        </div>
      </div>

      <div className="auth-panel auth-panel--form">
        <span className="eyebrow">Signup</span>
        <h2>Create account</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Enter name"
            value={form.name}
            onChange={handleChange}
          />
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
          <input type="text" value="Student" disabled />
          <button type="submit" className="button">Signup</button>
        </form>
      </div>
    </section>
  );
}

export default Signup;

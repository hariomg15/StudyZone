import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function CreateCourse() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    title: "",
    description: "",
    price: 0,
    is_free: false,
    thumbnail: "",
    is_published: false,
  });

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : type === "number" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const res = await api.post("/courses", {
        ...form,
        price: form.is_free ? 0 : Number(form.price),
      });
      navigate(`/teacher/courses/${res.data.id}`);
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Course creation failed");
    }
  };

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">New Course</span>
          <h2>Create a course shell and start building lessons</h2>
          <p>
            Add the basic metadata first. After saving, you will land in the course workspace to
            create sections, lectures, and notes.
          </p>
        </div>
      </div>

      <article className="panel-card panel-card--narrow">
        <div className="panel-card__header">
          <div>
            <span className="eyebrow">Course Setup</span>
            <h3>Basic details</h3>
          </div>
        </div>

        {error && <div className="notice notice--error">{error}</div>}

        <form className="auth-form" onSubmit={handleSubmit}>
          <input name="title" placeholder="Course title" value={form.title} onChange={handleChange} />
          <textarea
            name="description"
            placeholder="Course description"
            value={form.description}
            onChange={handleChange}
          />
          <div className="form-split">
            <input
              name="price"
              type="number"
              min="0"
              value={form.price}
              onChange={handleChange}
              disabled={form.is_free}
            />
            <input
              name="thumbnail"
              placeholder="Thumbnail URL"
              value={form.thumbnail}
              onChange={handleChange}
            />
          </div>
          <label className="checkbox-row">
            <input type="checkbox" name="is_free" checked={form.is_free} onChange={handleChange} />
            Free course
          </label>
          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_published"
              checked={form.is_published}
              onChange={handleChange}
            />
            Publish immediately
          </label>
          <button type="submit" className="button">Create Course</button>
        </form>
      </article>
    </section>
  );
}

export default CreateCourse;

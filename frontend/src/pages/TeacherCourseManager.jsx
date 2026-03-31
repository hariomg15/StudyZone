import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import { getUser } from "../utils/auth";

const defaultCourseForm = {
  title: "",
  description: "",
  price: 0,
  is_free: false,
  thumbnail: "",
  is_published: false,
};

const defaultSectionForm = {
  title: "",
  order_num: 1,
};

const defaultLectureForm = {
  title: "",
  video_url: "",
  duration: "",
  is_preview: false,
  order_num: 1,
};

const defaultNoteForm = {
  title: "",
  pdf_url: "",
};

function formatDuration(seconds) {
  if (!seconds && seconds !== 0) {
    return "No duration";
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
}

function TeacherCourseManager() {
  const { id } = useParams();
  const navigate = useNavigate();
  const user = getUser();

  const [course, setCourse] = useState(null);
  const [content, setContent] = useState(null);
  const [enrollments, setEnrollments] = useState([]);
  const [courseForm, setCourseForm] = useState(defaultCourseForm);
  const [sectionForm, setSectionForm] = useState(defaultSectionForm);
  const [lectureForms, setLectureForms] = useState({});
  const [noteForms, setNoteForms] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadCourseWorkspace = async () => {
    setLoading(true);
    setError("");

    try {
      const requests = [api.get(`/courses/${id}`), api.get(`/courses/${id}/content`)];

      if (user?.role === "teacher" || user?.role === "admin") {
        requests.push(api.get(`/enrollments/course/${id}`));
      }

      const [courseRes, contentRes, enrollmentRes] = await Promise.all(requests);
      setCourse(courseRes.data);
      setContent(contentRes.data);
      setEnrollments(enrollmentRes?.data || []);
      setCourseForm({
        title: courseRes.data.title || "",
        description: courseRes.data.description || "",
        price: courseRes.data.price || 0,
        is_free: courseRes.data.is_free || false,
        thumbnail: courseRes.data.thumbnail || "",
        is_published: courseRes.data.is_published || false,
      });
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to load course workspace");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCourseWorkspace();
  }, [id]);

  const handleCourseChange = (event) => {
    const { name, value, type, checked } = event.target;
    setCourseForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : type === "number" ? Number(value) : value,
    }));
  };

  const handleSectionChange = (event) => {
    const { name, value, type } = event.target;
    setSectionForm((prev) => ({
      ...prev,
      [name]: type === "number" ? Number(value) : value,
    }));
  };

  const handleLectureChange = (sectionId, event) => {
    const { name, value, type, checked } = event.target;
    setLectureForms((prev) => ({
      ...prev,
      [sectionId]: {
        ...(prev[sectionId] || defaultLectureForm),
        [name]: type === "checkbox" ? checked : type === "number" ? Number(value) : value,
      },
    }));
  };

  const handleNoteChange = (sectionId, event) => {
    const { name, value } = event.target;
    setNoteForms((prev) => ({
      ...prev,
      [sectionId]: {
        ...(prev[sectionId] || defaultNoteForm),
        [name]: value,
      },
    }));
  };

  const saveCourse = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.put(`/courses/${id}`, {
        ...courseForm,
        price: courseForm.is_free ? 0 : Number(courseForm.price),
      });
      setMessage("Course updated successfully.");
      await loadCourseWorkspace();
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to update course");
    } finally {
      setSaving(false);
    }
  };

  const togglePublish = async () => {
    setSaving(true);
    setError("");
    setMessage("");

    try {
      if (course?.is_published) {
        await api.patch(`/courses/${id}/unpublish`);
        setMessage("Course moved back to draft.");
      } else {
        await api.patch(`/courses/${id}/publish`);
        setMessage("Course published successfully.");
      }
      await loadCourseWorkspace();
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to update publish status");
    } finally {
      setSaving(false);
    }
  };

  const deleteCourse = async () => {
    const confirmed = window.confirm("Delete this course permanently?");
    if (!confirmed) {
      return;
    }

    setSaving(true);
    setError("");

    try {
      await api.delete(`/courses/${id}`);
      navigate("/teacher");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to delete course");
      setSaving(false);
    }
  };

  const addSection = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.post(`/courses/${id}/sections`, sectionForm);
      setSectionForm(defaultSectionForm);
      setMessage("Section added successfully.");
      await loadCourseWorkspace();
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to add section");
    } finally {
      setSaving(false);
    }
  };

  const addLecture = async (sectionId, event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      const payload = lectureForms[sectionId] || defaultLectureForm;
      await api.post(`/courses/sections/${sectionId}/lectures`, {
        ...payload,
        duration: payload.duration === "" ? null : Number(payload.duration),
      });
      setLectureForms((prev) => ({
        ...prev,
        [sectionId]: defaultLectureForm,
      }));
      setMessage("Lecture added successfully.");
      await loadCourseWorkspace();
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to add lecture");
    } finally {
      setSaving(false);
    }
  };

  const addNote = async (sectionId, event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    setMessage("");

    try {
      await api.post(`/courses/sections/${sectionId}/notes`, noteForms[sectionId] || defaultNoteForm);
      setNoteForms((prev) => ({
        ...prev,
        [sectionId]: defaultNoteForm,
      }));
      setMessage("Note added successfully.");
      await loadCourseWorkspace();
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Failed to add note");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <section className="page"><div className="notice">Loading course workspace...</div></section>;
  }

  if (error && !course) {
    return <section className="page"><div className="notice notice--error">{error}</div></section>;
  }

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">Course Workspace</span>
          <h2>{course?.title}</h2>
          <p>
            Edit the course, control publishing, add sections, and keep lectures and notes ready
            for students.
          </p>
        </div>
        <div className="hero-badge">
          <strong>{content?.sections?.length || 0}</strong>
          <span>sections in this course</span>
        </div>
      </div>

      <div className="action-row">
        <Link to="/teacher" className="button button--ghost">Back to dashboard</Link>
        <Link to={`/courses/${id}`} className="button button--ghost">Public view</Link>
        <button type="button" className="button" onClick={togglePublish} disabled={saving}>
          {course?.is_published ? "Unpublish" : "Publish"}
        </button>
        <button type="button" className="button button--danger" onClick={deleteCourse} disabled={saving}>
          Delete
        </button>
      </div>

      {message && <div className="notice notice--success">{message}</div>}
      {error && <div className="notice notice--error">{error}</div>}

      <div className="panel-grid">
        <article className="panel-card">
          <div className="panel-card__header">
            <div>
              <span className="eyebrow">Course Settings</span>
              <h3>Edit details</h3>
            </div>
            <span className="pill">{course?.is_published ? "Published" : "Draft"}</span>
          </div>

          <form className="auth-form" onSubmit={saveCourse}>
            <input name="title" placeholder="Course title" value={courseForm.title} onChange={handleCourseChange} />
            <textarea
              name="description"
              placeholder="Course description"
              value={courseForm.description}
              onChange={handleCourseChange}
            />
            <div className="form-split">
              <input
                name="price"
                type="number"
                min="0"
                placeholder="Price"
                value={courseForm.price}
                onChange={handleCourseChange}
                disabled={courseForm.is_free}
              />
              <input
                name="thumbnail"
                placeholder="Thumbnail URL"
                value={courseForm.thumbnail}
                onChange={handleCourseChange}
              />
            </div>
            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_free"
                checked={courseForm.is_free}
                onChange={handleCourseChange}
              />
              Mark as free course
            </label>
            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_published"
                checked={courseForm.is_published}
                onChange={handleCourseChange}
              />
              Keep publish flag in course data
            </label>
            <button type="submit" className="button" disabled={saving}>Save Changes</button>
          </form>
        </article>

        <article className="panel-card">
          <div className="panel-card__header">
            <div>
              <span className="eyebrow">Add Section</span>
              <h3>Build course structure</h3>
            </div>
          </div>

          <form className="auth-form" onSubmit={addSection}>
            <input
              name="title"
              placeholder="Section title"
              value={sectionForm.title}
              onChange={handleSectionChange}
            />
            <input
              name="order_num"
              type="number"
              min="1"
              value={sectionForm.order_num}
              onChange={handleSectionChange}
            />
            <button type="submit" className="button" disabled={saving}>Add Section</button>
          </form>
        </article>
      </div>

      <article className="panel-card">
        <div className="panel-card__header">
          <div>
            <span className="eyebrow">Content Builder</span>
            <h3>Sections, lectures, and notes</h3>
          </div>
        </div>

        <div className="stack-list">
          {content?.sections?.length ? (
            content.sections
              .slice()
              .sort((first, second) => first.order_num - second.order_num)
              .map((section) => (
                <div key={section.id} className="section-card">
                  <div className="section-card__header">
                    <div>
                      <h3>{section.title}</h3>
                      <p>Order #{section.order_num}</p>
                    </div>
                    <span className="pill">{section.lectures.length} lectures</span>
                  </div>

                  <div className="content-columns">
                    <div className="content-block">
                      <h4>Lectures</h4>
                      <div className="mini-list">
                        {section.lectures.map((lecture) => (
                          <div key={lecture.id} className="mini-card">
                            <strong>{lecture.title}</strong>
                            <span>{formatDuration(lecture.duration)}</span>
                            <span>{lecture.is_preview ? "Preview enabled" : "Students only"}</span>
                          </div>
                        ))}
                        {!section.lectures.length && <p>No lectures yet.</p>}
                      </div>

                      <form className="auth-form compact-form" onSubmit={(event) => addLecture(section.id, event)}>
                        <input
                          name="title"
                          placeholder="Lecture title"
                          value={lectureForms[section.id]?.title || ""}
                          onChange={(event) => handleLectureChange(section.id, event)}
                        />
                        <input
                          name="video_url"
                          placeholder="Video URL"
                          value={lectureForms[section.id]?.video_url || ""}
                          onChange={(event) => handleLectureChange(section.id, event)}
                        />
                        <div className="form-split">
                          <input
                            name="duration"
                            type="number"
                            min="0"
                            placeholder="Duration in seconds"
                            value={lectureForms[section.id]?.duration ?? ""}
                            onChange={(event) => handleLectureChange(section.id, event)}
                          />
                          <input
                            name="order_num"
                            type="number"
                            min="1"
                            placeholder="Order"
                            value={lectureForms[section.id]?.order_num ?? 1}
                            onChange={(event) => handleLectureChange(section.id, event)}
                          />
                        </div>
                        <label className="checkbox-row">
                          <input
                            type="checkbox"
                            name="is_preview"
                            checked={lectureForms[section.id]?.is_preview || false}
                            onChange={(event) => handleLectureChange(section.id, event)}
                          />
                          Allow preview
                        </label>
                        <button type="submit" className="button button--small" disabled={saving}>Add Lecture</button>
                      </form>
                    </div>

                    <div className="content-block">
                      <h4>Notes</h4>
                      <div className="mini-list">
                        {section.notes.map((note) => (
                          <a key={note.id} className="mini-card mini-card--link" href={note.pdf_url} target="_blank" rel="noreferrer">
                            <strong>{note.title}</strong>
                            <span>Open PDF</span>
                          </a>
                        ))}
                        {!section.notes.length && <p>No notes yet.</p>}
                      </div>

                      <form className="auth-form compact-form" onSubmit={(event) => addNote(section.id, event)}>
                        <input
                          name="title"
                          placeholder="Note title"
                          value={noteForms[section.id]?.title || ""}
                          onChange={(event) => handleNoteChange(section.id, event)}
                        />
                        <input
                          name="pdf_url"
                          placeholder="PDF URL"
                          value={noteForms[section.id]?.pdf_url || ""}
                          onChange={(event) => handleNoteChange(section.id, event)}
                        />
                        <button type="submit" className="button button--small" disabled={saving}>Add Note</button>
                      </form>
                    </div>
                  </div>
                </div>
              ))
          ) : (
            <div className="notice">No sections yet. Add the first section to start building content.</div>
          )}
        </div>
      </article>

      <article className="panel-card">
        <div className="panel-card__header">
          <div>
            <span className="eyebrow">Enrollments</span>
            <h3>Students in this course</h3>
          </div>
          <span className="pill">{enrollments.length} enrolled</span>
        </div>

        <div className="mini-list">
          {enrollments.length ? (
            enrollments.map((item) => (
              <div key={item.id} className="mini-card">
                <strong>{item.student?.name || "Student"}</strong>
                <span>{item.student?.email}</span>
              </div>
            ))
          ) : (
            <p>No students enrolled yet.</p>
          )}
        </div>
      </article>
    </section>
  );
}

export default TeacherCourseManager;

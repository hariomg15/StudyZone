import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";

function formatDuration(seconds) {
  if (!seconds && seconds !== 0) {
    return "No duration";
  }

  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}m ${remainingSeconds}s`;
}

function CourseContent() {
  const { id } = useParams();
  const [content, setContent] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const res = await api.get(`/courses/${id}/content`);
        setContent(res.data);
      } catch (requestError) {
        setError(requestError?.response?.data?.detail || "Failed to load content");
      }
    };

    fetchContent();
  }, [id]);

  if (error && !content) {
    return <section className="page"><div className="notice notice--error">{error}</div></section>;
  }

  if (!content) {
    return <section className="page"><div className="notice">Loading course content...</div></section>;
  }

  return (
    <section className="page">
      <div className="page-hero">
        <div>
          <span className="eyebrow">Course Content</span>
          <h2>{content.title}</h2>
          <p>{content.description || "Structured lessons and notes for this course."}</p>
        </div>
        <div className="hero-badge">
          <strong>{content.sections?.length || 0}</strong>
          <span>sections ready</span>
        </div>
      </div>

      {error && <div className="notice notice--error">{error}</div>}

      <div className="stack-list">
        {content.sections?.length ? (
          content.sections
            .slice()
            .sort((first, second) => first.order_num - second.order_num)
            .map((section) => (
              <article key={section.id} className="section-card">
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
                      {section.lectures.length ? (
                        section.lectures.map((lecture) => (
                          <a
                            key={lecture.id}
                            className="mini-card mini-card--link"
                            href={lecture.video_url}
                            target="_blank"
                            rel="noreferrer"
                          >
                            <strong>{lecture.title}</strong>
                            <span>{formatDuration(lecture.duration)}</span>
                            <span>{lecture.is_preview ? "Preview lecture" : "Course lecture"}</span>
                          </a>
                        ))
                      ) : (
                        <p>No lectures yet.</p>
                      )}
                    </div>
                  </div>

                  <div className="content-block">
                    <h4>Notes</h4>
                    <div className="mini-list">
                      {section.notes.length ? (
                        section.notes.map((note) => (
                          <a key={note.id} className="mini-card mini-card--link" href={note.pdf_url} target="_blank" rel="noreferrer">
                            <strong>{note.title}</strong>
                            <span>Open PDF</span>
                          </a>
                        ))
                      ) : (
                        <p>No notes yet.</p>
                      )}
                    </div>
                  </div>
                </div>
              </article>
            ))
        ) : (
          <div className="notice">No content has been added to this course yet.</div>
        )}
      </div>
    </section>
  );
}

export default CourseContent;

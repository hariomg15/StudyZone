import { Link, useNavigate } from "react-router-dom";
import { getUser, isLoggedIn, logout } from "../utils/auth";

function Navbar() {
  const navigate = useNavigate();
  const user = getUser();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar__brand">
        <img className="navbar__logo-mark" src="/brand/studyzone-logo.jpeg" alt="StudyZone logo" />
        <div className="navbar__brand-copy">
          <Link to="/" className="navbar__logo">StudyZone by Prince Jaiswal</Link>
          <span className="navbar__tag">Learn with structure</span>
        </div>
      </div>

      <div className="navbar__links">
        <Link to="/">Courses</Link>
        {user?.role === "student" && <Link to="/my-courses">My Courses</Link>}
        {(user?.role === "teacher" || user?.role === "admin") && <Link to="/teacher">Teacher Dashboard</Link>}
        {user?.role === "admin" && <Link to="/admin">Admin</Link>}
      </div>

      <div className="navbar__actions">
        {isLoggedIn() ? (
          <>
            <span className="navbar__user">{user?.name || user?.email || "Logged in"}</span>
            <button type="button" className="button button--ghost" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="button button--ghost">Login</Link>
            <Link to="/signup" className="button">Signup</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;

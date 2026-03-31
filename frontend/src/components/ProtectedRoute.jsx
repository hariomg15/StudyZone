import { Navigate } from "react-router-dom";
import { getUser, hasRole, isLoggedIn } from "../utils/auth";

function ProtectedRoute({ children, roles }) {
  if (!isLoggedIn()) {
    return <Navigate to="/login" replace />;
  }

  if (roles?.length && !hasRole(roles)) {
    const user = getUser();
    const fallbackRoute = user?.role === "teacher" ? "/teacher" : user?.role === "admin" ? "/admin" : "/";
    return <Navigate to={fallbackRoute} replace />;
  }

  return children;
}

export default ProtectedRoute;

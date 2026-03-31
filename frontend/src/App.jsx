import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import ToastHost from "./components/ToastHost";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Courses from "./pages/Courses";
import CourseDetail from "./pages/CourseDetail";
import MyCourses from "./pages/MyCourse";
import CourseContent from "./pages/CourseContent";
import TeacherDashboard from "./pages/TeacherDashboard";
import CreateCourse from "./pages/CreateCourse";
import AdminDashboard from "./pages/AdminDashboard";
import TeacherCourseManager from "./pages/TeacherCourseManager";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <ToastHost />
      <Routes>
        <Route path="/" element={<Courses />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/courses/:id" element={<CourseDetail />} />

        <Route
          path="/my-courses"
          element={
            <ProtectedRoute roles={["student"]}>
              <MyCourses />
            </ProtectedRoute>
          }
        />

        <Route
          path="/courses/:id/content"
          element={<CourseContent />}
        />

        <Route
          path="/teacher"
          element={
            <ProtectedRoute roles={["teacher", "admin"]}>
              <TeacherDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/teacher/create-course"
          element={
            <ProtectedRoute roles={["teacher", "admin"]}>
              <CreateCourse />
            </ProtectedRoute>
          }
        />

        <Route
          path="/teacher/courses/:id"
          element={
            <ProtectedRoute roles={["teacher", "admin"]}>
              <TeacherCourseManager />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <ProtectedRoute roles={["admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

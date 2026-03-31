import { useEffect, useState } from "react";

function ToastHost() {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const handleToast = (event) => {
      const toast = event.detail;
      setToasts((current) => [...current, toast]);

      window.setTimeout(() => {
        setToasts((current) => current.filter((item) => item.id !== toast.id));
      }, 3200);
    };

    window.addEventListener("studyzone:toast", handleToast);
    return () => window.removeEventListener("studyzone:toast", handleToast);
  }, []);

  if (!toasts.length) {
    return null;
  }

  return (
    <div className="toast-stack" aria-live="polite" aria-atomic="true">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast--${toast.type}`}>
          <strong>{toast.type === "success" ? "Success" : toast.type === "error" ? "Notice" : "Update"}</strong>
          <span>{toast.message}</span>
        </div>
      ))}
    </div>
  );
}

export default ToastHost;

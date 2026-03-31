export function showToast(message, type = "info") {
  window.dispatchEvent(
    new CustomEvent("studyzone:toast", {
      detail: {
        id: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
        message,
        type,
      },
    }),
  );
}

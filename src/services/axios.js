export default {
  async search(params) {
    const baseURL = import.meta.env.VITE_API_BASE || "http://localhost:8000";
    const response = await fetch(
      `${baseURL}/search/?${new URLSearchParams(params)}`
    );

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || response.statusText);
    }

    return await response.json();
  },
};
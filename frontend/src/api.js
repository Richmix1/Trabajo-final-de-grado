const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const buildAuthHeaders = (token) => {
  if (!token) {
    return {};
  }
  return { Authorization: `Bearer ${token}` };
};

export const apiRequest = async (path, { method = "GET", body, token } = {}) => {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...buildAuthHeaders(token)
    },
    body: body ? JSON.stringify(body) : undefined
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Error en la petición");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
};

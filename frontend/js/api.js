export const API_BASE_URL =
  (import.meta?.env?.VITE_API_BASE_URL) ?? "http://localhost:8000";

export const API_AUTH_URL_BASE = API_BASE_URL + "/auth";
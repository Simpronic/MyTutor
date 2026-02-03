export const API_BASE_URL =
  (import.meta?.env?.VITE_API_BASE_URL) ?? "http://localhost:8000";

export const API_AUTH_URL_BASE = API_BASE_URL + "/auth";
export const API_USER_MANAGEMENT_URL_BASE = API_BASE_URL + "/userManagement";

const SESSION_TOKEN_KEY = "session_token";

export function getSessionToken() {
  return localStorage.getItem(SESSION_TOKEN_KEY);
}

export function setAuthTokens({ sessionToken }) {
  if (sessionToken) {
    localStorage.setItem(SESSION_TOKEN_KEY, sessionToken);
  }
}

export function clearAuthTokens() {
  localStorage.removeItem(SESSION_TOKEN_KEY);
}
export async function logoutSession() {
  const sessionToken = getSessionToken();
    if (!sessionToken) {
      return;
    }
    await fetch(`${API_AUTH_URL_BASE}/logout`, {
    method: "POST",
    headers: { Authorization: `Bearer ${sessionToken}` },
    });
}

export async function authFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  const sessionToken = getSessionToken();
  if (sessionToken) {
    headers.set("Authorization", `Bearer ${sessionToken}`);
  }
  const activeRoleId = localStorage.getItem("active_role_id");
  if (activeRoleId) {
    headers.set("X-Active-Role-Id", activeRoleId);
  }
  const response = await fetch(url, { ...options, headers });
  if (response.status === 401) {
    clearAuthTokens();
  }
  return response;
}
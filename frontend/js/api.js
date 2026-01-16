export const API_BASE_URL =
  (import.meta?.env?.VITE_API_BASE_URL) ?? "http://localhost:8000";

export const API_AUTH_URL_BASE = API_BASE_URL + "/auth";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setAuthTokens({ accessToken, refreshToken }) {
  if (accessToken) {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  }
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
}

export function clearAuthTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

async function refreshAccessToken() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return false;
  }

  const response = await fetch(`${API_AUTH_URL_BASE}/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok) {
    clearAuthTokens();
    return false;
  }

  const data = await response.json();
  setAuthTokens({
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
  });
  return true;
}

export async function authFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  const accessToken = getAccessToken();
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }
  const activeRoleId = localStorage.getItem("active_role_id");
  if (activeRoleId) {
    headers.set("X-Active-Role-Id", activeRoleId);
  }
  const response = await fetch(url, { ...options, headers });
  if (response.status !== 401) {
    return response;
  }

  const refreshed = await refreshAccessToken();
  if (!refreshed) {
    return response;
  }

  const retryHeaders = new Headers(options.headers || {});
  const newAccessToken = getAccessToken();
  if (newAccessToken) {
    retryHeaders.set("Authorization", `Bearer ${newAccessToken}`);
  }

  return fetch(url, { ...options, headers: retryHeaders });
}
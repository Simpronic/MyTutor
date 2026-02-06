// ../js/router.js

import { clearAuthTokens, getSessionToken, logoutSession  } from "./api.js";

const ROUTES = {
  login: "./index.html",
  resetPassword: "./resetPassword.html",
  roleSelect: "./roleSelect.html",
  main: "./MainPage.html",
};

// Guardie centralizzate
function hasToken() {
  return Boolean(getSessionToken());
}

function hasActiveRole() {
  return Boolean(localStorage.getItem("active_role_id"));
}

/**
 * Naviga verso una route logica con eventuali guardie.
 * @param {keyof ROUTES} routeName
 * @param {{ requireAuth?: boolean, requireRole?: boolean, replace?: boolean }} opts
 */
export function navigate(routeName, opts = {}) {
  const { requireAuth = false, requireRole = false, replace = false } = opts;

  if (!ROUTES[routeName]) {
    console.error("Route non definita:", routeName);
    return;
  }

  if (requireAuth && !hasToken()) {
    // Non loggato -> vai al login
    return hardGo(ROUTES.login, replace);
  }

  if (requireRole && !hasActiveRole()) {
    // Loggato ma ruolo non scelto -> vai a roleSelect
    return hardGo(ROUTES.roleSelect, replace);
  }

  return hardGo(ROUTES[routeName], replace);
}

function hardGo(url, replace) {
  if (replace) window.location.replace(url);
  else window.location.href = url;
}

/**
 * Da chiamare su ogni pagina per applicare guardie automaticamente.
 * Esempio: enforceGuards({ requireAuth: true, requireRole: true })
 */
export function enforceGuards({ requireAuth = false, requireRole = false } = {}) {
  if (requireAuth && !hasToken()) {
    hardGo(ROUTES.login, true);
    return;
  }
  if (requireRole && !hasActiveRole()) {
    hardGo(ROUTES.roleSelect, true);
    return;
  }
}

/**
 * Logout “pulito”
 */
export async function logout() {
  await logoutSession();
  clearAuthTokens();
  localStorage.removeItem("active_role_id");
  localStorage.removeItem("active_role_name");
  hardGo(ROUTES.login, true);
}
import { enforceGuards } from "./router.js";

enforceGuards({ requireAuth: true, requireRole: true });


const REQUIRED_USER_PERMISSIONS = [
  "USER_READ",
  "USER_CREATE",
  "USER_UPDATE",
  "USER_DISABLE",
];

function normalizePermissions(raw) {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw.map((perm) => String(perm));

  try {
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return parsed.map((perm) => String(perm));
    }
  } catch (error) {
    // noop: fallback to split
  }

  return String(raw)
    .split(",")
    .map((perm) => perm.trim())
    .filter(Boolean);
}

function getUserPermissions() {
  const storedPermissions =
    localStorage.getItem("permissions") || localStorage.getItem("user_permissions");
  return normalizePermissions(storedPermissions);
}

function hasUserManagementPermissions(permissions) {
  return REQUIRED_USER_PERMISSIONS.every((perm) => permissions.includes(perm));
}

function getActiveRoleName() {
  return (localStorage.getItem("active_role_name") || "").toLowerCase();
}

function isTutorOrStudent(roleName) {
  return roleName === "tutor" || roleName === "studente" || roleName === "student";
}

function setupPermissions() {
  const permissions = getUserPermissions();
  const roleName = getActiveRoleName();
  const canManageUsers = hasUserManagementPermissions(permissions);
  const isLimitedUser = isTutorOrStudent(roleName) && !canManageUsers;

  const usersTab = document.getElementById("users-tab");
  const usersPane = document.getElementById("users");
  const accessMessage = document.getElementById("accessMessage");
  const settingsContent = document.getElementById("settingsContent");

  if (canManageUsers) {
    usersTab.classList.remove("d-none");
    usersPane.classList.remove("d-none");
    accessMessage.classList.add("d-none");
    return;
  }

  usersTab.classList.add("d-none");
  usersPane.classList.add("d-none");

  if (isLimitedUser) {
    accessMessage.textContent =
      "Sei loggato come tutor o studente: puoi aggiornare solo le tue informazioni e la password.";
    accessMessage.classList.remove("d-none");
    return;
  }

  accessMessage.textContent =
    "Non hai i permessi necessari per gestire gli utenti. Verifica i tuoi privilegi.";
  accessMessage.classList.remove("d-none");
  settingsContent.classList.remove("d-none");
}

document.addEventListener("DOMContentLoaded", setupPermissions);
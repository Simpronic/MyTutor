import { API_AUTH_URL_BASE,API_USER_MANAGEMENT_URL_BASE, authFetch } from "./api.js";
import { enforceGuards } from "./router.js";
import { setupCreateUserModal } from "./createUserModal.js";

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

async function fetchAndStorePermissions() {
  try {
    const response = await authFetch(`${API_AUTH_URL_BASE}/permissions_for_role`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    const permissions = Array.isArray(data.permissions)
      ? data.permissions.map((perm) => perm?.codice).filter(Boolean)
      : [];
    localStorage.setItem("user_permissions", JSON.stringify(permissions));
    return permissions;
  } catch (error) {
    console.warn("Errore nel caricamento permessi:", error);
    return getUserPermissions();
  }
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

async function setupPermissions() {
  const permissions = await fetchAndStorePermissions();
  const canManageUsers = hasUserManagementPermissions(permissions);

  const usersTab = document.getElementById("users-tab");
  const usersPane = document.getElementById("users");
  const settingsContent = document.getElementById("settingsContent");

  if (canManageUsers) {
    usersTab.classList.remove("d-none");
    usersPane.classList.remove("d-none");
    return;
  }

  usersTab.classList.add("d-none");
  usersPane.classList.add("d-none");

  settingsContent.classList.remove("d-none");
}

document.addEventListener("DOMContentLoaded", setupPermissions);


const selectors = {
  firstName: "#firstName",
  lastName: "#lastName",
  email: "#email",
  phone: "#phone",
  cf: "#cf",
  birth: "#birth",
  country: "#country",
  city: "#city",
  saveInfo: "#info_change",
  newPassword: "#newPassword",
  oldPassword: "#currentPassword",
  savePassword: "#psw_change",
  iban: "#iban",
  loadUsers: "#load-users",
  usersList: "#users-list",
  selectedUser: "#selected-user",
  createUserModal: "#createUserModal",
  createUserForm: "#create-user-form",
  createUserSubmit: "#submit-create-user",
  createUserRoles: "#create-roles",
  createUsername: "#create-username",
  createEmail: "#create-email",
  createFirstName: "#create-first-name",
  createLastName: "#create-last-name",
  createCf: "#create-cf",
  createPhone: "#create-phone",
  createBirth: "#create-birth",
  createCountry: "#create-country",
  createCity: "#create-city",
  createAddress: "#create-address",
  createCap: "#create-cap",
  generatedPassword: "#generated-password",
  toggleGeneratedPassword: "#toggle-generated-password",
  toggleCopyPassword: "#toggle-copy-password"
};

function formatUserLabel(user) {
  const nome = user?.nome || "";
  const cognome = user?.cognome || "";
  const username = user?.username ? `(@${user.username})` : "";
  const email = user?.email ? `• ${user.email}` : "";
  return `${cognome} ${nome}`.trim() || user?.email || user?.username || "Utente";
}

function renderUsersList(users) {
  const list = document.querySelector(selectors.usersList);
  if (!list) return;
  list.innerHTML = "";

  if (!Array.isArray(users) || users.length === 0) {
    const emptyItem = document.createElement("div");
    emptyItem.className = "list-group-item text-muted";
    emptyItem.textContent = "Nessun utente trovato.";
    list.appendChild(emptyItem);
    return;
  }

  const sortedUsers = [...users].sort((a, b) => {
    const aLabel = `${a?.cognome || ""} ${a?.nome || ""}`.trim().toLowerCase();
    const bLabel = `${b?.cognome || ""} ${b?.nome || ""}`.trim().toLowerCase();
    return aLabel.localeCompare(bLabel);
  });

  sortedUsers.forEach((user) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "list-group-item list-group-item-action";
    button.dataset.userId = user.id;
    button.textContent = `${formatUserLabel(user)} ${user?.email ? `• ${user.email}` : ""}`.trim();
    button.addEventListener("click", () => {
      const active = list.querySelector(".active");
      if (active) active.classList.remove("active");
      button.classList.add("active");
      const selectedUser = document.querySelector(selectors.selectedUser);
      if (selectedUser) {
        selectedUser.textContent = `Selezionato: ${formatUserLabel(user)} ${user?.email ? `(${user.email})` : ""}`.trim();
      }
      list.dataset.selectedUserId = String(user.id);
    });
    list.appendChild(button);
  });
}

async function loadUsers() {
  const list = document.querySelector(selectors.usersList);
  if (!list) return;
  list.innerHTML = `<div class="list-group-item text-muted">Caricamento utenti...</div>`;

  try {
    const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/allUsers`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const users = await response.json();
    renderUsersList(users);
  } catch (error) {
    console.warn("Errore nel caricamento utenti:", error);
    list.innerHTML = `<div class="list-group-item text-danger">Errore nel caricamento utenti.</div>`;
  }
}


function getValue(selector) {
  const element = document.querySelector(selector);
  if (!element) return "";
  return String(element.value || "").trim();
}

function toggleDisabled(selector, shouldDisable) {
  const element = document.querySelector(selector);
  if (element) {
    element.disabled = shouldDisable;
  }
}

function showAlert(message, type = "info") {
  if (type === "error") {
    console.error(message);
  }
  window.alert(message);
}

function updateStoredUser(payload) {
  const storedUser = localStorage.getItem("user");
  if (!storedUser) return;

  let currentUser;
  try {
    currentUser = JSON.parse(storedUser);
  } catch (error) {
    console.warn("Utente in localStorage non valido:", error);
    return;
  }

  if (!currentUser || typeof currentUser !== "object") return;

  const updatedUser = { ...currentUser, ...payload };
  localStorage.setItem("user", JSON.stringify(updatedUser));
}


async function loadCountries(selectElement) {
  if (!selectElement) return;
  try {
    const response = await authFetch(`${API_AUTH_URL_BASE}/countries`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    const options = Array.isArray(data) ? data : [];
    options.forEach((country) => {
      if (!country?.iso2 || !country?.nome) return;
      const option = document.createElement("option");
      option.value = country.iso2;
      option.textContent = country.nome;
      selectElement.appendChild(option);
    });
  } catch (error) {
    console.warn("Errore nel caricamento paesi:", error);
  }
}

async function handleSaveInfo() {
  toggleDisabled(selectors.saveInfo, true);

  const payload = {};
  const nome = getValue(selectors.firstName);
  const cognome = getValue(selectors.lastName);
  const email = getValue(selectors.email);
  const telefono = getValue(selectors.phone);
  const cf = getValue(selectors.cf);
  const data_nascita = getValue(selectors.birth);
  const paese = getValue(selectors.country);
  const citta = getValue(selectors.city);

  if (nome) payload.nome = nome;
  if (cognome) payload.cognome = cognome;
  if (email) payload.email = email;
  if (telefono) payload.telefono = telefono;
  if (cf) payload.cf = cf;
  if (data_nascita) payload.data_nascita = data_nascita;
  if (paese) payload.paese = paese;
  if (citta) payload.citta = citta;

  if (Object.keys(payload).length === 0) {
    showAlert("Compila almeno un campo da aggiornare.");
    toggleDisabled(selectors.saveInfo, false);
    return;
  }

  try {
    const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/me/modify`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const detail = errorBody?.detail ? `: ${errorBody.detail}` : "";
      throw new Error(`Errore aggiornamento${detail}`);
    }
    const data = await response.json().catch(() => ({}));
    const timestamp = data?.update_timestamp
      ? ` (aggiornato: ${data.update_timestamp})`
      : "";
    updateStoredUser(payload);
    showAlert(`Impostazioni aggiornate con successo${timestamp}.`, "success");
  } catch (error) {
    showAlert(error.message || "Errore durante l'aggiornamento.", "error");
  } finally {
    toggleDisabled(selectors.saveInfo, false);
  }
}

async function handlePasswordChange() {
  const payload = {};
  const oldPassword = getValue(selectors.oldPassword);
  const newPassword = getValue(selectors.newPassword);
  if (oldPassword) payload.old_password = oldPassword;
  if (newPassword) payload.new_password = newPassword;

  toggleDisabled(selectors.saveInfo, true);
    if (Object.keys(payload).length === 0) {
    showAlert("Compila almeno un campo da aggiornare.");
    toggleDisabled(selectors.saveInfo, false);
    return;
  }
  if(!confirm("Sei sicuro di voler cambiare password")){
    return;
  }
  try{
    const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/me/pswChange`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const detail = errorBody?.detail ? `: ${errorBody.detail}` : "";
      throw new Error(`Errore aggiornamento${detail}`);
    }
    const data = await response.json().catch(() => ({}));
    const timestamp = data?.update_timestamp
      ? ` (aggiornato: ${data.update_timestamp})`
      : "";
    showAlert(`Password aggiornata con successo${timestamp}.`, "success");
  }catch (error) {
    showAlert(error.message || "Errore durante l'aggiornamento.", "error");
  } finally {
    toggleDisabled(selectors.saveInfo, false);
  }
}

function disableUnsupportedFields() {
  const ibanInput = document.querySelector(selectors.iban);
  if (ibanInput) {
    ibanInput.setAttribute("disabled", "disabled");
    ibanInput.setAttribute("placeholder", "Non disponibile");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const countrySelect = document.querySelector(selectors.country);
  loadCountries(countrySelect);
  disableUnsupportedFields();
  toggleDisabled(selectors.city, true);

  const saveInfoButton = document.querySelector(selectors.saveInfo);
  if (saveInfoButton) {
    saveInfoButton.addEventListener("click", handleSaveInfo);
  }

  const passwordButton = document.querySelector(selectors.savePassword);
  if (passwordButton) {
    passwordButton.addEventListener("click", handlePasswordChange);
  }

  const loadUsersButton = document.querySelector(selectors.loadUsers);
  if (loadUsersButton) {
    loadUsersButton.addEventListener("click", loadUsers);
  }

  const usersTab = document.getElementById("users-tab");
  if (usersTab) {
    let usersLoaded = false;
    usersTab.addEventListener("shown.bs.tab", () => {
      if (!usersLoaded) {
        usersLoaded = true;
        loadUsers();
      }
    });
  }
  
  setupCreateUserModal({
    authFetch,
    userManagementBaseUrl: API_USER_MANAGEMENT_URL_BASE,
    loadCountries,
    loadUsers,
    getValue,
    showAlert,
  });

});

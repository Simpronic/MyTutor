import { API_AUTH_URL_BASE, API_USER_MANAGEMENT_URL_BASE, authFetch } from "./api.js";
import { enforceGuards } from "./router.js";
import { setupCreateUserModal } from "./createUserModal.js";
import { initProfileSettings, loadCountries } from "./profileSettings.js";
import { setupEditUserModal } from "./editUserModal.js";

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

function setupStudentsTab() {
  const studentsTab = document.getElementById("students-tab");
  const roleName = getActiveRoleName();
  const canManageStudents = roleName === "tutor";

  if (canManageStudents) {
    studentsTab.classList.remove("d-none");
    return;
  }

  studentsTab.classList.add("d-none");
}

document.addEventListener("DOMContentLoaded", setupStudentsTab);

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
  loadUser: "#load-user",
  refreshUsers: "#refresh-users",
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
  toggleCopyPassword: "#toggle-copy-password",
  cancelInfo: "#info_cancel",
  editProfile: "#edit-profile",
  profileActions: "#profile-actions",
  userDetailsModal: "#userDetailsModal",
  detailFirstName: "#detail-first-name",
  detailLastName: "#detail-last-name",
  detailUsername: "#detail-username",
  detailEmail: "#detail-email",
  detailPhone: "#detail-phone",
  detailCf: "#detail-cf",
  detailBirth: "#detail-birth",
  detailCountry: "#detail-country",
  detailCity: "#detail-city",
  detailAddress: "#detail-address",
  detailCap: "#detail-cap",
  detailRoles: "#detail-roles",
  detailId: "#detail-id",
  editUser: "#edit-user",
  editUserFooter: "#edit-user-footer",
  deleteUser: "#delete-user",
  activateDeactivate:"#activate-deactivate-user",
  pswResetBtn: '#user-psw-reset'
};

let cachedUsers = [];
let selectedUser = null;
let selectedUserDetails = null;
let lastFocusedElement = null;
let openEditUserModal = null;

function formatUserLabel(user) {
  const nome = user?.nome || "";
  const cognome = user?.cognome || "";
  const username = user?.username ? `(@${user.username})` : "";
  const email = user?.email ? `• ${user.email}` : "";
  return `${cognome} ${nome}`.trim() || user?.email || user?.username || "Utente";
}
function formatUserValue(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }
  return String(value);
}

function formatUserRoles(user) {
  const roles = user?.ruoli;
  if (!Array.isArray(roles) || roles.length === 0) {
    return "-";
  }
  return roles
    .map((role) => role?.nome || role?.descrizione || role)
    .filter(Boolean)
    .join(", ") || "-";
}

function updateUserDetailsModal(user) {
  const mapping = [
    [selectors.detailFirstName, user?.nome],
    [selectors.detailLastName, user?.cognome],
    [selectors.detailUsername, user?.username],
    [selectors.detailEmail, user?.email],
    [selectors.detailPhone, user?.telefono],
    [selectors.detailCf, user?.cf],
    [selectors.detailBirth, user?.data_nascita],
    [selectors.detailCountry, user?.paese],
    [selectors.detailCity, user?.citta],
    [selectors.detailAddress, user?.indirizzo],
    [selectors.detailCap, user?.cap],
    [selectors.detailRoles, formatUserRoles(user)],
    [selectors.detailId, user?.id],
  ];

  mapping.forEach(([selector, value]) => {
    const element = document.querySelector(selector);
    if (element) {
      element.textContent = formatUserValue(value);
    }
  });
}

async function fetchUserDetails(userId) {
  const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/user/userInfos?user_id=${encodeURIComponent(userId)}`, {
    method: "GET",
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function openUserDetailsModal(user) {
  const modalElement = document.querySelector(selectors.userDetailsModal);
  if (!modalElement) {
    showAlert("Modale dettagli utente non disponibile.");
    return;
  }
  updateUserDetailsModal(user);
  lastFocusedElement = document.activeElement instanceof HTMLElement ? document.activeElement : null;

  if (window.bootstrap?.Modal) {
    if (!modalElement.dataset.focusHandlerAttached) {
      modalElement.addEventListener("hide.bs.modal", () => {
        if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
          lastFocusedElement.focus();
        }
      });
      modalElement.dataset.focusHandlerAttached = "true";
    }
    const modalInstance =
      window.bootstrap.Modal.getInstance(modalElement) ||
      new window.bootstrap.Modal(modalElement);
    modalInstance.show();
  } else {
    modalElement.classList.add("show");
    modalElement.style.display = "block";
    modalElement.removeAttribute("aria-hidden");
  }
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
    button.innerHTML  = `${formatUserLabel(user)} ${user?.email ? `• ${user.email}` : ""} • <b>${(user.attivo == 1) ? 'attivo' : 'inattivo'}</b>`.trim();
    button.addEventListener("click", () => {
      const active = list.querySelector(".active");
      if (active) active.classList.remove("active");
      button.classList.add("active");
      const selectedUserLabel = document.querySelector(selectors.selectedUser);
      if (selectedUserLabel) {
        selectedUserLabel.textContent = `Selezionato: ${formatUserLabel(user)} ${user?.email ? `(${user.email})` : ""}`.trim();
      }
      list.dataset.selectedUserId = String(user.id);
      selectedUser = user;
      selectedUserDetails = null;
    });
    if (list.dataset.selectedUserId === String(user.id)) {
      button.classList.add("active");
    }
    list.appendChild(button);
  });
}

async function loadUser() {
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
    cachedUsers = Array.isArray(users) ? users : [];
    renderUsersList(users);
    if (list?.dataset.selectedUserId) {
      selectedUser = cachedUsers.find((user) => String(user.id) === list.dataset.selectedUserId) || null;
    }
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

async function toggleUser(){
  if(!selectedUser){
    alert("Nessun utente selezionato");
    return;
  } 
  if(!confirm(`Sicuro di voler disattivare l'utente ${selectedUser.username} ?`)) return;
  const id = selectedUser.id
  try{
    const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/user/toggleUser?id=${encodeURIComponent(id)}`,{
      method: "PATCH",
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
    showAlert(`Utente aggiornato con successo ${timestamp}.`, "success");
    loadUser()
  }catch(error){
    showAlert(error.message || "Errore durante la disativazione/attivazione utente", "error");
  }
}

async function deleteUser(){
  if(!selectedUser){
    alert("Nessun utente selezionato");
    return;
  } 
  if(!confirm(`Sicuro di voler eliminare l'utente ${selectedUser.username} ?`)) return;
  const id = selectedUser.id
  try{
    const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/user/deleteUser?id=${encodeURIComponent(id)}`,{
      method: "DELETE",
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
    showAlert(`Utente eliminato con successo ${timestamp}.`, "success");
    loadUser()
  }catch(error){
    showAlert(error.message || "Errore durante l'eliminazione dell' utente", "error");
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

async function pswReset(){
  if (!selectedUser) {
        showAlert("Seleziona un utente dall'elenco");
        return;
      }
      if(confirm(`Vuoi resettare la password di ${selectedUser.username}`)){
        try{
          const response = await authFetch(`${API_USER_MANAGEMENT_URL_BASE}/user/pswReset?user_id=${encodeURIComponent(selectedUser.id)}`, {
          method: "PATCH"
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
          showAlert(`Password resettata con successo${timestamp}.`, "success");
        }catch{
          showAlert( "Errore durante il reset.", "error");
        }
      }
} 

document.addEventListener("DOMContentLoaded", async () => {
  
  const editProfileButton = document.querySelector(selectors.editProfile);
  if (editProfileButton) {
    editProfileButton.addEventListener("click", () => {
      if (!profileSnapshot) {
        profileSnapshot = getProfileSnapshot({ countrySelect, citySelect });
      }
      setProfileEditable(true);
    });
  }

  const cancelProfileButton = document.querySelector(selectors.cancelInfo);
  if (cancelProfileButton) {
    cancelProfileButton.addEventListener("click", () => {
      if (profileSnapshot) {
        applyProfileSnapshot(profileSnapshot, { countrySelect, citySelect });
      }
      setProfileEditable(false);
    });
  }
  const passwordButton = document.querySelector(selectors.savePassword);
  if (passwordButton) {
    passwordButton.addEventListener("click", handlePasswordChange);
  }

  const resetPsw = document.querySelector(selectors.pswResetBtn);
  if(resetPsw){
    resetPsw.addEventListener('click',pswReset);
  }
  const loadUserButton = document.querySelector(selectors.loadUser);
  if (loadUserButton) {
      loadUserButton.addEventListener("click", async () => {
      if (!selectedUser) {
        showAlert("Seleziona un utente dall'elenco per visualizzarne i dettagli.");
        return;
      }
      try {
        const userDetails = await fetchUserDetails(selectedUser.id);
        selectedUserDetails = userDetails;
        openUserDetailsModal(userDetails);
      } catch (error) {
        console.warn("Errore nel caricamento dettagli utente:", error);
        showAlert("Errore nel caricamento dei dettagli utente.");
      }
    });
  }

  const refreshUsersButton = document.querySelector(selectors.refreshUsers);
  if (refreshUsersButton) {
    refreshUsersButton.addEventListener("click", loadUser);
  }

  const usersTab = document.getElementById("users-tab");
  if (usersTab) {
    let usersLoaded = false;
    usersTab.addEventListener("shown.bs.tab", () => {
      if (!usersLoaded) {
        usersLoaded = true;
        loadUser();
      }
    });
  }

  const activateDeactivateButton = document.querySelector(selectors.activateDeactivate);
  if(activateDeactivateButton){
    activateDeactivateButton.addEventListener('click',toggleUser)
  }
  
  const deleteButton = document.querySelector(selectors.deleteUser);
  if(deleteButton){
    deleteButton.addEventListener('click',deleteUser)
  }

  setupCreateUserModal({
    authFetch,
    userManagementBaseUrl: API_USER_MANAGEMENT_URL_BASE,
    loadCountries: (selectElement) => loadCountries(selectElement, authFetch, API_AUTH_URL_BASE),
    loadUser,
    getValue,
    showAlert,
  });
  
   openEditUserModal = await setupEditUserModal({
    authFetch,
    userManagementBaseUrl: API_USER_MANAGEMENT_URL_BASE,
    loadCountries: (selectElement) => loadCountries(selectElement, authFetch, API_AUTH_URL_BASE),
    showAlert,
    loadUser,
  });

  const editUserButtons = [
    document.querySelector(selectors.editUser),
    document.querySelector(selectors.editUserFooter),
  ].filter(Boolean);

  const handleEditUserClick = () => {
      if (!selectedUserDetails) {
        showAlert("Nessun utente caricato per la modifica.");
        return;
      }
      if (!openEditUserModal) {
        showAlert("Modale di modifica non disponibile.");
        return;
      }

      const detailsModal = document.querySelector(selectors.userDetailsModal);
      if (detailsModal && window.bootstrap?.Modal) {
        const detailsInstance =
          window.bootstrap.Modal.getInstance(detailsModal) ||
          new window.bootstrap.Modal(detailsModal);
        detailsInstance.hide();
      }

      openEditUserModal(selectedUserDetails);
  };

  editUserButtons.forEach((button) => {
    button.addEventListener("click", handleEditUserClick);
  });

  await initProfileSettings({
    authFetch,
    apiAuthBaseUrl: API_AUTH_URL_BASE,
    apiUserBaseUrl: API_USER_MANAGEMENT_URL_BASE,
    selectors,
    showAlert,
  });
});

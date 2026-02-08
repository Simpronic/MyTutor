const SELECTORS = {
  modalRoot: "#edit-user-modal-root",
  modal: "#editUserModal",
  form: "#edit-user-form",
  submitButton: "#submit-edit-user",
  rolesContainer: "#edit-roles",
  userId: "#edit-user-id",
  username: "#edit-username",
  email: "#edit-email",
  firstName: "#edit-first-name",
  lastName: "#edit-last-name",
  cf: "#edit-cf",
  phone: "#edit-phone",
  birth: "#edit-birth",
  iban: "#edit-iban",
  country: "#edit-country",
  city: "#edit-city",
  address: "#edit-address",
  cap: "#edit-cap",
};

function formatDateForInput(value) {
  if (!value) return "";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return "";
  return parsed.toISOString().split("T")[0];
}

async function insertModalMarkup() {
  const root = document.querySelector(SELECTORS.modalRoot);
  if (!root || root.dataset.modalLoaded === "true") {
    return root;
  }

  const modalUrl = new URL("./partials/edit-user-modal.html", window.location.href);
  const response = await fetch(modalUrl);
  if (!response.ok) {
    throw new Error(`Errore caricamento modale: HTTP ${response.status}`);
  }

  root.innerHTML = await response.text();
  root.dataset.modalLoaded = "true";
  return root;
}

function setInputValue(selector, value) {
  const element = document.querySelector(selector);
  if (element) {
    element.value = value ?? "";
  }
}

function setSelectValue(selector, value) {
  const element = document.querySelector(selector);
  if (element) {
    element.value = value ?? "";
  }
}

function getValue(selector) {
  const element = document.querySelector(selector);
  if (!element) return "";
  return String(element.value || "").trim();
}

function normalizeOptional(value) {
  return value === "" ? null : value;
}

async function loadEditUserRoles({
  authFetch,
  userManagementBaseUrl,
  selectedRoles,
}) {
  const rolesContainer = document.querySelector(SELECTORS.rolesContainer);
  if (!rolesContainer) return;

  rolesContainer.innerHTML = `<div class="text-muted">Caricamento ruoli...</div>`;

  try {
    const response = await authFetch(`${userManagementBaseUrl}/roles`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const roles = await response.json();
    if (!Array.isArray(roles) || roles.length === 0) {
      rolesContainer.innerHTML = `<div class="text-muted">Nessun ruolo disponibile.</div>`;
      return;
    }

    rolesContainer.innerHTML = "";
    roles.forEach((role) => {
      const wrapper = document.createElement("div");
      wrapper.className = "form-check";
      const checkbox = document.createElement("input");
      checkbox.className = "form-check-input";
      checkbox.type = "checkbox";
      checkbox.id = `edit-role-${role.id}`;
      checkbox.value = role.nome;
      checkbox.checked = selectedRoles.includes(role.nome);
      const label = document.createElement("label");
      label.className = "form-check-label";
      label.setAttribute("for", checkbox.id);
      label.textContent = role.descrizione ? `${role.nome} - ${role.descrizione}` : role.nome;
      wrapper.appendChild(checkbox);
      wrapper.appendChild(label);
      rolesContainer.appendChild(wrapper);
    });
  } catch (error) {
    console.warn("Errore nel caricamento ruoli:", error);
    rolesContainer.innerHTML = `<div class="text-danger">Errore nel caricamento ruoli.</div>`;
  }
}

function collectSelectedRoles() {
  const rolesContainer = document.querySelector(SELECTORS.rolesContainer);
  if (!rolesContainer) return [];
  return Array.from(rolesContainer.querySelectorAll("input[type='checkbox']:checked")).map(
    (checkbox) => ({ nome: checkbox.value })
  );
}

async function handleEditUser({
  authFetch,
  userManagementBaseUrl,
  showAlert,
  loadUser,
}) {
  const submitButton = document.querySelector(SELECTORS.submitButton);
  if (submitButton) submitButton.disabled = true;

  const userId = getValue(SELECTORS.userId);
  const username = getValue(SELECTORS.username);
  const email = getValue(SELECTORS.email);
  const nome = getValue(SELECTORS.firstName);
  const cognome = getValue(SELECTORS.lastName);
  const cf = getValue(SELECTORS.cf);
  const telefono = getValue(SELECTORS.phone);
  const data_nascita = getValue(SELECTORS.birth);
  const iban = getValue(SELECTORS.iban);
  const paese = getValue(SELECTORS.country);
  const citta = getValue(SELECTORS.city);
  const indirizzo = getValue(SELECTORS.address);
  const cap = getValue(SELECTORS.cap);
  const ruoli = collectSelectedRoles();

  if (!userId) {
    showAlert("Impossibile aggiornare: ID utente mancante.");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  if (!username || !email || !nome || !cognome) {
    showAlert("Compila tutti i campi obbligatori.");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  if (cf && cf.length !== 16) {
    showAlert("Il codice fiscale deve avere 16 caratteri.");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  const payload = {
    username,
    email,
    nome,
    cognome,
    cf: normalizeOptional(cf),
    telefono: normalizeOptional(telefono),
    data_nascita: normalizeOptional(data_nascita),
    iban: normalizeOptional(iban),
    paese: normalizeOptional(paese),
    citta: normalizeOptional(citta),
    indirizzo: normalizeOptional(indirizzo),
    cap: normalizeOptional(cap),
    ruoli,
  };

  try {
    const response = await authFetch(
      `${userManagementBaseUrl}/user/modify?user_id=${encodeURIComponent(userId)}`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }
    );
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const detail = errorBody?.detail ? `: ${errorBody.detail}` : "";
      throw new Error(`Errore aggiornamento${detail}`);
    }
    const data = await response.json().catch(() => ({}));
    const timestamp = data?.update_timestamp
      ? ` (aggiornato: ${data.update_timestamp})`
      : "";
    showAlert(`Utente aggiornato con successo${timestamp}.`, "success");
    await loadUser();

    const modalElement = document.querySelector(SELECTORS.modal);
    if (modalElement && window.bootstrap?.Modal) {
      const modalInstance =
        window.bootstrap.Modal.getInstance(modalElement) ||
        new window.bootstrap.Modal(modalElement);
      modalInstance.hide();
    }
  } catch (error) {
    showAlert(error.message || "Errore durante l'aggiornamento utente.", "error");
  } finally {
    if (submitButton) submitButton.disabled = false;
  }
}

function populateForm(user) {
  setInputValue(SELECTORS.userId, user?.id ?? "");
  setInputValue(SELECTORS.username, user?.username ?? "");
  setInputValue(SELECTORS.email, user?.email ?? "");
  setInputValue(SELECTORS.firstName, user?.nome ?? "");
  setInputValue(SELECTORS.lastName, user?.cognome ?? "");
  setInputValue(SELECTORS.cf, user?.cf ?? "");
  setInputValue(SELECTORS.phone, user?.telefono ?? "");
  setInputValue(SELECTORS.birth, formatDateForInput(user?.data_nascita));
  setInputValue(SELECTORS.iban, user?.iban ?? "");
  setSelectValue(SELECTORS.country, user?.paese ?? "");
  setInputValue(SELECTORS.city, user?.citta ?? "");
  setInputValue(SELECTORS.address, user?.indirizzo ?? "");
  setInputValue(SELECTORS.cap, user?.cap ?? "");
}

export async function setupEditUserModal({
  authFetch,
  userManagementBaseUrl,
  loadCountries,
  showAlert,
  loadUser,
}) {
  const root = document.querySelector(SELECTORS.modalRoot);
  if (!root) return null;

  try {
    await insertModalMarkup();
  } catch (error) {
    console.warn("Impossibile caricare la modale di modifica utente:", error);
    return null;
  }

  const modal = document.querySelector(SELECTORS.modal);
  if (!modal || modal.dataset.listenersAttached === "true") return null;
  modal.dataset.listenersAttached = "true";

  modal.addEventListener("hidden.bs.modal", () => {
    const form = document.querySelector(SELECTORS.form);
    if (form) {
      form.reset();
    }
  });

  const submitButton = document.querySelector(SELECTORS.submitButton);
  if (submitButton) {
    submitButton.addEventListener("click", () =>
      handleEditUser({
        authFetch,
        userManagementBaseUrl,
        showAlert,
        loadUser,
      })
    );
  }

  const form = document.querySelector(SELECTORS.form);
  if (form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      handleEditUser({
        authFetch,
        userManagementBaseUrl,
        showAlert,
        loadUser,
      });
    });
  }

  return async function openEditUserModal(user) {
    if (!user) {
      showAlert("Seleziona un utente per modificarne i dati.");
      return;
    }

    const selectedRoles = Array.isArray(user?.ruoli)
      ? user.ruoli.map((role) => role?.nome || role?.descrizione || role).filter(Boolean)
      : [];

    const modalCountry = document.querySelector(SELECTORS.country);
    if (modalCountry && modalCountry.options.length <= 1) {
      await loadCountries(modalCountry);
    }

    populateForm(user);
    await loadEditUserRoles({
      authFetch,
      userManagementBaseUrl,
      selectedRoles,
    });

    if (window.bootstrap?.Modal) {
      const modalInstance =
        window.bootstrap.Modal.getInstance(modal) || new window.bootstrap.Modal(modal);
      modalInstance.show();
    } else {
      modal.classList.add("show");
      modal.style.display = "block";
      modal.removeAttribute("aria-hidden");
    }
  };
}
const SELECTORS = {
  modalRoot: "#create-user-modal-root",
  modal: "#createUserModal",
  form: "#create-user-form",
  submitButton: "#submit-create-user",
  rolesContainer: "#create-roles",
  username: "#create-username",
  email: "#create-email",
  firstName: "#create-first-name",
  lastName: "#create-last-name",
  cf: "#create-cf",
  phone: "#create-phone",
  birth: "#create-birth",
  country: "#create-country",
  city: "#create-city",
  address: "#create-address",
  cap: "#create-cap",
  generatedPassword: "#generated-password",
  toggleGeneratedPassword: "#toggle-generated-password",
  toggleCopyPassword: "#toggle-copy-password",
};

async function insertModalMarkup() {
  const root = document.querySelector(SELECTORS.modalRoot);
  if (!root || root.dataset.modalLoaded === "true") {
    return root;
  }

  const modalUrl = new URL("./partials/create-user-modal.html", window.location.href);
  const response = await fetch(modalUrl);
  if (!response.ok) {
    throw new Error(`Errore caricamento modale: HTTP ${response.status}`);
  }

  root.innerHTML = await response.text();
  root.dataset.modalLoaded = "true";
  return root;
}

function setGeneratedPassword(value) {
  const input = document.querySelector(SELECTORS.generatedPassword);
  if (input) {
    input.value = value || "";
  }
}



function resetGeneratedPassword() {
  const input = document.querySelector(SELECTORS.generatedPassword);
  const toggle = document.querySelector(SELECTORS.toggleGeneratedPassword);
  if (input) {
    input.value = "";
  }
  if (toggle) {
    toggle.textContent = "Genera";
  }
}

function generatePassword(length = 12) {
  const charset = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%*";
  const values = new Uint32Array(length);
  if (window.crypto?.getRandomValues) {
    window.crypto.getRandomValues(values);
  } else {
    for (let i = 0; i < values.length; i += 1) {
      values[i] = Math.floor(Math.random() * charset.length);
    }
  }
  return Array.from(values, (value) => charset[value % charset.length]).join("");
}

function handleCopyPassword(){
  const input = document.querySelector(SELECTORS.generatedPassword);
  if (!input) return;
  input.select();
  input.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(input.value);
}

function handleGeneratePassword() {
  const input = document.querySelector(SELECTORS.generatedPassword);
  if (!input) return;
  input.value = generatePassword(14);
}

async function loadCreateUserRoles({ authFetch, userManagementBaseUrl }) {
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
      checkbox.id = `create-role-${role.id}`;
      checkbox.value = role.nome;
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

async function handleCreateUser({
  authFetch,
  userManagementBaseUrl,
  getValue,
  showAlert,
  loadUsers,
}) {
  const submitButton = document.querySelector(SELECTORS.submitButton);
  if (submitButton) submitButton.disabled = true;

  const username = getValue(SELECTORS.username);
  const email = getValue(SELECTORS.email);
  const nome = getValue(SELECTORS.firstName);
  const cognome = getValue(SELECTORS.lastName);
  const cf = getValue(SELECTORS.cf);
  const telefono = getValue(SELECTORS.phone);
  const data_nascita = getValue(SELECTORS.birth);
  const paese = getValue(SELECTORS.country);
  const citta = getValue(SELECTORS.city);
  const indirizzo = getValue(SELECTORS.address);
  const cap = getValue(SELECTORS.cap);
  const generatedPassword = getValue(SELECTORS.generatedPassword);

  if (!username || !email || !nome || !cognome) {
    showAlert("Compila tutti i campi obbligatori.");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  if (!generatedPassword) {
    showAlert("Genera una password prima di creare l'utente.");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  if (cf && cf.length !== 16) {
    showAlert("Il codice fiscale deve avere 16 caratteri.");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  const rolesContainer = document.querySelector(SELECTORS.rolesContainer);
  const selectedRoles = rolesContainer
    ? Array.from(rolesContainer.querySelectorAll("input[type='checkbox']:checked")).map(
        (checkbox) => ({ nome: checkbox.value })
      )
    : [];

  const payload = {
    username,
    email,
    nome,
    cognome,
    ruoli: selectedRoles,
  };

  if (cf) payload.cf = cf;
  if (telefono) payload.telefono = telefono;
  if (data_nascita) payload.data_nascita = data_nascita;
  if (paese) payload.paese = paese;
  if (citta) payload.citta = citta;
  if (indirizzo) payload.indirizzo = indirizzo;
  if (cap) payload.cap = cap;

  try {
    const response = await authFetch(`${userManagementBaseUrl}/addUser`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const detail = errorBody?.detail ? `: ${errorBody.detail}` : "";
      throw new Error(`Errore creazione${detail}`);
    }
    const data = await response.json().catch(() => ({}));
    if (data?.psw) {
      setGeneratedPassword(data.psw);
    }
    showAlert(`Utente creato con successo${data?.user ? `: ${data.user}` : ""}.`, "success");
    await loadUsers();
  } catch (error) {
    showAlert(error.message || "Errore durante la creazione utente.", "error");
  } finally {
    if (submitButton) submitButton.disabled = false;
  }
}

export async function setupCreateUserModal({
  authFetch,
  userManagementBaseUrl,
  loadCountries,
  loadUsers,
  getValue,
  showAlert,
}) {
  const root = document.querySelector(SELECTORS.modalRoot);
  if (!root) return;

  try {
    await insertModalMarkup();
  } catch (error) {
    console.warn("Impossibile caricare la modale di creazione utente:", error);
    return;
  }

  const modal = document.querySelector(SELECTORS.modal);
  if (!modal || modal.dataset.listenersAttached === "true") return;
  modal.dataset.listenersAttached = "true";

  modal.addEventListener("show.bs.modal", () => {
    const modalCountry = document.querySelector(SELECTORS.country);
    if (modalCountry && modalCountry.options.length <= 1) {
      loadCountries(modalCountry);
    }
    loadCreateUserRoles({ authFetch, userManagementBaseUrl });
  });

  modal.addEventListener("hidden.bs.modal", () => {
    const form = document.querySelector(SELECTORS.form);
    if (form) {
      form.reset();
    }
    resetGeneratedPassword();
  });

  const generatePasswordButton = document.querySelector(SELECTORS.toggleGeneratedPassword);
  if (generatePasswordButton) {
    generatePasswordButton.addEventListener("click", handleGeneratePassword);
  }

  const copyPasswordButton = document.querySelector(SELECTORS.toggleCopyPassword);
  if (copyPasswordButton) {
    copyPasswordButton.addEventListener("click",handleCopyPassword);
  }
  const createUserButton = document.querySelector(SELECTORS.submitButton);
  if (createUserButton) {
    createUserButton.addEventListener("click", () =>
      handleCreateUser({
        authFetch,
        userManagementBaseUrl,
        getValue,
        showAlert,
        loadUsers,
      })
    );
  }
}
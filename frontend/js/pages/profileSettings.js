function formatDateForInput(value) {
  if (!value) return "";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return "";
  return parsed.toISOString().split("T")[0];
}

function getValue(selector) {
  const element = document.querySelector(selector);
  if (!element) return "";
  return String(element.value || "").trim();
}

function setInputValue(selector, value) {
  const element = document.querySelector(selector);
  if (!element || value === undefined || value === null || value === "") return;
  element.value = value;
}

function setTextInputValue(selector, value) {
  const element = document.querySelector(selector);
  if (!element || value === undefined || value === null) return;
  element.value = String(value);
}

function setSelectValue(selectElement, value) {
  if (!selectElement) return;
  selectElement.value = value || "";
}

function ensureSelectValue(selectElement, value) {
  if (!selectElement || !value) return;
  const existing = Array.from(selectElement.options).find((option) => option.value === value);
  if (!existing) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    selectElement.appendChild(option);
  }
  selectElement.value = value;
}

function getStoredUser() {
  const storedUser = localStorage.getItem("user");
  if (!storedUser) return null;
  try {
    return JSON.parse(storedUser);
  } catch (error) {
    console.warn("Utente in localStorage non valido:", error);
    return null;
  }
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

function toggleDisabled(selector, shouldDisable) {
  const element = document.querySelector(selector);
  if (element) {
    element.disabled = shouldDisable;
  }
}

function prefillProfileFields(user, { countrySelect, citySelect }, selectors) {
  if (!user) return;
  setInputValue(selectors.firstName, user.nome);
  setInputValue(selectors.lastName, user.cognome);
  setInputValue(selectors.email, user.email);
  setInputValue(selectors.phone, user.telefono);
  setInputValue(selectors.cf, user.cf);
  setInputValue(selectors.birth, formatDateForInput(user.data_nascita));
  setInputValue(selectors.iban, user.iban);
  ensureSelectValue(countrySelect, user.paese);
  ensureSelectValue(citySelect, user.citta);
}

function applyProfileSnapshot(snapshot, { countrySelect, citySelect }, selectors) {
  if (!snapshot) return;
  setTextInputValue(selectors.firstName, snapshot.firstName);
  setTextInputValue(selectors.lastName, snapshot.lastName);
  setTextInputValue(selectors.email, snapshot.email);
  setTextInputValue(selectors.phone, snapshot.phone);
  setTextInputValue(selectors.iban, snapshot.iban);
  setTextInputValue(selectors.cf, snapshot.cf);
  setTextInputValue(selectors.birth, snapshot.birth);
  setSelectValue(countrySelect, snapshot.country);
  setSelectValue(citySelect, snapshot.city);
}

function getProfileSnapshot({ countrySelect, citySelect }, selectors) {
  return {
    firstName: getValue(selectors.firstName),
    lastName: getValue(selectors.lastName),
    email: getValue(selectors.email),
    phone: getValue(selectors.phone),
    iban: getValue(selectors.iban),
    cf: getValue(selectors.cf),
    birth: getValue(selectors.birth),
    country: countrySelect?.value || "",
    city: citySelect?.value || "",
  };
}

function setProfileEditable(editable, selectors) {
  const fields = [
    selectors.firstName,
    selectors.lastName,
    selectors.email,
    selectors.phone,
    selectors.iban,
    selectors.cf,
    selectors.birth,
    selectors.country,
    selectors.city,
  ];
  fields.forEach((selector) => toggleDisabled(selector, !editable));

  const actions = document.querySelector(selectors.profileActions);
  if (actions) {
    actions.classList.toggle("d-none", !editable);
  }
}

export async function loadCountries(selectElement, authFetch, apiAuthBaseUrl) {
  if (!selectElement) return;
  try {
    const response = await authFetch(`${apiAuthBaseUrl}/countries`, {
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

async function fetchUserProfile(authFetch, apiUserBaseUrl) {
  try {
    const response = await authFetch(`${apiUserBaseUrl}/me`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const profile = await response.json();
    if (profile) {
      localStorage.setItem("user", JSON.stringify(profile));
    }
    return profile;
  } catch (error) {
    console.warn("Errore nel caricamento profilo:", error);
    return null;
  }
}

export async function initProfileSettings({
  authFetch,
  apiAuthBaseUrl,
  apiUserBaseUrl,
  selectors,
  showAlert,
}) {
  const countrySelect = document.querySelector(selectors.country);
  const citySelect = document.querySelector(selectors.city);
  const saveButton = document.querySelector(selectors.saveInfo);
  let profileSnapshot = null;
  let isEditing = false;

  setProfileEditable(false, selectors);

  const updateSnapshot = () => {
    profileSnapshot = getProfileSnapshot({ countrySelect, citySelect }, selectors);
  };

  const handleSaveInfo = async () => {
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
    const iban = getValue(selectors.iban);

    if (nome) payload.nome = nome;
    if (cognome) payload.cognome = cognome;
    if (email) payload.email = email;
    if (telefono) payload.telefono = telefono;
    if (cf) payload.cf = cf;
    if (data_nascita) payload.data_nascita = data_nascita;
    if (iban) payload.iban = iban;
    if (paese) payload.paese = paese;
    if (citta) payload.citta = citta;

    if (Object.keys(payload).length === 0) {
      showAlert("Compila almeno un campo da aggiornare.");
      toggleDisabled(selectors.saveInfo, false);
      return;
    }

    try {
      const response = await authFetch(`${apiUserBaseUrl}/me/modify`, {
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
      updateSnapshot();
      isEditing = false;
      setProfileEditable(false, selectors);
    } catch (error) {
      showAlert(error.message || "Errore durante l'aggiornamento.", "error");
    } finally {
      toggleDisabled(selectors.saveInfo, false);
    }
  };

  if (saveButton) {
    saveButton.addEventListener("click", handleSaveInfo);
  }

  const handleEditClick = () => {
    if (!profileSnapshot) {
      updateSnapshot();
    }
    isEditing = true;
    setProfileEditable(true, selectors);
  };

  const handleCancelClick = () => {
    if (profileSnapshot) {
      applyProfileSnapshot(profileSnapshot, { countrySelect, citySelect }, selectors);
    }
    isEditing = false;
    setProfileEditable(false, selectors);
  };

  document.addEventListener("click", (event) => {
    if (event.target.closest(selectors.editProfile)) {
      handleEditClick();
      return;
    }

    if (event.target.closest(selectors.cancelInfo)) {
      handleCancelClick();
    }
  });

  const storedUser = getStoredUser();
  const profile = (await fetchUserProfile(authFetch, apiUserBaseUrl)) || storedUser;

  const loadCountriesPromise = loadCountries(countrySelect, authFetch, apiAuthBaseUrl);
  if (loadCountriesPromise?.then) {
    loadCountriesPromise
      .then(() => {
        prefillProfileFields(profile, { countrySelect, citySelect }, selectors);
        updateSnapshot();
        if (isEditing) {
          setProfileEditable(true, selectors);
        }
      })
      .catch(() => {
        prefillProfileFields(profile, { countrySelect, citySelect }, selectors);
        updateSnapshot();
        if (isEditing) {
          setProfileEditable(true, selectors);
        }
      });
  } else {
    prefillProfileFields(profile, { countrySelect, citySelect }, selectors);
    updateSnapshot();
    if (isEditing) {
      setProfileEditable(true, selectors);
    }
  }

  if (!isEditing) {
    setProfileEditable(false, selectors);
  }
}
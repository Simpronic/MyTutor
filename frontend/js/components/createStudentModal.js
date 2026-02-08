const SELECTORS = {
  modalRoot: "#create-student-modal-root",
  modal: "#createStudentModal",
  form: "#create-student-form",
  submitButton: "#submit-create-student",
  firstName: "#create-student-first-name",
  lastName: "#create-student-last-name",
  email: "#create-student-email",
  phone: "#create-student-phone",
  cf: "#create-student-cf",
  birth: "#create-student-birth",
  country: "#create-student-country",
  city: "#create-student-city",
  address: "#create-student-address",
  cap: "#create-student-cap",
  payerFirstName: "#create-student-payer-first-name",
  payerLastName: "#create-student-payer-last-name",
  payerCf: "#create-student-payer-cf",
  payerEmail: "#create-student-payer-email",
  payerPhone: "#create-student-payer-phone",
  payerCountry: "#create-student-payer-country",
  payerCity: "#create-student-payer-city",
  payerAddress: "#create-student-payer-address",
  payerCap: "#create-student-payer-cap",
  feedback: "#create-student-feedback",
};

async function insertModalMarkup() {
  const root = document.querySelector(SELECTORS.modalRoot);
  if (!root || root.dataset.modalLoaded === "true") {
    return root;
  }

  const modalUrl = new URL("./partials/create-student-modal.html", window.location.href);
  const response = await fetch(modalUrl);
  if (!response.ok) {
    throw new Error(`Errore caricamento modale: HTTP ${response.status}`);
  }

  root.innerHTML = await response.text();
  root.dataset.modalLoaded = "true";
  return root;
}

function setFeedback(message, type = "muted") {
  const feedback = document.querySelector(SELECTORS.feedback);
  if (!feedback) return;
  feedback.textContent = message;
  feedback.className = `small text-${type}`;
}

function getValue(selector) {
  const input = document.querySelector(selector);
  return input ? String(input.value || "").trim() : "";
}

function resetForm() {
  const form = document.querySelector(SELECTORS.form);
  if (form) form.reset();
}

async function handleCreateStudent({ authFetch, studentsBaseUrl }) {
  const submitButton = document.querySelector(SELECTORS.submitButton);
  if (submitButton) submitButton.disabled = true;
  setFeedback("");

  const payload = {
    nome: getValue(SELECTORS.firstName),
    cognome: getValue(SELECTORS.lastName),
    email: getValue(SELECTORS.email) || null,
    telefono: getValue(SELECTORS.phone) || null,
    cf: getValue(SELECTORS.cf) || null,
    data_nascita: getValue(SELECTORS.birth) || null,
    paese: getValue(SELECTORS.country) || null,
    citta: getValue(SELECTORS.city) || null,
    indirizzo: getValue(SELECTORS.address) || null,
    cap: getValue(SELECTORS.cap) || null,
    pagante_nome: getValue(SELECTORS.payerFirstName) || null,
    pagante_cognome: getValue(SELECTORS.payerLastName) || null,
    pagante_cf: getValue(SELECTORS.payerCf) || null,
    pagante_email: getValue(SELECTORS.payerEmail) || null,
    pagante_telefono: getValue(SELECTORS.payerPhone) || null,
    pagante_paese: getValue(SELECTORS.payerCountry) || null,
    pagante_citta: getValue(SELECTORS.payerCity) || null,
    pagante_indirizzo: getValue(SELECTORS.payerAddress) || null,
    pagante_cap: getValue(SELECTORS.payerCap) || null,
  };

  if (!payload.nome || !payload.cognome) {
    setFeedback("Nome e cognome sono obbligatori.", "danger");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  try {
    const response = await authFetch(`${studentsBaseUrl}/createStudent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData?.detail || `Errore HTTP ${response.status}`);
    }

    resetForm();
    setFeedback("Studente aggiunto con successo.", "success");
  } catch (error) {
    setFeedback(error?.message || "Errore durante il salvataggio.", "danger");
  } finally {
    if (submitButton) submitButton.disabled = false;
  }
}

export async function setupCreateStudentModal({ authFetch, studentsBaseUrl }) {
  await insertModalMarkup();
  const form = document.querySelector(SELECTORS.form);
  if (!form) return null;
  if (!form.dataset.listenerAttached) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      handleCreateStudent({ authFetch, studentsBaseUrl });
    });
    form.dataset.listenerAttached = "true";
  }

  const modalElement = document.querySelector(SELECTORS.modal);
  if (!modalElement) return null;
  return () => {
    if (window.bootstrap?.Modal) {
      const instance =
        window.bootstrap.Modal.getInstance(modalElement) || new window.bootstrap.Modal(modalElement);
      instance.show();
    } else {
      modalElement.classList.add("show");
      modalElement.style.display = "block";
      modalElement.removeAttribute("aria-hidden");
    }
  };
}
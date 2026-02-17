const SELECTORS = {
  modalRoot: "#create-lesson-modal-root",
  modal: "#createLessonModal",
  form: "#create-lesson-form",
  submitButton: "#submit-create-lesson",
  student: "#create-lesson-student",
  subject: "#create-lesson-subject",
  startAt: "#create-lesson-start",
  endAt: "#create-lesson-end",
  location: "#create-lesson-location",
  status: "#create-lesson-status",
  note: "#create-lesson-note",
  feedback: "#create-lesson-feedback",
};

async function insertModalMarkup() {
  const root = document.querySelector(SELECTORS.modalRoot);
  if (!root || root.dataset.modalLoaded === "true") {
    return root;
  }

  const modalUrl = new URL("./partials/create-lesson-modal.html", window.location.href);
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

async function loadStudents({ authFetch, studentsBaseUrl }) {
  const studentSelect = document.querySelector(SELECTORS.student);
  if (!studentSelect) return;

  studentSelect.innerHTML = '<option value="" selected disabled>Seleziona uno studente</option>';
  try {
    const response = await authFetch(`${studentsBaseUrl}/getStudents`);
    if (!response.ok) {
      throw new Error(`Errore HTTP ${response.status}`);
    }

    const students = await response.json();
    students
      .filter((student) => student?.attivo)
      .forEach((student) => {
        const option = document.createElement("option");
        option.value = String(student.id);
        option.textContent = `${student.nome} ${student.cognome}`;
        studentSelect.appendChild(option);
      });

    if (studentSelect.options.length <= 1) {
      setFeedback("Nessuno studente attivo disponibile.", "warning");
    }
  } catch (error) {
    setFeedback(`Impossibile caricare gli studenti: ${error?.message || "errore sconosciuto"}`, "danger");
  }
}



async function loadSubjects({ authFetch, lessonsBaseUrl }) {
  const subjectSelect = document.querySelector(SELECTORS.subject);
  if (!subjectSelect) return;

  subjectSelect.innerHTML = '<option value="" selected disabled>Seleziona una materia</option>';

  try {
    const response = await authFetch(`${lessonsBaseUrl}/allMaterie`);
    if (!response.ok) {
      throw new Error(`Errore HTTP ${response.status}`);
    }

    const subjects = await response.json();
    subjects.forEach((subject) => {
      const option = document.createElement("option");
      option.value = String(subject.code || "").trim();
      option.textContent = String(subject.label || subject.code || "").trim();
      if (option.value) {
        subjectSelect.appendChild(option);
      }
    });

    if (subjectSelect.options.length <= 1) {
      setFeedback("Nessuna materia disponibile.", "warning");
    }
  } catch (error) {
    setFeedback(`Impossibile caricare le materie: ${error?.message || "errore sconosciuto"}`, "danger");
  }
}

async function handleCreateLesson({ authFetch, lessonsBaseUrl }) {
  const submitButton = document.querySelector(SELECTORS.submitButton);
  if (submitButton) submitButton.disabled = true;
  setFeedback("");

  const payload = {
    student_id: Number(getValue(SELECTORS.student)),
    materia_code: getValue(SELECTORS.subject),
    start_at: getValue(SELECTORS.startAt),
    end_at: getValue(SELECTORS.endAt),
    note: getValue(SELECTORS.note) || null,
    luogo: getValue(SELECTORS.location),
    status: getValue(SELECTORS.status),
  };

  if (!payload.student_id || !payload.materia_code || !payload.start_at || !payload.end_at) {
    setFeedback("Compila tutti i campi obbligatori.", "danger");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  if (payload.start_at >= payload.end_at) {
    setFeedback("La data di fine deve essere successiva alla data di inizio.", "danger");
    if (submitButton) submitButton.disabled = false;
    return;
  }

  try {
    const response = await authFetch(`${lessonsBaseUrl}/createLesson`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData?.detail || `Errore HTTP ${response.status}`);
    }

    resetForm();
    setFeedback("Lezione aggiunta con successo.", "success");
  } catch (error) {
    setFeedback(error?.message || "Errore durante il salvataggio.", "danger");
  } finally {
    if (submitButton) submitButton.disabled = false;
  }
}

export async function setupCreateLessonModal({ authFetch, studentsBaseUrl, lessonsBaseUrl }) {
  await insertModalMarkup();

  const form = document.querySelector(SELECTORS.form);
  if (!form) return null;

  if (!form.dataset.listenerAttached) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      handleCreateLesson({ authFetch, lessonsBaseUrl });
    });
    form.dataset.listenerAttached = "true";
  }

  const modalElement = document.querySelector(SELECTORS.modal);
  if (!modalElement) return null;

  return async () => {
    setFeedback("");
    await Promise.all([
      loadStudents({ authFetch, studentsBaseUrl }),
      loadSubjects({ authFetch, lessonsBaseUrl }),
    ]);

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
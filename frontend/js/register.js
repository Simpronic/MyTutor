import { API_BASE_URL, API_AUTH_URL_BASE } from "./api.js";
import { navigate } from "./router.js";

const REGISTER_URL = `${API_BASE_URL}/registration/registerUser`;

const form = document.getElementById("registerForm");
const message = document.getElementById("registerMessage");
const countrySelect = document.getElementById("country");

function setMessage(text, type) {
  message.textContent = text;
  message.classList.remove("d-none", "alert-success", "alert-danger", "alert-warning");
  message.classList.add(`alert-${type}`);
}

function clearMessage() {
  message.textContent = "";
  message.classList.add("d-none");
}

async function loadCountries() {
  try {
    const response = await fetch(`${API_AUTH_URL_BASE}/countries`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    const countries = Array.isArray(data) ? data : [];
    countries.forEach((country) => {
      const option = document.createElement("option");
      option.value = country.iso2;
      option.textContent = country.nome;
      countrySelect.appendChild(option);
    });
  } catch (error) {
    setMessage("Impossibile caricare la lista dei paesi.", "warning");
  }
}

document.addEventListener("DOMContentLoaded", loadCountries);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessage();

  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirmPassword").value.trim();
  const cfValue = document.getElementById("cf").value.trim();

  if ((password.trim()).length <= 8 || (password.trim()).length > 200) {
    setMessage("La password non rientra nella dimensione, deve essere almeno 8 caratteri ma non più di 200 caratteri", "warning");
    return;
  }

  if (password !== confirmPassword) {
    setMessage("Le password non coincidono.", "warning");
    return;
  }

  if (cfValue && cfValue.length !== 16) {
    setMessage("Il codice fiscale deve avere 16 caratteri.", "warning");
    return;
  }

  const payload = {
    username: document.getElementById("username").value.trim(),
    email: document.getElementById("email").value.trim(),
    password,
    nome: document.getElementById("firstName").value.trim(),
    cognome: document.getElementById("lastName").value.trim(),
    cf: cfValue || null,
    telefono: document.getElementById("phone").value.trim() || null,
    data_nascita: document.getElementById("birthDate").value || null,
    paese: document.getElementById("country").value.trim() || null,
    citta: document.getElementById("city").value.trim() || null,
    indirizzo: document.getElementById("address").value.trim() || null,
    cap: document.getElementById("cap").value.trim() || null,
  };

  try {
    const response = await fetch(REGISTER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      const detail = data.detail || "Registrazione fallita. Riprova più tardi.";
      setMessage(detail, "danger");
      return;
    }

    setMessage("Registrazione completata. Puoi accedere con le tue credenziali.", "success");
    form.reset();
    navigate("login", { requireAuth: false });
  } catch (error) {
    setMessage("Errore di rete durante la registrazione.", "danger");
  }
});
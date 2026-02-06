import { API_AUTH_URL_BASE } from "./api.js";

const form = document.getElementById("resetPasswordForm");
const newPasswordInput = document.getElementById("newPassword");
const confirmPasswordInput = document.getElementById("confirmPassword");
const messageElement = document.getElementById("message");

const MIN_PASSWORD_LENGTH = 8;
const MAX_PASSWORD_LENGTH = 200;

function setMessage(message, variant = "danger") {
  messageElement.textContent = message;
  messageElement.classList.remove("d-none", "alert-danger", "alert-success", "alert-warning");
  messageElement.classList.add(`alert-${variant}`);
}

function clearMessage() {
  messageElement.textContent = "";
  messageElement.classList.add("d-none");
}

function getIdentifierFromQuery() {
  const params = new URLSearchParams(window.location.search);
  return params.get("identifier");
}

function validatePassword(password, confirmPassword) {
  if (!password || !confirmPassword) {
    setMessage("Compila tutti i campi della password.");
    return false;
  }
  if (password.length < MIN_PASSWORD_LENGTH || password.length > MAX_PASSWORD_LENGTH) {
    setMessage(
      `La password deve essere tra ${MIN_PASSWORD_LENGTH} e ${MAX_PASSWORD_LENGTH} caratteri.`,
      "warning",
    );
    return false;
  }
  if (password !== confirmPassword) {
    setMessage("Le password non coincidono.", "warning");
    return false;
  }
  return true;
}

async function resetPassword(identifier, newPassword) {
  const response = await fetch(`${API_AUTH_URL_BASE}/pswChange`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: identifier,
      old_password: "",
      new_password: newPassword
    }),
  });
  let result = await response.json();
  if (!response.ok || result.Result == -1) {
    throw new Error(`Reset password fallito`);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const identifierFromQuery = getIdentifierFromQuery();
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage();

    const identifier = identifierFromQuery.trim();
    const newPassword = newPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (!identifier) {
      setMessage("Errore !");
      return;
    }

    if (!validatePassword(newPassword, confirmPassword)) {
      return;
    }

    try {
      await resetPassword(identifier, newPassword);
      setMessage("Password aggiornata con successo. Verrai reindirizzato al login.", "success");
      setTimeout(() => {
        window.location.href = "./index.html";
      }, 1500);
    } catch (error) {
      setMessage(error.message || "Errore durante il reset della password.");
    }
  });
});
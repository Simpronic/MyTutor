import { API_BASE_URL } from "./api.js";

const form = document.getElementById("roleForm");
const roleSelect = document.getElementById("roleSelect");
const accessBtn = document.getElementById("accessBtn");
const errorBox = document.getElementById("errorBox");

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("d-none");
}

function clearError() {
  errorBox.textContent = "";
  errorBox.classList.add("d-none");
}

function getTokenOrRedirect() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    // non sei loggato
    window.location.href = "./index.html"; // o la tua pagina login reale
    return null;
  }
  return token;
}

async function loadRoles() {
  clearError();

  const token = getTokenOrRedirect();
  if (!token) return;

  // UI: reset
  roleSelect.innerHTML = `<option value="" selected disabled>Loading roles...</option>`;
  accessBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/me/roles`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `HTTP ${res.status}`);
    }

    const data = await res.json(); // { roles: [...] }

    if (!data.roles || data.roles.length === 0) {
      roleSelect.innerHTML = `<option value="" selected disabled>No roles available</option>`;
      showError("Nessun ruolo associato a questo utente.");
      return;
    }

    // Popola select
    roleSelect.innerHTML = `<option value="" selected disabled>Select a role...</option>`;
    for (const r of data.roles) {
      const opt = document.createElement("option");
      opt.value = String(r.id);         // oppure r.nome se preferisci
      opt.textContent = r.nome;         // label
      opt.dataset.roleName = r.nome;    // utile
      roleSelect.appendChild(opt);
    }

    accessBtn.disabled = false;

  } catch (err) {
    console.error(err);
    roleSelect.innerHTML = `<option value="" selected disabled>Error loading roles</option>`;
    showError("Errore nel caricamento ruoli. Controlla token o backend.");
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  clearError();

  const roleId = roleSelect.value;
  if (!roleId) {
    showError("Seleziona un ruolo prima di continuare.");
    return;
  }

  // Salvo la scelta (client-side). Puoi anche mandarla al backend se vuoi.
  const selectedOption = roleSelect.selectedOptions[0];
  const roleName = selectedOption?.dataset?.roleName || "";

  localStorage.setItem("active_role_id", roleId);
  localStorage.setItem("active_role_name", roleName);

  // Vai alla tua main page
  window.location.href = "./MainPage.html";
});

// Carica ruoli al load
window.addEventListener("DOMContentLoaded", loadRoles);

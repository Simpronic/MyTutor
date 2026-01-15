import { API_BASE_URL } from "./api.js";
import { navigate, enforceGuards } from "./router.js";

const form = document.getElementById("roleForm");
const roleSelect = document.getElementById("roleSelect");
const accessBtn = document.getElementById("accessBtn");
const errorBox = document.getElementById("errorBox");

enforceGuards({ requireAuth: true }); // ✅ se non loggato -> login

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("d-none");
}

function clearError() {
  errorBox.textContent = "";
  errorBox.classList.add("d-none");
}

async function loadRoles() {
  clearError();

  const token = localStorage.getItem("access_token");
  console.log(token)
  if (!token) return; // già gestito da enforceGuards, qui è solo safety

  roleSelect.innerHTML = `<option value="" selected disabled>Loading roles...</option>`;
  accessBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/me/roles`, {
      method: "GET",
      headers: { "Authorization": `Bearer ${token}` },
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `HTTP ${res.status}`);
    }

    const data = await res.json();

    if (!data.roles || data.roles.length === 0) {
      roleSelect.innerHTML = `<option value="" selected disabled>No roles available</option>`;
      showError("Nessun ruolo associato a questo utente.");
      return;
    }

    roleSelect.innerHTML = `<option value="" selected disabled>Select a role...</option>`;
    for (const r of data.roles) {
      const opt = document.createElement("option");
      opt.value = String(r.id);
      opt.textContent = r.nome;
      opt.dataset.roleName = r.nome;
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

  const selectedOption = roleSelect.selectedOptions[0];
  const roleName = selectedOption?.dataset?.roleName || "";

  localStorage.setItem("active_role_id", roleId);
  localStorage.setItem("active_role_name", roleName);

  navigate("main", { requireAuth: true, requireRole: true });
});

window.addEventListener("DOMContentLoaded", loadRoles);

import { API_AUTH_URL_BASE } from "./api.js";

const form = document.getElementById("loginForm");
const userIdInput = document.getElementById("userId");
const passwordInput = document.getElementById("password");

async function login(identifier, password) {
  const response = await fetch(`${API_AUTH_URL_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier, password }),
  });

  if (!response.ok) throw new Error("Login failed");

  const data = await response.json();
  localStorage.setItem("access_token", data.access_token);
  return data.user;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const identifier = userIdInput.value.trim();
  const password = passwordInput.value;

  if (!identifier || !password) {
    alert("Inserisci ID e password");
    return;
  }

  try {
    const user = await login(identifier, password);
    console.log("Login OK:", user);

    // ✅ vai alla tua pagina reale
    window.location.href = "./MainPage.html";
  } catch (err) {
    console.error(err);
    alert("Credenziali non valide");
  }
});

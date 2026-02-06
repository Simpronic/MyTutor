import { API_AUTH_URL_BASE, setAuthTokens} from "./api.js";
import { navigate } from "./router.js";



const form = document.getElementById("loginForm");
const userIdInput = document.getElementById("userId");
const passwordInput = document.getElementById("password");

async function login(identifier, password) {
  const response = await fetch(`${API_AUTH_URL_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ identifier, password }),
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const detail = errorBody?.detail || "Login failed";
    throw new Error(detail);
  }

  const data = await response.json();
  setAuthTokens({
    sessionToken: data.session_token,
  });
  localStorage.setItem("user", JSON.stringify(data.user));
  return data.user;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const identifier = userIdInput.value.trim();
  const password = passwordInput.value;

  if (!identifier) {
    alert("Inserisci ID");
    return;
  }

  try {
    const user = await login(identifier, password);
    console.log("Login OK:", user);

    navigate("roleSelect", { requireAuth: true });
  } catch (err) {
    if (err?.message === "PASSWORD_RESET_REQUIRED") {
      window.location.href = `./resetPassword.html?identifier=${encodeURIComponent(identifier)}`;
      return;
    }
    console.error(err);
    alert("Credenziali non valide");
  }
});

import { enforceGuards,logout } from "./router.js";

enforceGuards({ requireAuth: true, requireRole: true });

function getCurrentUser() {
  return JSON.parse(localStorage.getItem("user") || "null");
}

function renderWelcome() {
  const currentUser = getCurrentUser();
  const WelSec = document.getElementById("WelSec");
  if (!WelSec || !currentUser) return;
  WelSec.innerHTML = `<h2>Welcome ${currentUser.nome} ${currentUser.cognome}!</h2>`;
}


document.addEventListener("DOMContentLoaded", function () {

  const plusButton = document.getElementById('plusButton');
  const toolbarMenu = document.getElementById('toolbarMenu');
  renderWelcome();
  
  const logoutBtn = document.getElementById("logout");
  if (!logoutBtn) {
    console.error("Bottone logout non trovato (id='logout')");
    return;
  }

  plusButton.addEventListener('click', () => {
    const isVisible = toolbarMenu.style.display === 'flex';
    toolbarMenu.style.display = isVisible ? 'none' : 'flex';
  });

  document.addEventListener('click', (e) => {
    if (!plusButton.contains(e.target) && !toolbarMenu.contains(e.target)) {
      toolbarMenu.style.display = 'none';
    }
  });
  logoutBtn.addEventListener("click", async () => {
    if (confirm("Sei sicuro di voler uscire ? ")) {
      await logout();
    }
  });
});

window.addEventListener("pageshow", renderWelcome);
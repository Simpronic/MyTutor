import { API_STUDENTS_URL_BASE, authFetch } from "./api.js";
import { setupCreateStudentModal } from "./createStudentModal.js";
import { enforceGuards, logout } from "./router.js";

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
  const openCreateStudentButton = document.getElementById("open-create-student");
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

  setupCreateStudentModal({ authFetch, studentsBaseUrl: API_STUDENTS_URL_BASE })
      .then((openModal) => {
        if (!openModal || !openCreateStudentButton) return;
        openCreateStudentButton.addEventListener("click", () => {
          toolbarMenu.style.display = "none";
          openModal();
        });
      })
      .catch((error) => {
        console.warn("Errore nel caricamento modale studente:", error);
      });
});

window.addEventListener("pageshow", renderWelcome);
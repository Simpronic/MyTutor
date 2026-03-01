import { API_LESSONS_URL_BASE, API_STUDENTS_URL_BASE, authFetch } from "../core/api.js";
import { setupCreateStudentModal } from "../components/createStudentModal.js";
import { setupCreateLessonModal } from "../components/createLessonModal.js";
import { enforceGuards, logout } from "../core/router.js";

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
  const openCreateLessonButton = document.getElementById("open-create-lesson");
  const openLessonsPageButton = document.getElementById("open-lessons-page");
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

  if (openLessonsPageButton) {
    openLessonsPageButton.addEventListener("click", () => {
      toolbarMenu.style.display = "none";
      window.location.href = "./lessons.html";
    });
  }

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

  setupCreateLessonModal({
    authFetch,
    studentsBaseUrl: API_STUDENTS_URL_BASE,
    lessonsBaseUrl: API_LESSONS_URL_BASE,
  })
    .then((openModal) => {
      if (!openModal || !openCreateLessonButton) return;
      openCreateLessonButton.addEventListener("click", async () => {
        toolbarMenu.style.display = "none";
        await openModal();
      });
    })
    .catch((error) => {
      console.warn("Errore nel caricamento modale lezione:", error);
    });


});

window.addEventListener("pageshow", renderWelcome);
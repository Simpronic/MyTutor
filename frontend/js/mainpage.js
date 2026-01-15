import { enforceGuards } from "./router.js";

enforceGuards({ requireAuth: true, requireRole: true });

const currentUser = JSON.parse(localStorage.getItem("user") || "null");
const activeRoleId = localStorage.getItem("active_role_id");
const activeRoleName = localStorage.getItem("active_role_name");
document.addEventListener("DOMContentLoaded", function () {
  const plusButton = document.getElementById('plusButton');
  const toolbarMenu = document.getElementById('toolbarMenu');
  const WelSec = document.getElementById('WelSec')
  WelSec.innerHTML = `<h2>Welcome ${currentUser.nome} ${currentUser.cognome}!</h2>`
  

  plusButton.addEventListener('click', () => {
    const isVisible = toolbarMenu.style.display === 'flex';
    toolbarMenu.style.display = isVisible ? 'none' : 'flex';
  });

  document.addEventListener('click', (e) => {
    if (!plusButton.contains(e.target) && !toolbarMenu.contains(e.target)) {
      toolbarMenu.style.display = 'none';
    }
  });
});

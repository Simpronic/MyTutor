import { enforceGuards } from "./router.js";

enforceGuards({ requireAuth: true, requireRole: true });

// ... il resto del tuo codice (plusButton/toolbarMenu) ...
document.addEventListener("DOMContentLoaded", function () {
  const plusButton = document.getElementById('plusButton');
  const toolbarMenu = document.getElementById('toolbarMenu');

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

import { API_LESSONS_URL_BASE, authFetch } from "../core/api.js";
import { enforceGuards } from "../core/router.js";

enforceGuards({ requireAuth: true, requireRole: true });

let lessons = [];
let currentMonthDate = new Date();
let selectedLessonId = null;

const STATUS_BADGE_CLASS = {
  prenotata: "text-bg-warning",
  confermata: "text-bg-primary",
  svolta: "text-bg-success",
  annullata: "text-bg-danger",
  no_show: "text-bg-secondary",
};

function formatDateTime(value) {
  if (!value) return "-";
  const date = new Date(value);
  return date.toLocaleString("it-IT", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function lessonDateKey(lesson) {
  const date = new Date(lesson?.data_inizio);
  if (Number.isNaN(date.getTime())) return null;
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatStudents(students = []) {
  if (!Array.isArray(students) || students.length === 0) return "-";
  return students
    .map((student) => `#${student.id} ${student.nome} ${student.cognome}`.trim())
    .join(" | ");
}

function getStatusBadge(status) {
  const normalized = String(status || "").trim().toLowerCase();
  const badgeClass = STATUS_BADGE_CLASS[normalized] || "text-bg-light";
  return `<span class="badge ${badgeClass}">${normalized || "-"}</span>`;
}

function setSelectedLesson(lessonId) {
  selectedLessonId = lessonId;
  renderListView();
  renderSelectedLessonDetails();
}

function renderSelectedLessonDetails() {
  const container = document.getElementById("selected-lesson-content");
  if (!container) return;

  const selectedLesson = lessons.find((lesson) => lesson.id === selectedLessonId);
  if (!selectedLesson) {
    container.className = "small text-muted";
    container.textContent = "Nessuna lezione selezionata.";
    return;
  }

  container.className = "small";
  container.innerHTML = `
    <div><strong>ID:</strong> ${selectedLesson.id}</div>
    <div><strong>Stato:</strong> ${getStatusBadge(selectedLesson.status)}</div>
    <div><strong>Materia:</strong> ${selectedLesson.materia_nome || "-"}</div>
    <div><strong>Inizio:</strong> ${formatDateTime(selectedLesson.data_inizio)}</div>
    <div><strong>Fine:</strong> ${formatDateTime(selectedLesson.data_fine)}</div>
    <div><strong>Studenti:</strong> ${formatStudents(selectedLesson.students)}</div>
    <div><strong>Note:</strong> ${selectedLesson.note || "-"}</div>
  `;
}

function renderListView() {
  const list = document.getElementById("lessons-list");
  if (!list) return;

  if (!Array.isArray(lessons) || lessons.length === 0) {
    list.innerHTML = '<div class="list-group-item text-muted">Nessuna lezione trovata.</div>';
    return;
  }

  const sorted = [...lessons].sort(
    (a, b) => new Date(a?.data_inizio).getTime() - new Date(b?.data_inizio).getTime(),
  );

  list.innerHTML = "";
  sorted.forEach((lesson) => {
    const row = document.createElement("button");
    row.type = "button";
    row.className = `list-group-item list-group-item-action ${selectedLessonId === lesson.id ? "active" : ""}`;
    row.innerHTML = `
      <div class="d-flex justify-content-between flex-wrap gap-2 text-start">
        <div>
          <div><strong>Lezione #${lesson.id}</strong> • Stato: ${getStatusBadge(lesson.status)}</div>
          <div class="small text-muted">Inizio: ${formatDateTime(lesson.data_inizio)}</div>
          <div class="small text-muted">Fine: ${formatDateTime(lesson.data_fine)}</div>
          <div class="small text-muted">Studenti: ${formatStudents(lesson.students)}</div>
          <div class="small text-muted">Materia: ${lesson.materia_nome || "-"}</div>
          <div class="small text-muted">${lesson.note || "Nessuna nota"}</div>
        </div>
      </div>
    `;
    row.addEventListener("click", () => setSelectedLesson(lesson.id));
    list.appendChild(row);
  });
}

function renderCalendarView() {
  const monthLabel = document.getElementById("calendar-month-label");
  const grid = document.getElementById("calendar-grid");
  if (!monthLabel || !grid) return;

  const year = currentMonthDate.getFullYear();
  const monthIndex = currentMonthDate.getMonth();
  monthLabel.textContent = currentMonthDate.toLocaleString("it-IT", {
    month: "long",
    year: "numeric",
  });

  const firstDay = new Date(year, monthIndex, 1);
  const firstWeekday = (firstDay.getDay() + 6) % 7;
  const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();

  const countByDay = lessons.reduce((acc, lesson) => {
    const key = lessonDateKey(lesson);
    if (!key) return acc;
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  const weekHeaders = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"];
  grid.innerHTML = "";

  weekHeaders.forEach((label) => {
    const col = document.createElement("div");
    col.className = "col";
    col.innerHTML = `<div class="text-center fw-semibold small text-primary">${label}</div>`;
    grid.appendChild(col);
  });

  for (let i = 0; i < firstWeekday; i += 1) {
    const col = document.createElement("div");
    col.className = "col";
    col.innerHTML = '<div class="border rounded p-2 bg-light" style="min-height:64px;"></div>';
    grid.appendChild(col);
  }

  for (let day = 1; day <= daysInMonth; day += 1) {
    const key = `${year}-${String(monthIndex + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const totalLessons = countByDay[key] || 0;
    const col = document.createElement("div");
    col.className = "col";
    col.innerHTML = `
      <div class="border rounded p-2 ${totalLessons > 0 ? "border-primary" : ""}" style="min-height:64px;">
        <div class="fw-semibold">${day}</div>
        <div class="small ${totalLessons > 0 ? "text-primary" : "text-muted"}">
          ${totalLessons > 0 ? `${totalLessons} lezione${totalLessons > 1 ? "i" : ""}` : "-"}
        </div>
      </div>
    `;
    grid.appendChild(col);
  }
}

async function loadLessons() {
  const list = document.getElementById("lessons-list");
  if (list) {
    list.innerHTML = '<div class="list-group-item text-muted">Caricamento lezioni...</div>';
  }

  try {
    const response = await authFetch(`${API_LESSONS_URL_BASE}/user/getAllLessons`, { method: "GET" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const payload = await response.json();
    lessons = Array.isArray(payload) ? payload : [];
    if (lessons.length > 0 && !lessons.some((lesson) => lesson.id === selectedLessonId)) {
      selectedLessonId = lessons[0].id;
    }
  } catch (error) {
    console.warn("Errore nel caricamento lezioni:", error);
    lessons = [];
    selectedLessonId = null;
    if (list) {
      list.innerHTML = '<div class="list-group-item text-danger">Errore nel caricamento lezioni.</div>';
    }
  }

  renderListView();
  renderCalendarView();
  renderSelectedLessonDetails();
}

document.addEventListener("DOMContentLoaded", () => {
  const refreshButton = document.getElementById("refresh-lessons");
  const prevMonth = document.getElementById("prev-month");
  const nextMonth = document.getElementById("next-month");

  if (refreshButton) {
    refreshButton.addEventListener("click", loadLessons);
  }
  if (prevMonth) {
    prevMonth.addEventListener("click", () => {
      currentMonthDate = new Date(currentMonthDate.getFullYear(), currentMonthDate.getMonth() - 1, 1);
      renderCalendarView();
    });
  }
  if (nextMonth) {
    nextMonth.addEventListener("click", () => {
      currentMonthDate = new Date(currentMonthDate.getFullYear(), currentMonthDate.getMonth() + 1, 1);
      renderCalendarView();
    });
  }

  loadLessons();
});
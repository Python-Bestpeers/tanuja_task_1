const toggleBtn = document.getElementById("toggle-btn");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("main-content");

toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("hidden");
  mainContent.classList.toggle("full-width");
});

const createTaskBtn = document.getElementById("create-task-btn");

createTaskBtn.addEventListener("click", () => {
  window.location.href = "{% url 'create_task' %}";  // Redirect to create-task page
});
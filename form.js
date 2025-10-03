document.getElementById("jobForm").addEventListener("submit", function(e) {
  e.preventDefault();

  // Collect form data
  const formData = new FormData(this);
  const jobData = {};
  formData.forEach((value, key) => jobData[key] = value);

  // Send to Telegram bot (via WebApp API)
  if (window.Telegram && window.Telegram.WebApp) {
    window.Telegram.WebApp.sendData(JSON.stringify(jobData));
  } else {
    alert("Form submitted! (Not in Telegram)");
    console.log(jobData);
  }
});

// Example: update progress bar as user fills form
const inputs = document.querySelectorAll("input, select, textarea");
const progress = document.getElementById("progress");

inputs.forEach(input => {
  input.addEventListener("input", () => {
    const filled = [...inputs].filter(i => i.value.trim() !== "").length;
    const percent = Math.min(100, (filled / inputs.length) * 100);
    progress.style.width = percent + "%";
  });
});

console.log("Telegram WebApp object:", window.Telegram?.WebApp);

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Quill editor
  const quill = new Quill("#editor", {
    theme: "snow",
    placeholder: "Describe the role, responsibilities, and perks...",
    modules: {
      toolbar: [
        ["bold", "italic", "underline", "strike"],
        [{ list: "ordered" }, { list: "bullet" }],
        ["link"],
      ],
    },
  });

  // Elements
  const jobForm = document.getElementById("jobForm");
  const hiddenDescription = document.getElementById("hiddenDescription");
  const progress = document.getElementById("progress");
  const formSection = document.getElementById("formSection");
  const previewSection = document.getElementById("previewSection");
  const previewBtn = document.getElementById("previewBtn");
  const previewContent = document.getElementById("previewContent");
  const editJob = document.getElementById("editJob");
  const confirmSubmit = document.getElementById("confirmSubmit");

  // Progress bar
  const inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach((input) => {
    input.addEventListener("input", () => {
      const filled = [...inputs].filter((i) => i.value.trim() !== "").length;
      const percent = Math.min(100, (filled / inputs.length) * 100);
      progress.style.width = percent + "%";
    });
  });

  // Preview
  previewBtn.addEventListener("click", () => {
    hiddenDescription.value = quill.root.innerHTML;
    const formData = new FormData(jobForm);
    const jobData = {};
    formData.forEach((value, key) => (jobData[key] = value));

    previewContent.innerHTML = `
      <h3><i class="fa-solid fa-briefcase"></i> ${jobData.job_title}</h3>
      <p><b>Type:</b> ${jobData.job_type}</p>
      <p><b>Sector:</b> ${jobData.job_sector}</p>
      <hr>
      <p><b>Education:</b> ${jobData.education}</p>
      <p><b>Experience:</b> ${jobData.experience}</p>
      <p><b>Gender:</b> ${jobData.gender}</p>
      <p><b>Skills:</b> ${jobData.skills || "N/A"}</p>
      <hr>
      <p><b>Salary:</b> ${jobData.salary} ${jobData.currency}</p>
      <p><b>Location:</b> ${jobData.city}, ${jobData.country}</p>
      <hr>
      <h4><i class="fa-solid fa-file-lines"></i> Job Description</h4>
      <div>${jobData.description}</div>
    `;

    formSection.style.display = "none";
    previewSection.style.display = "block";
  });

  editJob.addEventListener("click", () => {
    previewSection.style.display = "none";
    formSection.style.display = "block";
  });

  // Confirm submit → send data to bot
  confirmSubmit.addEventListener("click", () => {
    const formData = new FormData(jobForm);
    const jobData = {};
    formData.forEach((value, key) => (jobData[key] = value));

    const tg = window.Telegram?.WebApp;
    if (tg) {
      console.log("✅ Telegram WebApp detected. Sending job data...");
      tg.ready(); // 🔥 REQUIRED for Mobile/Desktop
      tg.sendData(JSON.stringify(jobData));
      tg.close();
    } else {
      alert("⚠️ Telegram WebApp not active. Please open this form via the bot.");
    }
  });

  jobForm.addEventListener("submit", (e) => {
    e.preventDefault();
    previewBtn.click();
  });
});

// Initialize Quill editor
var quill = new Quill('#editor', {
  theme: 'snow',
  placeholder: 'Describe the role, responsibilities, and perks...',
  modules: {
    toolbar: [
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'list': 'ordered' }, { 'list': 'bullet' }],
      ['link']
    ]
  }
});

const jobForm = document.getElementById("jobForm");
const hiddenDescription = document.getElementById("hiddenDescription");
const progress = document.getElementById("progress");

// Modal elements
const previewModal = document.getElementById("previewModal");
const previewDetails = document.getElementById("previewDetails");
const closeModal = document.querySelector(".close");
const editJob = document.getElementById("editJob");
const confirmSubmit = document.getElementById("confirmSubmit");

// Progress bar update
const inputs = document.querySelectorAll("input, select, textarea");
inputs.forEach(input => {
  input.addEventListener("input", () => {
    const filled = [...inputs].filter(i => i.value.trim() !== "").length;
    const percent = Math.min(100, (filled / inputs.length) * 100);
    progress.style.width = percent + "%";
  });
});

// 🟢 Show preview modal before posting
jobForm.addEventListener("submit", function (e) {
  e.preventDefault();
  hiddenDescription.value = quill.root.innerHTML;

  const formData = new FormData(jobForm);
  const jobData = {};
  formData.forEach((value, key) => (jobData[key] = value));

  // Fill preview content
  previewDetails.innerHTML = `
    <h3><i class="fa-solid fa-briefcase"></i> ${jobData.job_title}</h3>
    <p><i class="fa-solid fa-list-check"></i> <b>Type:</b> ${jobData.job_type}</p>
    <p><i class="fa-solid fa-industry"></i> <b>Sector:</b> ${jobData.job_sector}</p>
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

  previewModal.style.display = "block";
});

// 🟠 Close modal
closeModal.addEventListener("click", () => {
  previewModal.style.display = "none";
});

// 🟡 Edit job (close modal and go back)
editJob.addEventListener("click", () => {
  previewModal.style.display = "none";
});

// 🟣 Confirm post — send to Telegram WebApp
confirmSubmit.addEventListener("click", () => {
  const formData = new FormData(jobForm);
  const jobData = {};
  formData.forEach((value, key) => (jobData[key] = value));

  const tg = window.Telegram?.WebApp;
  if (tg) {
    tg.sendData(JSON.stringify(jobData));
    tg.close();
  } else {
    alert("Job would be posted! (Pending)");
    console.log(jobData);
  }
});

const foundationData = {
  project: "The Archive of Merit Project",
  branch: "foundation/archive-of-merit-project",
  title: "Foundations About Me",
  name: "Justin-Ames Gamache, M.Ed., M.S.",
  roles: [
    "Scholar-Practitioner",
    "Doctoral Researcher",
    "Educational Technology Leadership",
    "Psychology and Education"
  ],
  summary:
    "Justin-Ames Gamache, M.Ed., M.S., is a scholar-practitioner whose work reflects a sustained commitment to education, psychology, leadership, and human-centered learning. His academic background includes graduate study in education and psychology, with doctoral work in educational technology leadership that further extends his interdisciplinary foundation.",
  purpose:
    "This foundation record preserves and presents a coherent public-facing account of academic and professional development. It organizes profile-based evidence into a durable and readable archival format.",
  interests: [
    "Educational Technology",
    "Psychology",
    "Leadership",
    "Higher Education",
    "Mindfulness",
    "Student Well-Being",
    "Identity",
    "Equity",
    "Human-Centered Learning"
  ],
  profiles: [
    {
      label: "ResearchGate",
      url: "https://www.researchgate.net/profile/Justin-Ames-Gamache-3"
    },
    {
      label: "LinkedIn",
      url: "https://www.linkedin.com/in/thescholarlypsychologistdoctoraleducationaltechnology/"
    }
  ],
  records: [
    "Justin-Ames Gamache®, M.Ed., M.S. _ LinkedIn.pdf",
    "Justin-Ames GAMACHE _ Student _ Master of Education, Master of Science in Psychology and Doctor of Education (in progress) _ University of Phoenix, Phoenix _ College of Education _ Research profile.pdf",
    "researchgate-linkedin-profile-record.html",
    "foundations-about-me.md"
  ]
};

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderList(items, className = "") {
  return items
    .map((item) => `<li class="${className}">${escapeHtml(item)}</li>`)
    .join("");
}

function renderProfiles(profiles) {
  return profiles
    .map(
      (profile) => `
        <a class="foundation-button" href="${escapeHtml(profile.url)}" target="_blank" rel="noopener noreferrer">
          ${escapeHtml(profile.label)}
        </a>
      `
    )
    .join("");
}

function createFoundationMarkup(data) {
  return `
    <section class="foundation-wrapper">
      <div class="foundation-card">
        <p class="foundation-eyebrow">${escapeHtml(data.project)}</p>
        <h1 class="foundation-title">${escapeHtml(data.title)}</h1>
        <p class="foundation-name">${escapeHtml(data.name)}</p>
        <p class="foundation-branch">${escapeHtml(data.branch)}</p>
      </div>

      <div class="foundation-card">
        <h2>Professional Identity</h2>
        <ul class="foundation-list">
          ${renderList(data.roles, "foundation-list-item")}
        </ul>
      </div>

      <div class="foundation-card">
        <h2>Summary</h2>
        <p>${escapeHtml(data.summary)}</p>
      </div>

      <div class="foundation-card">
        <h2>Purpose</h2>
        <p>${escapeHtml(data.purpose)}</p>
      </div>

      <div class="foundation-card">
        <h2>Core Interests</h2>
        <ul class="foundation-list">
          ${renderList(data.interests, "foundation-list-item")}
        </ul>
      </div>

      <div class="foundation-card">
        <h2>Public Profiles</h2>
        <div class="foundation-button-row">
          ${renderProfiles(data.profiles)}
        </div>
      </div>

      <div class="foundation-card">
        <h2>Foundation Records</h2>
        <ul class="foundation-list">
          ${renderList(data.records, "foundation-list-item")}
        </ul>
      </div>
    </section>
  `;
}

function applyFoundationStyles() {
  const style = document.createElement("style");
  style.textContent = `
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #101418;
      color: #f4f7fb;
      line-height: 1.6;
    }

    .foundation-wrapper {
      max-width: 960px;
      margin: 0 auto;
      padding: 40px 20px;
      display: grid;
      gap: 20px;
    }

    .foundation-card {
      background: #18202a;
      border: 1px solid #2a3440;
      border-radius: 14px;
      padding: 24px;
    }

    .foundation-eyebrow {
      margin: 0 0 8px;
      color: #9fc3ff;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 0.82rem;
      font-weight: 700;
    }

    .foundation-title {
      margin: 0 0 8px;
      font-size: 2rem;
    }

    .foundation-name {
      margin: 0 0 6px;
      font-size: 1.1rem;
      font-weight: 700;
    }

    .foundation-branch {
      margin: 0;
      color: #b8c4d1;
      font-size: 0.95rem;
    }

    .foundation-card h2 {
      margin-top: 0;
      margin-bottom: 12px;
    }

    .foundation-list {
      margin: 0;
      padding-left: 20px;
    }

    .foundation-list-item {
      margin-bottom: 8px;
    }

    .foundation-button-row {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }

    .foundation-button {
      display: inline-block;
      padding: 12px 16px;
      border-radius: 10px;
      border: 1px solid #3d4b5b;
      background: #202b36;
      color: #ffffff;
      text-decoration: none;
      font-weight: 700;
    }

    .foundation-button:hover {
      background: #2a3744;
    }
  `;
  document.head.appendChild(style);
}

function initFoundationsApp() {
  applyFoundationStyles();

  const root = document.getElementById("foundations-app") || document.body;
  root.innerHTML = createFoundationMarkup(foundationData);
}

document.addEventListener("DOMContentLoaded", initFoundationsApp);

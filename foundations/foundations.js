async function loadFoundationData() {
  const response = await fetch("foundations-links.json");
  if (!response.ok) {
    throw new Error("Failed to load foundations-links.json");
  }
  return response.json();
}

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
  return Object.entries(profiles)
    .map(
      ([label, url]) => `
        <a class="foundation-button" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">
          Open ${escapeHtml(label.charAt(0).toUpperCase() + label.slice(1))}
        </a>
      `
    )
    .join("");
}

function renderDocuments(documents) {
  return Object.entries(documents)
    .map(
      ([key, path]) => `
        <li class="foundation-list-item">
          <strong>${escapeHtml(key)}</strong>: ${escapeHtml(path)}
        </li>
      `
    )
    .join("");
}

function createFoundationMarkup(data) {
  return `
    <section class="foundation-wrapper">
      <div class="foundation-card">
        <p class="foundation-eyebrow">${escapeHtml(data.project_name)}</p>
        <h1 class="foundation-title">Foundations About Me</h1>
        <p class="foundation-name">${escapeHtml(data.display_name)}</p>
        <p class="foundation-branch">${escapeHtml(data.branch_name)}</p>
      </div>

      <div class="foundation-card">
        <h2>Professional Identity</h2>
        <p><strong>${escapeHtml(data.role)}</strong></p>
        <p>${escapeHtml(data.summary)}</p>
      </div>

      <div class="foundation-card">
        <h2>Focus Areas</h2>
        <ul class="foundation-list">
          ${renderList(data.focus_areas, "foundation-list-item")}
        </ul>
      </div>

      <div class="foundation-card">
        <h2>Public Profiles</h2>
        <div class="foundation-button-row">
          ${renderProfiles(data.profiles)}
          <a class="foundation-button" href="${escapeHtml(data.repository)}" target="_blank" rel="noopener noreferrer">
            Open Repository
          </a>
        </div>
      </div>

      <div class="foundation-card">
        <h2>Foundation Records</h2>
        <ul class="foundation-list">
          ${renderDocuments(data.documents)}
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

async function initFoundationsApp() {
  applyFoundationStyles();
  const root = document.getElementById("foundations-app") || document.body;

  try {
    const foundationData = await loadFoundationData();
    root.innerHTML = createFoundationMarkup(foundationData);
  } catch (error) {
    root.innerHTML = `<div style="padding:20px;color:#ffb3b3;">Error: ${escapeHtml(error.message)}</div>`;
  }
}

document.addEventListener("DOMContentLoaded", initFoundationsApp);

const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const queryPreview = document.getElementById("queryPreview");

const webLinks = document.getElementById("webLinks");
const newsLinks = document.getElementById("newsLinks");
const researchLinks = document.getElementById("researchLinks");

const presetButtons = Array.from(document.querySelectorAll(".preset"));

function encodeQuery(query) {
  return encodeURIComponent(query.trim());
}

function buildLink(label, url) {
  const li = document.createElement("li");
  const a = document.createElement("a");
  a.href = url;
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  a.textContent = label;
  li.appendChild(a);
  return li;
}

function clearLinks(node) {
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
}

function renderLinks(query) {
  const q = encodeQuery(query);

  clearLinks(webLinks);
  clearLinks(newsLinks);
  clearLinks(researchLinks);

  webLinks.appendChild(buildLink("Google Web", `https://www.google.com/search?q=${q}`));
  webLinks.appendChild(buildLink("Bing Web", `https://www.bing.com/search?q=${q}`));
  webLinks.appendChild(buildLink("DuckDuckGo", `https://duckduckgo.com/?q=${q}`));

  newsLinks.appendChild(buildLink("Google News", `https://news.google.com/search?q=${q}`));
  newsLinks.appendChild(buildLink("Google News Archive", `https://www.google.com/search?tbm=nws&q=${q}`));
  newsLinks.appendChild(buildLink("Yahoo News", `https://news.search.yahoo.com/search?p=${q}`));

  researchLinks.appendChild(buildLink("Google Scholar", `https://scholar.google.com/scholar?q=${q}&as_sdt=2006`));
  researchLinks.appendChild(buildLink("Google Books", `https://www.google.com/search?tbo=p&tbm=bks&q=${q}`));
  researchLinks.appendChild(buildLink("Justia Blawg Search", `https://blawgsearch.justia.com/search?query=${q}`));
}

function normalizeQuery(value) {
  return value.replace(/\s+/g, " ").trim();
}

function updateQuery(query) {
  const normalized = normalizeQuery(query);
  queryPreview.textContent = normalized || "";
  renderLinks(normalized);
}

searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  updateQuery(searchInput.value);
});

presetButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const query = button.dataset.query || "";
    searchInput.value = query;
    updateQuery(query);
  });
});

updateQuery(searchInput.value);

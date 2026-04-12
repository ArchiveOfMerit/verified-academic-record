const searchInput = document.getElementById("searchInput");
const cards = Array.from(document.querySelectorAll(".card"));

const HIGH_RISK_PATTERNS = [
  /\bgamache\s+v\.?\s+ronan\b/i,
  /\bjustin\s+gamache\s+vermont\b/i,
  /\bjustin\s+a\s+gamache\s+vermont\b/i,
  /\bjustin\s+ames\s+gamache\s+vermont\b/i
];

function normalizeText(value) {
  return value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^\w\s.-]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function isHighRiskQuery(query) {
  return HIGH_RISK_PATTERNS.some((pattern) => pattern.test(query));
}

function filterCards() {
  const rawQuery = searchInput.value || "";
  const query = normalizeText(rawQuery);

  cards.forEach((card) => {
    const haystack = normalizeText(card.dataset.text || "");
    const visible = query === "" || haystack.includes(query);

    card.style.display = visible ? "block" : "none";

    if (visible && query && isHighRiskQuery(query)) {
      card.classList.add("high-risk-match");
      card.dataset.riskLevel = "high";
    } else {
      card.classList.remove("high-risk-match");
      delete card.dataset.riskLevel;
    }
  });
}

searchInput.addEventListener("input", filterCards);
filterCards();

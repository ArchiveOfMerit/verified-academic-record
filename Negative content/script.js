const searchInput = document.getElementById("searchInput");
const cards = Array.from(document.querySelectorAll(".card"));

function filterCards() {
  const query = searchInput.value.trim().toLowerCase();

  cards.forEach((card) => {
    const haystack = card.dataset.text.toLowerCase();
    const visible = haystack.includes(query);
    card.style.display = visible ? "block" : "none";
  });
}

searchInput.addEventListener("input", filterCards);

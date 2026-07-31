// Recipe Finder — built by Sadia

const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const resultsDiv = document.getElementById("results");
const loadingDiv = document.getElementById("loading");
const noResultsDiv = document.getElementById("noResults");
const modal = document.getElementById("modal");
const modalBody = document.getElementById("modalBody");
const closeModal = document.getElementById("closeModal");

async function searchRecipes() {
  const query = searchInput.value.trim();
  if (!query) return;

  resultsDiv.innerHTML = "";
  noResultsDiv.classList.add("hidden");
  loadingDiv.classList.remove("hidden");

  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    loadingDiv.classList.add("hidden");

    if (!data.recipes || data.recipes.length === 0) {
      noResultsDiv.classList.remove("hidden");
      return;
    }

    data.recipes.forEach((recipe) => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `
        <img src="${recipe.image}" alt="${recipe.name}">
        <div class="card-info">
          <h3>${recipe.name}</h3>
          <span>${recipe.category}</span>
        </div>
      `;
      card.addEventListener("click", () => showRecipeDetail(recipe.id));
      resultsDiv.appendChild(card);
    });
  } catch (err) {
    loadingDiv.classList.add("hidden");
    noResultsDiv.classList.remove("hidden");
  }
}

async function showRecipeDetail(id) {
  const res = await fetch(`/api/recipe/${id}`);
  const recipe = await res.json();

  modalBody.innerHTML = `
    <img src="${recipe.image}" alt="${recipe.name}">
    <h2>${recipe.name}</h2>
    <p><strong>${recipe.category}</strong> · ${recipe.area}</p>
    <h4>Ingredients</h4>
    <ul>
      ${recipe.ingredients.map((i) => `<li>${i}</li>`).join("")}
    </ul>
    <h4>Instructions</h4>
    <p>${recipe.instructions}</p>
  `;

  modal.classList.remove("hidden");
}

searchBtn.addEventListener("click", searchRecipes);
searchInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") searchRecipes();
});

closeModal.addEventListener("click", () => {
  modal.classList.add("hidden");
});

modal.addEventListener("click", (e) => {
  if (e.target === modal) modal.classList.add("hidden");
});

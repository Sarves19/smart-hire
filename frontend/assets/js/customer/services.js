/**
 * ==========================================================
 * SMART HIRE - BROWSE SERVICES
 * ==========================================================
 */

let __services = [];
let __categories = [];

document.addEventListener("components:loaded", initializeServicesPage);

async function initializeServicesPage() {

    if (!AuthService.requireAuth()) return;

    await Promise.all([
        loadCategories(),
        loadServices(),
    ]);

    applyFiltersAndRender();

    initializeControls();

}

/**
 * ==========================================================
 * Load Data
 * ==========================================================
 */

async function loadCategories() {

    try {
        __categories = await ApiClient.get("/categories/", { auth: false });
    } catch (error) {
        console.error("Failed to load categories:", error);
        __categories = [];
    }

    const select = document.getElementById("categoryFilter");

    if (!select) return;

    __categories
        .filter(c => c.is_active)
        .forEach(cat => {
            const opt = document.createElement("option");
            opt.value = cat.id;
            opt.textContent = cat.name;
            select.appendChild(opt);
        });

}

async function loadServices() {

    const grid = document.getElementById("servicesGrid");

    try {
        __services = await ApiClient.get("/services/", { auth: false });
    } catch (error) {
        console.error("Failed to load services:", error);
        __services = [];
        if (grid) {
            grid.innerHTML = `
                <div class="services-error">
                    Couldn't load services right now. Please try again shortly.
                </div>
            `;
        }
    }

}

/**
 * ==========================================================
 * Controls
 * ==========================================================
 */

function initializeControls() {

    const searchInput = document.getElementById("searchInput");
    const categoryFilter = document.getElementById("categoryFilter");
    const sortFilter = document.getElementById("sortFilter");

    let debounceTimer;

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(applyFiltersAndRender, 200);
        });
    }

    if (categoryFilter) {
        categoryFilter.addEventListener("change", applyFiltersAndRender);
    }

    if (sortFilter) {
        sortFilter.addEventListener("change", applyFiltersAndRender);
    }

}

/**
 * ==========================================================
 * Filter + Sort + Render
 * ==========================================================
 */

function applyFiltersAndRender() {

    const searchTerm = (document.getElementById("searchInput")?.value || "")
        .trim()
        .toLowerCase();

    const categoryId = document.getElementById("categoryFilter")?.value || "";

    const sortBy = document.getElementById("sortFilter")?.value || "newest";

    let filtered = __services.filter(s => s.is_available && s.status === "ACTIVE");

    if (searchTerm) {
        filtered = filtered.filter(s =>
            s.title.toLowerCase().includes(searchTerm) ||
            s.description.toLowerCase().includes(searchTerm) ||
            s.category_name.toLowerCase().includes(searchTerm) ||
            s.provider_name.toLowerCase().includes(searchTerm)
        );
    }

    if (categoryId) {
        filtered = filtered.filter(s => String(s.category_id) === String(categoryId));
    }

    switch (sortBy) {
        case "price_asc":
            filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
            break;
        case "price_desc":
            filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
            break;
        case "rating":
            filtered.sort((a, b) => b.average_rating - a.average_rating);
            break;
        default:
            filtered.sort((a, b) => b.id - a.id);
    }

    renderServices(filtered);

}

function renderServices(services) {

    const grid = document.getElementById("servicesGrid");
    const emptyState = document.getElementById("servicesEmptyState");
    const resultsCount = document.getElementById("resultsCount");

    if (!grid) return;

    if (resultsCount) {
        resultsCount.textContent =
            `${services.length} service${services.length === 1 ? "" : "s"} found`;
    }

    if (services.length === 0) {
        grid.innerHTML = "";
        if (emptyState) emptyState.style.display = "block";
        return;
    }

    if (emptyState) emptyState.style.display = "none";

    grid.innerHTML = services.map(renderServiceCard).join("");

    grid.querySelectorAll(".service-card").forEach(card => {
        card.addEventListener("click", () => {
            window.location.href = `service-details.html?id=${card.dataset.id}`;
        });
    });

}

function renderServiceCard(service) {

    const price = parseFloat(service.price).toLocaleString("en-LK", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });

    const stars = renderStars(service.average_rating);

    return `
        <div class="service-card" data-id="${service.id}">
            <div class="service-card-image">
                ${
                    service.image_url
                        ? `<img src="${escapeHtml(service.image_url)}" alt="${escapeHtml(service.title)}">`
                        : `<i class="bi bi-tools"></i>`
                }
                <span class="service-category-badge">${escapeHtml(service.category_name)}</span>
            </div>
            <div class="service-card-body">
                <h3>${escapeHtml(service.title)}</h3>
                <p class="service-provider">
                    <i class="bi bi-shop"></i> ${escapeHtml(service.provider_name)}
                </p>
                <p class="service-description">${escapeHtml(truncate(service.description, 90))}</p>
                <div class="service-rating">
                    ${stars}
                    <span>${service.average_rating > 0 ? service.average_rating : "No reviews yet"}
                        ${service.review_count > 0 ? `(${service.review_count})` : ""}
                    </span>
                </div>
            </div>
            <div class="service-card-footer">
                <span class="service-price">Rs. ${price}</span>
                <button class="btn-view-details">View Details</button>
            </div>
        </div>
    `;

}

function renderStars(rating) {

    const full = Math.round(rating);
    let html = "";

    for (let i = 1; i <= 5; i++) {
        html += `<i class="bi ${i <= full ? "bi-star-fill" : "bi-star"}"></i>`;
    }

    return `<span class="stars">${html}</span>`;

}

function truncate(text, length) {
    if (!text) return "";
    return text.length > length ? text.slice(0, length).trim() + "…" : text;
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str ?? "";
    return div.innerHTML;
}

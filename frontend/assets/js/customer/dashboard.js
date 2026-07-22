/**
 * ==========================================================
 * SMART HIRE - CUSTOMER DASHBOARD
 * ==========================================================
 */

document.addEventListener("components:loaded", initializeDashboard);

let __allBookings = [];

/**
 * ==========================================================
 * Initialize Dashboard
 * ==========================================================
 */

async function initializeDashboard() {

    if (!AuthService.requireAuth()) return;

    await loadWelcomeBanner();

    await loadBookingsAndRender();

    initializeQuickActions();

}

/**
 * ==========================================================
 * Load Welcome Banner
 * ==========================================================
 */

async function loadWelcomeBanner() {

    const user = await AuthService.getCurrentUser();

    if (!user) return;

    const welcomeTitle = document.getElementById("welcomeTitle");
    const currentDate = document.getElementById("currentDate");

    if (welcomeTitle) {
        welcomeTitle.textContent = `Welcome back, ${user.full_name}!`;
    }

    if (currentDate) {
        currentDate.textContent = getCurrentDate();
    }

}

function getCurrentDate() {

    const today = new Date();

    return today.toLocaleDateString("en-US", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
    });

}

/**
 * ==========================================================
 * Load Bookings (real API) + Render Stats + Recent Table
 * ==========================================================
 */

async function loadBookingsAndRender() {

    try {

        __allBookings = await ApiClient.get("/bookings/");

    } catch (error) {

        console.error("Failed to load bookings:", error);
        __allBookings = [];

    }

    renderDashboardStatistics(__allBookings);

    await renderRecentBookings(__allBookings);

}

/**
 * ==========================================================
 * Render Dashboard Statistics (derived from real bookings)
 * ==========================================================
 */

function renderDashboardStatistics(bookings) {

    const active = bookings.filter(b =>
        ["ACCEPTED", "IN_PROGRESS"].includes(b.status)
    ).length;

    const pending = bookings.filter(b => b.status === "PENDING").length;

    const completed = bookings.filter(b => b.status === "COMPLETED").length;

    const distinctProviders = new Set(
        bookings.map(b => b.provider_id)
    ).size;

    setText("activeBookings", active);
    setText("pendingBookings", pending);
    setText("completedBookings", completed);
    setText("savedProviders", distinctProviders);

    // Relabel this card - there's no "saved/favorite providers"
    // concept in the backend yet, so show something real instead:
    // how many distinct providers you've actually booked with.
    const savedLabel = document.querySelector("#savedProviders + p, #savedProviders ~ p");
    if (savedLabel) savedLabel.textContent = "Providers Booked";

}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

/**
 * ==========================================================
 * Render Recent Bookings Table (real data)
 * ==========================================================
 */

async function renderRecentBookings(bookings) {

    const tableBody = document.getElementById("recentBookingsTable");

    if (!tableBody) return;

    if (bookings.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" class="text-center text-muted py-4">
                    No bookings yet.
                    <a href="services.html">Browse services</a> to get started.
                </td>
            </tr>
        `;
        return;
    }

    const recent = [...bookings]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 5);

    // Fetch service titles for the visible rows only.
    const serviceCache = {};

    await Promise.all(
        recent.map(async (b) => {
            if (serviceCache[b.service_id]) return;
            try {
                serviceCache[b.service_id] = await ApiClient.get(
                    `/services/${b.service_id}`,
                    { auth: false }
                );
            } catch (e) {
                serviceCache[b.service_id] = null;
            }
        })
    );

    tableBody.innerHTML = recent.map(booking => {

        const service = serviceCache[booking.service_id];
        const title = service ? service.title : `Service #${booking.service_id}`;
        const provider = service ? service.provider_name : "-";
        const statusClass = booking.status.toLowerCase();

        return `
            <tr class="booking-row" data-id="${booking.id}" style="cursor:pointer;">
                <td>${escapeHtml(title)}</td>
                <td>${escapeHtml(provider)}</td>
                <td>
                    <span class="status-badge ${statusClass}">
                        ${formatStatus(booking.status)}
                    </span>
                </td>
            </tr>
        `;

    }).join("");

    tableBody.querySelectorAll(".booking-row").forEach(row => {
        row.addEventListener("click", () => {
            window.location.href = `booking-details.html?id=${row.dataset.id}`;
        });
    });

}

function formatStatus(status) {
    return status.charAt(0) + status.slice(1).toLowerCase().replace("_", " ");
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

/**
 * ==========================================================
 * Quick Actions
 * ==========================================================
 */

function initializeQuickActions() {

    const buttons = document.querySelectorAll(".quick-actions .action-btn");

    if (buttons.length >= 3) {
        buttons[0].addEventListener("click", () => window.location.href = "services.html");
        buttons[1].addEventListener("click", () => window.location.href = "services.html");
        buttons[2].addEventListener("click", () => window.location.href = "profile.html");
    }

    const viewAllLink = document.querySelector(".view-all-link");
    if (viewAllLink) {
        viewAllLink.addEventListener("click", (e) => {
            e.preventDefault();
            window.location.href = "bookings.html";
        });
    }

}

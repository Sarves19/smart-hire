/**
 * ==========================================================
 * SMART HIRE - MY BOOKINGS
 * ==========================================================
 */

let __bookings = [];
let __currentFilter = "ALL";
let __serviceCache = {};

document.addEventListener("components:loaded", initializeBookingsPage);

async function initializeBookingsPage() {

    if (!AuthService.requireAuth()) return;

    await loadBookings();

    initializeTabs();

    renderBookings();

}

async function loadBookings() {

    const list = document.getElementById("bookingsList");

    try {

        __bookings = await ApiClient.get("/bookings/");

        // Preload service details for each distinct service_id
        // referenced, so the list can show real titles/providers.
        const uniqueServiceIds = [...new Set(__bookings.map(b => b.service_id))];

        await Promise.all(
            uniqueServiceIds.map(async (id) => {
                try {
                    __serviceCache[id] = await ApiClient.get(`/services/${id}`, { auth: false });
                } catch (e) {
                    __serviceCache[id] = null;
                }
            })
        );

    } catch (error) {
        console.error("Failed to load bookings:", error);
        __bookings = [];
        if (list) {
            list.innerHTML = `<div class="bookings-error">Couldn't load your bookings right now.</div>`;
        }
    }

}

function initializeTabs() {

    const tabs = document.querySelectorAll(".tab-btn");

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            __currentFilter = tab.dataset.status;
            renderBookings();
        });
    });

}

function renderBookings() {

    const list = document.getElementById("bookingsList");

    if (!list) return;

    const filtered = __currentFilter === "ALL"
        ? __bookings
        : __bookings.filter(b => b.status === __currentFilter);

    if (filtered.length === 0) {
        list.innerHTML = `
            <div class="bookings-empty">
                <i class="bi bi-calendar-x"></i>
                <h3>No bookings here</h3>
                <p>
                    ${__bookings.length === 0
                        ? `You haven't booked any services yet.`
                        : `No bookings match this filter.`}
                </p>
                <a href="services.html" class="btn-primary-inline">Browse Services</a>
            </div>
        `;
        return;
    }

    const sorted = [...filtered].sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );

    list.innerHTML = sorted.map(renderBookingRow).join("");

    list.querySelectorAll(".booking-item").forEach(item => {
        item.addEventListener("click", (e) => {
            if (e.target.closest(".booking-cancel-btn")) return;
            window.location.href = `booking-details.html?id=${item.dataset.id}`;
        });
    });

    list.querySelectorAll(".booking-cancel-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            handleCancelBooking(btn.dataset.id);
        });
    });

}

function renderBookingRow(booking) {

    const service = __serviceCache[booking.service_id];
    const title = service ? service.title : `Service #${booking.service_id}`;
    const provider = service ? service.provider_name : "-";
    const price = service ? parseFloat(service.price).toLocaleString("en-LK", { minimumFractionDigits: 2 }) : "-";

    const date = new Date(booking.booking_date).toLocaleString("en-US", {
        weekday: "short", day: "numeric", month: "short",
        year: "numeric", hour: "numeric", minute: "2-digit",
    });

    const canCancel = ["PENDING", "ACCEPTED"].includes(booking.status);

    return `
        <div class="booking-item" data-id="${booking.id}">
            <div class="booking-item-main">
                <h3>${escapeHtml(title)}</h3>
                <p><i class="bi bi-shop"></i> ${escapeHtml(provider)}</p>
                <p><i class="bi bi-calendar"></i> ${date}</p>
            </div>
            <div class="booking-item-side">
                <span class="status-badge ${booking.status.toLowerCase()}">
                    ${formatStatus(booking.status)}
                </span>
                <span class="booking-price">Rs. ${price}</span>
                ${canCancel ? `
                    <button class="booking-cancel-btn" data-id="${booking.id}">
                        Cancel
                    </button>
                ` : ""}
            </div>
        </div>
    `;

}

async function handleCancelBooking(bookingId) {

    const confirmed = confirm("Are you sure you want to cancel this booking?");

    if (!confirmed) return;

    try {

        await ApiClient.patch(`/bookings/${bookingId}/status`, {
            status: "CANCELLED",
        });

        const booking = __bookings.find(b => b.id === parseInt(bookingId, 10));
        if (booking) booking.status = "CANCELLED";

        renderBookings();

    } catch (error) {
        alert(error.message || "Failed to cancel booking. Please try again.");
    }

}

function formatStatus(status) {
    return status.charAt(0) + status.slice(1).toLowerCase().replace("_", " ");
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str ?? "";
    return div.innerHTML;
}

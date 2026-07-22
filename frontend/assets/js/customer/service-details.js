/**
 * ==========================================================
 * SMART HIRE - SERVICE DETAILS
 * ==========================================================
 */

let __service = null;

document.addEventListener("components:loaded", initializeServiceDetails);

async function initializeServiceDetails() {

    if (!AuthService.requireAuth()) return;

    const serviceId = getServiceIdFromUrl();

    if (!serviceId) {
        renderError("No service was specified.");
        return;
    }

    try {
        __service = await ApiClient.get(`/services/${serviceId}`, { auth: false });
        renderService(__service);
    } catch (error) {
        console.error("Failed to load service:", error);
        renderError(
            error.status === 404
                ? "This service could not be found. It may have been removed."
                : "Couldn't load this service right now. Please try again."
        );
        return;
    }

    initializeBookingModal();

}

function getServiceIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function renderError(message) {
    const container = document.getElementById("serviceDetailsContainer");
    if (!container) return;
    container.innerHTML = `<div class="details-error">${escapeHtml(message)}</div>`;
}

/**
 * ==========================================================
 * Render
 * ==========================================================
 */

function renderService(service) {

    const container = document.getElementById("serviceDetailsContainer");

    if (!container) return;

    const price = parseFloat(service.price).toLocaleString("en-LK", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });

    const stars = renderStars(service.average_rating);

    container.innerHTML = `
        <div class="details-card">

            <div class="details-image">
                ${
                    service.image_url
                        ? `<img src="${escapeHtml(service.image_url)}" alt="${escapeHtml(service.title)}">`
                        : `<i class="bi bi-tools"></i>`
                }
            </div>

            <div class="details-body">

                <span class="service-category-badge">${escapeHtml(service.category_name)}</span>

                <h1>${escapeHtml(service.title)}</h1>

                <p class="details-provider">
                    <i class="bi bi-shop"></i> ${escapeHtml(service.provider_name)}
                </p>

                <div class="details-rating">
                    ${stars}
                    <span>${service.average_rating > 0 ? service.average_rating : "No reviews yet"}
                        ${service.review_count > 0 ? `(${service.review_count} review${service.review_count === 1 ? "" : "s"})` : ""}
                    </span>
                </div>

                <div class="details-meta">
                    <div>
                        <i class="bi bi-clock"></i>
                        ${service.duration_minutes} minutes
                    </div>
                    ${service.service_location ? `
                        <div>
                            <i class="bi bi-geo-alt"></i>
                            ${escapeHtml(service.service_location)}
                        </div>
                    ` : ""}
                </div>

                <h3>Description</h3>
                <p class="details-description">${escapeHtml(service.description)}</p>

            </div>

            <div class="details-sidebar">
                <div class="price-card">
                    <p class="price-label">Price</p>
                    <p class="price-value">Rs. ${price}</p>
                    ${
                        service.is_available && service.status === "ACTIVE"
                            ? `<button id="openBookingModal" class="btn-primary-full">Book Now</button>`
                            : `<button class="btn-primary-full" disabled>Currently Unavailable</button>`
                    }
                </div>
            </div>

        </div>
    `;

    const openBtn = document.getElementById("openBookingModal");
    if (openBtn) {
        openBtn.addEventListener("click", openBookingModal);
    }

}

function renderStars(rating) {
    const full = Math.round(rating);
    let html = "";
    for (let i = 1; i <= 5; i++) {
        html += `<i class="bi ${i <= full ? "bi-star-fill" : "bi-star"}"></i>`;
    }
    return `<span class="stars">${html}</span>`;
}

/**
 * ==========================================================
 * Booking Modal
 * ==========================================================
 */

function initializeBookingModal() {

    const modal = document.getElementById("bookingModal");
    const closeBtn = document.getElementById("closeBookingModal");
    const form = document.getElementById("bookingForm");
    const dateInput = document.getElementById("bookingDate");

    if (dateInput) {
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset() + 60);
        dateInput.min = now.toISOString().slice(0, 16);
    }

    if (closeBtn) {
        closeBtn.addEventListener("click", closeBookingModal);
    }

    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) closeBookingModal();
        });
    }

    if (form) {
        form.addEventListener("submit", handleBookingSubmit);
    }

}

function openBookingModal() {
    const modal = document.getElementById("bookingModal");
    if (modal) modal.style.display = "flex";
}

function closeBookingModal() {
    const modal = document.getElementById("bookingModal");
    if (modal) modal.style.display = "none";
}

async function handleBookingSubmit(event) {

    event.preventDefault();

    const errorEl = document.getElementById("bookingFormError");
    const successEl = document.getElementById("bookingFormSuccess");
    const submitBtn = document.getElementById("bookingSubmitBtn");

    errorEl.style.display = "none";
    successEl.style.display = "none";

    const bookingDate = document.getElementById("bookingDate").value;
    const note = document.getElementById("bookingNote").value.trim();

    if (!bookingDate) {
        errorEl.textContent = "Please select a date and time.";
        errorEl.style.display = "block";
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Booking…";

    try {

        await ApiClient.post("/bookings/", {
            service_id: __service.id,
            booking_date: new Date(bookingDate).toISOString(),
            customer_note: note || null,
        });

        successEl.textContent = "Booking confirmed! Redirecting to your bookings…";
        successEl.style.display = "block";

        setTimeout(() => {
            window.location.href = "bookings.html";
        }, 1200);

    } catch (error) {

        errorEl.textContent = error.message || "Failed to create booking. Please try again.";
        errorEl.style.display = "block";

        submitBtn.disabled = false;
        submitBtn.textContent = "Confirm Booking";

    }

}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str ?? "";
    return div.innerHTML;
}

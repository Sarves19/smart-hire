/**
 * ==========================================================
 * SMART HIRE - BOOKING DETAILS
 * ==========================================================
 */

let __booking = null;
let __service = null;
let __existingReview = null;

document.addEventListener("components:loaded", initializeBookingDetails);

async function initializeBookingDetails() {

    if (!AuthService.requireAuth()) return;

    const bookingId = getBookingIdFromUrl();

    if (!bookingId) {
        renderError("No booking was specified.");
        return;
    }

    try {

        __booking = await ApiClient.get(`/bookings/${bookingId}`);

        __service = await ApiClient.get(`/services/${__booking.service_id}`, { auth: false });

        if (__booking.status === "COMPLETED") {
            const allReviews = await ApiClient.get("/reviews/", { auth: false });
            __existingReview = allReviews.find(r => r.booking_id === __booking.id) || null;
        }

        renderBooking();

    } catch (error) {
        console.error("Failed to load booking:", error);
        renderError(
            error.status === 404
                ? "This booking could not be found, or you don't have access to it."
                : "Couldn't load this booking right now. Please try again."
        );
    }

}

function getBookingIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function renderError(message) {
    const container = document.getElementById("bookingDetailsContainer");
    if (container) {
        container.innerHTML = `<div class="details-error">${escapeHtml(message)}</div>`;
    }
}

/**
 * ==========================================================
 * Render
 * ==========================================================
 */

function renderBooking() {

    const container = document.getElementById("bookingDetailsContainer");

    if (!container) return;

    const price = parseFloat(__service.price).toLocaleString("en-LK", {
        minimumFractionDigits: 2,
    });

    const date = new Date(__booking.booking_date).toLocaleString("en-US", {
        weekday: "long", day: "numeric", month: "long",
        year: "numeric", hour: "numeric", minute: "2-digit",
    });

    const canCancel = ["PENDING", "ACCEPTED"].includes(__booking.status);

    container.innerHTML = `

        <div class="booking-details-header">
            <h1>${escapeHtml(__service.title)}</h1>
            <span class="status-badge ${__booking.status.toLowerCase()}">
                ${formatStatus(__booking.status)}
            </span>
        </div>

        <div class="details-card">

            <div class="details-body">

                <h3>Booking Information</h3>

                <div class="info-grid">
                    <div>
                        <p class="info-label">Provider</p>
                        <p class="info-value">${escapeHtml(__service.provider_name)}</p>
                    </div>
                    <div>
                        <p class="info-label">Date &amp; Time</p>
                        <p class="info-value">${date}</p>
                    </div>
                    <div>
                        <p class="info-label">Duration</p>
                        <p class="info-value">${__service.duration_minutes} minutes</p>
                    </div>
                    <div>
                        <p class="info-label">Booked On</p>
                        <p class="info-value">${new Date(__booking.created_at).toLocaleDateString()}</p>
                    </div>
                </div>

                ${__booking.customer_note ? `
                    <h3>Your Notes</h3>
                    <p class="details-description">${escapeHtml(__booking.customer_note)}</p>
                ` : ""}

                ${__booking.status === "COMPLETED" ? renderReviewSection() : ""}

            </div>

            <div class="details-sidebar">
                <div class="price-card">
                    <p class="price-label">Total</p>
                    <p class="price-value">Rs. ${price}</p>
                    ${canCancel ? `
                        <button id="cancelBookingBtn" class="btn-cancel-full">
                            Cancel Booking
                        </button>
                    ` : ""}
                    <a href="service-details.html?id=${__service.id}" class="btn-secondary-full">
                        View Service
                    </a>
                </div>
            </div>

        </div>
    `;

    const cancelBtn = document.getElementById("cancelBookingBtn");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", handleCancel);
    }

    const reviewForm = document.getElementById("reviewForm");
    if (reviewForm) {
        reviewForm.addEventListener("submit", handleReviewSubmit);
        initializeStarPicker();
    }

}

function renderReviewSection() {

    if (__existingReview) {
        return `
            <h3>Your Review</h3>
            <div class="review-display">
                <div class="stars">${"★".repeat(__existingReview.rating)}${"☆".repeat(5 - __existingReview.rating)}</div>
                ${__existingReview.comment ? `<p>${escapeHtml(__existingReview.comment)}</p>` : ""}
            </div>
        `;
    }

    return `
        <h3>Leave a Review</h3>
        <form id="reviewForm" class="review-form">
            <div class="star-picker" id="starPicker">
                ${[1,2,3,4,5].map(n => `<i class="bi bi-star" data-value="${n}"></i>`).join("")}
            </div>
            <input type="hidden" id="ratingInput" value="0">
            <textarea id="reviewComment" rows="3" placeholder="How was your experience? (optional)"></textarea>
            <div id="reviewFormError" class="form-error" style="display:none;"></div>
            <div id="reviewFormSuccess" class="form-success" style="display:none;"></div>
            <button type="submit" class="btn-primary-full">Submit Review</button>
        </form>
    `;

}

function initializeStarPicker() {

    const picker = document.getElementById("starPicker");
    const ratingInput = document.getElementById("ratingInput");

    if (!picker) return;

    picker.querySelectorAll("i").forEach(star => {
        star.addEventListener("click", () => {
            const value = parseInt(star.dataset.value, 10);
            ratingInput.value = value;
            picker.querySelectorAll("i").forEach(s => {
                s.classList.toggle("bi-star-fill", parseInt(s.dataset.value, 10) <= value);
                s.classList.toggle("bi-star", parseInt(s.dataset.value, 10) > value);
            });
        });
    });

}

async function handleReviewSubmit(event) {

    event.preventDefault();

    const errorEl = document.getElementById("reviewFormError");
    const successEl = document.getElementById("reviewFormSuccess");
    const rating = parseInt(document.getElementById("ratingInput").value, 10);
    const comment = document.getElementById("reviewComment").value.trim();

    errorEl.style.display = "none";
    successEl.style.display = "none";

    if (!rating) {
        errorEl.textContent = "Please select a star rating.";
        errorEl.style.display = "block";
        return;
    }

    try {

        await ApiClient.post("/reviews/", {
            booking_id: __booking.id,
            rating,
            comment: comment || null,
        });

        successEl.textContent = "Thank you for your review!";
        successEl.style.display = "block";

        setTimeout(() => window.location.reload(), 1000);

    } catch (error) {
        errorEl.textContent = error.message || "Failed to submit review.";
        errorEl.style.display = "block";
    }

}

async function handleCancel() {

    const confirmed = confirm("Are you sure you want to cancel this booking?");

    if (!confirmed) return;

    try {
        await ApiClient.patch(`/bookings/${__booking.id}/status`, { status: "CANCELLED" });
        window.location.reload();
    } catch (error) {
        alert(error.message || "Failed to cancel booking.");
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

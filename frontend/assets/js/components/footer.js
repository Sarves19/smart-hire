/**
 * ==========================================================
 * Smart Hire Footer
 * ==========================================================
 */

document.addEventListener("components:loaded", () => {

    const yearEl = document.getElementById("footerYear");

    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

});

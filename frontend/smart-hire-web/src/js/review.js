/**
 * Star rating input — ported from customer-hifi-2.jsx CustReview.
 * Each [data-star-input] is a row of star buttons; clicking one sets the
 * rating to its value and fills every star up to that point.
 */
(function () {
  "use strict";

  const RATING_LABEL = { 5: "Excellent", 4: "Great", 3: "Good", 2: "Fair", 1: "Poor" };

  function paint(widget, value) {
    widget.querySelectorAll(".star-btn").forEach((btn) => {
      const v = Number(btn.getAttribute("data-value"));
      btn.querySelector("svg").style.fill = v <= value ? "var(--brand)" : "var(--line2)";
    });
    widget.setAttribute("data-value", value);

    const labelSelector = widget.getAttribute("data-label-target");
    if (labelSelector) {
      const labelEl = document.querySelector(labelSelector);
      if (labelEl) labelEl.textContent = `${RATING_LABEL[value] || ""} · ${value.toFixed(1)}`;
    }

    const input = widget.parentElement.querySelector('input[type="hidden"]');
    if (input) input.value = value;
  }

  function initStarInputs(root) {
    root.querySelectorAll("[data-star-input]").forEach((widget) => {
      widget.addEventListener("click", (e) => {
        const btn = e.target.closest(".star-btn");
        if (!btn) return;
        paint(widget, Number(btn.getAttribute("data-value")));
      });
      paint(widget, Number(widget.getAttribute("data-value")) || 0);
    });
  }

  document.addEventListener("DOMContentLoaded", () => initStarInputs(document));
})();

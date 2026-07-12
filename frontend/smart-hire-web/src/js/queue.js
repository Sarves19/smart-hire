/**
 * Generic actionable-queue behavior shared by provider requests
 * (accept/decline), admin provider verification (approve/reject) and admin
 * moderation (dismiss/warn/suspend/remove) — any click on a
 * [data-queue-remove] button inside a [data-queue-card] removes that card
 * from its [data-queue-list] and keeps the count badge in sync.
 */
(function () {
  "use strict";

  function updateCount(list) {
    const remaining = list.querySelectorAll("[data-queue-card]").length;
    document.querySelectorAll("[data-queue-count]").forEach((el) => (el.textContent = remaining));
    const empty = list.querySelector("[data-queue-empty]") || list.parentElement.querySelector("[data-queue-empty]");
    if (empty) empty.hidden = remaining !== 0;
  }

  function removeCard(card, list) {
    card.style.transition = "opacity .18s, transform .18s";
    card.style.opacity = "0";
    card.style.transform = "translateX(8px)";
    setTimeout(() => {
      card.remove();
      updateCount(list);
    }, 160);
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-queue-list]").forEach((list) => {
      list.addEventListener("click", (e) => {
        const btn = e.target.closest("[data-queue-remove]");
        if (!btn) return;
        const card = btn.closest("[data-queue-card]");
        if (card) removeCard(card, list);
      });
    });
  });
})();

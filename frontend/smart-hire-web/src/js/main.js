/**
 * Smart Hire — shared page behavior.
 * Loaded on every page. Feature modules for a single screen (auth, booking,
 * review) live in their own files and are included only where needed.
 */
(function () {
  "use strict";

  /* Chip groups: [data-chip-group="single"] → radio-like, only one .on at a time.
     [data-chip-group="multi"] → checkbox-like, each chip toggles independently. */
  function initChipGroups(root) {
    root.querySelectorAll("[data-chip-group]").forEach((group) => {
      const mode = group.getAttribute("data-chip-group");
      group.addEventListener("click", (e) => {
        const chip = e.target.closest(".chip");
        if (!chip || !group.contains(chip)) return;
        if (mode === "single") {
          group.querySelectorAll(".chip").forEach((c) => c.classList.remove("on"));
          chip.classList.add("on");
        } else {
          chip.classList.toggle("on");
        }
      });
    });
  }

  /* Generic icon-button toggle, e.g. the heart/save button on provider cards. */
  function initToggleButtons(root) {
    root.querySelectorAll("[data-toggle-active]").forEach((btn) => {
      btn.addEventListener("click", () => btn.classList.toggle("is-active"));
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initChipGroups(document);
    initToggleButtons(document);
  });
})();

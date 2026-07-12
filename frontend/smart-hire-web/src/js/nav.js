/**
 * Responsive navigation chrome: the customer top-nav's hamburger panel and
 * the provider/admin sidebar's off-canvas drawer. Both follow the same
 * open/close pattern via a `data-open` attribute so the CSS in
 * _responsive.scss can key off it.
 */
(function () {
  "use strict";

  function wireToggle(toggleSelector, panelSelector, backdropSelector) {
    const toggle = document.querySelector(toggleSelector);
    const panel = document.querySelector(panelSelector);
    if (!toggle || !panel) return;
    const backdrop = backdropSelector ? document.querySelector(backdropSelector) : null;

    function setOpen(open) {
      if (open) {
        panel.setAttribute("data-open", "");
        if (backdrop) backdrop.setAttribute("data-open", "");
      } else {
        panel.removeAttribute("data-open");
        if (backdrop) backdrop.removeAttribute("data-open");
      }
      toggle.setAttribute("aria-expanded", String(open));
    }

    toggle.addEventListener("click", () => setOpen(!panel.hasAttribute("data-open")));
    if (backdrop) backdrop.addEventListener("click", () => setOpen(false));
    panel.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setOpen(false)));
  }

  document.addEventListener("DOMContentLoaded", () => {
    wireToggle("[data-nav-toggle]", "[data-nav-panel]");
    wireToggle("[data-menu-toggle]", "[data-sidebar]", "[data-sidebar-backdrop]");
  });
})();

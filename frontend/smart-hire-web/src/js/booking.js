/**
 * Booking flow — 3-step stepper (When → Details → Confirm), ported from
 * customer-hifi-2.jsx CustBooking. The mockup only ever showed step 1;
 * this wires up real step navigation plus a live-updating summary rail.
 */
(function () {
  "use strict";

  const MONTH = "June 2026";
  const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  // June 1 2026 is a Monday, used only to derive a friendly weekday label for the demo calendar.
  const JUNE_1_WEEKDAY = 1;

  function dayLabel(day) {
    const weekday = WEEKDAYS[(JUNE_1_WEEKDAY + (day - 1)) % 7];
    return `${weekday} ${day} June`;
  }

  function initStepper(root) {
    const stepper = root.querySelector("[data-stepper]");
    if (!stepper) return;

    const items = stepper.querySelectorAll("[data-step-item]");
    const panels = root.querySelectorAll("[data-step-panel]");

    function goToStep(step) {
      items.forEach((item) => {
        const n = Number(item.getAttribute("data-step-item"));
        item.classList.toggle("on", n === step);
        item.classList.toggle("done", n < step);
      });
      panels.forEach((panel) => {
        panel.hidden = Number(panel.getAttribute("data-step-panel")) !== step;
      });
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    root.querySelectorAll("[data-step-next]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const current = root.querySelector('[data-step-panel]:not([hidden])');
        const step = Number(current.getAttribute("data-step-panel"));
        goToStep(step + 1);
      });
    });
    root.querySelectorAll("[data-step-back]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const current = root.querySelector('[data-step-panel]:not([hidden])');
        const step = Number(current.getAttribute("data-step-panel"));
        goToStep(step - 1);
      });
    });
  }

  function updateSummaryDate(day) {
    const label = dayLabel(day);
    document.querySelectorAll("[data-summary-date]").forEach((el) => (el.textContent = label));
    document.querySelectorAll("[data-summary-date-label]").forEach((el) => (el.textContent = label));
  }

  function updateSummaryTime(time) {
    document.querySelectorAll("[data-summary-time]").forEach((el) => (el.textContent = time));
  }

  function initCalendar(root) {
    const calendar = root.querySelector("[data-calendar]");
    if (!calendar) return;
    calendar.addEventListener("click", (e) => {
      const day = e.target.closest(".cal-day");
      if (!day || day.classList.contains("disabled")) return;
      calendar.querySelectorAll(".cal-day.selected").forEach((d) => d.classList.remove("selected"));
      day.classList.add("selected");
      updateSummaryDate(Number(day.getAttribute("data-day")));
    });
  }

  function initTimeChips(root) {
    const group = root.querySelector("[data-time-group]");
    if (!group) return;
    group.addEventListener("click", (e) => {
      const chip = e.target.closest(".chip");
      if (!chip) return;
      updateSummaryTime(chip.getAttribute("data-time"));
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const page = document;
    initStepper(page);
    initCalendar(page);
    initTimeChips(page);
  });
})();

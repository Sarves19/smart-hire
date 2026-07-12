/**
 * Auth screen — role-aware login/register (ported from auth-hifi.jsx).
 * One screen serves all three roles; switching mode/role never navigates.
 */
(function () {
  "use strict";

  const DEMO = {
    customer: { name: "Anya Roberts", email: "anya.roberts@email.com" },
    provider: { name: "Ravi Patel", email: "ravi.patel@email.com" },
    admin: { name: "Operations user", email: "you@smarthire.app" },
  };

  function initAuth(root) {
    root.querySelectorAll("[data-auth-root]").forEach((wrap) => {
      const modeTabs = wrap.querySelectorAll("[data-mode-tab]");
      const modePanels = wrap.querySelectorAll("[data-mode-panel]");
      const roleTabs = wrap.querySelectorAll("[data-role-tab]");
      const rolePanels = wrap.querySelectorAll("[data-role-panel]");
      const roleOnly = wrap.querySelectorAll("[data-role-only]");

      function setMode(mode) {
        wrap.setAttribute("data-mode", mode);
        modeTabs.forEach((t) => t.classList.toggle("on", t.getAttribute("data-mode-tab") === mode));
        modePanels.forEach((p) => {
          p.style.display = p.getAttribute("data-mode-panel") === mode ? "" : "none";
        });
        if (history.replaceState) {
          const url = mode === "register" ? "/auth/register.html" : "/auth/login.html";
          history.replaceState(null, "", url);
        }
      }

      function setRole(role) {
        wrap.setAttribute("data-role", role);
        roleTabs.forEach((t) => t.classList.toggle("on", t.getAttribute("data-role-tab") === role));
        rolePanels.forEach((p) => {
          p.style.display = p.getAttribute("data-role-panel") === role ? "" : "none";
        });
        roleOnly.forEach((el) => {
          el.style.display = el.getAttribute("data-role-only") === role ? "" : "none";
        });
        wrap.querySelectorAll("[data-role-input]").forEach((el) => { el.value = role; });

        const demo = DEMO[role] || DEMO.customer;
        const loginEmail = wrap.querySelector("#login-email");
        const regName = wrap.querySelector("#register-name");
        const regEmail = wrap.querySelector("#register-email");
        if (loginEmail) loginEmail.placeholder = demo.email;
        if (regName) regName.placeholder = demo.name;
        if (regEmail) regEmail.placeholder = demo.email;

        const submitBtn = wrap.querySelector(".js-register-submit");
        if (submitBtn) submitBtn.textContent = role === "provider" ? "Submit application" : "Create account";
      }

      modeTabs.forEach((tab) => tab.addEventListener("click", () => setMode(tab.getAttribute("data-mode-tab"))));
      roleTabs.forEach((tab) => tab.addEventListener("click", () => setRole(tab.getAttribute("data-role-tab"))));

      setMode(wrap.getAttribute("data-mode") || "login");
      setRole(wrap.getAttribute("data-role") || "customer");
    });
  }

  document.addEventListener("DOMContentLoaded", () => initAuth(document));
})();

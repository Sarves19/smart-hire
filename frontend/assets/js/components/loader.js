/**
 * ==========================================================
 * Smart Hire Component Loader
 * ==========================================================
 * Injects shared HTML fragments (sidebar, navbar, footer)
 * into their containers, then fires "components:loaded" so
 * dependent scripts (navbar.js, sidebar.js) know it's safe
 * to query the DOM for elements like #navbarUserName.
 *
 * Usage: give any container a data-component attribute
 * pointing at the fragment to load, e.g.
 *   <aside id="sidebar-container" data-component="../../components/sidebar.html"></aside>
 */

document.addEventListener("DOMContentLoaded", () => {
    showPageLoader();
    initComponents();
});

async function initComponents() {

    const targets = Array.from(
        document.querySelectorAll("[data-component]")
    );

    await Promise.all(targets.map(loadComponent));

    document.dispatchEvent(new CustomEvent("components:loaded"));

    hidePageLoader();
}

async function loadComponent(el) {

    const url = el.getAttribute("data-component");

    if (!url) return;

    try {

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Failed to load component: ${url}`);
        }

        el.innerHTML = await response.text();

    } catch (error) {

        console.error(error);

    }

}

/**
 * Full-page loading spinner shown while components + first
 * page data are loading.
 */
function showPageLoader() {

    const container = document.getElementById("loader-container");

    if (!container) return;

    container.innerHTML = `
        <div class="page-loader-overlay">
            <div class="page-loader-spinner"></div>
        </div>
    `;

}

function hidePageLoader() {

    const container = document.getElementById("loader-container");

    if (!container) return;

    const overlay = container.querySelector(".page-loader-overlay");

    if (!overlay) return;

    overlay.classList.add("page-loader-hidden");

    setTimeout(() => {
        container.innerHTML = "";
    }, 300);

}

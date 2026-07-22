/**
 * ==========================================================
 * Smart Hire Sidebar
 * ==========================================================
 */

document.addEventListener("components:loaded", () => {

    loadSidebarUser();

    setActiveMenu();

    initializeLogout();

});

/**
 * Logout Button
 */

function initializeLogout() {

    const logoutBtn = document.getElementById("logoutBtn");

    if (!logoutBtn) return;

    logoutBtn.addEventListener("click", (event) => {

        event.preventDefault();

        const confirmed = confirm("Are you sure you want to logout?");

        if (!confirmed) return;

        AuthService.logout();

        window.location.href = "../auth/login.html";

    });

}

/**
 * ==========================================================
 * Load Sidebar User
 * ==========================================================
 */

async function loadSidebarUser() {

    const user = await AuthService.getCurrentUser();

    if (!user) return;

    setSidebarUser(user);

}

/**
 * ==========================================================
 * Set Sidebar User
 * ==========================================================
 */

function setSidebarUser(user) {

    const avatar = document.getElementById("sidebarAvatar");
    const userName = document.getElementById("sidebarUserName");
    const userRole = document.getElementById("sidebarUserRole");

    if (!avatar || !userName || !userRole) return;

    userName.textContent = user.full_name;

    userRole.textContent =
        user.role.charAt(0) + user.role.slice(1).toLowerCase();

    if (user.profile_image) {
        const image = document.createElement("img");
        image.src = user.profile_image;
        image.alt = "Profile";
        avatar.replaceChildren(image);
    } else {
        avatar.textContent = getInitials(user.full_name);
    }

}

/**
 * ==========================================================
 * Active Sidebar Menu
 * ==========================================================
 */

function setActiveMenu() {

    const currentPage = window.location.pathname
        .split("/")
        .pop()
        .replace(".html", "");

    const links = document.querySelectorAll(".sidebar-link[data-page]");

    links.forEach(link => {

        link.classList.remove("active");

        if (link.dataset.page === currentPage) {
            link.classList.add("active");
        }

    });

}

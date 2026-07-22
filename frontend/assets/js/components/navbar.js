/**
 * ==========================================================
 * Smart Hire Navbar
 * ==========================================================
 */

document.addEventListener("components:loaded", () => {

    loadNavbarUser();

    initializeNavbar();

});

/**
 * Load Navbar User
 */

async function loadNavbarUser() {

    const user = await AuthService.getCurrentUser();

    if (!user) return;

    setNavbarUser(user);

}

/**
 * Set Navbar User
 */

function setNavbarUser(user) {

    const nameEl = document.getElementById("navbarUserName");
    const roleEl = document.getElementById("navbarUserRole");
    const avatarEl = document.getElementById("navbarAvatar");

    if (nameEl) nameEl.textContent = user.full_name;

    if (roleEl) {
        roleEl.textContent =
            user.role.charAt(0) + user.role.slice(1).toLowerCase();
    }

    if (avatarEl) {

        if (user.profile_image) {
            const image = document.createElement("img");
            image.src = user.profile_image;
            image.alt = "Profile";
            avatarEl.replaceChildren(image);
        } else {
            avatarEl.textContent = getInitials(user.full_name);
        }

    }

}

/**
 * ==========================================================
 * Navbar Events
 * ==========================================================
 */

function initializeNavbar() {

    const navbarUser = document.getElementById("navbarUser");
    const navbarDropdown = document.getElementById("navbarDropdown");

    if (navbarUser && navbarDropdown) {

        navbarUser.addEventListener("click", (event) => {
            event.stopPropagation();
            navbarDropdown.classList.toggle("active");
        });

        document.addEventListener("click", () => {
            navbarDropdown.classList.remove("active");
        });

    }

    const logoutBtn = document.getElementById("navbarLogoutBtn");

    if (logoutBtn) {

        logoutBtn.addEventListener("click", (event) => {

            event.preventDefault();

            const confirmed = confirm("Are you sure you want to logout?");

            if (!confirmed) return;

            AuthService.logout();

            window.location.href = "../auth/login.html";

        });

    }

}

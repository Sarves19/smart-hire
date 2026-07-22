/**
 * ==========================================================
 * SMART HIRE - MY PROFILE
 * ==========================================================
 */

document.addEventListener("components:loaded", initializeProfilePage);

async function initializeProfilePage() {

    if (!AuthService.requireAuth()) return;

    await loadUserData();

    document.getElementById("accountForm")
        .addEventListener("submit", handleAccountSubmit);

    document.getElementById("addressForm")
        .addEventListener("submit", handleAddressSubmit);

    document.getElementById("profileImageForm")
        .addEventListener("submit", handleImageSubmit);

    document.getElementById("passwordForm")
        .addEventListener("submit", handlePasswordSubmit);

}

/**
 * ==========================================================
 * Load Data
 * ==========================================================
 */

async function loadUserData() {

    try {

        const user = await ApiClient.get("/users/me");

        document.getElementById("firstName").value = user.first_name;
        document.getElementById("lastName").value = user.last_name;
        document.getElementById("email").value = user.email;
        document.getElementById("phoneNumber").value = user.phone_number;
        setImagePreview(null, `${user.first_name} ${user.last_name}`);

    } catch (error) {
        console.error("Failed to load user:", error);
    }

    try {

        const profile = await ApiClient.get("/customer/profile");

        document.getElementById("address").value = profile.address || "";
        document.getElementById("city").value = profile.city || "";
        document.getElementById("district").value = profile.district || "";
        setImagePreview(profile.profile_image);

    } catch (error) {
        // No profile created yet - that's fine, form just stays empty
        // and the first save will create it.
    }

}

function setImagePreview(imageUrl, fullName = "") {
    const preview = document.getElementById("profileImagePreview");
    if (!preview) return;
    preview.replaceChildren();
    if (imageUrl) {
        const image = document.createElement("img");
        image.src = imageUrl.startsWith("/") ? `${ApiClient.BASE_URL.replace("/api/v1", "")}${imageUrl}` : imageUrl;
        image.alt = "Profile photo";
        preview.append(image);
    } else {
        preview.textContent = fullName.split(" ").filter(Boolean).map(part => part[0]).join("").slice(0, 2).toUpperCase() || "?";
    }
}

async function handleImageSubmit(event) {
    event.preventDefault();
    const input = document.getElementById("profileImage");
    const errorEl = document.getElementById("imageFormError");
    const successEl = document.getElementById("imageFormSuccess");
    errorEl.hidden = true;
    successEl.hidden = true;
    const file = input.files[0];
    if (!file || file.size > 5 * 1024 * 1024 || !["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
        errorEl.textContent = "Choose a JPEG, PNG, or WebP image under 5 MB.";
        errorEl.hidden = false;
        return;
    }
    try {
        const formData = new FormData();
        formData.append("image", file);
        const profile = await ApiClient.upload("/customer/profile/image", formData);
        setImagePreview(profile.profile_image);
        AuthService._cachedUser = null;
        successEl.textContent = "Profile photo updated.";
        successEl.hidden = false;
        input.value = "";
    } catch (error) {
        errorEl.textContent = error.message || "Failed to upload photo.";
        errorEl.hidden = false;
    }
}

async function handlePasswordSubmit(event) {
    event.preventDefault();
    const errorEl = document.getElementById("passwordFormError");
    const successEl = document.getElementById("passwordFormSuccess");
    errorEl.hidden = true;
    successEl.hidden = true;
    const current_password = document.getElementById("currentPassword").value;
    const new_password = document.getElementById("newPassword").value;
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$/.test(new_password)) {
        errorEl.textContent = "Your new password does not meet the stated requirements.";
        errorEl.hidden = false;
        return;
    }
    try {
        await ApiClient.post("/users/me/change-password", { current_password, new_password });
        event.currentTarget.reset();
        successEl.textContent = "Password changed successfully.";
        successEl.hidden = false;
    } catch (error) {
        errorEl.textContent = error.message || "Failed to change password.";
        errorEl.hidden = false;
    }
}

/**
 * ==========================================================
 * Account Form
 * ==========================================================
 */

async function handleAccountSubmit(event) {

    event.preventDefault();

    const errorEl = document.getElementById("accountFormError");
    const successEl = document.getElementById("accountFormSuccess");

    errorEl.style.display = "none";
    successEl.style.display = "none";

    const payload = {
        first_name: document.getElementById("firstName").value.trim(),
        last_name: document.getElementById("lastName").value.trim(),
        phone_number: document.getElementById("phoneNumber").value.trim(),
    };

    try {

        const updated = await ApiClient.put("/users/me", payload);

        // Refresh the cached user so the navbar/sidebar name
        // updates immediately without a full reload.
        AuthService.setCurrentUser({
            ...(await AuthService.getCurrentUser()),
            first_name: updated.first_name,
            last_name: updated.last_name,
            full_name: `${updated.first_name} ${updated.last_name}`.trim(),
            phone_number: updated.phone_number,
        });

        document.querySelectorAll("#navbarUserName, #sidebarUserName").forEach(el => {
            el.textContent = `${updated.first_name} ${updated.last_name}`;
        });

        successEl.textContent = "Account details saved.";
        successEl.style.display = "block";

    } catch (error) {
        errorEl.textContent = error.message || "Failed to save account details.";
        errorEl.style.display = "block";
    }

}

/**
 * ==========================================================
 * Address Form
 * ==========================================================
 */

async function handleAddressSubmit(event) {

    event.preventDefault();

    const errorEl = document.getElementById("addressFormError");
    const successEl = document.getElementById("addressFormSuccess");

    errorEl.style.display = "none";
    successEl.style.display = "none";

    const payload = {
        address: document.getElementById("address").value.trim() || null,
        city: document.getElementById("city").value.trim() || null,
        district: document.getElementById("district").value.trim() || null,
    };

    try {

        // Try update first; if no profile exists yet, create one.
        try {
            await ApiClient.put("/customer/profile", payload);
        } catch (error) {
            if (error.status === 404 || error.status === 400) {
                await ApiClient.post("/customer/profile", payload);
            } else {
                throw error;
            }
        }

        successEl.textContent = "Address saved.";
        successEl.style.display = "block";

    } catch (error) {
        errorEl.textContent = error.message || "Failed to save address.";
        errorEl.style.display = "block";
    }

}

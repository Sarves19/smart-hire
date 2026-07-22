/**
 * ==========================================================
 * Smart Hire Auth Service
 * ==========================================================
 * Real implementation backed by ApiClient / GET /users/me.
 * Keeps the same public shape (getCurrentUser, logout) that
 * navbar.js / sidebar.js already call, but getCurrentUser is
 * now async since it may need to fetch the profile.
 */

const AuthService = {

    _cachedUser: null,

    /**
     * Get Current User
     * Returns a promise resolving to:
     * { id, full_name, first_name, last_name, email, role, profile_image }
     * or null if not authenticated / request failed.
     */
    async getCurrentUser(forceRefresh = false) {

        if (this._cachedUser && !forceRefresh) {
            return this._cachedUser;
        }

        if (!ApiClient.isAuthenticated()) {
            return null;
        }

        try {
            const user = await ApiClient.get("/users/me");

            const normalized = {
                id: user.id,
                first_name: user.first_name,
                last_name: user.last_name,
                full_name: `${user.first_name} ${user.last_name}`.trim(),
                email: user.email,
                phone_number: user.phone_number,
                role: user.role,
                is_verified: user.is_verified,
                profile_image: null,
            };

            // Customers additionally have a profile_image on their
            // customer profile; fetch it best-effort, ignore failure
            // (e.g. profile not created yet).
            if (user.role === "CUSTOMER") {
                try {
                    const profile = await ApiClient.get("/customer/profile");
                    normalized.profile_image = profile.profile_image
                        ? `${ApiClient.BASE_URL.replace("/api/v1", "")}${profile.profile_image}`
                        : null;
                } catch (e) {
                    // No profile yet - not an error for display purposes.
                }
            }

            this._cachedUser = normalized;
            return normalized;

        } catch (error) {
            console.error("Failed to load current user:", error);
            return null;
        }
    },

    /**
     * Set Current User (used right after login to seed the cache
     * without an extra round trip, if the caller already has it)
     */
    setCurrentUser(user) {
        this._cachedUser = user;
    },

    /**
     * Require Authentication
     * Call at the top of any protected page. Redirects to login
     * immediately if there is no access token.
     */
    requireAuth() {
        if (!ApiClient.isAuthenticated()) {
            ApiClient.redirectToLogin();
            return false;
        }
        return true;
    },

    /**
     * Require a specific role (e.g. "CUSTOMER"). Must be awaited.
     * Redirects to login if unauthenticated; alerts + redirects
     * to dashboard if authenticated but wrong role.
     */
    async requireRole(role) {
        if (!this.requireAuth()) return false;

        const user = await this.getCurrentUser();

        if (!user || user.role !== role) {
            window.location.href = "../auth/login.html";
            return false;
        }

        return true;
    },

    /**
     * Logout
     */
    logout() {
        this._cachedUser = null;
        ApiClient.clearTokens();
    }

};

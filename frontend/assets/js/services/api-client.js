/**
 * ==========================================================
 * Smart Hire API Client
 * ==========================================================
 * Single shared client used by every page. Reads/writes the
 * exact same storage keys that login.js already uses
 * (access_token, refresh_token, token_type) so a session
 * started on the login page keeps working everywhere else.
 */

const ApiClient = (() => {

    const BASE_URL = "http://127.0.0.1:8000/api/v1";

    // A single in-flight refresh promise so parallel 401s
    // don't each try to refresh the token separately.
    let refreshPromise = null;

    /* =========================================================
       TOKEN STORAGE
       (mirrors login.js: uses localStorage if "remember me"
       was checked, sessionStorage otherwise)
    ========================================================= */

    function getAccessToken() {
        return (
            localStorage.getItem("access_token") ||
            sessionStorage.getItem("access_token") ||
            null
        );
    }

    function getRefreshToken() {
        return (
            localStorage.getItem("refresh_token") ||
            sessionStorage.getItem("refresh_token") ||
            null
        );
    }

    function getTokenType() {
        return (
            localStorage.getItem("token_type") ||
            sessionStorage.getItem("token_type") ||
            "bearer"
        );
    }

    function isAuthenticated() {
        return !!getAccessToken();
    }

    function setAccessToken(token) {
        // Write the new access token back into whichever
        // storage currently holds the session.
        if (localStorage.getItem("access_token")) {
            localStorage.setItem("access_token", token);
        } else {
            sessionStorage.setItem("access_token", token);
        }
    }

    function clearTokens() {
        ["access_token", "refresh_token", "token_type"].forEach(key => {
            localStorage.removeItem(key);
            sessionStorage.removeItem(key);
        });
        sessionStorage.removeItem("smarthire_user");
        localStorage.removeItem("smarthire_user");
    }

    /* =========================================================
       REDIRECT TO LOGIN
       Works out how many "../" segments are needed based on
       how deep the current page is under /frontend/pages/.
    ========================================================= */

    function redirectToLogin() {
        clearTokens();

        const path = window.location.pathname;
        const marker = "/pages/";
        const idx = path.indexOf(marker);

        if (idx === -1) {
            window.location.href = "pages/auth/login.html";
            return;
        }

        const afterPages = path.substring(idx + marker.length);
        const depth = afterPages.split("/").length - 1; // segments after /pages/
        const prefix = "../".repeat(Math.max(depth, 0));

        window.location.href = `${prefix}auth/login.html`;
    }

    /* =========================================================
       TOKEN REFRESH
    ========================================================= */

    async function refreshAccessToken() {

        if (refreshPromise) return refreshPromise;

        const refreshToken = getRefreshToken();

        if (!refreshToken) {
            return Promise.reject(new Error("No refresh token available."));
        }

        refreshPromise = fetch(`${BASE_URL}/auth/refresh`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refreshToken }),
        })
            .then(async (res) => {
                if (!res.ok) throw new Error("Refresh failed.");
                const data = await res.json();
                setAccessToken(data.access_token);
                return data.access_token;
            })
            .finally(() => {
                refreshPromise = null;
            });

        return refreshPromise;
    }

    /* =========================================================
       CORE REQUEST
    ========================================================= */

    async function request(method, path, body, { auth = true, retry = true } = {}) {

        const headers = { "Content-Type": "application/json" };

        if (auth) {
            const token = getAccessToken();
            if (token) {
                headers["Authorization"] = `${getTokenType()} ${token}`;
            }
        }

        const res = await fetch(`${BASE_URL}${path}`, {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });

        // Token expired -> try one silent refresh, then retry once.
        if (res.status === 401 && auth && retry && getRefreshToken()) {
            try {
                await refreshAccessToken();
                return request(method, path, body, { auth, retry: false });
            } catch (e) {
                redirectToLogin();
                throw new Error("Session expired. Please log in again.");
            }
        }

        if (res.status === 204) return null;

        let data = null;
        try {
            data = await res.json();
        } catch (e) {
            data = null;
        }

        if (!res.ok) {
            const message =
                (data && (data.detail || data.message)) ||
                `Request failed with status ${res.status}.`;
            const error = new Error(message);
            error.status = res.status;
            error.data = data;
            throw error;
        }

        return data;
    }

    async function upload(path, formData, { auth = true } = {}) {
        const headers = {};
        if (auth) {
            const token = getAccessToken();
            if (token) headers.Authorization = `${getTokenType()} ${token}`;
        }
        const res = await fetch(`${BASE_URL}${path}`, { method: "POST", headers, body: formData });
        const data = await res.json().catch(() => null);
        if (!res.ok) {
            const error = new Error((data && (data.detail || data.message)) || "Upload failed.");
            error.status = res.status;
            throw error;
        }
        return data;
    }

    return {
        BASE_URL,
        get: (path, opts) => request("GET", path, undefined, opts),
        post: (path, body, opts) => request("POST", path, body, opts),
        put: (path, body, opts) => request("PUT", path, body, opts),
        patch: (path, body, opts) => request("PATCH", path, body, opts),
        delete: (path, opts) => request("DELETE", path, undefined, opts),
        upload,
        getAccessToken,
        getRefreshToken,
        isAuthenticated,
        clearTokens,
        redirectToLogin,
    };

})();

/*
==========================================================
Smart Hire
Authentication Module

Description:
Handles authentication, JWT token management,
route protection, authorization headers,
session management, and user authentication.

Author: Smart Hire Team
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    "use strict";

    /*=========================================================
      BACKEND CONFIGURATION
    =========================================================*/

    // FastAPI Base URL
    const API_BASE_URL =
        "http://127.0.0.1:8000/api/v1";

    /*=========================================================
      AUTHENTICATION ENDPOINTS
    =========================================================*/

    // Login Endpoint
    const LOGIN_API =
        `${API_BASE_URL}/auth/login`;

    // Register Endpoint
    const REGISTER_API =
        `${API_BASE_URL}/auth/register`;

    // Refresh Access Token
    const REFRESH_API =
        `${API_BASE_URL}/auth/refresh`;

    // Current Logged-in User
    const CURRENT_USER_API =
        `${API_BASE_URL}/users/me`;

    // Logout Endpoint (Optional)
    const LOGOUT_API =
        `${API_BASE_URL}/auth/logout`;

    /*=========================================================
      TOKEN STORAGE KEYS
    =========================================================*/

    const ACCESS_TOKEN_KEY =
        "access_token";

    const REFRESH_TOKEN_KEY =
        "refresh_token";

    const TOKEN_TYPE_KEY =
        "token_type";

    const REMEMBER_ME_KEY =
        "rememberedEmail";

    /*=========================================================
      JWT TOKEN MANAGEMENT
    =========================================================*/

    /**
     * Save Authentication Tokens
     * Stores tokens in Local Storage.
     */
    function saveTokens(data) {

        if (!data) return;

        localStorage.setItem(
            ACCESS_TOKEN_KEY,
            data.access_token
        );

        localStorage.setItem(
            REFRESH_TOKEN_KEY,
            data.refresh_token
        );

        localStorage.setItem(
            TOKEN_TYPE_KEY,
            data.token_type || "bearer"
        );

    }

    /**
     * Get Access Token
     */
    function getAccessToken() {

        return localStorage.getItem(
            ACCESS_TOKEN_KEY
        );

    }

    /**
     * Get Refresh Token
     */
    function getRefreshToken() {

        return localStorage.getItem(
            REFRESH_TOKEN_KEY
        );

    }

    /**
     * Get Token Type
     */
    function getTokenType() {

        return (
            localStorage.getItem(
                TOKEN_TYPE_KEY
            ) || "bearer"
        );

    }

    /**
     * Check Authentication Status
     */
    function isAuthenticated() {

        return !!getAccessToken();

    }

    /**
     * Remove Stored Tokens
     */
    function clearTokens() {

        localStorage.removeItem(
            ACCESS_TOKEN_KEY
        );

        localStorage.removeItem(
            REFRESH_TOKEN_KEY
        );

        localStorage.removeItem(
            TOKEN_TYPE_KEY
        );

    }

    /**
     * Generate Authorization Header
     */
    function getAuthorizationHeader() {

        const token =
            getAccessToken();

        if (!token) return null;

        return `${getTokenType()} ${token}`;

    }

    /**
     * Get Auth Headers
     */
    function getAuthHeaders() {

        const authorization =
            getAuthorizationHeader();

        const headers = {

            "Content-Type":
                "application/json"

        };

        if (authorization) {

            headers.Authorization =
                authorization;

        }

        return headers;

    }
    /*=========================================================
      AUTHENTICATION & ROUTE PROTECTION
    =========================================================*/

    /**
     * Require Authentication
     * Redirect unauthenticated users to login page.
     */
    function requireAuthentication() {

        if (isAuthenticated()) return;

        console.warn(
            "Authentication required. Redirecting to login page."
        );

        window.location.href =
            "login.html";

    }

    /**
     * Redirect Authenticated Users
     * Prevent logged-in users from accessing
     * login or register pages.
     */
    function redirectIfAuthenticated() {

        if (!isAuthenticated()) return;

        console.info(
            "User already authenticated. Redirecting to dashboard."
        );

        window.location.href =
            "dashboard.html";

    }

    /**
     * Check Current Authentication Status
     */
    function checkAuthentication() {

        return {

            authenticated:
                isAuthenticated(),

            accessToken:
                getAccessToken(),

            refreshToken:
                getRefreshToken(),

            tokenType:
                getTokenType()

        };

    }

    /**
     * Get Current User ID
     * (Future Implementation)
     */
    function getCurrentUserId() {

        /*
        Future Enhancement

        Decode the JWT Access Token
        and extract the user's ID.

        Example:

        {
            "sub": "15",
            "email": "user@example.com",
            "role": "customer",
            "exp": 1785632148
        }

        return payload.sub;
        */

        return null;

    }
    /*=========================================================
      LOGOUT & SESSION MANAGEMENT
    =========================================================*/

    /**
     * Logout User
     * Clears authentication data and
     * redirects to the login page.
     */
    function logout() {

        console.info(
            "Logging out user..."
        );

        clearTokens();

        window.location.href =
            "login.html";

    }

    /**
     * Session Expired
     * Clears tokens and forces the user
     * to log in again.
     */
    function handleSessionExpired() {

        console.warn(
            "Session expired."
        );

        clearTokens();

        alert(
            "Your session has expired. Please log in again."
        );

        window.location.href =
            "login.html";

    }

    /**
     * Handle Unauthorized Response
     * Used whenever the backend returns
     * HTTP 401 Unauthorized.
     */
    function handleUnauthorized() {

        console.warn(
            "Unauthorized request."
        );

        handleSessionExpired();

    }

    /**
     * Logout Button Initialization
     */
    function initializeLogout() {

        const logoutButton =
            document.getElementById("logoutButton");

        if (!logoutButton) return;

        logoutButton.addEventListener(
            "click",
            logout
        );

    }

    /**
     * Clear Entire Session
     */
    function clearSession() {

        clearTokens();

        sessionStorage.clear();

    }

        /*=========================================================
      API REQUEST MANAGER
    =========================================================*/

    /**
     * Send Authenticated API Request
     */
    async function apiRequest(
        url,
        options = {}
    ) {

        const config = {

            ...options,

            headers: {

                ...getAuthHeaders(),

                ...(options.headers || {})

            }

        };

        try {

            const response =
                await fetch(
                    url,
                    config
                );

            if (response.status === 401) {

                handleUnauthorized();

                return null;

            }

            return response;

        }

        catch (error) {

            console.error(
                "API Request Failed:",
                error
            );

            throw error;

        }

    }

    /**
     * GET Request
     */
    async function get(
        url
    ) {

        return await apiRequest(
            url,
            {
                method: "GET"
            }
        );

    }

    /**
     * POST Request
     */
    async function post(
        url,
        data
    ) {

        return await apiRequest(
            url,
            {

                method: "POST",

                body: JSON.stringify(
                    data
                )

            }
        );

    }

    /**
     * PUT Request
     */
    async function put(
        url,
        data
    ) {

        return await apiRequest(
            url,
            {

                method: "PUT",

                body: JSON.stringify(
                    data
                )

            }
        );

    }

    /**
     * DELETE Request
     */
    async function remove(
        url
    ) {

        return await apiRequest(
            url,
            {

                method: "DELETE"

            }
        );

    }

        /*=========================================================
      CURRENT USER MANAGEMENT
    =========================================================*/

    /**
     * Cached Current User
     */
    let currentUser = null;

    /**
     * Fetch Current User
     */
    async function fetchCurrentUser() {

        try {

            const response =
                await get(
                    CURRENT_USER_API
                );

            if (!response) return null;

            if (!response.ok) {

                throw new Error(
                    "Unable to retrieve current user."
                );

            }

            currentUser =
                await response.json();

            return currentUser;

        }

        catch (error) {

            console.error(
                "Current User Error:",
                error
            );

            return null;

        }

    }

    /**
     * Get Cached Current User
     */
    function getCurrentUser() {

        return currentUser;

    }

    /**
     * Refresh Current User
     */
    async function refreshCurrentUser() {

        return await fetchCurrentUser();

    }

    /**
     * Check User Role
     */
    function hasRole(role) {

        if (!currentUser) {

            return false;

        }

        return (
            currentUser.role === role
        );

    }

    /**
     * Check Multiple Roles
     */
    function hasAnyRole(roles = []) {

        if (!currentUser) {

            return false;

        }

        return roles.includes(
            currentUser.role
        );

    }

    /**
     * Get User Full Name
     */
    function getUserFullName() {

        if (!currentUser) {

            return "";

        }

        return `${currentUser.first_name} ${currentUser.last_name}`;

    }

    /**
     * Get User Email
     */
    function getUserEmail() {

        if (!currentUser) {

            return "";

        }

        return currentUser.email;

    }
    /*=========================================================
      JWT EXPIRATION & REFRESH TOKEN MANAGEMENT
    =========================================================*/

    /**
     * Refresh Access Token
     */
    async function refreshAccessToken() {

        const refreshToken =
            getRefreshToken();

        if (!refreshToken) {

            console.warn(
                "Refresh token not found."
            );

            return false;

        }

        try {

            const response =
                await fetch(
                    REFRESH_API,
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body: JSON.stringify({

                            refresh_token:
                                refreshToken

                        })

                    }
                );

            if (!response.ok) {

                throw new Error(
                    "Failed to refresh access token."
                );

            }

            const data =
                await response.json();

            saveTokens(data);

            console.info(
                "Access token refreshed successfully."
            );

            return true;

        }

        catch (error) {

            console.error(
                "Token Refresh Error:",
                error
            );

            clearTokens();

            window.location.href =
                "login.html";

            return false;

        }

    }

    /**
     * Decode JWT Payload
     */
    function parseJwt(token) {

        if (!token) return null;

        try {

            const base64 =
                token.split(".")[1];

            const payload =
                atob(base64);

            return JSON.parse(payload);

        }

        catch (error) {

            console.error(
                "Invalid JWT:",
                error
            );

            return null;

        }

    }

    /**
     * Check Token Expiration
     */
    function isTokenExpired() {

        const token =
            getAccessToken();

        if (!token) {

            return true;

        }

        const payload =
            parseJwt(token);

        if (!payload || !payload.exp) {

            return true;

        }

        const currentTime =
            Math.floor(
                Date.now() / 1000
            );

        return currentTime >= payload.exp;

    }

    /**
     * Ensure Valid Authentication
     */
    async function ensureAuthenticated() {

        if (!isAuthenticated()) {

            return false;

        }

        if (!isTokenExpired()) {

            return true;

        }

        console.info(
            "Access token expired. Refreshing..."
        );

        return await refreshAccessToken();

    }

        /*=========================================================
      INITIALIZATION
    =========================================================*/

    function initializeAuth() {

        const currentPage =
            window.location.pathname
                .split("/")
                .pop()
                .toLowerCase();

        // Protect private pages
        const protectedPages = [

            "dashboard.html",
            "profile.html",
            "services.html",
            "bookings.html",
            "settings.html"

        ];

        // Public pages
        const publicPages = [

            "login.html",
            "register.html"

        ];

        if (
            protectedPages.includes(currentPage)
        ) {

            requireAuthentication();

        }

        if (
            publicPages.includes(currentPage)
        ) {

            redirectIfAuthenticated();

        }

        initializeLogout();

    }

    /*=========================================================
      EXPOSE AUTH MODULE
    =========================================================*/

    window.Auth = {

        // Token Management
        saveTokens,
        getAccessToken,
        getRefreshToken,
        getTokenType,
        clearTokens,

        // Authentication
        isAuthenticated,
        requireAuthentication,
        redirectIfAuthenticated,
        ensureAuthenticated,

        // User
        fetchCurrentUser,
        getCurrentUser,
        refreshCurrentUser,
        getUserFullName,
        getUserEmail,
        hasRole,
        hasAnyRole,

        // Session
        logout,
        handleSessionExpired,

        // API
        apiRequest,
        get,
        post,
        put,
        remove,

        // Headers
        getAuthorizationHeader,
        getAuthHeaders

    };

    /*=========================================================
      START AUTH MODULE
    =========================================================*/

    initializeAuth();

});







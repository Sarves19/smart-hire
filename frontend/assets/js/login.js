/*
==========================================================
Smart Hire
Login Module

Description:
Handles user authentication using FastAPI Backend.

Author: Smart Hire Team
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    "use strict";

    /*=========================================================
      BACKEND CONFIGURATION
    =========================================================*/

    // FastAPI Base URL
    const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

    // Authentication Endpoints
    const LOGIN_API = `${API_BASE_URL}/auth/login`;

    const REFRESH_API = `${API_BASE_URL}/auth/refresh`;

        /*=========================================================
      DOM ELEMENTS
    =========================================================*/

    // Login Form
    const loginForm =
        document.getElementById("loginForm");

    // Input Fields
    const email =
        document.getElementById("email");

    const password =
        document.getElementById("password");

    // Password Visibility Toggle
    const togglePassword =
        document.getElementById("togglePassword");

    // Remember Me Checkbox
    const rememberMe =
        document.getElementById("rememberMe");

    // Login Button
    const loginButton =
        document.getElementById("loginButton");

    // Google Login Button
    const googleLogin =
        document.getElementById("googleLogin");

            /*=========================================================
      PASSWORD VISIBILITY
    =========================================================*/

    function initializePasswordToggle() {

        setupPasswordToggle(
            password,
            togglePassword
        );

    }

    function setupPasswordToggle(
        inputField,
        button
    ) {

        // Ensure both elements exist
        if (!button || !inputField) return;

        button.addEventListener("click", () => {

            // Determine current input type
            const isHidden =
                inputField.type === "password";

            // Toggle password visibility
            inputField.type =
                isHidden ? "text" : "password";

            // Update eye icon
            const icon =
                button.querySelector("i");

            if (!icon) return;

            icon.classList.toggle(
                "bi-eye",
                !isHidden
            );

            icon.classList.toggle(
                "bi-eye-slash",
                isHidden
            );

            // Keep cursor in the password field
            inputField.focus();

            // Move cursor to the end of the text
            const length =
                inputField.value.length;

            inputField.setSelectionRange(
                length,
                length
            );

        });

    }
        /*=========================================================
      INITIALIZE APPLICATION
    =========================================================*/

    initialize();

    function initialize() {

        // Initialize Password Visibility Toggle
        initializePasswordToggle();

        // Load Remembered Email (if available)
        loadRememberedEmail();

        // Initialize Google Login Button
        initializeGoogleLogin();

        // Initialize Login Form
        initializeLoginForm();

        // Set Initial Focus
        if (email) {

            email.focus();

        }

    }

        /*=========================================================
      REMEMBER ME
    =========================================================*/

    function loadRememberedEmail() {

        // Ensure required elements exist
        if (!rememberMe || !email) return;

        // Retrieve saved email from local storage
        const savedEmail =
            localStorage.getItem("rememberedEmail");

        // Exit if nothing is stored
        if (!savedEmail) return;

        // Populate email field
        email.value = savedEmail;

        // Check Remember Me
        rememberMe.checked = true;

    }

    function handleRememberMe() {

        // Ensure required elements exist
        if (!rememberMe || !email) return;

        const emailValue =
            email.value
                .trim()
                .toLowerCase();

        if (rememberMe.checked) {

            // Save email locally
            localStorage.setItem(
                "rememberedEmail",
                emailValue
            );

        }

        else {

            // Remove saved email
            localStorage.removeItem(
                "rememberedEmail"
            );

        }

    }

        /*=========================================================
      GOOGLE LOGIN
    =========================================================*/

    function initializeGoogleLogin() {

        // Ensure Google Login button exists
        if (!googleLogin) return;

        googleLogin.addEventListener("click", () => {

            /*
            =====================================================
            FUTURE IMPLEMENTATION

            Google OAuth 2.0 / Google Identity Services

            Authentication Flow

            User
                │
                ▼
            Click "Continue with Google"
                │
                ▼
            Google Identity Services
                │
                ▼
            User Authentication
                │
                ▼
            Google Returns ID Token
                │
                ▼
            FastAPI Backend
                │
                ▼
            Verify Google Token
                │
                ▼
            Create User (if new)
                │
                ▼
            Login Existing User
                │
                ▼
            Generate JWT Access Token
                │
                ▼
            Generate Refresh Token
                │
                ▼
            Return Tokens
                │
                ▼
            Save Tokens
                │
                ▼
            Redirect to Dashboard

            =====================================================
            */

            showToast(
                "Google Sign-In will be available in a future update.",
                "info"
            );

            console.info(
                "Google OAuth is not implemented yet."
            );

        });

    }
    /*=========================================================
      LOGIN FORM
      FastAPI Integration
    =========================================================*/

    function initializeLoginForm() {

        // Ensure the login form exists
        if (!loginForm) return;

        // Register form submission event
        loginForm.addEventListener(
            "submit",
            handleLogin
        );

    }

        /*=========================================================
      HANDLE LOGIN
    =========================================================*/

    async function handleLogin(event) {

        // Prevent default form submission
        event.preventDefault();

        /*=====================================================
          GET FORM VALUES
        =====================================================*/

        const emailValue =
            email.value
                .trim()
                .toLowerCase();

        const passwordValue =
            password.value;

        /*=====================================================
          VALIDATION
        =====================================================*/

        if (!validateEmail(emailValue)) {

            showToast(
                "Please enter a valid email address.",
                "warning"
            );

            email.focus();

            return;

        }

        if (passwordValue.length === 0) {

            showToast(
                "Please enter your password.",
                "warning"
            );

            password.focus();

            return;

        }

        if (passwordValue.length < 8) {

            showToast(
                "Password must contain at least 8 characters.",
                "warning"
            );

            password.focus();

            return;

        }

        /*=====================================================
          REQUEST PAYLOAD
        =====================================================*/

        const payload = {

            email: emailValue,

            password: passwordValue

        };

        /*=====================================================
          LOADING STATE
        =====================================================*/

        setLoadingState(true);

        /*=====================================================
          SEND LOGIN REQUEST
        =====================================================*/

        try {

            const response = await fetch(
                LOGIN_API,
                {

                    method: "POST",

                    headers: {

                        "Content-Type": "application/json"

                    },

                    body: JSON.stringify(payload)

                }
            );

            const data = await response.json();

            /*=================================================
              HANDLE BACKEND ERRORS
            =================================================*/

            if (!response.ok) {

                let message =
                    "Login failed.";

                if (
                    typeof data.detail === "string"
                ) {

                    message =
                        data.detail;

                }

                else if (
                    Array.isArray(data.detail) &&
                    data.detail.length > 0
                ) {

                    message =
                        data.detail[0].msg;

                }

                throw new Error(message);

            }

            /*=================================================
              SUCCESS
            =================================================*/

            saveTokens(data);

            handleRememberMe();

            showToast(
                "Login successful!",
                "success"
            );

            setTimeout(() => {

                window.location.href =
                    "dashboard.html";

            }, 1000);

        }

        /*=====================================================
          HANDLE EXCEPTIONS
        =====================================================*/

        catch (error) {

            console.error(
                "Login Error:",
                error
            );

            showToast(

                error.message ||

                "Unable to login. Please try again.",

                "error"

            );

        }

        /*=====================================================
          RESET UI
        =====================================================*/

        finally {

            setLoadingState(false);

        }

    }
    /*=========================================================
      JWT TOKEN MANAGEMENT
    =========================================================*/

    /**
     * Save authentication tokens
     */
    function saveTokens(data) {

        if (!data) return;

        const storage =
            rememberMe && rememberMe.checked
                ? localStorage
                : sessionStorage;

        storage.setItem(
            "access_token",
            data.access_token
        );

        storage.setItem(
            "refresh_token",
            data.refresh_token
        );

        storage.setItem(
            "token_type",
            data.token_type || "bearer"
        );

    }

    /**
     * Get Access Token
     */
    function getAccessToken() {

        return (

            localStorage.getItem("access_token") ||

            sessionStorage.getItem("access_token")

        );

    }

    /**
     * Get Refresh Token
     */
    function getRefreshToken() {

        return (

            localStorage.getItem("refresh_token") ||

            sessionStorage.getItem("refresh_token")

        );

    }

    /**
     * Get Token Type
     */
    function getTokenType() {

        return (

            localStorage.getItem("token_type") ||

            sessionStorage.getItem("token_type") ||

            "bearer"

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

        const keys = [

            "access_token",

            "refresh_token",

            "token_type"

        ];

        keys.forEach(key => {

            localStorage.removeItem(key);

            sessionStorage.removeItem(key);

        });

    }

    /**
     * Logout User
     */
    function logout() {

        clearTokens();

        showToast(
            "Logged out successfully.",
            "success"
        );

        setTimeout(() => {

            window.location.href =
                "login.html";

        }, 500);

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
     * Get Authentication Headers
     */
    function getAuthHeaders() {

        const authorization =
            getAuthorizationHeader();

        if (!authorization) {

            return {

                "Content-Type":
                    "application/json"

            };

        }

        return {

            "Content-Type":
                "application/json",

            "Authorization":
                authorization

        };

    }

        /*=========================================================
      HELPER FUNCTIONS
    =========================================================*/

    /**
     * Validate Email Address
     */
    function validateEmail(emailAddress) {

        if (!emailAddress) return false;

        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        return emailPattern.test(
            emailAddress
        );

    }

    /**
     * Set Login Button Loading State
     */
    function setLoadingState(isLoading) {

        if (!loginButton) return;

        loginButton.disabled =
            isLoading;

        if (isLoading) {

            loginButton.innerHTML = `

                <span
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true">
                </span>

                Signing In...

            `;

        }

        else {

            loginButton.innerHTML = `

                <i class="bi bi-box-arrow-in-right me-2"></i>

                Login

            `;

        }

    }

    /**
     * Display Toast Notification
     *
     * Types:
     * success
     * error
     * warning
     * info
     */
  function showToast(
    message,
    type = "info"
) {

    //=====================================================
    // Replace this with Bootstrap Toast / SweetAlert
    // when available.
    //=====================================================

    console.log(
        `[${type.toUpperCase()}] ${message}`
    );

    alert(message);

}

});

/*
==========================================================
Smart Hire
Register Module

Description:
Handles user registration using FastAPI Backend.

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
    const REGISTER_API = `${API_BASE_URL}/auth/register`;
    const LOGIN_API = `${API_BASE_URL}/auth/login`;

    /*=========================================================
      DOM ELEMENTS
    =========================================================*/

    const registerForm = document.getElementById("registerForm");

    const fullName = document.getElementById("fullName");
    const email = document.getElementById("email");
    const phone = document.getElementById("phone");

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");

    const togglePassword =
        document.getElementById("togglePassword");

    const toggleConfirmPassword =
        document.getElementById("toggleConfirmPassword");

    const registerButton =
        document.getElementById("registerButton");

    const googleRegister =
        document.getElementById("googleRegister");

    const terms =
        document.getElementById("terms");

    /*=========================================================
      PASSWORD STRENGTH
    =========================================================*/

    const strengthBar =
        document.getElementById("strengthBar");

    const strengthText =
        document.getElementById("strengthText");

    /*=========================================================
      PASSWORD RULES
    =========================================================*/

    const ruleLength =
        document.getElementById("ruleLength");

    const ruleUpper =
        document.getElementById("ruleUpper");

    const ruleLower =
        document.getElementById("ruleLower");

    const ruleNumber =
        document.getElementById("ruleNumber");

    const ruleSpecial =
        document.getElementById("ruleSpecial");

    /*=========================================================
      INITIALIZE APPLICATION
    =========================================================*/

    initialize();

    function initialize() {

        initializePasswordToggle();

        initializeGoogleRegister();

        initializePasswordStrength();

        initializePasswordMatch();

        initializeRegisterForm();

        fullName.focus();

    }

        /*=========================================================
      PASSWORD VISIBILITY
    =========================================================*/

    function initializePasswordToggle() {

        setupPasswordToggle(
            password,
            togglePassword
        );

        setupPasswordToggle(
            confirmPassword,
            toggleConfirmPassword
        );

    }

    function setupPasswordToggle(
        inputField,
        button
    ) {

        if (!button || !inputField) return;

        button.addEventListener("click", () => {

            const isHidden =
                inputField.type === "password";

            inputField.type =
                isHidden ? "text" : "password";

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

            inputField.focus();

        });

    }

        /*=========================================================
      GOOGLE REGISTER
    =========================================================*/

    function initializeGoogleRegister() {

        if (!googleRegister) return;

        googleRegister.addEventListener("click", () => {

            /*
            =====================================================
            FUTURE IMPLEMENTATION

            Google OAuth 2.0 / Google Identity Services

            Flow:

            User
                │
                ▼
            Google Login
                │
                ▼
            Google Returns ID Token
                │
                ▼
            FastAPI Backend
                │
                ▼
            Verify Token
                │
                ▼
            Create/Login User
                │
                ▼
            Generate JWT
                │
                ▼
            Dashboard

            =====================================================
            */

            showToast(
                "Google Sign-In will be available soon.",
                "info"
            );

        });

    }

        /*=========================================================
      REGISTER FORM
      FastAPI Integration
    =========================================================*/

    function initializeRegisterForm() {

        if (!registerForm) return;

        registerForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            /*=====================================================
              GET FORM VALUES
            =====================================================*/

            const fullNameValue = fullName.value.trim();

            const emailValue = email.value.trim().toLowerCase();

            const phoneValue = phone.value.trim();

            const passwordValue = password.value;

            const confirmPasswordValue = confirmPassword.value;

            const role = document.querySelector(
                'input[name="role"]:checked'
            )?.value;

            /*=====================================================
              VALIDATION
            =====================================================*/

            if (fullNameValue.length < 3) {

                showToast(
                    "Please enter your full name.",
                    "warning"
                );

                fullName.focus();

                return;

            }

            if (!validateEmail(emailValue)) {

                showToast(
                    "Please enter a valid email address.",
                    "warning"
                );

                email.focus();

                return;

            }

            if (!validatePhone(phoneValue)) {

                showToast(
                    "Please enter a valid Sri Lankan phone number.",
                    "warning"
                );

                phone.focus();

                return;

            }

            if (!validatePassword(passwordValue)) {

                showToast(
                    "Password does not meet all requirements.",
                    "warning"
                );

                password.focus();

                return;

            }

            if (passwordValue !== confirmPasswordValue) {

                showToast(
                    "Passwords do not match.",
                    "error"
                );

                confirmPassword.focus();

                return;

            }

            if (!role) {

                showToast(
                    "Please select your account type.",
                    "warning"
                );

                return;

            }

            if (!terms.checked) {

                showToast(
                    "Please accept the Terms & Conditions.",
                    "warning"
                );

                terms.focus();

                return;

            }

            /*=====================================================
              SPLIT FULL NAME
            =====================================================*/
// Split full name
const names = fullNameValue
    .trim()
    .split(/\s+/);

// Require first and last name
if (names.length < 2) {

    showToast(
        "Please enter your first and last name.",
        "warning"
    );

    setLoadingState(false);

    return;

}

const firstName = names[0];

const lastName = names
    .slice(1)
    .join(" ");

// Payload
const payload = {
    first_name: firstName,
    last_name: lastName,
    email: emailValue,
    phone_number: phoneValue,
    password: passwordValue,
    role: role.toUpperCase()
};


            /*=====================================================
              SEND REQUEST
            =====================================================*/

            setLoadingState(true);

            try {

                const response = await fetch(
                    REGISTER_API,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify(payload)
                    }
                );

                const data = await response.json();

            if (!response.ok) {

    let message = "Registration failed.";

    if (typeof data.detail === "string") {
        message = data.detail;
    } else if (Array.isArray(data.detail) && data.detail.length > 0) {
        message = data.detail[0].msg;
    }

    throw new Error(message);
}

                /*=================================================
                  SUCCESS
                =================================================*/

                showToast(
                    data.message,
                    "success"
                );

                registerForm.reset();

                strengthBar.style.width = "0%";

                strengthBar.className =
                    "progress-bar bg-danger";

                strengthText.textContent =
                    "Very Weak";

                setTimeout(() => {

                    window.location.href =
                        "login.html";

                }, 1500);

            }

            catch (error) {

                console.error(error);

                showToast(
                    error.message ||
                    "Registration failed.",
                    "error"
                );

            }

            finally {

                setLoadingState(false);

            }

        });

    }

        /*=========================================================
      PASSWORD STRENGTH
    =========================================================*/

    function initializePasswordStrength() {

        if (!password) return;

        password.addEventListener("input", () => {

            const value = password.value;

            const checks = {

                length: value.length >= 8,

                upper: /[A-Z]/.test(value),

                lower: /[a-z]/.test(value),

                number: /\d/.test(value),

                special: /[!@#$%^&*(),.?":{}|<>]/.test(value)

            };

            updateRule(
                ruleLength,
                checks.length
            );

            updateRule(
                ruleUpper,
                checks.upper
            );

            updateRule(
                ruleLower,
                checks.lower
            );

            updateRule(
                ruleNumber,
                checks.number
            );

            updateRule(
                ruleSpecial,
                checks.special
            );

            const score =
                Object.values(checks)
                    .filter(Boolean)
                    .length;

            updateStrength(score);

            if (
                confirmPassword.value.length > 0
            ) {

                checkPasswordMatch();

            }

        });

    }

    /*=========================================================
      UPDATE PASSWORD RULE
    =========================================================*/

    function updateRule(
        rule,
        valid
    ) {

        if (!rule) return;

        const icon =
            rule.querySelector("i");

        if (!icon) return;

        if (valid) {

            icon.className =
                "bi bi-check-circle-fill text-success me-2";

        }

        else {

            icon.className =
                "bi bi-x-circle-fill text-danger me-2";

        }

    }

    /*=========================================================
      UPDATE PASSWORD STRENGTH BAR
    =========================================================*/

    function updateStrength(
        score
    ) {

        if (
            !strengthBar ||
            !strengthText
        ) return;

        const levels = [

            {
                width: "0%",
                text: "Very Weak",
                bar: "bg-danger",
                textColor: "text-danger"
            },

            {
                width: "20%",
                text: "Weak",
                bar: "bg-danger",
                textColor: "text-danger"
            },

            {
                width: "40%",
                text: "Fair",
                bar: "bg-warning",
                textColor: "text-warning"
            },

            {
                width: "60%",
                text: "Good",
                bar: "bg-info",
                textColor: "text-info"
            },

            {
                width: "80%",
                text: "Strong",
                bar: "bg-primary",
                textColor: "text-primary"
            },

            {
                width: "100%",
                text: "Very Strong",
                bar: "bg-success",
                textColor: "text-success"
            }

        ];

        const level =
            levels[score];

        strengthBar.style.width =
            level.width;

        strengthBar.className =
            `progress-bar ${level.bar}`;

        strengthText.textContent =
            level.text;

        strengthText.className =
            `fw-semibold ${level.textColor}`;

    }

    /*=========================================================
      PASSWORD MATCH
    =========================================================*/

    function initializePasswordMatch() {

        if (!confirmPassword) return;

        confirmPassword.addEventListener(
            "input",
            checkPasswordMatch
        );

    }

    function checkPasswordMatch() {

        /*=====================================================
          EMPTY CONFIRM PASSWORD
        =====================================================*/

        if (
            confirmPassword.value.length === 0
        ) {

            confirmPassword.classList.remove(
                "is-valid",
                "is-invalid"
            );

            return;

        }

        /*=====================================================
          PASSWORDS MATCH
        =====================================================*/

        if (
            password.value ===
            confirmPassword.value
        ) {

            confirmPassword.classList.remove(
                "is-invalid"
            );

            confirmPassword.classList.add(
                "is-valid"
            );

        }

        /*=====================================================
          PASSWORDS DO NOT MATCH
        =====================================================*/

        else {

            confirmPassword.classList.remove(
                "is-valid"
            );

            confirmPassword.classList.add(
                "is-invalid"
            );

        }

    }

        /*=========================================================
      VALIDATION HELPERS
    =========================================================*/

    /**
     * Validate Email Address
     */
    function validateEmail(emailAddress) {

        const emailRegex =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        return emailRegex.test(emailAddress);

    }

    /**
     * Validate Sri Lankan Phone Number
     *
     * Supported:
     * 0771234567
     * +94771234567
     */
    function validatePhone(phoneNumber) {

        const cleaned =
            phoneNumber.replace(/\s+/g, "");

        const phoneRegex =
            /^(\+94|0)\d{9}$/;

        return phoneRegex.test(cleaned);

    }

    /**
     * Validate Password
     *
     * Requirements:
     * - Minimum 8 characters
     * - One uppercase letter
     * - One lowercase letter
     * - One number
     * - One special character
     */
    function validatePassword(passwordValue) {

        return (

            passwordValue.length >= 8 &&

            /[A-Z]/.test(passwordValue) &&

            /[a-z]/.test(passwordValue) &&

            /\d/.test(passwordValue) &&

            /[!@#$%^&*(),.?":{}|<>]/.test(passwordValue)

        );

    }

    /*=========================================================
      HELPER FUNCTIONS
    =========================================================*/

    /**
     * Split Full Name into
     * First Name and Last Name
     */

    /*=========================================================
      BUTTON LOADING STATE
    =========================================================*/

    function setLoadingState(isLoading) {

        if (!registerButton) return;

        if (isLoading) {

            registerButton.disabled = true;

            registerButton.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true">
                </span>
                Creating Account...
            `;

        }

        else {

            registerButton.disabled = false;

            registerButton.innerHTML = `
                <span class="btn-text">
                    <i class="bi bi-person-plus-fill me-2"></i>
                    Create Account
                </span>
            `;

        }

    }

    /*=========================================================
      FORM RESET
    =========================================================*/

    function resetRegistrationForm() {

        registerForm.reset();

        if (strengthBar) {

            strengthBar.style.width = "0%";

            strengthBar.className =
                "progress-bar bg-danger";

        }

        if (strengthText) {

            strengthText.textContent =
                "Very Weak";

            strengthText.className =
                "fw-semibold text-danger";

        }

        confirmPassword.classList.remove(
            "is-valid",
            "is-invalid"
        );

        [
            ruleLength,
            ruleUpper,
            ruleLower,
            ruleNumber,
            ruleSpecial
        ].forEach(rule => {

            if (!rule) return;

            const icon =
                rule.querySelector("i");

            if (!icon) return;

            icon.className =
                "bi bi-x-circle-fill text-danger me-2";

        });

    }

        /*=========================================================
      TOAST NOTIFICATIONS
    =========================================================*/

    function showToast(
        message,
        type = "success"
    ) {

        // Remove any existing toast
        const existingToast =
            document.querySelector(".toast-message");

        if (existingToast) {

            existingToast.remove();

        }

        // Create toast
        const toast =
            document.createElement("div");

        toast.className =
            `toast-message toast-${type}`;

        /*=====================================================
          ICON
        =====================================================*/

        let icon =
            "bi-check-circle-fill";

        switch (type) {

            case "success":

                icon =
                    "bi-check-circle-fill";

                break;

            case "error":

                icon =
                    "bi-x-circle-fill";

                break;

            case "warning":

                icon =
                    "bi-exclamation-triangle-fill";

                break;

            case "info":

                icon =
                    "bi-info-circle-fill";

                break;

            default:

                icon =
                    "bi-check-circle-fill";

        }

        /*=====================================================
          TOAST CONTENT
        =====================================================*/

        toast.innerHTML = `

            <div class="toast-content">

                <i class="bi ${icon} me-2"></i>

                <span>${message}</span>

            </div>

        `;

        document.body.appendChild(toast);

        /*=====================================================
          SHOW ANIMATION
        =====================================================*/

        requestAnimationFrame(() => {

            toast.classList.add("show");

        });

        /*=====================================================
          AUTO REMOVE
        =====================================================*/

        setTimeout(() => {

            toast.classList.remove("show");

            setTimeout(() => {

                toast.remove();

            }, 300);

        }, 3000);

    }

        /*=========================================================
      INPUT CLEANUP
    =========================================================*/

    if (email) {

        email.addEventListener("blur", () => {

            email.value = email.value
                .trim()
                .toLowerCase();

        });

    }

    if (phone) {

        phone.addEventListener("input", () => {

            phone.value = phone.value.replace(
                /[^\d+]/g,
                ""
            );

        });

    }

    if (fullName) {

        fullName.addEventListener("input", () => {

            fullName.value = fullName.value
                .replace(/\s{2,}/g, " ");

        });

    }

    /*=========================================================
      END OF MODULE
    =========================================================*/

});







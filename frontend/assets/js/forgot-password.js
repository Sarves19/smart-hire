/**
 * ==========================================================
 * Smart Hire - Forgot Password
 * ==========================================================
 */

document.addEventListener("DOMContentLoaded", () => {

    // ======================================================
    // DOM ELEMENTS
    // ======================================================

    const forgotPasswordForm = document.getElementById("forgotPasswordForm");
    const emailInput = document.getElementById("email");
    const forgotPasswordButton = document.getElementById("forgotPasswordButton");
    const backToLoginButton = document.getElementById("backToLogin");

    // ======================================================
    // INITIALIZE
    // ======================================================

    initialize();

    function initialize() {

        initializeForgotPasswordForm();
        initializeInputListeners();
        initializeNavigation();

    }

    // ======================================================
    // INPUT LISTENERS
    // ======================================================

    function initializeInputListeners() {

        emailInput?.addEventListener("input", () => {

            emailInput.classList.remove("is-invalid");
            emailInput.classList.remove("is-valid");

        });

    }

    // ======================================================
    // BACK TO LOGIN
    // ======================================================

    function initializeNavigation() {

        backToLoginButton?.addEventListener("click", (event) => {

            event.preventDefault();

            window.location.href = "login.html";

        });

    }

    // ======================================================
    // PLACEHOLDER FUNCTIONS
    // (Implemented in the next parts)
    // ======================================================

      // ======================================================
    // EMAIL VALIDATION
    // ======================================================

    function validateEmail(email) {

        const emailRegex =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        return emailRegex.test(email.trim());

    }

    // ======================================================
    // FORM VALIDATION
    // ======================================================

    function validateForm() {

        let isValid = true;

        const email = emailInput.value.trim();

        // ---------------------------------------------
        // Email Required
        // ---------------------------------------------

        if (!email) {

            emailInput.classList.add("is-invalid");
            emailInput.classList.remove("is-valid");

            showToast(
                "Please enter your email address.",
                "error"
            );

            return false;

        }

        // ---------------------------------------------
        // Email Format
        // ---------------------------------------------

        if (!validateEmail(email)) {

            emailInput.classList.add("is-invalid");
            emailInput.classList.remove("is-valid");

            showToast(
                "Please enter a valid email address.",
                "error"
            );

            return false;

        }

        emailInput.classList.remove("is-invalid");
        emailInput.classList.add("is-valid");

        return isValid;

    }

        // ======================================================
    // FORGOT PASSWORD FORM
    // ======================================================

    function initializeForgotPasswordForm() {

        forgotPasswordForm?.addEventListener("submit", async (event) => {

            event.preventDefault();

            if (!validateForm()) {
                return;
            }

            const email = emailInput.value.trim();

            try {

                setLoadingState(true);

                /*
                 * ======================================================
                 * FastAPI Integration
                 * Replace this demo section with:
                 *
                 * const response = await fetch(
                 *     "http://127.0.0.1:8000/api/v1/auth/forgot-password",
                 *     {
                 *         method: "POST",
                 *         headers: {
                 *             "Content-Type": "application/json"
                 *         },
                 *         body: JSON.stringify({ email })
                 *     }
                 * );
                 *
                 * const result = await response.json();
                 *
                 * if (!response.ok) {
                 *     throw new Error(result.detail);
                 * }
                 * ======================================================
                 */

                await new Promise(resolve => setTimeout(resolve, 1800));

                sessionStorage.setItem(
                    "resetEmail",
                    email
                );

                showToast(
                    "OTP has been sent to your email.",
                    "success"
                );

                setTimeout(() => {

                    window.location.href = "verify-otp.html";

                }, 1200);

            }
            catch (error) {

                console.error(error);

                showToast(

                    error.message ||

                    "Unable to process your request. Please try again.",

                    "error"

                );

            }
            finally {

                setLoadingState(false);

            }

        });

    }


    // ======================================================
    // LOADING STATE
    // ======================================================

    function setLoadingState(isLoading) {

        if (!forgotPasswordButton) {
            return;
        }

        forgotPasswordButton.disabled = isLoading;

        if (isLoading) {

            forgotPasswordButton.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2"></span>
                Sending OTP...
            `;

        } else {

            forgotPasswordButton.innerHTML = `
                <i class="fas fa-paper-plane me-2"></i>
                Send OTP
            `;

        }

    }

    // ======================================================
    // TOAST NOTIFICATION
    // ======================================================

    function showToast(message, type = "info") {

        const existingToast = document.querySelector(".toast-message");

        if (existingToast) {
            existingToast.remove();
        }

        const icons = {
            success: "fa-circle-check",
            error: "fa-circle-xmark",
            warning: "fa-triangle-exclamation",
            info: "fa-circle-info"
        };

        const toast = document.createElement("div");

        toast.className = `toast-message toast-${type}`;

        toast.innerHTML = `
            <i class="fas ${icons[type] || icons.info}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add("show");
        });

        setTimeout(() => {

            toast.classList.remove("show");

            setTimeout(() => {

                toast.remove();

            }, 300);

        }, 3000);

    }

});


/*
==========================================================
Smart Hire

Reset Password

==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    /*
    ==========================================================
    DOM Elements
    ==========================================================
    */

    const form = document.getElementById("resetPasswordForm");

    const newPassword = document.getElementById("newPassword");

    const confirmPassword = document.getElementById("confirmPassword");

    const toggleNewPassword =
        document.getElementById("toggleNewPassword");

    const toggleConfirmPassword =
        document.getElementById("toggleConfirmPassword");

    const strengthBar =
        document.getElementById("strengthBar");

    const strengthText =
        document.getElementById("strengthText");

    const passwordMatch =
        document.getElementById("passwordMatch");

    const resetButton =
        document.getElementById("resetButton");

    /*
    ==========================================================
    Password Rules
    ==========================================================
    */

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

    /*
    ==========================================================
    Initialize
    ==========================================================
    */

    initializePasswordToggle();

    initializeStrengthChecker();

    initializePasswordMatch();

    initializeForm();

    /*
    ==========================================================
    Function Placeholders
    ==========================================================
    */

  /*
==========================================================
Password Visibility Toggle
==========================================================
*/

function initializePasswordToggle() {

    setupPasswordToggle(
        newPassword,
        toggleNewPassword,
        "New Password"
    );

    setupPasswordToggle(
        confirmPassword,
        toggleConfirmPassword,
        "Confirm Password"
    );

}

/*
==========================================================
Reusable Toggle Helper
==========================================================
*/

function setupPasswordToggle(input, button, fieldName) {

    button.setAttribute(
        "aria-label",
        `Show ${fieldName}`
    );

    button.addEventListener("click", () => {

        const isHidden = input.type === "password";

        input.type = isHidden ? "text" : "password";

        const icon = button.querySelector("i");

        icon.classList.toggle("bi-eye", !isHidden);
        icon.classList.toggle("bi-eye-slash", isHidden);

        button.setAttribute(
            "aria-label",
            `${isHidden ? "Hide" : "Show"} ${fieldName}`
        );

        input.focus();

    });

}

    function initializeStrengthChecker() {

         newPassword.addEventListener("input", () => {

        const password = newPassword.value;

        const checks = {
            length: password.length >= 8,
            upper: /[A-Z]/.test(password),
            lower: /[a-z]/.test(password),
            number: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };

        updateRule(ruleLength, checks.length);
        updateRule(ruleUpper, checks.upper);
        updateRule(ruleLower, checks.lower);
        updateRule(ruleNumber, checks.number);
        updateRule(ruleSpecial, checks.special);

        const score = Object.values(checks).filter(Boolean).length;

        updateStrength(score);

    });

    }

    /*
==========================================================
Update Password Rule
==========================================================
*/

function updateRule(element, isValid) {

    const icon = element.querySelector("i");

    if (isValid) {

        icon.className = "bi bi-check-circle-fill text-success me-2";

    } else {

        icon.className = "bi bi-x-circle text-danger me-2";

    }

}

/*
==========================================================
Update Strength Meter
==========================================================
*/

function updateStrength(score) {

    const levels = [
        {
            width: "0%",
            text: "Weak",
            bar: "bg-danger",
            textClass: "text-danger"
        },
        {
            width: "20%",
            text: "Weak",
            bar: "bg-danger",
            textClass: "text-danger"
        },
        {
            width: "40%",
            text: "Fair",
            bar: "bg-warning",
            textClass: "text-warning"
        },
        {
            width: "60%",
            text: "Good",
            bar: "bg-info",
            textClass: "text-info"
        },
        {
            width: "80%",
            text: "Strong",
            bar: "bg-primary",
            textClass: "text-primary"
        },
        {
            width: "100%",
            text: "Very Strong",
            bar: "bg-success",
            textClass: "text-success"
        }
    ];

    const level = levels[score];

    strengthBar.style.width = level.width;

    strengthBar.className = `progress-bar ${level.bar}`;

    strengthText.textContent = level.text;

    strengthText.className = `fw-semibold ${level.textClass}`;

}

    function initializePasswordMatch() {

    newPassword.addEventListener("input", checkPasswordMatch);

    confirmPassword.addEventListener("input", checkPasswordMatch);

    }

    /*
==========================================================
Check Password Match
==========================================================
*/

function checkPasswordMatch() {

    const password = newPassword.value;

    const confirm = confirmPassword.value;

    // Don't show anything until user starts typing
    if (confirm.length === 0) {

        passwordMatch.textContent = "Passwords must match.";

        passwordMatch.className = "small mb-3 text-muted";

        confirmPassword.classList.remove("is-valid", "is-invalid");

        return;

    }

    if (password === confirm) {

        passwordMatch.innerHTML = `
            <i class="bi bi-check-circle-fill me-1"></i>
            Passwords match.
        `;

        passwordMatch.className = "small mb-3 text-success";

        confirmPassword.classList.remove("is-invalid");

        confirmPassword.classList.add("is-valid");

    } else {

        passwordMatch.innerHTML = `
            <i class="bi bi-x-circle-fill me-1"></i>
            Passwords do not match.
        `;

        passwordMatch.className = "small mb-3 text-danger";

        confirmPassword.classList.remove("is-valid");

        confirmPassword.classList.add("is-invalid");

    }

}


  /*
==========================================================
Reset Password Form
==========================================================
*/

function initializeForm() {

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const password = newPassword.value.trim();
        const confirm = confirmPassword.value.trim();

        /*
        ==========================================================
        Validation
        ==========================================================
        */

        if (!password || !confirm) {

            showToast(
                "Please fill in all required fields.",
                "warning"
            );

            return;

        }

        if (password !== confirm) {

            showToast(
                "Passwords do not match.",
                "error"
            );

            confirmPassword.focus();

            return;

        }

        const validations = [
            password.length >= 8,
            /[A-Z]/.test(password),
            /[a-z]/.test(password),
            /\d/.test(password),
            /[!@#$%^&*(),.?":{}|<>]/.test(password)
        ];

        if (!validations.every(Boolean)) {

            showToast(
                "Please satisfy all password requirements.",
                "warning"
            );

            return;

        }

        /*
        ==========================================================
        Loading State
        ==========================================================
        */

        resetButton.disabled = true;

        resetButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2"></span>
            Updating Password...
        `;

        try {

            /*
            ==========================================================
            Future FastAPI API

            await fetch("/api/auth/reset-password")

            ==========================================================
            */

            await new Promise(resolve => setTimeout(resolve, 1800));

            showToast(
                "Password updated successfully!",
                "success"
            );

            setTimeout(() => {

                window.location.href = "login.html";

            }, 1500);

        }

        catch (error) {

            console.error(error);

            showToast(
                "Something went wrong. Please try again.",
                "error"
            );

        }

        finally {

            resetButton.disabled = false;

            resetButton.innerHTML = `
                <i class="bi bi-arrow-repeat me-2"></i>
                Reset Password
            `;

        }

    });

}

    /*
==========================================================
Toast Notification
==========================================================
*/

function showToast(message, type = "success") {

    const toast = document.createElement("div");

    toast.className = `toast-message toast-${type}`;

    toast.innerHTML = `
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

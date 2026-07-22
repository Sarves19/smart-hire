// Smart Hire JavaScript

console.log("Smart Hire Loaded Successfully");


/* ==========================================================
   REGISTER PAGE
========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    if (!registerForm) return;

    const fullName = document.getElementById("fullName");
    const email = document.getElementById("email");
    const phone = document.getElementById("phone");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const terms = document.getElementById("terms");

    /* ==========================
       PASSWORD TOGGLE
    ========================== */

    document.querySelectorAll(".password-toggle").forEach(button => {

        button.addEventListener("click", () => {

            const input = button.previousElementSibling;
            const icon = button.querySelector("i");

            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("bi-eye");
                icon.classList.add("bi-eye-slash");
            } else {
                input.type = "password";
                icon.classList.remove("bi-eye-slash");
                icon.classList.add("bi-eye");
            }

        });

    });

    /* ==========================
       VALIDATION
    ========================== */

    registerForm.addEventListener("submit", function (e) {

        e.preventDefault();

        if (fullName.value.trim().length < 3) {
            alert("Please enter your full name.");
            fullName.focus();
            return;
        }

        const emailRegex =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email.value.trim())) {
            alert("Enter a valid email address.");
            email.focus();
            return;
        }

        const phoneRegex =
            /^(\+94|0)?7\d{8}$/;

        if (!phoneRegex.test(phone.value.trim())) {
            alert("Enter a valid Sri Lankan mobile number.");
            phone.focus();
            return;
        }

        if (password.value.length < 8) {
            alert("Password must contain at least 8 characters.");
            password.focus();
            return;
        }

        if (password.value !== confirmPassword.value) {
            alert("Passwords do not match.");
            confirmPassword.focus();
            return;
        }

        if (!terms.checked) {
            alert("Please accept the Terms & Conditions.");
            return;
        }

        const submitButton =
            registerForm.querySelector(".auth-btn");

        submitButton.disabled = true;

        submitButton.innerHTML =
            '<span class="spinner-border spinner-border-sm"></span> Creating Account...';

        setTimeout(() => {

            submitButton.disabled = false;

            submitButton.innerHTML = "Create Account";

            alert("Frontend validation completed.\n\nBackend integration will be added next.");

        }, 1500);

    });

});


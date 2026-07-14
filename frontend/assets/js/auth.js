/* ==========================================================
   SMART HIRE AUTHENTICATION
========================================================== */

"use strict";

/* ==========================================================
   DOM ELEMENTS
========================================================== */

const loginForm = document.getElementById("loginForm");

const emailInput = document.getElementById("email");

const passwordInput = document.getElementById("password");

const togglePassword = document.getElementById("togglePassword");

/* ==========================================================
   PASSWORD TOGGLE
========================================================== */

togglePassword.addEventListener("click", () => {

    const type =
        passwordInput.getAttribute("type") === "password"
            ? "text"
            : "password";

    passwordInput.setAttribute("type", type);

    togglePassword.classList.toggle("bi-eye");

    togglePassword.classList.toggle("bi-eye-slash");

});

/* ==========================================================
   EMAIL VALIDATION
========================================================== */

function validateEmail(email){

    const regex =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    return regex.test(email);

}

/* ==========================================================
   PASSWORD VALIDATION
========================================================== */

function validatePassword(password){

    return password.length >= 6;

}

/* ==========================================================
   LOGIN FORM
========================================================== */

loginForm.addEventListener("submit", function(event){

    event.preventDefault();

    const email =
        emailInput.value.trim();

    const password =
        passwordInput.value.trim();

    if(email === ""){

        alert("Please enter your email.");

        emailInput.focus();

        return;

    }

    if(!validateEmail(email)){

        alert("Please enter a valid email.");

        emailInput.focus();

        return;

    }

    if(password === ""){

        alert("Please enter your password.");

        passwordInput.focus();

        return;

    }

    if(!validatePassword(password)){

        alert("Password must contain at least 6 characters.");

        passwordInput.focus();

        return;

    }

    console.log("Email :", email);

    console.log("Password :", password);

    alert("Validation Successful!");

});

/* ==========================================================
   TOAST NOTIFICATION
========================================================== */

function showToast(message, type = "success") {

    const existingToast = document.querySelector(".toast-message");

    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement("div");

    toast.className = "toast-message";

    toast.textContent = message;

    if (type === "error") {
        toast.style.background = "#EF4444";
    } else {
        toast.style.background = "#22C55E";
    }

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 3000);

}

/* ==========================================================
   LOADING BUTTON
========================================================== */

const loginButton = document.querySelector(".login-btn");

function startLoading() {

    loginButton.disabled = true;

    loginButton.innerHTML = `

        <span class="spinner-border spinner-border-sm"></span>

        Signing In...

    `;

}

function stopLoading() {

    loginButton.disabled = false;

    loginButton.innerHTML = "Login";

}

/* ==========================================================
   UPDATE FORM SUBMIT
========================================================== */

loginForm.addEventListener("submit", function (event) {

    event.preventDefault();

    const email = emailInput.value.trim();

    const password = passwordInput.value.trim();

    if (email === "") {

        showToast("Please enter your email.", "error");

        emailInput.focus();

        return;

    }

    if (!validateEmail(email)) {

        showToast("Please enter a valid email.", "error");

        emailInput.focus();

        return;

    }

    if (password === "") {

        showToast("Please enter your password.", "error");

        passwordInput.focus();

        return;

    }

    if (!validatePassword(password)) {

        showToast("Password must be at least 6 characters.", "error");

        passwordInput.focus();

        return;

    }

    startLoading();

    setTimeout(() => {

        stopLoading();

        showToast("Validation Successful!");

        console.log("Email:", email);

        console.log("Password:", password);

    }, 1500);

});
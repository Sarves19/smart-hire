/*
==========================================================
Smart Hire
Verify OTP JavaScript
==========================================================
*/

document.addEventListener("DOMContentLoaded", () => {

    /*
    ==========================================================
    DOM ELEMENTS
    ==========================================================
    */

    const otpInputs = document.querySelectorAll(".otp-input");

    const otpForm = document.getElementById("otpForm");

    const resendButton = document.getElementById("resendOtp");

    const countdown = document.getElementById("countdown");

    const verifyButton = otpForm.querySelector(".login-btn");

    /*
    ==========================================================
    CONFIGURATION
    ==========================================================
    */

    const OTP_LENGTH = 6;

    const TIMER_DURATION = 120;

    let timer = TIMER_DURATION;

    let timerInterval = null;

    /*
    ==========================================================
    INITIALIZATION
    ==========================================================
    */

    initializeOTPInputs();

    initializePasteSupport();

    initializeCountdown();

    initializeForm();

    /*
    ==========================================================
    FUNCTION PLACEHOLDERS
    ==========================================================
    */

    function initializeOTPInputs() {

        // Part 2

    }

    function initializePasteSupport() {

    otpInputs.forEach((input) => {

        input.addEventListener("paste", (event) => {

            event.preventDefault();

            // Get pasted text
            const pastedData = (event.clipboardData || window.clipboardData)
                .getData("text")
                .trim();

            // Keep only digits
            const otp = pastedData.replace(/\D/g, "");

            // OTP must contain exactly 6 digits
            if (otp.length !== OTP_LENGTH) {

                showToast(
                    "Please paste a valid 6-digit OTP.",
                    "warning"
                );

                return;

            }

            // Fill OTP boxes
            otpInputs.forEach((box, index) => {

                box.value = otp[index];

            });

            // Focus last input
            otpInputs[OTP_LENGTH - 1].focus();

        });

    });

}

   /*
==========================================================
Update Countdown Display
==========================================================
*/

function updateCountdownDisplay() {

    const minutes = Math.floor(timer / 60);

    const seconds = timer % 60;

    countdown.textContent =
        `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

}

   function initializeForm() {

    otpForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const otp = Array.from(otpInputs)
            .map(input => input.value.trim())
            .join("");

        /*
        ==========================================
        Validation
        ==========================================
        */

        if (otp.length !== OTP_LENGTH) {

            showToast(
                "Please enter the complete 6-digit OTP.",
                "error"
            );

            otpInputs[0].focus();

            return;

        }

        /*
        ==========================================
        Loading State
        ==========================================
        */

        verifyButton.disabled = true;

        verifyButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2"></span>
            Verifying...
        `;

        try {

            /*
            ==========================================
            Future FastAPI Call

            await fetch("/api/auth/verify-otp")
            ==========================================
            */

            console.log("OTP:", otp);

            await new Promise(resolve => setTimeout(resolve, 1500));

            showToast(
                "OTP verified successfully!",
                "success"
            );

            setTimeout(() => {

                window.location.href = "reset-password.html";

            }, 1200);

        }

        catch (error) {

            showToast(
                "OTP verification failed.",
                "error"
            );

            console.error(error);

        }

        finally {

            verifyButton.disabled = false;

            verifyButton.innerHTML = `
                <i class="bi bi-shield-check me-2"></i>
                Verify OTP
            `;

        }

    });

}

 function showToast(message, type = "success") {

    const toast = document.createElement("div");

    toast.className = `toast-message toast-${type}`;

    toast.textContent = message;

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
function initializeOTPInputs() {

    otpInputs.forEach((input, index) => {

        /*
        ==========================================
        Allow Numbers Only
        ==========================================
        */

        input.addEventListener("input", (event) => {

            let value = event.target.value;

            // Remove non-numeric characters
            value = value.replace(/\D/g, "");

            // Keep only one digit
            event.target.value = value.substring(0, 1);

            // Move to next input
            if (value !== "" && index < OTP_LENGTH - 1) {

                otpInputs[index + 1].focus();

            }

        });

        /*
        ==========================================
        Keyboard Navigation
        ==========================================
        */

        input.addEventListener("keydown", (event) => {

            switch (event.key) {

                case "Backspace":

                    // If current box is empty, go to previous
                    if (input.value === "" && index > 0) {

                        otpInputs[index - 1].focus();

                    }

                    break;

                case "ArrowLeft":

                    if (index > 0) {

                        otpInputs[index - 1].focus();

                    }

                    break;

                case "ArrowRight":

                    if (index < OTP_LENGTH - 1) {

                        otpInputs[index + 1].focus();

                    }

                    break;

                default:

                    break;

            }

        });

        /*
        ==========================================
        Auto Select on Focus
        ==========================================
        */

        input.addEventListener("focus", () => {

            input.select();

        });

    });

}



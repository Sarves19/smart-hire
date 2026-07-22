    /* =======================================================
       QUICK ACTIONS
    ======================================================= */

    function initializeQuickActions() {

        const browseServicesButton =
            document.getElementById(
                "btnBrowseServices"
            );

        const bookServiceButton =
            document.getElementById(
                "btnBookService"
            );

        const profileButton =
            document.getElementById(
                "btnProfile"
            );

        /* Browse Services */

        if (browseServicesButton) {

            browseServicesButton.addEventListener(
                "click",
                () => {

                    window.location.href =
                        "services.html";

                }
            );

        }

        /* Book Service */

        if (bookServiceButton) {

            bookServiceButton.addEventListener(
                "click",
                () => {

                    window.location.href =
                        "booking.html";

                }
            );

        }

        /* My Profile */

        if (profileButton) {

            profileButton.addEventListener(
                "click",
                () => {

                    window.location.href =
                        "profile.html";

                }
            );

        }

    }

    
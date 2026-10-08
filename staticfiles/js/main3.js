'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Car filter
        --------------------*/
        $('.filter__controls li').on('click', function () {
            $('.filter__controls li').removeClass('active');
            $(this).addClass('active');
        });

        if ($('.car-filter').length > 0) {
            var containerEl = document.querySelector('.car-filter');
            var mixer = mixitup(containerEl);
        }
    });


    /*--------------------------
        Background Set
    ----------------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });


    // Canvas Menu
    $(".canvas__open").on('click', function () {
        $(".offcanvas-menu-wrapper").addClass("active");
        $(".offcanvas-menu-overlay").addClass("active");
    });


    $(".offcanvas-menu-overlay").on('click', function () {
        $(".offcanvas-menu-wrapper").removeClass("active");
        $(".offcanvas-menu-overlay").removeClass("active");
    });


    // Search Switch
    $('.search-switch').on('click', function () {
        $('.search-model').fadeIn(400);
    });


    $('.search-close-switch').on('click', function () {
        $('.search-model').fadeOut(400, function () {
            $('#search-input').val('');
        });
    });


    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

})(jQuery);


/* =====================================================
   CSRF COOKIE
   ===================================================== */

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (
                cookie.substring(0, name.length + 1) ===
                (name + '=')
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                break;
            }
        }
    }

    return cookieValue;
}


const csrftoken = getCookie('csrftoken');


/* =====================================================
   PRICE RANGE
   ===================================================== */

function applyPrice() {

    const fromInput =
        document.querySelector('input[name="price_from"]');

    const toInput =
        document.querySelector('input[name="price_to"]');

    const priceToggle =
        document.getElementById('price-toggle');

    const priceDropdown =
        document.querySelector('.price-dropdown');


    if (!fromInput || !toInput || !priceToggle) {
        return;
    }


    const from = fromInput.value || 0;

    const to = toInput.value || 'Any';


    priceToggle.value =
        `${from} AED - ${to} AED`;


    if (priceDropdown) {
        priceDropdown.style.display = 'none';
    }
}


/* =====================================================
   PRICE DROPDOWN
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const priceToggle =
        document.getElementById('price-toggle');

    const priceDropdown =
        document.querySelector('.price-dropdown');


    if (priceToggle && priceDropdown) {

        priceToggle.addEventListener('click', function () {

            priceDropdown.style.display = 'block';

        });

    }

});


/* =====================================================
   NAVBAR SCROLL
   ===================================================== */

window.addEventListener('scroll', function () {

    const navbar =
        document.querySelector('.navbar');


    if (!navbar) {
        return;
    }


    if (window.scrollY > 50) {

        navbar.classList.add('scrolled');

    } else {

        navbar.classList.remove('scrolled');

    }

});
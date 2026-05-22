(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);
    
    
    // Initiate the wowjs
    new WOW().init();

})(jQuery);

function toggleReadMore(button) {
    const cardBody =
    button.closest('.c7-article-content');

    const moreText =
    cardBody.querySelector('.more-text');

    moreText.classList.toggle('show');

    button.textContent =
    moreText.classList.contains('show')

    ? button.getAttribute('data-less-text')

    : button.getAttribute('data-more-text');
}



window.addEventListener('scroll', function () {

    const navbar = document.querySelector('.navbar');

    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

});
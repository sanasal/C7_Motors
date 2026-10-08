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

    const article = button.closest('.c7-article-content');

    if (!article) {
        return;
    }

    const moreText = article.querySelector('.more-text');

    if (!moreText) {
        return;
    }

    const isOpen = moreText.classList.contains('show');

    if (isOpen) {
        moreText.classList.remove('show');

        button.textContent =
            button.getAttribute('data-more-text');

    } else {
        moreText.classList.add('show');

        button.textContent =
            button.getAttribute('data-less-text');
    }
}


window.addEventListener('scroll', function () {

    const navbar = document.querySelector('.navbar');

    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }

});
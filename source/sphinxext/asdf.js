$(document).ready(function () {
    activateCarousel('.example-item', '.example-section-indicator');
    activateCarousel('.anyof-item', '.anyof-carousel-indicator');
});

function activateCarousel(itemClass, indicatorClass) {
    item = $(itemClass)[0];
    $(item).addClass('active');

    indicator = $(indicatorClass)[0];
    $(indicator).addClass('active');
}

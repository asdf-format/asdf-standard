$(document).ready(function () {
    first = $('.tab-pane.fade')[0];
    $(first).addClass('in active');

    first_example = $('.example-item')[0];
    $(first_example).addClass('active');

    first_indicator = $('.example-section-indicator')[0];
    $(first_indicator).addClass('active');
});

function onClick(link) {
    current = $('.tab-pane.fade.in.active')[0];

    if ($(link).hasClass('anyof-previous')) {
        prev = $(current).prev();
        if ($(prev).hasClass('tab-pane')) {
            $(current).removeClass('in active');
            $(prev).addClass('in active');
        }
    }
    else if ($(link).hasClass('anyof-next')) {
        next = $(current).next();
        if ($(next).hasClass('tab-pane')) {
            $(current).removeClass('in active');
            $(next).addClass('in active');
        }
    }
    else {
        $(current).removeClass('in active');
        active = document.getElementById(link.title);
        $(active).addClass('in active');
    }
}

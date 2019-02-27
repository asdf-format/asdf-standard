function onClick(link) {
    current = $('.tab-pane.fade.in.active')[0];
    $(current).removeClass('in active');
    id = link.href.split('#')[1];
    active = document.getElementById(id);
    $(active).addClass('in active');
}

$(document).ready(function () {
  $('[id^="header-logo-visibility-toggler"]').on('click', function (e) {
    e.preventDefault();
    const id = $(this).data('id');
    $.post(`/header_management/header_logo/toggle_visibility/${id}`, function () {
      location.reload();
    });
  });

  $('[id^="main-menu-visibility-toggler"]').on('click', function (e) {
    e.preventDefault();
    const id = $(this).data('id');
    $.post(`/header_management/main_menu/toggle_visibility/${id}`, function () {
      location.reload();
    });
  });

  $('[id^="secondary-menu-visibility-toggler"]').on('click', function (e) {
    e.preventDefault();
    const id = $(this).data('id');
    $.post(`/header_management/secondary_menu/toggle_visibility/${id}`, function () {
      location.reload();
    });
  });
});

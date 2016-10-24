//Hide and show nav bar when on home
$(document).ready(function() {
  if ($(window).scrollTop() >= $('.section--home').outerHeight()) {
    $('.navigation.navigation--hidden').addClass('show-translate');
  }

  $(window).scroll(function() {
    var aboutHeight = $('.section--home').outerHeight();
    var scroll = $(window).scrollTop();
    
    if (scroll >= aboutHeight) {
      $('.navigation.navigation--hidden').addClass('show-translate');

    } else {
      $('.navigation.navigation--hidden').removeClass('show-translate');
    }
  });
});
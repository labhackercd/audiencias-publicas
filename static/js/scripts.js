//Hide and show nav bar when on home
$(document).ready(function() {
  var aboutHeight = $('.section--home').outerHeight();

  if ($(window).scrollTop() >= aboutHeight) {
    $('.navigation.navigation--hidden').addClass('show-translate');
  }

  $(window).scroll(function() {
    var scroll = $(window).scrollTop();
    
    if (scroll >= aboutHeight) {
      $('.navigation.navigation--hidden').addClass('show-translate');

    } else {
      $('.navigation.navigation--hidden').removeClass('show-translate');
    }

  });
});
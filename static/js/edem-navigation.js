let searchWrapper = document.querySelector('.search-form'),
    searchInput = document.querySelector('.search-form__input');
    navBar = document.querySelector('.edem-navigation');

document.addEventListener('click', (e) => {
  if (~e.target.className.indexOf('search-form')) {
    searchWrapper.classList.add('focused');
    navBar.classList.add('search-on');
    searchInput.focus();
  } else {
    searchWrapper.classList.remove('focused');
    navBar.classList.remove('search-on');
  }
});

$('.menu-list--dropdown')
  .click(function() {
    $('.menu-list--dropdown, .menu-list--dropdown__wrapper')
      .not(this)
      .removeClass('toggled');

    $(this)
      .toggleClass('toggled');

    $(this)
      .find('.menu-list--dropdown__wrapper')
      .addClass('toggled');
});

$('.menu-list--dropdown__wrapper')
  .click(function() {
    event.stopPropagation();
});

$(document).click(function(e) {
    var target = e.target
    if (!$(target).closest('.toggled').length) {

      $('.toggled')
        .removeClass('toggled');
    }
});

$('.c-hamburger')
  .click(function() {
    $(this).toggleClass('toggled');
    $('.navigation-wrapper').toggleClass('toggled');
});

$('.js-access-link')
  .click(function() {
    if ($(this).hasClass('-active')) {  
      $('.js-access-link').parent('li').removeClass('-active');
    } else {
      $(this).parent('li').addClass('-active');
    }
});

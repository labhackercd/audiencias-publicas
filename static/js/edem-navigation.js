var searchWrapper = document.querySelector('.search-form'),
    searchInput = document.querySelector('.search-form__input'),
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


// eDemocracia open/close edem-access

$('.js-access-link').click(function() {

  $('.edem-access').removeClass('-open');

  if ($(this).parent().hasClass('-active')) { 
    $(this).parent().removeClass('-active');
  } else {
    $('.js-access-link').parent().removeClass('-active');
    $(this).parent().addClass('-active');
  
    if ($(this).hasClass('js-login-link')) {
      $('.js-edem-login').addClass('-open');
    }
  
    else if ($(this).hasClass('js-signup-link')) {
      $('.js-edem-signup').addClass('-open');
    }
  
  }

});


// eDemocracia edem-access input status

$('.form__field').focus(function() {
  $(this).addClass('form__field--filled');
});

$('.form__field').blur(function() {
  if (!$(this).val() == '') {
    $(this).addClass('form__field--filled');
  } else {
    $(this).removeClass('form__field--filled')
  }
});

$('#id_form_login').submit(function(event) {
  event.preventDefault();
  $.ajax({
    type:"POST",
    url: 'http://localhost:8000/ajax/login/', // only development
    data: $(event.target).serialize(),
    success: function(response){
      window.location = window.location;
    },
    error: function(jqXRH){
      $('.form__input-error').text('');
      $.each(jqXRH.responseJSON["data"], function(key, value) {
        if (key == '__all__') {
          console.log(value); // only development
        } else {
          $('[data-input-name="'+key+'"]').text(value).removeAttr('hidden');
        }
      });
    }
  });
});

$('#id_form_validation').submit(function(event) {
  event.preventDefault();
  $.ajax({
    type:"POST",
    url: 'http://localhost:8000/ajax/validation/', // only development
    data: $(event.target).serialize(),
    success: function(response){
      window.sessionStorage.setItem('userData', JSON.stringify(response['data']));
      // go to next sign up page
    },
    error: function(jqXRH) {
      $('.form__input-error').text('');
      $.each(jqXRH.responseJSON["data"], function(key, value) {
        if (key == '__all__') {
          console.log(value); // only development
        } else {
          $('[data-input-name="'+key+'"]').text(value).removeAttr('hidden');
        }
      });
    }
  });
});
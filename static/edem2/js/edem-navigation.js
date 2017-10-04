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

$('.JS-access-link').click(function() {

  $('.JS-access').removeClass('-open');

  if ($(this).parent().hasClass('-active')) {
    $(this).parent().removeClass('-active');
  } else {
    $('.JS-access-link').parent().removeClass('-active');
    $(this).parent().addClass('-active');

    if ($(this).hasClass('JS-login-link')) {
      $('.JS-login').addClass('-open');
      $('.JS-login-link').closest('.menu-list__item').addClass('-active');
    }

    else if ($(this).hasClass('JS-signup-link')) {
      $('.JS-signup').addClass('-open');
      $('.JS-signup-link').closest('.menu-list__item').addClass('-active');
    }
  }
});

function showError(errorMessage) {
  $('.JS-error-box').addClass('-show');
  $('.JS-error-message').text(errorMessage);
}

// eDemocracia edem-access input status

$('.JS-form-field').focus(function() {
  $(this).addClass('form__field--filled');
});

$('.JS-form-field').blur(function() {
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
    url: '/ajax/login/',
    data: $(event.target).serialize(),
    success: function(response){
      location.reload();
    },
    error: function(jqXRH){
      if (jqXRH.status == 0) {
        showError("Verifique sua conexão com a internet.")
      } else if (jqXRH.status == 401) {
        $('.JS-input-error').text('');
        $(event.target)
          .find('.JS-input-error')
          .text(jqXRH.responseJSON['data'])
          .removeAttr('hidden');
      } else {
        showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
      }
    }
  });
});

// Go back function inside signup

$('.JS-prev-form').click(function(){
  $('.login-box__signup-wrapper').removeClass('step-2');
});

// Toggle country/state input

$('.JS-input-action-state').click(function(){
  $(this).closest('.form__input').attr('hidden','');
  $('.JS-input-action-country').closest('.form__input').removeAttr('hidden');
  $('#id_uf').val('').removeClass('form__field--filled');
});

$('.JS-input-action-country').click(function(){
  $(this).closest('.form__input').attr('hidden','');
  $('.JS-input-action-state').closest('.form__input').removeAttr('hidden');
  $('#id_country').val('').removeClass('form__field--filled');
});

// Toggle show password

$('.JS-field-action-password').click(function(){
  var input = $(this).closest('.form__field-container').find('.JS-form-field');
  if (input.attr('type') === 'text') {
    input.attr('type', 'password');
    $(this).children('span').text('Mostrar Senha');
    $(this).children('i').addClass('icon-eye').removeClass('icon-eye-slash');
  } else {
    input.attr('type', 'text');
    $(this).children('span').text('Esconder Senha');
    $(this).children('i').addClass('icon-eye-slash').removeClass('icon-eye');
  }
});

// Close error

$('.JS-error-close').click(function(){
  $('.JS-error-box').removeClass('-show');
});

$('#id_form_validation').submit(function(event) {
  event.preventDefault();
  $.ajax({
    type:"POST",
    url: '/ajax/validation/',
    data: $(event.target).serialize(),
    success: function(response){
      window.sessionStorage
        .setItem('userData', JSON.stringify(response['data']));
      $('.login-box__signup-wrapper').addClass('step-2');
    },
    error: function(jqXRH) {
      if (jqXRH.status == 0) {
        showError('Verifique sua conexão com a internet.');
      } else if (jqXRH.status == 400) {
        $('.JS-input-error').text('');
        $.each(jqXRH.responseJSON["data"], function(key, value) {
          if (key != '__all__') {
            $(event.target)
              .find('[data-input-name="'+key+'"]')
              .text(value)
              .removeAttr('hidden');
          }
        });
      } else {
        showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
      }
    }
  });
});

$('#id_form_signup').submit(function(event) {
  event.preventDefault();
  var signup_form = {}
  $.map($(event.target).serializeArray(), function(n, i){
    signup_form[n['name']] = n['value'];
  });
  var user_data = $.extend(JSON.parse(sessionStorage.userData), signup_form);
  if (grecaptcha.getResponse() == ""){
    alert("Por favor preencha o reCAPTCHA.");
  } else {
    $.ajax({
      type:"POST",
      url: '/ajax/signup/',
      data: user_data,
      success: function(response){
        $('.login-box__signup-wrapper').removeClass('step-2').addClass('step-3');
      },
      error: function(jqXRH) {
        if (jqXRH.status == 0) {
          showError('Verifique sua conexão com a internet.');
        } else if (jqXRH.status == 400) {
          $('.JS-input-error').text('');
          $.each(jqXRH.responseJSON["data"], function(key, value) {
            if (key == 'email') {
              $('.login-box__signup-wrapper').removeClass('step-2');
              $('#id_form_validation')
                .find('[data-input-name="'+key+'"]')
                .text(value)
                .removeAttr('hidden');
            } else if (key != '__all__') {
              $(event.target)
                .find('[data-input-name="'+key+'"]')
                .text(value)
                .removeAttr('hidden');
            }
          });
        } else {

          showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
        }
      }
    });
  }
});

// eDemocracia open/toggle sidebar/signin/signup
$('.JS-openSidebar').click(function() {
  if ($(this).hasClass('-active')) {
    $(this).removeClass('-active');
    $('body').removeClass('-sidebaropen');
  } else {
    $('body').addClass('-sidebaropen')
    $('.JS-sidebarContent').removeClass('-show');
    $('.JS-openSidebar').removeClass('-active');
    $(this).addClass('-active');

    if ($(this).hasClass('JS-showSignin')) {
      $('.JS-signinContent').addClass('-show');
    } else if ($(this).hasClass('JS-showSignup')) {
      $('.JS-signupContent').addClass('-show');
    } else if ($(this).hasClass('JS-showProfile')) {
      $('.JS-profileContent').addClass('-show');
    }
  }
});

// eDemocracia sidebar close button
$('.JS-closeSidebar').click(function(){
  $('.JS-openSidebar').removeClass('-active');
  $('body').removeClass('-sidebaropen');
});

// Close sidebar if click is outside of sidebar or topbar
document.addEventListener('click', function(e) {
  var onEdemCore = $(e.target).closest('.edem-topbar, .edem-sidebar').length;
  var sidebarOpen = $('body').hasClass('-sidebaropen');

  if (!onEdemCore && sidebarOpen ) {
    $('.JS-openSidebar').removeClass('-active');
    $('body').removeClass('-sidebaropen');
  }
});

function showError(errorMessage) {
  $('.JS-accessErrorBox').removeAttr('hidden','');
  $('.JS-accessError').text(errorMessage);
}

// eDemocracia edem-access input status
$('.JS-formInput').focus(function() {
  $(this).closest('.form-field').addClass('-filled');
});

$('.JS-formInput').blur(function() {
  if (!$(this).val() == '') {
    $(this).closest('.form-field').addClass('-filled');
  } else {
    $(this).closest('.form-field').removeClass('-filled');
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
        $('.JS-inputError').text('');
        $(event.target)
          .find('.JS-inputError')
          .text(jqXRH.responseJSON['data'])
          .removeAttr('hidden');
      } else {
        showError("Ocorreu um erro no servidor, tente novamente em alguns instantes.");
      }
    }
  });
});

// Toggle country/state input
$('.JS-inputActionState').on('mousedown', function(e){
  e.preventDefault();
  $(this).closest('.form-field').attr('hidden','').removeClass('-filled');
  $(this).siblings('.JS-formInput').val('');
  $('.JS-inputActionCountry').closest('.form-field').removeAttr('hidden');
});

$('.JS-inputActionCountry').on('mousedown', function(e){
  e.preventDefault();
  $(this).closest('.form-field').attr('hidden','').removeClass('-filled');
  $(this).siblings('.JS-formInput').val('');
  $('.JS-inputActionState').closest('.form-field').removeAttr('hidden');
});

// Toggle show password
$('.JS-fieldActionPassword').on('mousedown', function(e){
  var input = $(this).siblings('.JS-formInput');
  e.preventDefault();
  if (input.attr('type') === 'text') {
    input.attr('type', 'password');
    $(this).text('Mostrar Senha');
  } else {
    input.attr('type', 'text');
    $(this).text('Esconder Senha');
  }
});

// Close error
$('.JS-closeAccessError').click(function(){
  $('.JS-accessErrorBox').attr('hidden', '');
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
        $('.JS-inputError').text('');
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
          $('.JS-inputError').text('');
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

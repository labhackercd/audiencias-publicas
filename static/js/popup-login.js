$('.js-login-button').click(function(e){
  e.preventDefault();
  var target = $(e.target);
  var popup = window.open(target.attr('href'), 'Login e-Democracia', 'height=500,width=600');

  function checkWindow() {
    if(!popup.closed) {
      setTimeout(checkWindow, 100);
      return;
    } else {
      document.location.reload(true);
    }
  }

  checkWindow();
});

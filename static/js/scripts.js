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

//
var createSocket = function(path='') {
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + "://" + window.location.host + window.location.pathname;
  if (ws_path.endsWith('/')) {
    ws_path += path;
  } else {
    ws_path += '/' + path;
  }

  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  return socket;
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

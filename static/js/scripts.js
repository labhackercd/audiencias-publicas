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

//Notify of more messages in chat if not scrolled down to bottom.
$(".chat__list").scroll(function() {
  var chat = $(".chat__list")[0];
  var toBottomValue = chat.scrollHeight - chat.clientHeight;

  if(toBottomValue <= chat.scrollTop + 1) {
    $(".chat__read-more").addClass("chat__read-more--hidden");
  }
});

//
$(".chat__read-more").click(function() {
  var chatBottom = $(".chat__list")[0].scrollHeight;
  $(".chat__list").animate({ scrollTop: chatBottom }, "slow");
});

//
var createSocket = function(path='') {
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + "://" + window.location.host + window.location.pathname + path;

  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  return socket;
}

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

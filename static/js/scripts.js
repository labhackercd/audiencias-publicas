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
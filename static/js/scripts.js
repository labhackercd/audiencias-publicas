var createSocket = function(path='') {
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  var ws_path = ws_scheme + "://" + window.location.host + window.location.pathname + path;

  console.log("Connecting to " + ws_path);
  var socket = new ReconnectingWebSocket(ws_path);

  return socket;
}
var chatSocket = createSocket("chat/stream/");

chatSocket.onmessage = function(message) {
  var data = JSON.parse(message.data);
  var chat = $("#chat");
  chat.append(data.hmtl);
};

$("#chatform").on("submit", function() {
  chatSocket.send(JSON.stringify({
    handler: HANDLER,
    message: $(this).find('input[name=message]').val(),
  }));
  $("#message").val('').focus();
  return false;
});

chatSocket.onopen = function() { console.log("Connected to chat socket"); }
chatSocket.onclose = function() { console.log("Disconnected to chat socket"); }

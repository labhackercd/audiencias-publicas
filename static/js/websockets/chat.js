var chatSocket = createSocket("chat/stream/");

chatSocket.onmessage = function(message) {
  var data = JSON.parse(message.data);
  var chat = $("#chat");


  var chatList = $(".chat__list")[0];
  var chatListHeight = chatList.clientHeight;
  var chatListContentHeight = chatList.scrollHeight;
  var isScrolledToBottom = chatList.scrollHeight - chatList.clientHeight <= chatList.scrollTop + 1;

  chat.append(data.hmtl);

  if(isScrolledToBottom) {
    chatList.scrollTop = chatList.scrollHeight - chatList.clientHeight;
  } else {
    $(".chat__read-more").removeClass("chat__read-more--hidden");
  }

};

$("#chatform").on("submit", function() {
  var chatBottom = $(".chat__list")[0].scrollHeight;

  chatSocket.send(JSON.stringify({
    handler: HANDLER,
    message: $(this).find('input[name=message]').val(),
  }));
  $("#message").val('').focus();

  $(".chat__list")[0].scrollTop = $(".chat__list")[0].scrollHeight;

  return false;
});

chatSocket.onopen = function() { console.log("Connected to chat socket"); }
chatSocket.onclose = function() { console.log("Disconnected to chat socket"); }


var chatList = $('.chat__list');
var isScrolledToBottom = chatList.scrollHeight - chatList.clientHeight <= chatList.scrollTop + 1;
var socket = createSocket();

socket.onopen = function() {
  console.log("Connected to notification socket");
}

socket.onclose = function() {
  console.log("Disconnected to notification socket");
}

socket.onmessage = function(message) {
  console.log("Message received");
  var data = JSON.parse(message.data);

  if (!data.deleted) {
    var exists = $(`[data-video-id=${data.id}]`);
    if (exists.length && !data.is_closed) {
      exists.replaceWith(data.html);
    } else if(exists.length && data.is_closed) {
      exists.remove();
      $(".closed-videos").prepend(data.html);
    } else {
      $(".live-videos").prepend(data.html);
    }
  } else {
    $(`[data-video-id=${data.id}]`).remove();
  }
}
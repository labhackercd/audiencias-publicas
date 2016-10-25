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
      if ($('.video-list--live').children().length === 0) {
        $('.section--live-videos').addClass('hide');
      }
      if ($('.video-list--closed-videos').children().length === 0) {
        $('.section--closed-videos').removeClass('hide');
      } else if ($('.video-list--closed-videos').children().length >= 5) {
        $('.video-list--closed-videos>li:last-child').remove();
      }
      $(".video-list--closed-videos ").prepend(data.html);
    } else {
      if ($('.video-list--live').children().length === 0) {
        $('.section--live-videos').removeClass('hide');
      }
      $(".video-list--live").prepend(data.html);
    }
  } else {
    $(`[data-video-id=${data.id}]`).remove();
  }
}
function previewVideosComponent(socket) {
  const elements = {
    $live: $('.preview--live-videos'),
    $liveList: $('.preview--live-videos .preview__list'),
    $closed: $('.preview--closed-videos'),
    $closedList: $('.preview--closed-videos .preview__list'),
    $calendarList: $('.calendar-rooms'),
  };

  const elementsVar = {
    $closedLastVideo: () => $('.preview--closed-videos .list__video:last-of-type'),
  };

  function evaluateSocketMessage(message) {
    const data = JSON.parse(message.data);
    const $video = $(`[data-video-id=${data.id}]`);
    
    if (data.deleted) {
      $video.remove();
      return;
    }

    const videoExists = $video.length;

    if (data.html.trim().length) {
      if (videoExists && !data.is_closed) {
        $video.replaceWith(data.html);
      } else if (videoExists && data.is_closed) {
        $video.remove();

        if (elements.$liveList.children().length === 0) {
          elements.$live.addClass('hide');
        }

        if (elements.$closedList.children().length === 0) {
          elements.$closed.removeClass('hide');
        } else if (elements.$closedList.children().length >= 5) {
          elementsVar.$closedLastVideo().remove();
        }

        elements.$closedList.prepend(data.html);
      } else if(!videoExists && !data.is_closed) {
        if (elements.$liveList.children().length === 0) {
          elements.$live.removeClass('hide');
        }

        elements.$liveList.prepend(data.html);
        elements.$calendarList.filter(function(){
          return $(this).data('calendar-id') === data.id
        }).remove();
      } else if(!videoExists && data.is_closed) {
        if (elements.$closedList.children().length === 0) {
          elements.$closed.removeClass('hide');
        }

        elements.$closedList.prepend(data.html);
      }
    }
  }

  socket.onmessage = evaluateSocketMessage;
}

export default previewVideosComponent;

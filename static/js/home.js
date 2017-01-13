(function homeAP() { // eslint-disable-line no-unused-vars
  let socket = {};

  const elements = {
    $previewLive: $('.preview--live-videos'),
    $previewLiveList: $('.preview--live-videos .preview__list'),
    $previewClosed: $('.preview--closed-videos'),
    $previewClosedList: $('.preview--closed-videos .preview__list'),
  };

  const elementsVar = {
    $previewClosedLastVideo: () => $('.preview--closed-videos .list__video:last-of-type'),
  };

  function add(message) {
    const data = JSON.parse(message.data);

    if (data.deleted) {
      $(`[data-video-id=${data.id}]`).remove();
    } else {
      const $video = $(`[data-video-id=${data.id}]`);
      const videoExists = $video.length;

      if (videoExists && !data.is_closed) {
        $video.replaceWith(data.html);
      } else if (videoExists && data.is_closed) {
        $video.remove();

        if (elements.$previewLiveList.children().length === 0) {
          elements.$previewLive.addClass('hide');
        }

        if (elements.$previewClosedList.children().length === 0) {
          elements.$previewClosed.removeClass('hide');
        } else if (elements.$previewClosedList.children().length >= 5) {
          elementsVar.$previewClosedLastVideo().remove();
        }

        elements.$previewClosedList.prepend(data.html);
      } else {
        if (elements.$previewLiveList.children().length === 0) {
          elements.$previewLive.removeClass('hide');
        }

        elements.$previewLiveList.prepend(data.html);
      }
    }
  }

  function socketInit() {
    socket = createSocket();

    socket.onmessage = add;
    socket.onopen = () => console.log('Connected to home socket'); // eslint-disable-line no-console
    socket.onclose = () => console.log('Disconnected to home socket'); // eslint-disable-line no-console

    window.onbeforeunload = () => socket.close();
  }

  (function init() {
    socketInit();
  }());
}());

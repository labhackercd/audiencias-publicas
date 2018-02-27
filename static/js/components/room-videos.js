function roomVideosComponent() {
  const elements = {
    $selectVideo: $('.JS-selectVideo'),
  };

  const events = {
    selectVideo() {
      const $videoElements = elements.$selectVideo;
      const $currentVideo = $(this);

      $videoElements.removeClass('-current');
      $currentVideo.addClass('-current');
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      elements.$selectVideo.on('click', events.selectVideo);
    }
  };

  (function init() {
    bindEventsHandlers.onPageLoad();
  }());
}

export default roomVideosComponent;

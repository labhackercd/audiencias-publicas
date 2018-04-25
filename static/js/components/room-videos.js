import playVideoById from './play-video';

function roomVideosComponent() {
  const elements = {
    $selectVideo: $('.JS-selectVideo'),
    $videoFrame: $('.JS-videoFrame'),
  };

  const events = {
    selectVideo() {
      const $videoElements = elements.$selectVideo;
      const $currentVideo = $(this);

      $videoElements.removeClass('-current');
      $currentVideo.addClass('-current');
      elements.$videoFrame.html('<div class="video" id="player"></div>')
      playVideoById($currentVideo.attr('data-video-id'));
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

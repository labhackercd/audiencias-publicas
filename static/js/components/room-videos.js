import playVideoById from './play-video';

function roomVideosComponent() {
  const elements = {
    $selectVideo: $('.JS-selectVideo'),
    $videoFrame: $('.JS-videoFrame'),
    $deleteBtn: $('.JS-deleteVideo'),
  };

  const events = {
    selectVideo(event) {
      const $videoElements = elements.$selectVideo;
      const $currentVideo = $(this);

      console.log($(event.target));

      if (!($(event.target).hasClass('aud-button') || $currentVideo.hasClass('-current'))) {

        $videoElements.removeClass('-current');
        $currentVideo.addClass('-current');

        if (elements.$videoFrame.find('.video').hasClass('-empty')) {

          elements.$videoFrame.html('<div class="video" id="player"></div>')
          playVideoById($currentVideo.attr('data-video-id'));

        } else {

          player.loadVideoById($currentVideo.attr('data-video-id'));

        }
      }
    },
    showDeleteBtn() {
      const $deleteBtn = $('.JS-deleteVideo');
      const $groupName = $('.JS-groupName');

      if ($.inArray($groupName.attr('data-room-group'), HANDLER_GROUPS) > -1) {
        $deleteBtn.removeClass('hide');
      } else if (HANDLER_ADMIN) {
        $deleteBtn.removeClass('hide');
      } else {
        $deleteBtn.addClass('hide');
      }
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      elements.$selectVideo.on('click', events.selectVideo);
      events.showDeleteBtn();
    }
  };

  $('.header').click(function(e){
       //Do nothing if .header was not directly clicked
       if(e.target !== e.currentTarget) return;

       $(this).children(".children").toggle();
  });

  (function init() {
    bindEventsHandlers.onPageLoad();
  }());
}

export default roomVideosComponent;

import playVideoById from './play-video';

function roomVideosComponent() {
  const elements = {
    $selectVideo: $('.JS-selectVideo'),
    $videoFrame: $('.JS-videoFrame'),
    $deleteBtn: $('.JS-deleteVideo'),
    $changeOrder: $('.JS-changeOrder'),
    $thumbList: $('.JS-thumbList')
  };

  function mixItUpInit() {
    elements.$thumbList.mixItUp({
      selectors: {
        target: '.JS-selectVideo',
      },
      layout: {
        display: 'flex',
      },
    });
  }

  const events = {
    selectVideo(event) {
      const $videoElements = elements.$selectVideo;
      const $currentVideo = $(this);

      if (!($(event.target).hasClass('aud-button') || $currentVideo.hasClass('-current'))) {

        $videoElements.removeClass('-current');
        $currentVideo.addClass('-current');

        if (elements.$videoFrame.find('.video').hasClass('-empty')) {
          elements.$videoFrame.html('<div class="video" id="player"></div>')
          playVideoById($currentVideo.attr('data-video-id'));
        } else {
          player.loadVideoById($currentVideo.attr('data-video-id'));
          if ($currentVideo.attr('data-video-id') == $('.JS-alertPlayBtn').attr('data-video-id')) {
            $('.JS-roomAlert').addClass('hide');
          }
        }
        $('.JS-videoStatus').html($currentVideo.attr('data-video-title'));
        if ($currentVideo.attr('data-live-video') == "true") {
          $('.JS-videoStatus').prepend('<span class="live-icon"></span>');
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
    },

    changeOrder() {
      const selectedVideo = $(this).closest('.JS-selectVideo');
      const selectedVideoOrder = selectedVideo.attr('data-video-order');

      if ($(this).hasClass('-left')) {
        selectedVideo.attr('data-video-order', selectedVideo.prev().attr('data-video-order'));
        selectedVideo.prev().attr('data-video-order', selectedVideoOrder);
      } else if ($(this).hasClass('-right')) {
        selectedVideo.attr('data-video-order', selectedVideo.next().attr('data-video-order'));
        selectedVideo.next().attr('data-video-order', selectedVideoOrder);
      }

      elements.$thumbList.mixItUp('sort', 'video-order:asc');
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      elements.$selectVideo.on('click', events.selectVideo);
      elements.$changeOrder.on('click', events.changeOrder);
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
    mixItUpInit();
  }());
}

export default roomVideosComponent;

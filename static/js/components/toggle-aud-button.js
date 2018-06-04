import { getCookie } from '../helpers/cookies';

function toggleAudButtonComponent() {
  const elements = {
    $toggleAudButton: $('.JS-toggleAudButton'),
  };

  function sendOrderedVideos() {
    const url = window.location.pathname + '/ordered-videos/';
    const csrftoken = getCookie('csrftoken');
    const videos = new Array(); 

    $('.JS-selectVideo[data-video-order]').each(function() {
      videos.push({'id': $(this).attr('data-id'),
                   'order': $(this).attr('data-video-order')});
    });

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });

    $.post(url, {
      data: JSON.stringify(videos),
    })
  };

  const events = {
    toggle() {

      const data = {
        toggledText: $(this).data('toggledText'),
        toggledIcon: $(this).data('toggledIcon'),
        untoggledText: $(this).data('untoggledText'),
        untoggledIcon: $(this).data('untoggledIcon')
      }

      if ($(this).hasClass('-toggled')) {
        $(this).text(data.untoggledText).removeClass(data.toggledIcon).removeClass('-toggled').addClass(data.untoggledIcon)
        sendOrderedVideos();
      } else {
        $(this).text(data.toggledText).removeClass(data.untoggledIcon).addClass(data.toggledIcon).addClass('-toggled');
      }
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      elements.$toggleAudButton.on('click', events.toggle);
    }
  };

  (function init() {
    bindEventsHandlers.onPageLoad();
  }());
}

export default toggleAudButtonComponent;

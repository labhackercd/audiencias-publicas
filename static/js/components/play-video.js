function playVideoById(video_id) {
  window.player = new YT.Player('player', {
    height: '',
    width: '',
    videoId: video_id,
    playerVars: { 'rel': 0 },
    events: {
      'onReady': onPlayerReady
    }
  });

  function onPlayerReady(event) {
    event.target.playVideo();
    const currentVideo = $(`.JS-selectVideo[data-video-id=${video_id}]`);
    currentVideo.addClass('-current');
    $('.JS-videoStatus').text(currentVideo.attr('data-video-title'));
    if (currentVideo.attr('data-live-video') == "true") {
      $('.JS-videoStatus').prepend('<span class="live-icon JS-liveIcon"></span>');
    }
  }
}

export default playVideoById;
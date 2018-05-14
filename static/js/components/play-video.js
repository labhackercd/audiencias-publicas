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
    $(`.JS-selectVideo[data-video-id=${video_id}]`).addClass('-current');
  }
}

export default playVideoById;
var Share = {
  results: function(shareButton) {
    var socialNetwork = $(shareButton).data('social');
    var roomId = $(shareButton).closest('.JS-room-wrapper').data('roomId');
    var audienciaUrl = window.location.origin + window.Urls.video_room(roomId);

    var windowOptions = 'height=500,width=1000,left=100,top=100,resizable=yes,' +
      'scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes';

    switch (socialNetwork) {
      case 'facebook':
        var facebookUrl = 'http://www.facebook.com/sharer/sharer.php?u=' + audienciaUrl;
        window.open(facebookUrl, 'popUpWindow', windowOptions);
        break;
      case 'twitter':
        var twitterUrl = 'http://twitter.com/share?text=Eu já estou participando, participe você tambem! &url=' + audienciaUrl;
        window.open(twitterUrl, 'popUpWindow', windowOptions);
        break;
      case 'whatsapp':
        var whatsappUrl = encodeURIComponent('Eu já estou participando, participe você tambem! ') + encodeURIComponent(audienciaUrl);
        window.open('whatsapp://send?text=' + whatsappUrl, 'popUpWindow', windowOptions);
        break;
      default:
        break;
    }
  }
}

$('.JS-share-lnk').click(function(event) {
  Share.results(event.target);
});

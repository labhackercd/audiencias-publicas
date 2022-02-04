import createSocketHelper from '../helpers/create-socket';
import previewVideosComponent from '../components/preview-videos';

const previewVideosSocket = createSocketHelper('preview videos', 'home/stream/');

previewVideosComponent(previewVideosSocket.socket);

window.onbeforeunload = () => previewVideosSocket.close();

$(".show-more a").on("click", function() {
  var $this = $(this); 
  var $contentTruncate = $this.parent().prev().prev("div.content-truncate");
  var $contentFull = $this.parent().prev("div.content-full");
  var linkText = $this.text();   
  if(linkText === "Ver mais"){
    linkText = "Ver menos";
    $contentTruncate.addClass("hide");
    $contentFull.removeClass("hide");
  } else {
    linkText = "Ver mais";
    $contentTruncate.removeClass("hide");
    $contentFull.addClass("hide");
  };

  $this.text(linkText);
});
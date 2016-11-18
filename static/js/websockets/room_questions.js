var questionSocket = createSocket("questions/stream/");
var questionList = $('#questions');

questionList.mixItUp({
  selectors: {
    target: '.questions__item'
  },
  layout: {
    display: 'flex'
  }
});

questionList.on('mixStart', function(){
  $('.vote-block__upvote-button').attr('disabled', '').attr('style','cursor:default; background-color: transparent;');
});
questionList.on('mixEnd', function(){
  $('.vote-block__upvote-button').removeAttr('disabled').removeAttr('style');
});

questionSocket.onmessage = function(message) {
  var data = JSON.parse(message.data);

  var exists = $(`[data-question-id=${data.id}]`);

  if (exists.length) {
    if (data.removeFromList) {
      exists.remove();
    } else {
      exists.replaceWith(data.html);
    }
  } else {
    var questionsContainer = $('#questions');
    questionsContainer.append(data.html);
  }
  questionList.mixItUp('sort', 'question-votes:desc question-id:asc');
  $('.questions__empty').remove();

};


questionSocket.onopen = function() { console.log("Connected to question socket"); }
questionSocket.onclose = function() { console.log("Disconnected to question socket"); }

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

//Question share action
$('.questions__share-button').click(function(){
  $(this).siblings('.questions__share-list').addClass('active')
});

$('.questions__share-close').click(function(){
  $(this).parent('.questions__share-list').removeClass('active')
});

questionList.on('mixStart', function(){
  $('.vote-block__upvote-button').attr('disabled', '').attr('style','cursor:default;');
});
questionList.on('mixEnd', function(){
  $('.vote-block__upvote-button').removeAttr('disabled').removeAttr('style');
});

questionSocket.onmessage = function(message) {
  if(message.data == 'closed'){
    $('#questionform').remove();
    $('#closedQuestionForm').removeClass('hide');
    $('.vote-block__upvote-button').addClass('disabled').attr('disabled');
  }else{
    var data = JSON.parse(message.data);
    var exists = $(`[data-question-id=${data.id}]`);

    if (exists.length) {
      exists.replaceWith(data.html);
    } else {
      var questionsContainer = $('#questions');
      questionsContainer.append(data.html);
    }
    var newElement = $(`[data-question-id=${data.id}]`);
    newElement.find('.question-vote').on('click', upVote);
    newElement.find('.questions__share-link').on('click', shareClick);
    var upvoteButton = newElement.find('.vote-block__upvote-button');
    var totalVotes = newElement.find('.vote-block__total-votes');

    if (HANDLER === newElement.data('question-author')) {
      upvoteButton.addClass('voted disabled');
      upvoteButton.attr('disabled', true);
      upvoteButton.html('Sua Pergunta');
      totalVotes.addClass('voted disabled');
    } else if ($.inArray(HANDLER, data.voteList) > -1) {
      upvoteButton.addClass('voted');
      upvoteButton.html('Apoiada por você');
      totalVotes.addClass('voted');
    } else {
      upvoteButton.removeClass('voted disabled');
      upvoteButton.removeAttr('disabled');
      upvoteButton.html('Votar Nesta Pergunta');
      totalVotes.removeClass('voted');
    }

    questionList.mixItUp('sort', 'question-votes:desc question-id:asc');

    $('.questions__empty').remove();

    //Question share action
    $('.questions__share-button').click(function(){
      $(this).siblings('.questions__share-list').addClass('active')
    });

    $('.questions__share-close').click(function(){
      $(this).parent('.questions__share-list').removeClass('active')
    });
  }

};

$("#questionform").on("submit", function(event) {
  questionSocket.send(JSON.stringify({
    handler: HANDLER,
    question: $(this).find('input[name=question]').val(),
    is_vote: false,
  }));
  $("#question").val('').focus();
  return false;
});

function upVote() {
  if (HANDLER != "") {
    var question_id = $(this).closest('.questions__item').data('question-id');
    questionSocket.send(JSON.stringify({
      handler: HANDLER,
      question: question_id,
      is_vote: true,
    }))
  } else {
    loginRedirect();
  }
}

function shareClick() {
  var pathname = window.location.pathname;
  var url = window.location.href;
  url = url.replace(location.hash, '');
  var question = $(this).closest('.questions__item')
  var questionPath = question.attr('data-question-path');
  url = url.replace(pathname, questionPath);
  var window_opts = 'height=500,width=1000,left=100,top=100,resizable=yes,scrollbars=yes,' +
                    'toolbar=yes,menubar=no,location=no,directories=no, status=yes'

  if ($(this).find('.icon-facebook').length) {
    window.open('http://www.facebook.com/sharer/sharer.php?u=' + url,'popUpWindow', window_opts);
  } else if ($(this).find('.icon-twitter').length) {
    var twitter_url = `http://twitter.com/share?text=Apoie esta pergunta!&url=${url}`;
    window.open(twitter_url, 'popUpWindow', window_opts);
  } else if ($(this).find('.icon-whatsapp').length) {
    var message = encodeURIComponent('As perguntas mais votadas serão respondidas pelos deputados agora! Acesse em ') + encodeURIComponent(url);
    window.open('whatsapp://send?text=' + message)
  }

  return false;
}

$(".question-vote").on('click', upVote);
$('.questions__share-link').on('click', shareClick);

questionSocket.onopen = function() { console.log("Connected to question socket"); }
questionSocket.onclose = function() { console.log("Disconnected to question socket"); }

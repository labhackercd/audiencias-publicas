var questionSocket = createSocket("questions/stream/");

questionSocket.onmessage = function(message) {
  var data = JSON.parse(message.data);
  var questions = $("#questions");
  questions.html(data.html);
  $(".question-vote").on('click', upVote);
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
  var question_id = $(this).closest('.questions__item').data('question-id');
  questionSocket.send(JSON.stringify({
    handler: HANDLER,
    question: question_id,
    is_vote: true,
  }))
}

$(".question-vote").on('click', upVote);

questionSocket.onopen = function() { console.log("Connected to question socket"); }
questionSocket.onclose = function() { console.log("Disconnected to question socket"); }

function questionsListComponent(socket) {
  const elements = {
    $list: $('.room-questions__list'),
    $listEmpty: $('.room-questions__empty'),
  };

  function evaluateSocketMessage(message) {
    const data = JSON.parse(message.data);
    const $existingQuestion = $(`[data-question-id=${data.id}]`);
    const questionExists = $existingQuestion.length;

    if (questionExists) {
      if (data.removeFromList) {
        $existingQuestion.remove();
      } else {
        $existingQuestion.replaceWith(data.html);
      }
    } else {
      elements.$list.append(data.html);
    }

    elements.$listEmpty.remove();
    elements.$list.mixItUp('sort', 'question-votes:desc question-id:asc');
  }

  function mixItUpInit() {
    elements.$list.mixItUp({
      selectors: {
        target: '.list__item',
      },
      layout: {
        display: 'flex',
      },
    });
  }

  (function init() {
    socket.onmessage = evaluateSocketMessage;
    mixItUpInit();
  }());
}

export default questionsListComponent;

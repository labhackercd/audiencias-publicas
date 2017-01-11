(function roomQuestionsListAP() { // eslint-disable-line no-unused-vars
  const socket = createSocket('questions/stream/');

  const elements = {
    $list: $('.room-questions__list'),
    $listEmpty: $('.room-questions__empty'),
  };

  function add(message) {
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

  function socketInit() {
    socket.onmessage = add;
    socket.onopen = () => console.log('Connected to chat socket'); // eslint-disable-line no-console
    socket.onclose = () => console.log('Disconnected to chat socket'); // eslint-disable-line no-console
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
    socketInit();
    mixItUpInit();
  }());
}());

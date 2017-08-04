/* global urlPrefix */
import { getCookie } from '../helpers/cookies';

function questionsListComponent(socket) {
  const elements = {
    $list: $('.room-questions__list'),
    $listEmpty: $('.room-questions__empty'),
    $answeredCheckbox: $('.js-answered-checkbox'),
    $priorityCheckbox: $('.js-priority-checkbox'),
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

    const $question = $(`[data-question-id=${data.id}]`);
    elements.$listEmpty.remove();
    bindEventsHandlers.onAdd($question);
    elements.$list.mixItUp('sort', 'question-priority:desc question-votes:desc question-id:asc');
  }

  function mixItUpInit() {
    elements.$list.mixItUp({
      selectors: {
        target: '.question-card',
      },
      layout: {
        display: 'flex',
      },
    });
  }

  const events = {
    sendAnsweredForm(event) {
      const questionId = $(event.target).closest('[data-question-id]')[0].dataset.questionId;
      const csrftoken = getCookie('csrftoken');

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      $.post(`${urlPrefix}/pergunta/${questionId}/respondida/`, {
        answered: event.target.checked
      })
    },

    sendPriorityForm(event) {
      const questionId = $(event.target).closest('[data-question-id]')[0].dataset.questionId;
      const csrftoken = getCookie('csrftoken');

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      $.post(`${urlPrefix}/pergunta/${questionId}/prioritaria/`, {
        is_priority: event.target.checked
      })
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      socket.onmessage = evaluateSocketMessage;
      elements.$answeredCheckbox.on('change', events.sendAnsweredForm);
      elements.$priorityCheckbox.on('change', events.sendPriorityForm);
    },
    onAdd($question) {
      const $answeredCheckbox = $question.find('.js-answered-checkbox');
      const $priorityCheckbox = $question.find('.js-priority-checkbox');

      $answeredCheckbox.on('change', events.sendAnsweredForm);
      $priorityCheckbox.on('change', events.sendPriorityForm);
    },
  };

  (function init() {
    bindEventsHandlers.onPageLoad();
    mixItUpInit();
  }());
}

export default questionsListComponent;

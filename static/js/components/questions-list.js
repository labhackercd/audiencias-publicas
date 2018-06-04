import { getCookie } from '../helpers/cookies';

function questionsListComponent(socket) {
  const elements = {
    $list: $('.room-questions__list'),
    $listEmpty: $('.room-questions__empty'),
    $answeredCheckbox: $('.JS-answeredCheckbox'),
    $priorityCheckbox: $('.JS-priorityCheckbox'),
    $numberOfQuestions: $('.numberofquestions'),
    $openQuestionManaging: $('.JS-openQuestionManaging'),
    $closeQuestionManaging: $('.JS-closeQuestionManaging'),
    $questionManagingList: $('.JS-questionManagingList'),
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

    if (data.counter) {
      if (data.counter > 1) {
        elements.$numberOfQuestions.html(`${data.counter} perguntas`);
      } else {
        elements.$numberOfQuestions.html(`${data.counter} pergunta`);
      }
    }

    const $question = $(`[data-question-id=${data.id}]`);
    elements.$listEmpty.remove();
    bindEventsHandlers.onAdd($question);
    elements.$list.mixItUp('sort', 'question-answered:asc question-priority:desc question-votes:desc question-id:asc');
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

      $.post(event.target.form.action, {
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

      $.post(event.target.form.action, {
        is_priority: event.target.checked
      })
    },

    openQuestionManaging() {
      $(this).parent().siblings('.JS-questionManagingList').addClass('-active');
    },

    closeQuestionManaging() {
      $(this).closest('.JS-questionManagingList').removeClass('-active');
    },

    showAdminBtns() {
      if ($.inArray($('.JS-groupName').attr('data-room-group'), HANDLER_GROUPS) > -1) {
        $('.JS-openQuestionManaging').removeClass('hide');
      } else if (HANDLER_ADMIN) {
        $('.JS-openQuestionManaging').removeClass('hide');
      } else {
        $('.JS-openQuestionManaging').addClass('hide');
      }
    },
  };

  const bindEventsHandlers = {
    onPageLoad() {
      socket.onmessage = evaluateSocketMessage;
      elements.$answeredCheckbox.on('change', events.sendAnsweredForm);
      elements.$priorityCheckbox.on('change', events.sendPriorityForm);
      elements.$openQuestionManaging.on('click', events.openQuestionManaging);
      elements.$closeQuestionManaging.on('click', events.closeQuestionManaging);
      events.showAdminBtns();
    },
    onAdd($question) {
      const $answeredCheckbox = $question.find('.JS-answeredCheckbox');
      const $priorityCheckbox = $question.find('.JS-priorityCheckbox');
      const $openQuestionManaging = $question.find('.JS-openQuestionManaging');
      const $closeQuestionManaging = $question.find('.JS-closeQuestionManaging');

      $answeredCheckbox.on('change', events.sendAnsweredForm);
      $priorityCheckbox.on('change', events.sendPriorityForm);
      $openQuestionManaging.on('click', events.openQuestionManaging);
      $closeQuestionManaging.on('click', events.closeQuestionManaging);
      events.showAdminBtns();
    },
  };

  (function init() {
    bindEventsHandlers.onPageLoad();
    mixItUpInit();
  }());
}

export default questionsListComponent;

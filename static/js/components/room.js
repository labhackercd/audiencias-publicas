/* global HANDLER, HANDLER_ADMIN, loginRedirect, player */
import sendFormHelper from '../helpers/send-form';
import { getCookie } from '../helpers/cookies';
import characterCounterComponent from './character-counter';

const characterCounter = characterCounterComponent();
characterCounter.setElements();


function roomComponent(socket) {
  const elements = {
    $wrapperQuestion: $('.JS-wrapperQuestion'),
    $questionList: $('.JS-questionsList'),
    $questionlistEmpty: $('.JS-questionlistEmpty'),
    $voteBtnEnabled: $('.JS-voteBtnEnabled'),
    $voteBtn: $('.JS-voteBtn'),
    $totalVotes: $('.JS-totalVotes'),
    $shareListOpenBtn: $('.JS-shareListOpenBtn'),
    $shareListCloseBtn: $('.JS-shareListCloseBtn'),
    $shareListItemLink: $('.JS-shareListItemLink'),
    $readMoreQuestion: $('.JS-readMoreQuestion'),
    $formQuestion: $('.JS-formQuestion'),
    $openQuestionForm: $('.JS-openQuestionForm'),
    $closeQuestionForm: $('.JS-closeQuestionForm'),
    $formInputQuestion: $('.JS-formInputQuestion'),
    $answeredCheckbox: $('.JS-answeredCheckbox'),
    $wrapperChat: $('.JS-wrapperChat'),
    $messages: $('.JS-messages'),
    $messagesList: $('.JS-messagesList'),
    $messagesListEmpty: $('.JS-messagesListEmpty'),
    $readMoreChat: $('.JS-readMoreChat'),
    $formChat: $('.JS-formChat'),
    $formInputChat: $('.JS-formInputChat'),
    $videoFrame: $('.JS-videoFrame'),
    $priorityCheckbox: $('.JS-priorityCheckbox'),
    $answerTimeCheckbox: $('.JS-answerTimeCheckbox'),
    $answerTimeCheckbox: $('.JS-answerTimeCheckbox'),
    $addLinks: $('.JS-addLinks'),
    $linkModal: $('.JS-linkModal'),
    $closeModal: $('.JS-closeModal'),
  };

  const vars = {
    listHeight: () => elements.$questionList[0].offsetHeight,
    listScrollHeight: () => elements.$questionList[0].scrollHeight,
    listScrollTop: () => elements.$questionList[0].scrollTop,
    wrapperHeight: () => elements.$wrapperQuestion[0].offsetHeight,
    wrapperScrollHeight: () => elements.$wrapperQuestion[0].scrollHeight,
    wrapperScrollTop: () => elements.$wrapperQuestion[0].scrollTop,
    messagesListHeight: () => elements.$messagesList[0].offsetHeight,
    messagesListScrollHeight: () => elements.$messagesList[0].scrollHeight,
    messagesListScrollTop: () => elements.$messagesList[0].scrollTop,
  };

  document.querySelectorAll('.JS-addLinks').forEach(function(openLinkModal) {
    openLinkModal.onclick = function() {
      elements.$linkModal.addClass('-open');
    }
  });

  document.querySelectorAll('.JS-closeModal').forEach(function(openLinkModal) {
    openLinkModal.onclick = function() {
      elements.$linkModal.removeClass('-open');
    }
  });

  let isCurrentUserQuestion = false;
  let newQuestionsCount = 0;
  let sendQuestionForm = {};
  let sendChatForm = {};

  function closeQuestionForm() {
    elements.$formQuestion.removeClass('-active');
  }

  function openQuestionForm() {
    elements.$formQuestion.addClass('-active');
    elements.$formInputQuestion.focus();
  }

  function animateToBottomQuestion() {
      elements.$questionList.animate({
        scrollTop: vars.listScrollHeight(),
      }, 600, () => {
        isCurrentUserQuestion = false;
      });

  }

  function animateToBottomChat() {
    elements.$messagesList.animate({ scrollTop: vars.messagesListScrollHeight() }, 'slow');
  }

  function isScrolledToBottomQuestion() {
    return vars.listScrollTop() === (vars.listScrollHeight() - vars.listHeight());
  }

  function isScrolledToBottomChat() {
    return vars.messagesListScrollTop() === (vars.messagesListScrollHeight() - vars.messagesListHeight());
  }

  function scrollToBottomChat() {
    elements.$messagesList[0].scrollTop = vars.messagesListScrollHeight();
  }

  function showReadMoreQuestion() {
    if (newQuestionsCount === 1) {
      elements.$readMoreQuestion.html('Há 1 nova pergunta disponível abaixo');
    } else {
      elements.$readMoreQuestion.html(`Há ${newQuestionsCount} novas perguntas disponíveis abaixo`);
    }

    elements.$readMoreQuestion.removeClass('more');
    elements.$readMoreQuestion.addClass('more -visible');
  }

  function showReadMoreChat() {
    elements.$readMoreChat.removeClass('more');
    elements.$readMoreChat.addClass('more -visible');
  }

  function hideReadMoreQuestion() {
    elements.$readMoreQuestion.removeClass('more -visible');
    elements.$readMoreQuestion.addClass('more');
  }

  function hideReadMoreChat() {
    elements.$readMoreChat.removeClass('more -visible');
    elements.$readMoreChat.addClass('more');
  }

  function updateVoteBlock($question, data) {
    const $upvoteButton = $question.find('.JS-voteBtn');
    const $totalVotes = $question.find('.JS-totalVotes');

    if (data.answered) {
      $upvoteButton.addClass('voted disabled');
      $upvoteButton.attr('disabled', true);
      $upvoteButton.html('Pergunta Respondida');
      $totalVotes.addClass('voted disabled');
    } else if (HANDLER === $question.data('question-author')) {
      $upvoteButton.addClass('voted disabled');
      $upvoteButton.attr('disabled', true);
      $upvoteButton.html('Sua Pergunta');
      $totalVotes.addClass('voted disabled');
    } else if ($.inArray(HANDLER, data.voteList) > -1) {
      $upvoteButton.addClass('voted question-vote JS-voteBtnEnabled');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.html('Apoiada por você');
      $upvoteButton.removeClass('disabled');
      $totalVotes.removeClass('disabled');
      $totalVotes.addClass('voted');
    } else {
      $upvoteButton.removeClass('voted disabled');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.addClass('question-vote JS-voteBtnEnabled');
      $upvoteButton.html('Votar Nesta Pergunta');
      $totalVotes.removeClass('voted');
    }
  }

  function evaluateSocketMessage(message) {
    const questionlistIsEmpty = elements.$questionlistEmpty.length;
    const messagesListIsEmpty = elements.$messagesListEmpty.length;
    if (questionlistIsEmpty) elements.$questionlistEmpty.remove();
    if (messagesListIsEmpty) elements.$messagesListEmpty.remove();

    if (message.data === 'closed') {
      sendChatForm.close();
      sendQuestionForm.close();
      elements.$shareListOpenBtn.remove();
      elements.$voteBtn.addClass('disabled');
      elements.$voteBtn.attr('disabled', true);
      elements.$totalVotes.addClass('voted disabled');
      return;
    }

    const data = JSON.parse(message.data);

    if (data.video) {
        elements.$videoFrame.html(data.html);
    } else if (data.question) {
        const $existingQuestion = $(`[data-question-id=${data.id}]`);
        const questionExists = $existingQuestion.length;

        if (questionExists) {
          $existingQuestion.replaceWith(data.html);
        } else {
          elements.$questionList.append(data.html);

          if (!isScrolledToBottomQuestion() && !isCurrentUserQuestion) {
            newQuestionsCount += 1;
            showReadMoreQuestion();
          }
        }

        const $question = $(`[data-question-id=${data.id}]`);
        const $answeredForm = $question.find('.JS-answeredForm');
        const $priorityForm = $question.find('.JS-priorityForm');
        const $answerTimeForm = $question.find('.JS-answerTimeForm');

        if ($.inArray(data.groupName, HANDLER_GROUPS) > -1) {
          $answeredForm.removeClass('hide');
        } else if (HANDLER_ADMIN) {
          $answeredForm.removeClass('hide');
          $priorityForm.removeClass('hide');
          $answerTimeForm.removeClass('hide');
        } else {
          $answeredForm.addClass('hide');
          $priorityForm.addClass('hide');
          $answerTimeForm.addClass('hide');
        }

        updateVoteBlock($question, data);
        bindEventsHandlers.onAdd($question);
        elements.$questionList.mixItUp('sort', 'question-votes:desc question-id:asc');
    } else if (data.chat) {
        if (isScrolledToBottomChat()) {
          elements.$messagesList.append(data.html);
          animateToBottomChat();
        } else {
          elements.$messagesList.append(data.html);
          showReadMoreChat();
        }
    }
  }

  function mixItUpInit() {
    elements.$questionList.mixItUp({
      selectors: {
        target: '.question-card',
      },
      layout: {
        display: 'flex',
      },
    });
  }

  function sendFormHelperInit() {
    sendQuestionForm = sendFormHelper(elements.$wrapperQuestion);
    sendChatForm = sendFormHelper(elements.$wrapperChat);
  }

  const events = {
    readMoreClickQuestion() {
      animateToBottomQuestion();
    },

    readMoreClickChat() {
      animateToBottomChat();
    },

    questionsScroll() {
      if (isScrolledToBottomQuestion()) {
        newQuestionsCount = 0;
        hideReadMoreQuestion();
      }
    },

    messagesListScroll() {
      if (isScrolledToBottomChat()) hideReadMoreChat();
    },

    vote() {
      if (HANDLER === '') {
        loginRedirect(); // defined in room.html
      } else {
        const id = $(this).closest('.question-card').data('question-id');

        socket.send(JSON.stringify({
          handler: HANDLER,
          question: id,
          is_vote: true,
        }));
      }
    },

    closeQuestionFormClick() {
      closeQuestionForm();
    },

    openQuestionFormClick() {
      openQuestionForm();
      characterCounter.updateCounter();
    },

    openShareList() {
      const $shareList = $(this).siblings('.question-block__share-list');
      $shareList.removeClass('question-block__share-list');
      $shareList.addClass('question-block__share-list--active');
    },

    closeShareList() {
      const $shareList = $(this).parent('.question-block__share-list--active');
      $shareList.removeClass('question-block__share-list--active');
      $shareList.addClass('question-block__share-list');
    },

    share() {
      const socialNetwork = $(this).data('social');

      const $question = $(this).closest('.question-card');
      const questionPath = $question.data('question-path');

      const windowOptions = 'height=500,width=1000,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes';
      const questionUrl = location.href
        .replace(location.hash, '')
        .replace(location.pathname, questionPath);

      const facebookUrl = `http://www.facebook.com/sharer/sharer.php?u=${questionUrl}`;
      const twitterUrl = `http://twitter.com/share?text=Apoie esta pergunta!&url=${questionUrl}`;
      const whatsappMessage = encodeURIComponent('As perguntas mais votadas serão respondidas pelos deputados agora! Acesse em ') + encodeURIComponent(questionUrl);

      switch (socialNetwork) {
        case 'facebook': window.open(facebookUrl, 'popUpWindow', windowOptions); break;
        case 'twitter': window.open(twitterUrl, 'popUpWindow', windowOptions); break;
        case 'whatsapp': window.open(`whatsapp://send?text=${whatsappMessage}`); break;
        default: break;
      }
    },

    sendQuestion(event) {
      event.preventDefault();

      if (sendQuestionForm.isBlank()) return false;

      isCurrentUserQuestion = true;

      socket.send(JSON.stringify({
        handler: HANDLER,
        question: elements.$formInputQuestion.val(),
        is_vote: false,
      }));

      elements.$formInputQuestion.val('').focus();
      animateToBottomQuestion();
      closeQuestionForm();

      return true;
    },

    sendMessage(event) {
      event.preventDefault();

      if (sendChatForm.isBlank()) return false;

      socket.send(JSON.stringify({
        handler: HANDLER, // defined in room.html
        message: elements.$formInputChat.val(),
      }));

      elements.$formInputChat.val('').focus();
      scrollToBottomChat();

      return true;
    },

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

    sendAnswerTimeForm(event) {
      const questionId = $(event.target).closest('[data-question-id]')[0].dataset.questionId;
      const csrftoken = getCookie('csrftoken');

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      var answer_time = '0';
      if(event.target.checked){
        answer_time = player.getCurrentTime();
      };
      $.post(event.target.form.action, {
          answer_time: answer_time
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
    }
  };


  const bindEventsHandlers = {
    onPageLoad() {
      socket.onmessage = evaluateSocketMessage;
      elements.$voteBtnEnabled.on('click', events.vote);
      elements.$shareListOpenBtn.on('click', events.openShareList);
      elements.$shareListCloseBtn.on('click', events.closeShareList);
      elements.$shareListItemLink.on('click', events.share);
      elements.$formQuestion.on('submit', events.sendQuestion);
      elements.$openQuestionForm.on('click', events.openQuestionFormClick);
      elements.$closeQuestionForm.on('click', events.closeQuestionFormClick);
      elements.$questionList.on('scroll', events.questionsScroll);
      elements.$readMoreQuestion.on('click', events.readMoreClickQuestion);
      elements.$answeredCheckbox.on('change', events.sendAnsweredForm);
      elements.$messagesList.on('scroll', events.messagesListScroll);
      elements.$readMoreChat.on('click', events.readMoreClickChat);
      elements.$formChat.on('submit', events.sendMessage);
      setInterval(function() {
        socket.send(JSON.stringify({heartbeat: true}));
      }, 3000);
      elements.$priorityCheckbox.on('change', events.sendPriorityForm);
      elements.$answerTimeCheckbox.on('change', events.sendAnswerTimeForm);
    },

    onAdd($question) {
      const $voteBtnEnabled = $question.find('.JS-voteBtnEnabled');
      const $shareListOpenBtn = $question.find('.JS-shareListOpenBtn');
      const $shareListCloseBtn = $question.find('.JS-shareListCloseBtn');
      const $shareListItemLink = $question.find('.JS-shareListItemLink');
      const $answeredCheckbox = $question.find('.JS-answeredCheckbox');
      const $priorityCheckbox = $question.find('.JS-priorityCheckbox');
      const $answerTimeCheckbox = $question.find('.JS-answerTimeCheckbox');

      $voteBtnEnabled.on('click', events.vote);
      $shareListOpenBtn.on('click', events.openShareList);
      $shareListCloseBtn.on('click', events.closeShareList);
      $shareListItemLink.on('click', events.share);
      $answeredCheckbox.on('change', events.sendAnsweredForm);
      $priorityCheckbox.on('change', events.sendPriorityForm);
      $answerTimeCheckbox.on('change', events.sendAnswerTimeForm);
    },
  };

  (function init() {
    scrollToBottomChat();
    mixItUpInit();
    sendFormHelperInit(); // defined in room.html
    bindEventsHandlers.onPageLoad();
  }());
}

export default roomComponent;

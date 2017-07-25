/* global HANDLER, HANDLER_ADMIN, loginRedirect */
import sendFormHelper from '../helpers/send-form';
import { getCookie } from '../helpers/cookies';

function roomComponent(socket) {
  const elements = {
    $wrapperQuestion: $('.questions'),
    $list: $('.questions__list'),
    $listEmpty: $('.questions__list--empty'),
    $voteBtnEnabled: $('.question-vote'),
    $voteBtn: $('.vote-block__upvote-button'),
    $voteLabel: $('.vote-block__vote-label'),
    $shareListOpenBtn: $('.question-block__share-button'),
    $shareListCloseBtn: $('.share-list__close'),
    $shareListItemLink: $('.question-block__share-list .item__link'),
    $readMoreQuestion: $('.questions__read-more'),
    $formQuestion: $('#questionform'),
    $formInputQuestion: $('#question'),
    $answeredCheckbox: $('.js-answered-checkbox'),
    $wrapperChat: $('.chat'),
    $messages: $('.chat__messages'),
    $messagesList: $('.messages__list'),
    $messagesListEmpty: $('.messages__list--empty'),
    $readMoreChat: $('.chat__read-more'),
    $formChat: $('#chatform'),
    $formInputChat: $('#message'),
    $videoFrame: $('.video__iframe-wrapper'),
  };

  const vars = {
    listHeight: () => elements.$list[0].offsetHeight,
    listScrollHeight: () => elements.$list[0].scrollHeight,
    listScrollTop: () => elements.$list[0].scrollTop,
    wrapperHeight: () => elements.$wrapperQuestion[0].offsetHeight,
    wrapperScrollHeight: () => elements.$wrapperQuestion[0].scrollHeight,
    wrapperScrollTop: () => elements.$wrapperQuestion[0].scrollTop,
    messagesHeight: () => elements.$messages[0].offsetHeight,
    messagesScrollHeight: () => elements.$messages[0].scrollHeight,
    messagesScrollTop: () => elements.$messages[0].scrollTop,
    messagesListHeight: () => elements.$messagesList[0].offsetHeight,
  };

  let isCurrentUserQuestion = false;
  let newQuestionsCount = 0;
  let sendQuestionForm = {};
  let sendChatForm = {};

  function animateToBottomQuestion() {
    if (window.matchMedia('(min-width: 1024px)').matches) {
      elements.$list.animate({
        scrollTop: vars.listScrollHeight(),
      }, 600, () => {
        isCurrentUserQuestion = false;
      });
    } else {
      elements.$wrapperQuestion.animate({
        scrollTop: vars.wrapperScrollHeight(),
      }, 600, () => {
        isCurrentUserQuestion = false;
      });
    }
  }

  function animateToBottomChat() {
    elements.$messages.animate({ scrollTop: vars.messagesListHeight() }, 'slow');
  }

  function isScrolledToBottomQuestion() {
    if (window.matchMedia('(min-width: 1024px)').matches) {
      return vars.listScrollTop() === (vars.listScrollHeight() - vars.listHeight());
    }
    return vars.wrapperScrollTop() === (vars.wrapperScrollHeight() - vars.wrapperHeight());
  }

  function isScrolledToBottomChat() {
    return vars.messagesScrollTop() === (vars.messagesScrollHeight() - vars.messagesHeight());
  }

  function scrollToBottomChat() {
    elements.$messages[0].scrollTop = vars.messagesListHeight();
  }

  function showReadMoreQuestion() {
    if (newQuestionsCount === 1) {
      elements.$readMoreQuestion.html('Há 1 nova pergunta disponível abaixo');
    } else {
      elements.$readMoreQuestion.html(`Há ${newQuestionsCount} novas perguntas disponíveis abaixo`);
    }

    elements.$readMoreQuestion.removeClass('questions__read-more');
    elements.$readMoreQuestion.addClass('questions__read-more--visible');
  }

  function showReadMoreChat() {
    elements.$readMoreChat.removeClass('chat__read-more');
    elements.$readMoreChat.addClass('chat__read-more--visible');
  }

  function hideReadMore() {
    elements.$readMoreQuestion.removeClass('questions__read-more--visible');
    elements.$readMoreQuestion.addClass('questions__read-more');
  }

  function hideReadMore() {
    elements.$readMoreChat.removeClass('chat__read-more--visible');
    elements.$readMoreChat.addClass('chat__read-more');
  }

  function updateVoteBlock($question, data) {
    const $upvoteButton = $question.find('.vote-block__upvote-button');
    const $totalVotes = $question.find('.vote-block__total-votes');

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
      $upvoteButton.addClass('voted question-vote');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.html('Apoiada por você');
      $upvoteButton.removeClass('disabled');
      $totalVotes.removeClass('disabled');
      $totalVotes.addClass('voted');
    } else {
      $upvoteButton.removeClass('voted disabled');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.addClass('question-vote');
      $upvoteButton.html('Votar Nesta Pergunta');
      $totalVotes.removeClass('voted');
    }
  }

  function evaluateSocketMessage(message) {
    const listIsEmpty = elements.$listEmpty.length;
    const messagesListIsEmpty = elements.$messagesListEmpty.length;
    if (listIsEmpty) elements.$listEmpty.remove();
    if (messagesListIsEmpty) elements.$messagesListEmpty.remove();

    if (message.data === 'closed') {
      sendChatForm.close();
      sendQuestionForm.close();
      elements.$shareListOpenBtn.remove();
      elements.$voteBtn.remove();
      elements.$voteLabel.removeClass('hide');
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
          elements.$list.append(data.html);

          if (!isScrolledToBottomQuestion() && !isCurrentUserQuestion) {
            newQuestionsCount += 1;
            showReadMoreQuestion();
          }
        }

        const $question = $(`[data-question-id=${data.id}]`);
        const $answeredForm = $question.find('.js-answered-form');

        if ($.inArray(data.groupName, HANDLER_GROUPS) > -1) {
          $answeredForm.removeClass('hide');
        } else if (HANDLER_ADMIN) {
          $answeredForm.removeClass('hide');
        } else {
          $answeredForm.addClass('hide');
        }

        updateVoteBlock($question, data);
        bindEventsHandlers.onAdd($question);
        elements.$list.mixItUp('sort', 'question-votes:desc question-id:asc');
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
    elements.$list.mixItUp({
      selectors: {
        target: '.list__item',
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
        hideReadMore();
      }
    },

    messagesScroll() {
      if (isScrolledToBottomChat()) hideReadMore();
    },

    vote() {
      if (HANDLER === '') {
        loginRedirect(); // defined in room.html
      } else {
        const id = $(this).closest('.list__item').data('question-id');

        socket.send(JSON.stringify({
          handler: HANDLER,
          question: id,
          is_vote: true,
        }));
      }
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

      const $question = $(this).closest('.list__item');
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

      $.post(`${urlPrefix}/pergunta/${questionId}/respondida/`, {
        answered: event.target.checked
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
      elements.$list.on('scroll', events.questionsScroll);
      elements.$wrapperQuestion.on('scroll', events.questionsScroll);
      elements.$readMoreQuestion.on('click', events.readMoreClickQuestion);
      elements.$answeredCheckbox.on('change', events.sendAnsweredForm);
      elements.$messages.on('scroll', events.messagesScroll);
      elements.$readMoreChat.on('click', events.readMoreClickChat);
      elements.$formChat.on('submit', events.sendMessage);
      setInterval(function() {
        socket.send(JSON.stringify({heartbeat: true}));
      }, 3000);
    },

    onAdd($question) {
      const $voteBtnEnabled = $question.find('.question-vote');
      const $shareListOpenBtn = $question.find('.question-block__share-button');
      const $shareListCloseBtn = $question.find('.share-list__close');
      const $shareListItemLink = $question.find('.question-block__share-list .item__link');
      const $answeredCheckbox = $question.find('.js-answered-checkbox');

      $voteBtnEnabled.on('click', events.vote);
      $shareListOpenBtn.on('click', events.openShareList);
      $shareListCloseBtn.on('click', events.closeShareList);
      $shareListItemLink.on('click', events.share);
      $answeredCheckbox.on('change', events.sendAnsweredForm);
      $('.answered_time__input').inputmask("99:99:99", {
        placeholder: "0",
        numericInput: true,
        showMaskOnHover: false,
      });
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

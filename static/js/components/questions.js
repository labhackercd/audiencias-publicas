/* global HANDLER, loginRedirect */
import sendFormHelper from '../helpers/send-form';

function questionsComponent(socket) {
  const elements = {
    $wrapper: $('.questions'),
    $list: $('.questions__list'),
    $listEmpty: $('.questions__list--empty'),
    $voteBtnEnabled: $('.question-vote'),
    $voteBtn: $('.vote-block__upvote-button'),
    $voteLabel: $('.vote-block__vote-label'),
    $shareListOpenBtn: $('.question-block__share-button'),
    $shareListCloseBtn: $('.share-list__close'),
    $shareListItemLink: $('.question-block__share-list .item__link'),
    $readMore: $('.questions__read-more'),
    $form: $('#questionform'),
    $formInput: $('#question'),
  };

  const vars = {
    listHeight: () => elements.$list[0].offsetHeight,
    listScrollHeight: () => elements.$list[0].scrollHeight,
    listScrollTop: () => elements.$list[0].scrollTop,
    wrapperHeight: () => elements.$wrapper[0].offsetHeight,
    wrapperScrollHeight: () => elements.$wrapper[0].scrollHeight,
    wrapperScrollTop: () => elements.$wrapper[0].scrollTop,
  };

  let isCurrentUserQuestion = false;
  let newQuestionsCount = 0;
  let sendForm = {};

  function animateToBottom() {
    if (window.matchMedia('(min-width: 1024px)').matches) {
      elements.$list.animate({
        scrollTop: vars.listScrollHeight(),
      }, 600, () => {
        isCurrentUserQuestion = false;
      });
    } else {
      elements.$wrapper.animate({
        scrollTop: vars.wrapperScrollHeight(),
      }, 600, () => {
        isCurrentUserQuestion = false;
      });
    }
  }

  function scrollToBottom() {
    elements.$messages[0].scrollTop = vars.messagesListHeight();
  }

  function isScrolledToBottom() {
    if (window.matchMedia('(min-width: 1024px)').matches) {
      return vars.listScrollTop() === (vars.listScrollHeight() - vars.listHeight());
    }
    return vars.wrapperScrollTop() === (vars.wrapperScrollHeight() - vars.wrapperHeight());
  }

  function showReadMore() {
    if (newQuestionsCount === 1) {
      elements.$readMore.html('Há 1 nova pergunta disponível abaixo');
    } else {
      elements.$readMore.html(`Há ${newQuestionsCount} novas perguntas disponíveis abaixo`);
    }

    elements.$readMore.removeClass('questions__read-more');
    elements.$readMore.addClass('questions__read-more--visible');
  }

  function hideReadMore() {
    elements.$readMore.removeClass('questions__read-more--visible');
    elements.$readMore.addClass('questions__read-more');
  }

  function updateVoteBlock($question, data) {
    const $upvoteButton = $question.find('.vote-block__upvote-button');
    const $totalVotes = $question.find('.vote-block__total-votes');

    if (HANDLER === $question.data('question-author')) {
      $upvoteButton.addClass('voted disabled');
      $upvoteButton.attr('disabled', true);
      $upvoteButton.html('Sua Pergunta');
      $totalVotes.addClass('voted disabled');
    } else if ($.inArray(HANDLER, data.voteList) > -1) {
      $upvoteButton.addClass('voted');
      $upvoteButton.html('Apoiada por você');
      $totalVotes.addClass('voted');
    } else {
      $upvoteButton.removeClass('voted disabled');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.html('Votar Nesta Pergunta');
      $totalVotes.removeClass('voted');
    }
  }

  function evaluateSocketMessage(message) {
    const listIsEmpty = elements.$listEmpty.length;
    if (listIsEmpty) elements.$listEmpty.remove();

    if (message.data === 'closed') {
      sendForm.close();
      elements.$shareListOpenBtn.remove();
      elements.$voteBtn.remove();
      elements.$voteLabel.removeClass('hide');
      return;
    }

    const data = JSON.parse(message.data);
    const $existingQuestion = $(`[data-question-id=${data.id}]`);
    const questionExists = $existingQuestion.length;

    if (questionExists) {
      $existingQuestion.replaceWith(data.html);
    } else {
      elements.$list.append(data.html);

      if (!isCurrentUserQuestion) {
        newQuestionsCount += 1;
        showReadMore();
      }
    }

    const $question = $(`[data-question-id=${data.id}]`);

    bindEventsHandlers.onAdd($question);
    updateVoteBlock($question, data);
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

  function sendFormHelperInit() {
    sendForm = sendFormHelper(elements.$wrapper);
  }

  const events = {
    readMoreClick() {
      animateToBottom();
    },

    questionsScroll() {
      if (isScrolledToBottom()) {
        newQuestionsCount = 0;
        hideReadMore();
      }
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

      if (sendForm.isBlank()) return false;

      isCurrentUserQuestion = true;

      socket.send(JSON.stringify({
        handler: HANDLER,
        question: elements.$formInput.val(),
        is_vote: false,
      }));

      elements.$formInput.val('').focus();
      animateToBottom();

      return true;
    },
  };

  const bindEventsHandlers = {
    onPageLoad() {
      socket.onmessage = evaluateSocketMessage;
      elements.$voteBtnEnabled.on('click', events.vote);
      elements.$shareListOpenBtn.on('click', events.openShareList);
      elements.$shareListCloseBtn.on('click', events.closeShareList);
      elements.$shareListItemLink.on('click', events.share);
      elements.$form.on('submit', events.sendQuestion);
      elements.$list.on('scroll', events.questionsScroll);
      elements.$wrapper.on('scroll', events.questionsScroll);
      elements.$readMore.on('click', events.readMoreClick);
    },

    onAdd($question) {
      const $voteBtnEnabled = $question.find('.question-vote');
      const $shareListOpenBtn = $question.find('.question-block__share-button');
      const $shareListCloseBtn = $question.find('.share-list__close');
      const $shareListItemLink = $question.find('.question-block__share-list .item__link');

      $voteBtnEnabled.on('click', events.vote);
      $shareListOpenBtn.on('click', events.openShareList);
      $shareListCloseBtn.on('click', events.closeShareList);
      $shareListItemLink.on('click', events.share);
    },
  };

  (function init() {
    mixItUpInit();
    sendFormHelperInit(); // defined in room.html
    bindEventsHandlers.onPageLoad();
  }());
}

export default questionsComponent;

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
    $form: $('#questionform'),
    $formInput: $('#question'),
  };

  const vars = {
    listScrollHeight: () => elements.$list[0].scrollHeight,
    wrapperScrollHeight: () => elements.$wrapper[0].scrollHeight,
  };

  function animateToBottom() {
    elements.$list.animate({ scrollTop: vars.listScrollHeight() }, 600);
    elements.$wrapper.animate({ scrollTop: vars.wrapperScrollHeight() }, 600);
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
      sendFormHelper(elements.$wrapper).closeForm();
      elements.$shareListOpenBtn.remove();
      elements.$voteBtn.remove();
      elements.$voteLabel.removeClass('hide');
      return;
    }

    const data = JSON.parse(message.data);
    const $existingQuestion = $(`[data-question-id=${data.id}]`);
    const questionExists = $existingQuestion.length;

    if (questionExists) $existingQuestion.replaceWith(data.html);
    else elements.$list.append(data.html);

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

  const sendFormHelperInit = () => sendFormHelper(elements.$wrapper);

  const events = {
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

    submit(event) {
      event.preventDefault();

      socket.send(JSON.stringify({
        handler: HANDLER,
        question: elements.$formInput.val(),
        is_vote: false,
      }));

      elements.$formInput.val('').focus();
      animateToBottom();
    },
  };

  const bindEventsHandlers = {
    onPageLoad() {
      socket.onmessage = evaluateSocketMessage;
      elements.$voteBtnEnabled.on('click', events.vote);
      elements.$shareListOpenBtn.on('click', events.openShareList);
      elements.$shareListCloseBtn.on('click', events.closeShareList);
      elements.$shareListItemLink.on('click', events.share);
      elements.$form.on('submit', events.submit);
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

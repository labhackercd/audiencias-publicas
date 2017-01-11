/* global sendFormAP, HANDLER, loginRedirect */
(function questionsAP() { // eslint-disable-line no-unused-vars
  const socket = createSocket('questions/stream/');

  const elements = {
    $wrapper: $('.questions'),
    $list: $('.questions__list'),
    $listEmpty: $('.questions__list--empty'),
    $voteBtn: $('.question-vote'),
    $shareListOpenBtn: $('.question-block__share-button'),
    $shareListCloseBtn: $('.share-list__close'),
    $shareListItemLink: $('.question-block__share-list .item__link'),
    $form: $('#questionform'),
    $formInput: $('#question'),
  };

  const vars = {
    listScrollHeight: () => elements.$list[0].scrollHeight,
  };

  function animateToBottom() {
    elements.$list.animate({ scrollTop: vars.listScrollHeight() }, 600);
  }

  function add(message) {
    if (message.data === 'closed') {
      sendFormAP(elements.wrapper).closeForm();
    } else {
      const data = JSON.parse(message.data);
      const $existingQuestion = $(`[data-question-id=${data.id}]`);
      const questionExists = $existingQuestion.length;

      if (questionExists) {
        $existingQuestion.replaceWith(data.html);
      } else {
        elements.$list.append(data.html);
        animateToBottom();
      }

      elements.$listEmpty.remove();

      const $question = $(`[data-question-id=${data.id}]`);
      const $upvoteButton = $question.find('.vote-block__upvote-button');
      const $totalVotes = $question.find('.vote-block__total-votes');
      const $voteBtn = $question.find('.question-vote');

      $voteBtn.on('click', events.vote);

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

      elements.$list.mixItUp('sort', 'question-votes:desc question-id:asc');
    }
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

  const sendFormAPInit = () => sendFormAP(elements.$wrapper);

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
    },
  };

  function bindEventsHandlers() {
    elements.$voteBtn.on('click', events.vote);
    elements.$shareListOpenBtn.on('click', events.openShareList);
    elements.$shareListCloseBtn.on('click', events.closeShareList);
    elements.$shareListItemLink.on('click', events.share);
    elements.$form.on('submit', events.submit);
  }

  (function init() {
    socketInit();
    mixItUpInit();
    sendFormAPInit(); // defined in room.html
    bindEventsHandlers();
  }());
}());

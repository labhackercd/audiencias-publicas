/* global sendFormAP HANDLER */
(function chatAP() { // eslint-disable-line no-unused-vars
  const socket = createSocket('chat/stream/');

  const elements = {
    $wrapper: $('.chat'),
    $messages: $('.chat__messages'),
    $messagesList: $('.messages__list'),
    $readMore: $('.chat__read-more'),
    $form: $('#chatform'),
    $formInput: $('#message'),
  };

  const vars = {
    messagesHeight: () => elements.$messages[0].offsetHeight,
    messagesScrollHeight: () => elements.$messages[0].scrollHeight,
    messagesScrollTop: () => elements.$messages[0].scrollTop,
    messagesListHeight: () => elements.$messagesList[0].offsetHeight,
  };

  function isScrolledToBottom() {
    return vars.messagesScrollTop() === (vars.messagesScrollHeight() - vars.messagesHeight());
  }

  function scrollToBottom() {
    elements.$messages[0].scrollTop = vars.messagesListHeight();
  }

  function animateToBottom() {
    elements.$messages.animate({ scrollTop: vars.messagesListHeight() }, 'slow');
  }

  function showReadMore() {
    elements.$readMore.removeClass('chat__read-more');
    elements.$readMore.addClass('chat__read-more--visible');
  }

  function hideReadMore() {
    elements.$readMore.removeClass('chat__read-more--visible');
    elements.$readMore.addClass('chat__read-more');
  }

  function addMessage(message) {
    if (message.data === 'closed') {
      sendFormAP(elements.$wrapper).closeForm();
    } else {
      const data = JSON.parse(message.data);

      if (isScrolledToBottom()) {
        elements.$messagesList.append(data.hmtl);
        scrollToBottom();
      } else {
        elements.$messagesList.append(data.hmtl);
        showReadMore();
      }
    }
  }

  function socketInit() {
    socket.onmessage = addMessage;
    socket.onopen = () => console.log('Connected to chat socket'); // eslint-disable-line no-console
    socket.onclose = () => console.log('Disconnected to chat socket'); // eslint-disable-line no-console
  }

  const sendFormAPInit = () => sendFormAP(elements.$wrapper);

  const events = {
    readMoreClick() {
      animateToBottom();
    },

    readMoreScroll() {
      if (isScrolledToBottom()) hideReadMore();
    },

    formInputKeyDown(event) {
      if (event.which === 13) event.preventDefault();
    },

    formInputKeyUp(event) {
      if (event.which === 13) elements.$form.trigger('submit');
    },

    sendMessage(event) {
      event.preventDefault();

      socket.send(JSON.stringify({
        handler: HANDLER, // defined in room.html
        message: elements.$formInput.val(),
      }));

      elements.$formInput.val('').focus();
      scrollToBottom();
    },
  };

  function bindEventsHandlers() {
    elements.$messages.on('scroll', events.readMoreScroll);
    elements.$readMore.on('click', events.readMoreClick);
    elements.$form.on('submit', events.sendMessage);
  }

  (function init() {
    socketInit();
    scrollToBottom();
    sendFormAPInit(); // defined in room.html
    bindEventsHandlers();
  }());
}());

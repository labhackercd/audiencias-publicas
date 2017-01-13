/* global HANDLER */
import sendFormModule from '../modules/send-form';

function chatComponent(socket) {
  const elements = {
    $wrapper: $('.chat'),
    $messages: $('.chat__messages'),
    $messagesList: $('.messages__list'),
    $messagesListEmpty: $('.messages__list--empty'),
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

  function evaluateSocketMessage(message) {
    const messagesListIsEmpty = elements.$messagesListEmpty.length;
    if (messagesListIsEmpty) elements.$messagesListEmpty.remove();

    if (message.data === 'closed') {
      sendFormModule(elements.$wrapper).closeForm();
    } else {
      const data = JSON.parse(message.data);

      if (isScrolledToBottom()) {
        elements.$messagesList.append(data.hmtl);
        animateToBottom();
      } else {
        elements.$messagesList.append(data.hmtl);
        showReadMore();
      }
    }
  }

  const sendFormModuleInit = () => sendFormModule(elements.$wrapper);

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
    socket.onmessage = evaluateSocketMessage;
    elements.$messages.on('scroll', events.readMoreScroll);
    elements.$readMore.on('click', events.readMoreClick);
    elements.$form.on('submit', events.sendMessage);
  }

  (function init() {
    scrollToBottom();
    sendFormModuleInit();
    bindEventsHandlers();
  }());
}

export default chatComponent;

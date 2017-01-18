/* global HANDLER */
import sendFormHelper from '../helpers/send-form';

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

  let sendForm = {};

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
      sendForm.close();
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

  function sendFormHelperInit() {
    sendForm = sendFormHelper(elements.$wrapper);
  }

  const events = {
    readMoreClick() {
      animateToBottom();
    },

    readMoreScroll() {
      if (isScrolledToBottom()) hideReadMore();
    },

    sendMessage(event) {
      event.preventDefault();

      if (sendForm.isBlank()) return false;

      socket.send(JSON.stringify({
        handler: HANDLER, // defined in room.html
        message: elements.$formInput.val(),
      }));

      elements.$formInput.val('').focus();
      scrollToBottom();

      return true;
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
    sendFormHelperInit();
    bindEventsHandlers();
  }());
}

export default chatComponent;

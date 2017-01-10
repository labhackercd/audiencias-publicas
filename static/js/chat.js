function chat() {
  var chatEl = $('.chat');

  var elements = {
    messages: $('.chat__messages'),
    messagesList: $('.messages__list'),
    readMore: $('.chat__read-more'),
  };

  var vars = {
    messagesHeight: elements.messages[0].offsetHeight,
    messagesScrollHeight: function messagesScrollTop() { return elements.messages[0].scrollHeight },
    messagesScrollTop: function messagesScrollTop() { return elements.messages[0].scrollTop },

    messagesListHeight: elements.messagesList[0].offsetHeight,
  };

  function isScrolledToBottom() {
    return vars.messagesScrollTop() === (vars.messagesScrollHeight() - vars.messagesHeight)
  }

  function scrollToBottom() {
    elements.messages[0].scrollTop = vars.messagesListHeight;
  }

  function showReadMore() {
    elements.readMore.addClass('show-translate');
  }

  return {
    isScrolledToBottom: isScrolledToBottom,
    scrollToBottom: scrollToBottom,
    showReadMore: showReadMore,
  };
}

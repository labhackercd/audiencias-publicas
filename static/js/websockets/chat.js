/* global chatAP, HANDLER */
const chat = chatAP(); // Using 'chatAP' module from '../chat.js'

const chatSocket = createSocket('chat/stream/');
const $chatForm = $('#chatform');

$(document).ready(() => chat.scrollToBottom());

chatSocket.onmessage = (message) => {
  if (message.data === 'closed') {
    chat.closeForm();
  } else {
    const data = JSON.parse(message.data);
    const messagesListEl = chat.elements.messagesList;

    if (chat.isScrolledToBottom()) {
      messagesListEl.append(data.hmtl);
      chat.scrollToBottom();
    } else {
      messagesListEl.append(data.hmtl);
      chat.toggleReadMore('show');
    }
  }
};

$chatForm.on('submit', function sendMessage(event) {
  const $formMessage = $(this).find('#message');

  event.preventDefault();

  chatSocket.send(JSON.stringify({
    handler: HANDLER, // defined in room.html
    message: $formMessage.val(),
  }));

  $formMessage.val('').focus();
  chat.scrollToBottom();
});

chatSocket.onopen = () => console.log('Connected to chat socket'); // eslint-disable-line no-console
chatSocket.onclose = () => console.log('Disconnected to chat socket'); // eslint-disable-line no-console

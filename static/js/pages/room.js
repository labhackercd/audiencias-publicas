import createSocket from '../helpers/create-socket';
import questionsComponent from '../components/questions';
import chatComponent from '../components/chat';
import tabsNavComponent from '../components/tabs-nav';

const questionsSocket = createSocket('questions', 'questions/stream/');
const chatSocket = createSocket('chat', 'chat/stream/');

questionsComponent(questionsSocket.socket);
chatComponent(chatSocket.socket);

tabsNavComponent();

window.onbeforeunload = () => {
  questionsSocket.close();
  chatSocket.close();
};

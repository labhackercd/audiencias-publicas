import socketModule from '../modules/socket';
import questionsComponent from '../components/questions';
import chatComponent from '../components/chat';
import tabsNavComponent from '../components/tabs-nav';

const questionsSocket = socketModule('questions', 'questions/stream/');
const chatSocket = socketModule('chat', 'chat/stream/');

questionsComponent(questionsSocket.socket);
chatComponent(chatSocket.socket);

tabsNavComponent();

window.onbeforeunload = () => {
  questionsSocket.close();
  chatSocket.close();
};

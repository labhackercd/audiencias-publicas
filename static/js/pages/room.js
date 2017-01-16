import createSocketHelper from '../helpers/create-socket';
import questionsComponent from '../components/questions';
import chatComponent from '../components/chat';
import tabsNavComponent from '../components/tabs-nav';
import characterCounterComponent from '../components/character-counter';

const questionsSocket = createSocketHelper('questions', 'questions/stream/');
const chatSocket = createSocketHelper('chat', 'chat/stream/');

questionsComponent(questionsSocket.socket);
chatComponent(chatSocket.socket);

tabsNavComponent();
characterCounterComponent();

window.onbeforeunload = () => {
  questionsSocket.close();
  chatSocket.close();
};

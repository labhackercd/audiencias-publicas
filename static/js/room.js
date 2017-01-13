import questionsAP from './questions';
import chatAP from './chat';

const roomQuestionsAP = questionsAP();
const roomChatAP = chatAP();

window.onbeforeunload = () => {
  roomQuestionsAP.socket.close();
  roomChatAP.socket.close();
};

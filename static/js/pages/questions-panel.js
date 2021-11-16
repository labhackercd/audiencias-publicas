import createSocketHelper from '../helpers/create-socket';
import questionsListComponent from '../components/questions-list';


const questionsPanelSocket = createSocketHelper('questions-list', 'stream/');

questionsPanelSocket.socket.onopen = () => {
  console.log('Connected to questions panel socket'); // eslint-disable-line no-console
};

questionsListComponent(questionsPanelSocket.socket);

window.onbeforeunload = () => {
  questionsListComponent.close();
};

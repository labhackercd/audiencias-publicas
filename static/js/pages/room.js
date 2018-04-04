import createSocketHelper from '../helpers/create-socket';
import roomComponent from '../components/room';
import tabsNavComponent from '../components/tabs-nav';
import characterCounterComponent from '../components/character-counter';
import onlineUsersComponent from '../components/online-users';
import roomVideosComponent from '../components/room-videos';
import modalsComponent from '../components/modals';
import countdownTimerComponent from '../components/countdown-timer';
import toggleAudButtonComponent from '../components/toggle-aud-button';


const onlineUsers = onlineUsersComponent();

const roomSocket = createSocketHelper('room', 'stream/');

roomSocket.socket.onopen = () => {
  console.log('Connected to room socket'); // eslint-disable-line no-console
  onlineUsers.get();
};

roomComponent(roomSocket.socket);

window.onbeforeunload = () => {
  roomSocket.close();
};

characterCounterComponent().init();

roomVideosComponent();

modalsComponent();

countdownTimerComponent();

toggleAudButtonComponent();

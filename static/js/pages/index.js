import socketModule from '../modules/socket';
import previewVideosComponent from '../components/preview-videos';

const previewVideos = previewVideosComponent();
const socket = socketModule('home', '', previewVideos.evaluateSocketMessage);

window.onbeforeunload = () => socket.close();

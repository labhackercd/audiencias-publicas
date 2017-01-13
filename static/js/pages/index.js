import socketModule from '../modules/socket';
import previewVideosComponent from '../components/preview-videos';

const previewVideosSocket = socketModule('preview videos', '');

previewVideosComponent(previewVideosSocket.socket);

window.onbeforeunload = () => previewVideosSocket.close();

import createSocket from '../helpers/create-socket';
import previewVideosComponent from '../components/preview-videos';

const previewVideosSocket = createSocket('preview videos', '');

previewVideosComponent(previewVideosSocket.socket);

window.onbeforeunload = () => previewVideosSocket.close();

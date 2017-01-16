import createSocketHelper from '../helpers/create-socket';
import previewVideosComponent from '../components/preview-videos';

const previewVideosSocket = createSocketHelper('preview videos', '');

previewVideosComponent(previewVideosSocket.socket);

window.onbeforeunload = () => previewVideosSocket.close();

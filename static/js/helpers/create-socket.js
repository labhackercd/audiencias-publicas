import ReconnectingWebSocket from 'reconnectingwebsocket';

function createSocket(name = 'unknown', path = '') {
  function setSocketPath() {
    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    let wsPath = `${wsScheme}://${window.location.host}${window.location.pathname}`;
    wsPath = wsPath.endsWith('/') ? `${wsPath}${path}` : `${wsPath}/${path}`;

    console.log(`Connecting to ${wsPath}`); // eslint-disable-line no-console
    return wsPath;
  }

  const socketPath = setSocketPath(path);
  const socket = new ReconnectingWebSocket(socketPath);

  const close = () => socket.close();

  socket.onopen = () => console.log(`Connected to ${name} socket`); // eslint-disable-line no-console
  socket.onclose = () => console.log(`Disconnected to ${name} socket`); // eslint-disable-line no-console

  return { socket, close };
}

export default createSocket;

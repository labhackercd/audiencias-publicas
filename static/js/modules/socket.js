import createSocket from '../create-socket';

function socketModule(name = 'unknown', path = '') {
  const socket = createSocket(path);

  const close = () => socket.close();

  socket.onopen = () => console.log(`Connected to ${name} socket`); // eslint-disable-line no-console
  socket.onclose = () => console.log(`Disconnected to ${name} socket`); // eslint-disable-line no-console

  return { socket, close };
}

export default socketModule;

function socketModule(socketName = 'unknown', socketCreateParam = '') {
  const socket = createSocket(socketCreateParam);

  const close = () => socket.close();

  socket.onopen = () => console.log(`Connected to ${socketName} socket`); // eslint-disable-line no-console
  socket.onclose = () => console.log(`Disconnected to ${socketName} socket`); // eslint-disable-line no-console

  return { socket, close };
}

export default socketModule;

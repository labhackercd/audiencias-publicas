function socketModule(socketName = 'unknown', socketCreateParam = '', evaluateMessage) {
  const socket = createSocket(socketCreateParam);

  const close = () => socket.close();

  socket.onmessage = message => evaluateMessage(message);
  socket.onopen = () => console.log(`Connected to ${socketName} socket`); // eslint-disable-line no-console
  socket.onclose = () => console.log(`Disconnected to ${socketName} socket`); // eslint-disable-line no-console

  return { close };
}

export default socketModule;

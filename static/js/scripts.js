function createSocket(path = '') {
  const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  let wsPath = `${wsScheme}://${window.location.host}${window.location.pathname}`;
  if (wsPath.endsWith('/')) {
    wsPath += path;
  } else {
    wsPath += `/${path}`;
  }

  console.log(`Connecting to ${wsPath}`); // eslint-disable-line no-console
  const socket = new ReconnectingWebSocket(wsPath);

  return socket;
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

/* global videoApiUrl */
function onlineUsersComponent() {
  const onlineUsersEl = document.getElementById('online-users');

  function update(usersCount) {
    onlineUsersEl.innerHTML = usersCount;
  }

  function get() {
    $.get(roomApiUrl, (data) => {
      update(data.online_users);
    });
  }

  setInterval(() => get(), 5000);

  return { get };
}

export default onlineUsersComponent;

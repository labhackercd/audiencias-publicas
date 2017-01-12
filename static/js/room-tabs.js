(function tabsNavAP() {
  const elements = {
    $room: $('.room'),
    $wrapper: $('.tabs-nav'),
    $links: $('.tabs-nav__list .item__link'),
  };

  const events = {
    changeTab() {
      const dataTab = $(this).data('tab');
      elements.$room.attr('data-tab', dataTab);
    },
  };

  function bindEventsHandlers() {
    elements.$links.on('click', events.changeTab);
  }

  (function init() {
    bindEventsHandlers();
  }());
}());

(function tabsNavAP() {
  const elements = {
    $room: $('.room'),
    $itemMarker: $('.tabs-nav .list__item-marker'),
    $links: $('.tabs-nav__list .item__link'),
  };

  const events = {
    changeTab() {
      const dataTab = $(this).data('tab');

      elements.$itemMarker.attr('data-tab', dataTab);
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

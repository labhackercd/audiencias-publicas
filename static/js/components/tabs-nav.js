function tabsNavComponent() {
  const elements = {
    $room: $('.room'),
    $wrapper: $('.tabs-nav'),
    $itemMarker: $('.tabs-nav .list__item-marker'),
    $links: $('.tabs-nav__list .item__link'),
  };

  const tabs = {
    count: elements.$links.length,
    activeDataTabIndex: () => parseInt(elements.$room.attr('data-tab-index'), 10),
  };

  const touch = {
    direction: 0,
    positionX: {
      start: 0,
      end: 0,
    },
  };

  function updateActiveTab(dataTabIndex) {
    elements.$itemMarker.attr('data-tab-index', dataTabIndex);
    elements.$room.attr('data-tab-index', dataTabIndex);
  }

  function setTouchPositionX(key, value) {
    touch.positionX[key] = value;
  }

  function resetTouchPositionX() {
    touch.positionX.start = 0;
    touch.positionX.end = 0;
  }

  const events = {
    changeTab: event => updateActiveTab(event.target.dataset.tabIndex),

    touchStart: event => setTouchPositionX('start', event.touches[0].pageX),
    touchMove: event => setTouchPositionX('end', event.touches[0].pageX),
    touchEnd: () => {
      const touchMoved = touch.positionX.end !== 0;
      if (!touchMoved) return;

      const touchPositionXMoved = touch.positionX.start - touch.positionX.end;
      const movedEnough = Math.abs(touchPositionXMoved) > 80;

      if (!movedEnough) return;

      touch.direction = touchPositionXMoved > 0 ? 1 : -1;

      if (tabs.activeDataTabIndex() === 0 && touch.direction === -1) return;
      if (tabs.activeDataTabIndex() === tabs.count && touch.direction === 1) return;

      const newTabIndex = tabs.activeDataTabIndex() + touch.direction;
      updateActiveTab(newTabIndex);
      resetTouchPositionX();
    },
  };

  function bindEventsHandlers() {
    elements.$links.on('click', events.changeTab);
    window.addEventListener('touchstart', events.touchStart);
    window.addEventListener('touchend', events.touchEnd);
    window.addEventListener('touchmove', events.touchMove);
  }

  (function init() {
    bindEventsHandlers();
  }());
}

export default tabsNavComponent;

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
    positionY: {
      start: 0,
      end: 0,
    },
  };

  function updateActiveTab(dataTabIndex) {
    elements.$itemMarker.attr('data-tab-index', dataTabIndex);
    elements.$room.attr('data-tab-index', dataTabIndex);
  }

  function setTouchPosition(key, touchEvent) {
    touch.positionX[key] = touchEvent.clientX;
    touch.positionY[key] = touchEvent.clientY;
  }

  function resetTouchPosition() {
    touch.positionX.start = 0;
    touch.positionX.end = 0;

    touch.positionY.start = 0;
    touch.positionY.end = 0;
  }

  const events = {
    changeTab: event => updateActiveTab(event.target.dataset.tabIndex),

    touchStart: (event) => {
      resetTouchPosition();
      setTouchPosition('start', event.touches[0]);
    },

    touchMove: (event) => {
      setTouchPosition('end', event.touches[0]);
    },

    touchEnd: () => {
      const touchMoved = touch.positionX.end !== 0;
      if (!touchMoved) return;

      const touchPositionXMoved = touch.positionX.start - touch.positionX.end;
      const xMovedEnough = Math.abs(touchPositionXMoved) > 80;

      const touchPositionYMoved = touch.positionY.end - touch.positionY.start;
      const yMovedTooMuch = Math.abs(touchPositionYMoved) > 50;

      if (!xMovedEnough || yMovedTooMuch) return;

      touch.direction = touchPositionXMoved > 0 ? 1 : -1;

      if (tabs.activeDataTabIndex() === 0 && touch.direction === -1) return;
      if (tabs.activeDataTabIndex() === (tabs.count - 1) && touch.direction === 1) return;

      const newTabIndex = tabs.activeDataTabIndex() + touch.direction;
      updateActiveTab(newTabIndex);
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

tabsNavComponent();

(function tabsNavAP() {
  const elements = {
    $room: $('.room'),
    $itemMarker: $('.tabs-nav .list__item-marker'),
    $links: $('.tabs-nav__list .item__link'),
  };

  const vars = {
    tabs: {},
    tabsCount: elements.$links.length,
    activeTab: () => elements.$room.attr('data-tab'),
  };

  const touchPosition = {
    x: {
      start: 0,
      end: 0,
    },
  };

  function setTabs() {
    elements.$links.each(function setTab(index) {
      const dataTab = $(this).attr('data-tab');
      vars.tabs[index] = dataTab;
    });
  }

  function setDataTab(dataTab) {
    elements.$itemMarker.attr('data-tab', dataTab);
    elements.$room.attr('data-tab', dataTab);
  }

  function setTouchPositionX(key, value) {
    touchPosition.x[key] = value;
  }

  function getTabIndex() {
    const activeTab = vars.activeTab();
    let activeTabIndex = 0;

    for (let index = 0; index < vars.tabsCount; index += 1) {
      if (vars.tabs[index] === activeTab) {
        activeTabIndex = index;
      }
    }

    return activeTabIndex;
  }

  const events = {
    changeTab: (event) => {
      const dataTab = event.target.dataset.tab;
      setDataTab(dataTab);
    },

    touchStart: () => setTouchPositionX('start', event.touches[0].pageX),
    touchMove: () => setTouchPositionX('end', event.touches[0].pageX),
    touchEnd: () => {
      const touchMoved = touchPosition.x.start - touchPosition.x.end;

      if (Math.abs(touchMoved) < 100) return;

      const activeTabIndex = getTabIndex();
      const swipeDirection = touchMoved > 0 ? 1 : -1;

      if (activeTabIndex === 0 && swipeDirection === -1) return;
      if (activeTabIndex === vars.tabsCount && swipeDirection === 1) return;

      const nextTabIndex = activeTabIndex + swipeDirection;
      const nextTabDataTab = vars.tabs[nextTabIndex];

      setDataTab(nextTabDataTab);
    },
  };

  function bindEventsHandlers() {
    elements.$links.on('click', events.changeTab);
    window.addEventListener('touchstart', events.touchStart);
    window.addEventListener('touchend', events.touchEnd);
    window.addEventListener('touchmove', events.touchMove);
  }

  (function init() {
    setTabs();
    bindEventsHandlers();
  }());
}());

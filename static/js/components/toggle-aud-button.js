function toggleAudButtonComponent() {
  const elements = {
    $toggleAudButton: $('.JS-toggleAudButton'),
  };

  const events = {
    toggle() {

      const data = {
        toggledText: $(this).data('toggledText'),
        toggledIcon: $(this).data('toggledIcon'),
        untoggledText: $(this).data('untoggledText'),
        untoggledIcon: $(this).data('untoggledIcon')
      }

      if ($(this).hasClass('-toggled')) {
        $(this).text(data.untoggledText).removeClass(data.toggledIcon).removeClass('-toggled').addClass(data.untoggledIcon)
      } else {
        $(this).text(data.toggledText).removeClass(data.untoggledIcon).addClass(data.toggledIcon).addClass('-toggled');
      }
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      elements.$toggleAudButton.on('click', events.toggle);
    }
  };

  (function init() {
    bindEventsHandlers.onPageLoad();
  }());
}

export default toggleAudButtonComponent;

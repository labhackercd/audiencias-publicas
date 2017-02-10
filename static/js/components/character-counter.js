function characterCounterComponent() {
  const elements = {
    $input: [],
    $wrapper: $('[class$="__character-counter"]'),
    $actualLength: $('.character-counter__actual-length'),
  };

  function setElements() {
    elements.$input = elements.$wrapper.parents('form').children('[maxlength]');
  }

  const characters = () => elements.$input.val().length;
  const updateCounter = () => elements.$actualLength.html(characters());

  function bindEventsHandlers() {
    elements.$input.on('input', updateCounter);
  }

  (function init() {
    setElements();
    bindEventsHandlers();
  }());
}

export default characterCounterComponent;

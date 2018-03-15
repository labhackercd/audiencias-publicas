function characterCounterComponent() {
  const elements = {
    $input: [],
    $wrapper: $('.JS-character-counter'),
    $actualLength: $('.JS-characterCounterAtualLength'),
  };

  function setElements() {
    elements.$input = elements.$wrapper.parents('form').children('[maxlength]');
  }

  const characters = () => elements.$input.val().length;
  const updateCounter = () => elements.$actualLength.html(characters());

  function bindEventsHandlers() {
    elements.$input.on('input', updateCounter);
  }

  function init() {
    setElements();
    bindEventsHandlers();
  }

  return {
    updateCounter,
    init,
    setElements,
  }
}

export default characterCounterComponent;

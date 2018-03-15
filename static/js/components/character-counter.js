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
  const updateCounter = () => {
    elements.$actualLength.html(characters());

    if (characters() == elements.$input.attr('maxlength')) {
      elements.$wrapper.addClass('-limitreached');
    } else {
      elements.$wrapper.removeClass('-limitreached');
    }
  }

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

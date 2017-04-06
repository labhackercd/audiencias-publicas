function sendFormHelper($wrapper) {
  const elements = {
    $wrapper,
    $form: $wrapper.find('[class^="send-form--"]'),
    $formInput: $wrapper.find('.send-form__input'),
    $formBtn: $wrapper.find('.actions__button'),
  };

  function createClosedFormEl() {
    const closedFormEl = document.createElement('div');
    const closedFormSpanEl = document.createElement('span');

    closedFormEl.className = 'send-form--closed';
    closedFormSpanEl.innerHTML = 'Audiência encerrada para participações.';

    closedFormEl.appendChild(closedFormSpanEl);
    elements.$wrapper[0].appendChild(closedFormEl);
  }

  function closeForm() {
    createClosedFormEl();
    elements.$form.remove();
  }

  function formIsBlank() {
    const text = elements.$formInput.val();
    const isBlank = text.trim() ? 0 : 1;
    return isBlank;
  }

  const events = {
    formInputKeyDown(event) {
      if (event.which === 13) event.preventDefault();
    },

    formInputKeyUp(event) {
      if (event.which === 13) elements.$formBtn.trigger('click');
    },
  };

  (function bindEventsHandlers() {
    elements.$formInput.on('keydown', events.formInputKeyDown);
    elements.$formInput.on('keyup', events.formInputKeyUp);
  }());

  return {
    close: closeForm,
    isBlank: formIsBlank,
  };
}

export default sendFormHelper;

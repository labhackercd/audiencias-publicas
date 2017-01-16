function sendFormHelper($wrapper) {
  const elements = {
    $wrapper,
    $form: $wrapper.find('[class^="send-form--"]'),
    $formInput: $wrapper.find('.send-form__input'),
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

  const events = {
    formInputKeyDown(event) {
      if (event.which === 13) event.preventDefault();
    },

    formInputKeyUp(event) {
      if (event.which === 13) elements.$form.trigger('submit');
    },
  };

  (function bindEventsHandlers() {
    elements.$formInput.on('keydown', events.formInputKeyDown);
    elements.$formInput.on('keyup', events.formInputKeyUp);
  }());

  return { closeForm };
}

export default sendFormHelper;

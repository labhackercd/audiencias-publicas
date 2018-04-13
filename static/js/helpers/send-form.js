import countdownTimerComponent from '../components/countdown-timer';

function sendChatFormHelper($wrapper) {
  const elements = {
    $wrapper,
    $form: $wrapper.find('.JS-formChat'),
    $formInput: $wrapper.find('.input'),
    $formBtn: $wrapper.find('.button'),
    $countdown: $wrapper.find('.JS-countdown'),
  };

  function createClosedFormEl() {
    const closedFormEl = document.createElement('div');
    const closedFormSpanEl = document.createElement('span');

    closedFormEl.className = 'closed';
    closedFormSpanEl.innerHTML = 'Audiência encerrada para participações.';
    closedFormEl.appendChild(closedFormSpanEl);

    if(!elements.$wrapper[0].querySelector(".closed")){
      elements.$wrapper[0].appendChild(closedFormEl);
    }
  }

  function closeForm(){
    createClosedFormEl();
    elements.$form.remove();
  }

  function showCountdown(){
    elements.$countdown.addClass('-show');
    countdownTimerComponent(closeForm);
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
    close: showCountdown,
    isBlank: formIsBlank,
  };
}

function sendQuestionFormHelper($wrapper) {
  const elements = {
    $wrapper,
    $form: $wrapper.find('.JS-formQuestion'),
    $formInput: $wrapper.find('.send-form__input'),
    $formBtn: $wrapper.find('.actions__button'),
    $questionAction: $wrapper.find('.JS-questionAction'),
  };

  function createClosedFormEl() {
    const closedFormEl = document.createElement('div');
    const closedFormSpanEl = document.createElement('span');

    closedFormEl.className = 'closed';
    closedFormSpanEl.innerHTML = 'Audiência encerrada para participações.';
    closedFormEl.appendChild(closedFormSpanEl);

    if(!elements.$wrapper[0].querySelector(".closed")){
      elements.$wrapper[0].appendChild(closedFormEl);
    }
  }

  function closeForm() {
    createClosedFormEl();
    elements.$form.remove();
    elements.$questionAction.remove();
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

export {sendChatFormHelper, sendQuestionFormHelper};

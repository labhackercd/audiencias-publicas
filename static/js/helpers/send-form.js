import countdownTimerComponent from '../components/countdown-timer';

function sendChatFormHelper($wrapper) {
  const elements = {
    $wrapper,
    $form: $wrapper.find('.JS-formChat'),
    $formInput: $wrapper.find('.input'),
    $formBtn: $wrapper.find('.button'),
    $countdown: $wrapper.find('.JS-countdown'),
    $chatFooter: $wrapper.find('.JS-chatFooter'),
  };

  function createClosedFormEl() {
    elements.$chatFooter.addClass('-closed');
    elements.$chatFooter.prepend('<p class="info JS-closedChatMessage">Audiência encerrada para participações.</p>');
  }

  function closeForm(){
    if(!elements.$chatFooter.hasClass('-closed')){
      createClosedFormEl();
      elements.$form.remove();
    }
  }

  function showCountdown(time){
    elements.$countdown.addClass('-show');
    countdownTimerComponent(time, closeForm);
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
    $formInput: $wrapper.find('.JS-formInputQuestion'),
    $formBtn: $wrapper.find('.button'),
    $questionFooter: $wrapper.find('.JS-questionFooter'),
  };

  function createClosedFormEl() {
    elements.$questionFooter.addClass('-closed');
    elements.$questionFooter.html('<p class="info JS-closedQuestionMessage">Audiência encerrada para participações.</p>');
  }

  function closeForm() {
    if(!elements.$questionFooter.hasClass('-closed')){  
      createClosedFormEl();
      elements.$form.remove();
    }
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

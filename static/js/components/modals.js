function modalsComponent() {
  const elements = {
    $openModal: $('.JS-openModal'),
    $closeModal: $('.JS-closeModal'),
    $modal: $('.JS-modal')
  };

  function getModalById(modalId) {
    let modal = undefined;

    elements.$modal.each(function() {
      if ($(this).data('modalId') === modalId) {
        modal = $(this);
        return;
      }
    });

    return modal;
  }

  const events = {
    openModal() {
      const modalTarget = $(this).data('modalTarget');
      const $modal = getModalById(modalTarget);

      $modal.addClass('-open');
    },

    closeModal() {
      if ($(event.target).is('.JS-modal') || $(event.target).is('.JS-closeModal')) {
        $(this).removeClass('-open')
      }
    }
  };

  const bindEventsHandlers = {
    onPageLoad() {
      elements.$openModal.on('click', events.openModal);
      elements.$modal.on('click', events.closeModal);
    }
  };

  (function init() {
    bindEventsHandlers.onPageLoad();
  }());
}

export default modalsComponent;

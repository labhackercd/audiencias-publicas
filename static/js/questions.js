function questionsAP() {
  const elements = {
    shareListOpenBtn: $('.question-block__share-button'),
    shareListCloseBtn: $('.share-list__close'),
  };

  const vars = {};

  const events = {
    openShareList() {
      const shareList = $(this).siblings('.question-block__share-list');

      shareList.removeClass('question-block__share-list');
      shareList.addClass('question-block__share-list--active');
    },

    closeShareList() {
      const shareList = $(this).parent('.question-block__share-list--active');

      shareList.removeClass('question-block__share-list--active');
      shareList.addClass('question-block__share-list');
    },
  };

  (function bindEventsHandlers() {
    elements.shareListOpenBtn.on('click', events.openShareList);
    elements.shareListCloseBtn.on('click', events.closeShareList);
  }());

  return {};
}

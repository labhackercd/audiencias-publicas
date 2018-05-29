/* global HANDLER, HANDLER_ADMIN, openEdemSidebar, player */
import {sendQuestionFormHelper, sendChatFormHelper} from '../helpers/send-form';
import { getCookie } from '../helpers/cookies';
import characterCounterComponent from './character-counter';
import playVideoById from './play-video';
import roomVideosComponent from './room-videos';
import modalsComponent from '../components/modals';

const characterCounter = characterCounterComponent();
characterCounter.setElements();


function roomComponent(socket) {
  const elements = {
    $wrapperQuestion: $('.JS-wrapperQuestion'),
    $questionList: $('.JS-questionsList'),
    $questionlistEmpty: $('.JS-questionlistEmpty'),
    $openQuestionManaging: $('.JS-openQuestionManaging'),
    $closeQuestionManaging: $('.JS-closeQuestionManaging'),
    $questionManagingList: $('.JS-questionManagingList'),
    $shareListOpenBtn: $('.JS-shareListOpenBtn'),
    $shareListCloseBtn: $('.JS-shareListCloseBtn'),
    $shareListItemLink: $('.JS-shareListItemLink'),
    $shareRoom: $('.JS-shareRoom'),
    $readMoreQuestion: $('.JS-readMoreQuestion'),
    $formInputQuestion: $('.JS-formInputQuestion'),
    $answeredCheckbox: $('.JS-answeredCheckbox'),
    $messages: $('.JS-messages'),
    $messagesList: $('.JS-messagesList'),
    $messagesListEmpty: $('.JS-messagesListEmpty'),
    $readMoreChat: $('.JS-readMoreChat'),
    $videoFrame: $('.JS-videoFrame'),
    $thumbList: $('.JS-thumbList'),
    $priorityCheckbox: $('.JS-priorityCheckbox'),
    $answerTimeCheckbox: $('.JS-answerTimeCheckbox'),
    $answerTimeCheckbox: $('.JS-answerTimeCheckbox'),
    $addLinks: $('.JS-addLinks'),
    $linkModal: $('.JS-linkModal'),
    $closeModal: $('.JS-closeModal'),
    $selectVideo: $('.JS-selectVideo'),
    $orderVideos: $('.JS-orderVideos'),
    $roomVideo: $('.JS-roomVideo'),
    $answeredButton: $('.JS-answeredButton'),
  };

  const vars = {
    listHeight: () => elements.$questionList[0].offsetHeight,
    listScrollHeight: () => elements.$questionList[0].scrollHeight,
    listScrollTop: () => elements.$questionList[0].scrollTop,
    wrapperHeight: () => elements.$wrapperQuestion[0].offsetHeight,
    wrapperScrollHeight: () => elements.$wrapperQuestion[0].scrollHeight,
    wrapperScrollTop: () => elements.$wrapperQuestion[0].scrollTop,
    messagesListHeight: () => elements.$messagesList[0].offsetHeight,
    messagesListScrollHeight: () => elements.$messagesList[0].scrollHeight,
    messagesListScrollTop: () => elements.$messagesList[0].scrollTop,
  };

  document.querySelectorAll('.JS-addLinks').forEach(function(openLinkModal) {
    openLinkModal.onclick = function() {
      elements.$linkModal.addClass('-open');
    }
  });

  document.querySelectorAll('.JS-closeModal').forEach(function(openLinkModal) {
    openLinkModal.onclick = function() {
      elements.$linkModal.removeClass('-open');
    }
  });

  let isCurrentUserQuestion = false;
  let newQuestionsCount = 0;
  let sendQuestionForm = {};
  let sendChatForm = {};

  function closeQuestionForm() {
    $('.JS-formQuestion').removeClass('-active');
  }

  function openQuestionForm() {
    $('.JS-formQuestion').addClass('-active');
    elements.$formInputQuestion.focus();
  }

  function animateToBottomQuestion() {
      elements.$questionList.animate({
        scrollTop: vars.listScrollHeight(),
      }, 600, () => {
        isCurrentUserQuestion = false;
      });

  }

  function animateToBottomChat() {
    elements.$messagesList.animate({ scrollTop: vars.messagesListScrollHeight() }, 'slow');
  }

  function isScrolledToBottomQuestion() {
    return vars.listScrollTop() === (vars.listScrollHeight() - vars.listHeight());
  }

  function isScrolledToBottomChat() {
    return vars.messagesListScrollTop() === (vars.messagesListScrollHeight() - vars.messagesListHeight());
  }

  function scrollToBottomChat() {
    elements.$messagesList[0].scrollTop = vars.messagesListScrollHeight();
  }

  function showReadMoreQuestion() {
    if (newQuestionsCount === 1) {
      elements.$readMoreQuestion.html('Há 1 nova pergunta disponível abaixo');
    } else {
      elements.$readMoreQuestion.html(`Há ${newQuestionsCount} novas perguntas disponíveis abaixo`);
    }

    elements.$readMoreQuestion.removeClass('more');
    elements.$readMoreQuestion.addClass('more -visible');
  }

  function showReadMoreChat() {
    elements.$readMoreChat.removeClass('more');
    elements.$readMoreChat.addClass('more -visible');
  }

  function hideReadMoreQuestion() {
    elements.$readMoreQuestion.removeClass('more -visible');
    elements.$readMoreQuestion.addClass('more');
  }

  function hideReadMoreChat() {
    elements.$readMoreChat.removeClass('more -visible');
    elements.$readMoreChat.addClass('more');
  }

  function updateVoteBlock($question, data) {
    const $upvoteButton = $question.find('.JS-voteBtn');
    const $totalVotes = $question.find('.JS-totalVotes');

    if (data.answered) {
      $upvoteButton.addClass('voted disabled');
      $upvoteButton.attr('disabled', true);
      $upvoteButton.html('Pergunta Respondida');
      $totalVotes.addClass('voted disabled');
    } else if (HANDLER === $question.data('question-author')) {
      $upvoteButton.addClass('voted disabled');
      $upvoteButton.attr('disabled', true);
      $upvoteButton.html('Sua Pergunta');
      $totalVotes.addClass('voted disabled');
    } else if ($.inArray(HANDLER, data.voteList) > -1) {
      $upvoteButton.addClass('voted question-vote JS-voteBtnEnabled');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.html('Apoiada por você');
      $upvoteButton.removeClass('disabled');
      $totalVotes.removeClass('disabled');
      $totalVotes.addClass('voted');
    } else {
      $upvoteButton.removeClass('voted disabled');
      $upvoteButton.removeAttr('disabled');
      $upvoteButton.addClass('question-vote JS-voteBtnEnabled');
      $upvoteButton.html('Votar Nesta Pergunta');
      $totalVotes.removeClass('voted');
    }
  }

  function openRoom() {
    if (HANDLER === '') {
      $('.JS-closedQuestionMessage').parent().removeClass('-closed').prepend('<span><a class="link JS-openSidebar" data-sidebar-content="signin">Faça Login</a> para enviar uma pergunta!</span>');
      $('.JS-closedChatMessage').parent().removeClass('-closed').prepend('<p class="info JS-openSidebar" data-sidebar-content="signin">Faça Login</a> para participar no chat!</p>');
    } else {
      $('.JS-closedQuestionMessage').parent().removeClass('-closed').prepend('<button class="action JS-openQuestionForm">Fazer uma pergunta</button>')
      $('.JS-closedChatMessage').parent().removeClass('-closed').prepend('<form class="form JS-formChat" id="chatform"><textarea class="input JS-formInputChat" id="message" name="message" placeholder="Digite mensagens do bate-papo aqui" autocomplete="off" required></textarea><div class="actions"><button class="button" id="go" title="Enviar">Enviar</button></div></form>')
    }
    $('.JS-closedQuestionMessage').remove();
    $('.JS-closedChatMessage').remove();
    $('.JS-countdown').removeClass('-show');
    $('.JS-roomStatus').text('Em andamento');
    $('.JS-shareListOpenBtn').removeClass('hide');
    $('.JS-voteBtn').each(function() {
      if($(this).text() !== 'Sua Pergunta'){
        $(this).removeClass('disabled');
        $(this).attr('disabled', false);
        $(this).next('.JS-totalVotes').removeClass('disabled');
      }
    });
    sendChatForm = sendChatFormHelper($('.JS-wrapperChat'));
    sendChatForm.bindEvents();
    $(document).on("click", ".JS-openQuestionForm",function() {
      events.openQuestionFormClick();
    });
    $(document).on("submit", ".JS-formChat",function(event) {
      events.sendMessage(event);
    });
  }

  function evaluateSocketMessage(message) {
    const data = JSON.parse(message.data);

    if (data.closed) {
      sendChatForm.close(data.time_to_close);
      sendQuestionForm.close();
      $('.JS-shareListOpenBtn').addClass('hide');
      $('.JS-voteBtn').addClass('disabled');
      $('.JS-voteBtn').attr('disabled', true);
      $('.JS-totalVotes').addClass('disabled');
      $('.JS-liveIcon').remove();
      $('.JS-mainVideoLabel').addClass('-transmited').text('Transmitido');
      $('.JS-roomStatus').text('Transmissão encerrada');
      return;
    }

    if (data.video) {
      elements.$thumbList.html(data.thumbs_html);
      if(!data.is_attachment && !data.deleted && !data.ordered) {
        if (typeof player !== 'undefined') {
          $('.JS-roomAlert').removeClass('hide');
          $('.JS-alertPlayBtn').attr('data-video-id', data.video_id);
          $(`.JS-selectVideo[data-video-id=${player.getVideoData().video_id}]`).addClass('-current');
          if($('.JS-selectVideo[data-live-video]') && $('.JS-closedQuestionMessage')){
            openRoom();
          }
        } else {
          elements.$videoFrame.html(data.video_html);
          playVideoById(data.video_id);
          $('.JS-roomStatus').text('Em andamendo');
        }
      }
      roomVideosComponent();
      modalsComponent();
    } else if (data.question) {
        const $existingQuestion = $(`[data-question-id=${data.id}]`);
        const questionExists = $existingQuestion.length;
        const questionlistIsEmpty = elements.$questionlistEmpty.length;
        if (questionlistIsEmpty) elements.$questionlistEmpty.remove();

        if (questionExists) {
          $existingQuestion.replaceWith(data.html);
        } else {
          elements.$questionList.append(data.html);

          if (!isScrolledToBottomQuestion() && !isCurrentUserQuestion) {
            newQuestionsCount += 1;
            showReadMoreQuestion();
          }
        }

        const $question = $(`[data-question-id=${data.id}]`);
        const $answeredForm = $question.find('.JS-answeredForm');
        const $priorityForm = $question.find('.JS-priorityForm');
        const $answerTimeForm = $question.find('.JS-answerTimeForm');

        if ($.inArray(data.groupName, HANDLER_GROUPS) > -1) {
          $answeredForm.removeClass('hide');
        } else if (HANDLER_ADMIN) {
          $answeredForm.removeClass('hide');
          $priorityForm.removeClass('hide');
          $answerTimeForm.removeClass('hide');
        } else {
          $answeredForm.addClass('hide');
          $priorityForm.addClass('hide');
          $answerTimeForm.addClass('hide');
        }

        if (data.handlerAction == HANDLER) {
          $question.find('.JS-questionManagingList').addClass('-active');
        }

        updateVoteBlock($question, data);
        bindEventsHandlers.onAdd($question);
        elements.$questionList.mixItUp('sort', 'question-votes:desc question-id:asc');
    } else if (data.chat) {
        const messagesListIsEmpty = elements.$messagesListEmpty.length;
        if (messagesListIsEmpty) elements.$messagesListEmpty.remove();
        if (isScrolledToBottomChat()) {
          elements.$messagesList.append(data.html);
          animateToBottomChat();
        } else {
          elements.$messagesList.append(data.html);
          showReadMoreChat();
        }
    }
  }

  function mixItUpInit() {
    elements.$questionList.mixItUp({
      selectors: {
        target: '.question-card',
      },
      layout: {
        display: 'flex',
      },
    });
  }

  function sendFormHelperInit() {
    sendQuestionForm = sendQuestionFormHelper(elements.$wrapperQuestion);
    sendChatForm = sendChatFormHelper($('.JS-wrapperChat'));
  }

  function clickToggleButton() {
      $('.JS-selectVideo').find('.aud-button').toggleClass('-active');
      $('.JS-roomVideo').toggleClass('-ordering');
  }

  const events = {
    readMoreClickQuestion() {
      animateToBottomQuestion();
    },

    readMoreClickChat() {
      animateToBottomChat();
    },

    questionsScroll() {
      if (isScrolledToBottomQuestion()) {
        newQuestionsCount = 0;
        hideReadMoreQuestion();
      }
    },

    messagesListScroll() {
      if (isScrolledToBottomChat()) hideReadMoreChat();
    },

    vote() {
      if (HANDLER === '') {
        openEdemSidebar('signin'); // defined in room.html
      } else {
        const id = $(this).closest('.question-card').data('question-id');

        socket.send(JSON.stringify({
          handler: HANDLER,
          question: id,
          is_vote: true,
        }));
      }
    },

    closeQuestionFormClick() {
      closeQuestionForm();
    },

    openQuestionFormClick() {
      openQuestionForm();
      characterCounter.updateCounter();
    },

    openQuestionManaging() {
      $(this).parent().siblings('.JS-questionManagingList').addClass('-active');
    },

    closeQuestionManaging() {
      $(this).closest('.JS-questionManagingList').removeClass('-active');
    },

    openShareList() {
      const $shareList = $(this).siblings('.question-block__share-list');
      $shareList.removeClass('question-block__share-list');
      $shareList.addClass('question-block__share-list--active');
    },

    closeShareList() {
      const $shareList = $(this).parent('.question-block__share-list--active');
      $shareList.removeClass('question-block__share-list--active');
      $shareList.addClass('question-block__share-list');
    },

    shareRoom(event) {
      event.preventDefault();
      const windowOptions = 'height=600,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes';
      window.open($(this).attr('href'), 'popUpWindow', windowOptions);
    },

    shareQuestion() {
      const socialNetwork = $(this).data('social');

      const $question = $(this).closest('.question-card');
      const questionPath = $question.data('question-path');

      const windowOptions = 'height=500,width=1000,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes';
      const questionUrl = location.href
        .replace(location.hash, '')
        .replace(location.pathname, questionPath);

      const facebookUrl = `http://www.facebook.com/sharer/sharer.php?u=${questionUrl}`;
      const twitterUrl = `http://twitter.com/share?text=Apoie esta pergunta!&url=${questionUrl}`;
      const whatsappMessage = encodeURIComponent('As perguntas mais votadas serão respondidas pelos deputados agora! Acesse em ') + encodeURIComponent(questionUrl);

      switch (socialNetwork) {
        case 'facebook': window.open(facebookUrl, 'popUpWindow', windowOptions); break;
        case 'twitter': window.open(twitterUrl, 'popUpWindow', windowOptions); break;
        case 'whatsapp': window.open(`https://api.whatsapp.com/send?text=${whatsappMessage}`); break;
        default: break;
      }
    },

    sendQuestion(event) {
      event.preventDefault();

      if (sendQuestionForm.isBlank()) return false;

      isCurrentUserQuestion = true;

      socket.send(JSON.stringify({
        handler: HANDLER,
        question: elements.$formInputQuestion.val(),
        is_vote: false,
      }));

      elements.$formInputQuestion.val('').focus();
      animateToBottomQuestion();
      closeQuestionForm();

      return true;
    },

    sendMessage(event) {
      event.preventDefault();

      if (sendChatForm.isBlank()) return false;

      socket.send(JSON.stringify({
        handler: HANDLER, // defined in room.html
        message: $('.JS-formInputChat').val(),
      }));

      $('.JS-formInputChat').val('').focus();
      scrollToBottomChat();

      return true;
    },

    sendAnsweredForm(event) {
      const questionId = $(event.target).closest('[data-question-id]')[0].dataset.questionId;
      const csrftoken = getCookie('csrftoken');

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      $.post(event.target.form.action, {
        answered: event.target.checked
      })
    },

    sendAnswerTimeForm(event) {
      const questionId = $(event.target).closest('[data-question-id]')[0].dataset.questionId;
      const csrftoken = getCookie('csrftoken');

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      var answer_time = '0';
      if(event.target.checked){
        answer_time = player.getCurrentTime();
      };
      $.post(event.target.form.action, {
          answer_time: answer_time,
          video_id: player.getVideoData().video_id
      })
    },

    sendPriorityForm(event) {
      const questionId = $(event.target).closest('[data-question-id]')[0].dataset.questionId;
      const csrftoken = getCookie('csrftoken');

      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      });

      $.post(event.target.form.action, {
        is_priority: event.target.checked
      })
    },

    setCurrentVideo() {
      player.loadVideoById({
        videoId:$(this).attr('data-youtube-id'),
        startSeconds:$(this).attr('data-answer-time')
      });
      const currentVideo = $(`.JS-selectVideo[data-video-id=${$(this).attr('data-youtube-id')}]`)
      $('.JS-selectVideo').removeClass('-current');
      currentVideo.addClass('-current');
      $('.JS-videoStatus').text(currentVideo.attr('data-video-title'));
      if (currentVideo.attr('data-live-video') == "true") {
        $('.JS-videoStatus').prepend('<span class="live-icon JS-liveIcon"></span>');
      }
    },

    showAdminBtns() {
      if ($.inArray($('.JS-groupName').attr('data-room-group'), HANDLER_GROUPS) > -1) {
        $('.JS-openQuestionManaging').removeClass('hide');
      } else if (HANDLER_ADMIN) {
        $('.JS-openQuestionManaging').removeClass('hide');
      } else {
        $('.JS-openQuestionManaging').addClass('hide');
      }
    },

    alertPlayBtn(){
      const video_id = $('.JS-alertPlayBtn').attr('data-video-id')
      const currentVideo = $(`.JS-selectVideo[data-video-id=${video_id}]`)
      player.loadVideoById(video_id);
      $('.JS-roomAlert').addClass('hide');
      $('.JS-selectVideo').removeClass('-current');
      currentVideo.addClass('-current');
      $('.JS-videoStatus').text(currentVideo.attr('data-video-title'));
      if (currentVideo.attr('data-live-video') == "true") {
        $('.JS-videoStatus').prepend('<span class="live-icon JS-liveIcon"></span>');
      }
    },
  };


  const bindEventsHandlers = {
    onPageLoad() {
      socket.onmessage = evaluateSocketMessage;
      $('.JS-voteBtnEnabled').on('click', events.vote);
      elements.$openQuestionManaging.on('click', events.openQuestionManaging);
      elements.$closeQuestionManaging.on('click', events.closeQuestionManaging);
      elements.$shareListOpenBtn.on('click', events.openShareList);
      elements.$shareListCloseBtn.on('click', events.closeShareList);
      elements.$shareListItemLink.on('click', events.shareQuestion);
      elements.$shareRoom.on('click', events.shareRoom);
      $('.JS-formQuestion').on('submit', events.sendQuestion);
      $('.JS-openQuestionForm').on('click', events.openQuestionFormClick);
      $('.JS-closeQuestionForm').on('click', events.closeQuestionFormClick);
      elements.$questionList.on('scroll', events.questionsScroll);
      elements.$readMoreQuestion.on('click', events.readMoreClickQuestion);
      elements.$answeredCheckbox.on('change', events.sendAnsweredForm);
      elements.$messagesList.on('scroll', events.messagesListScroll);
      elements.$readMoreChat.on('click', events.readMoreClickChat);
      $('.JS-formChat').on('submit', events.sendMessage);
      elements.$orderVideos.on('click', clickToggleButton);
      elements.$priorityCheckbox.on('change', events.sendPriorityForm);
      elements.$answerTimeCheckbox.on('change', events.sendAnswerTimeForm);
      elements.$answeredButton.on('click', events.setCurrentVideo);
      elements.$answeredButton.on('click', events.setCurrentVideo);
      $('.JS-alertPlayBtn').on('click', events.alertPlayBtn);
      events.showAdminBtns();
    },

    onAdd($question) {
      const $voteBtnEnabled = $question.find('.JS-voteBtnEnabled');
      const $openQuestionManaging = $question.find('.JS-openQuestionManaging');
      const $closeQuestionManaging = $question.find('.JS-closeQuestionManaging');
      const $shareListOpenBtn = $question.find('.JS-shareListOpenBtn');
      const $shareListCloseBtn = $question.find('.JS-shareListCloseBtn');
      const $shareListItemLink = $question.find('.JS-shareListItemLink');
      const $answeredCheckbox = $question.find('.JS-answeredCheckbox');
      const $priorityCheckbox = $question.find('.JS-priorityCheckbox');
      const $answerTimeCheckbox = $question.find('.JS-answerTimeCheckbox');
      const $answeredButton = $question.find('.JS-answeredButton');

      $voteBtnEnabled.on('click', events.vote);
      $openQuestionManaging.on('click', events.openQuestionManaging);
      $closeQuestionManaging.on('click', events.closeQuestionManaging);
      $shareListOpenBtn.on('click', events.openShareList);
      $shareListCloseBtn.on('click', events.closeShareList);
      $shareListItemLink.on('click', events.shareQuestion);
      $answeredCheckbox.on('change', events.sendAnsweredForm);
      $priorityCheckbox.on('change', events.sendPriorityForm);
      $answerTimeCheckbox.on('change', events.sendAnswerTimeForm);
      $answeredButton.on('click', events.setCurrentVideo);
      events.showAdminBtns();
    },
  };

  (function init() {
    scrollToBottomChat();
    mixItUpInit();
    sendFormHelperInit(); // defined in room.html
    bindEventsHandlers.onPageLoad();
    setInterval(function() {
      socket.send(JSON.stringify({heartbeat: true}));
    }, 3000);
  }());
}

export default roomComponent;

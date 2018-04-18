function countdownTimerComponent(time, closeForm) {
  
  const elements = {
    $countdownTimer: $('.JS-countdownTimer'),
    $countdownMinutes: $('.JS-countdownMinutes'),
    $countdownSeconds: $('.JS-countdownSeconds'),
    $countdown: $('.JS-countdown')
  }

  function getTimeRemaining(time) {
    var seconds = Math.floor(time % 60);
    var minutes = Math.floor(time / 60);
    return {
      'total' : time,
      'minutes': minutes,
      'seconds': seconds
    };
  }

  function initializeClock(time) {

    function updateClock() {
      var t = getTimeRemaining(time);

      elements.$countdownMinutes.html(('0' + t.minutes).slice(-2));
      elements.$countdownSeconds.html(('0' + t.seconds).slice(-2));

      time--

      if (t.total <= 0) {
        elements.$countdownTimer.removeClass('-finishing').addClass('-done')
        clearInterval(timeinterval);
        closeForm();
        elements.$countdown.removeClass('-show');

      } else if (t.total <= 60) {
        elements.$countdownTimer.removeClass('-halfway').addClass('-finishing');

      } else if (t.total <= 300) {
        elements.$countdownTimer.addClass('-halfway');
      }
    }

    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
  }

  (function init() {
    initializeClock(time);
  }());
}

export default countdownTimerComponent;

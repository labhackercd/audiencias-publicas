function countdownTimerComponent(closeForm) {
  
  const elements = {
    $countdownTimer: $('.JS-countdownTimer'),
    $countdownMinutes: $('.JS-countdownMinutes'),
    $countdownSeconds: $('.JS-countdownSeconds'),
    $countdown: $('.JS-countdown')
  }

  function getTimeRemaining(totalTimeInSeconds) {
    var seconds = Math.floor(totalTimeInSeconds % 60);
    var minutes = Math.floor(totalTimeInSeconds / 60);
    return {
      'total' : totalTimeInSeconds,
      'minutes': minutes,
      'seconds': seconds
    };
  }

  function initializeClock(totalTimeInSeconds) {

    function updateClock() {
      var t = getTimeRemaining(totalTimeInSeconds);

      elements.$countdownMinutes.html(('0' + t.minutes).slice(-2));
      elements.$countdownSeconds.html(('0' + t.seconds).slice(-2));

      totalTimeInSeconds--

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

  var totalTimeInSeconds = 0.1 * 60;

  (function init() {
    initializeClock(totalTimeInSeconds);
  }());
}

export default countdownTimerComponent;

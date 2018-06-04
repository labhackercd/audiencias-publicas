$('.JS-readMoreLess').each(function() {
  if($(this).height() > 224) {
    $(this).addClass('-large');
  }
});

$(".JS-toggleDiv").click(function() {
  $(this).parent().toggleClass('-open');
  if ($(this).parent().hasClass('-open')) {
    $(this).text("Ver menos");
  } else {
    $(this).text("Ver mais");
  }
});

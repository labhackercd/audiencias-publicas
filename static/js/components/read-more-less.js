$('.JS-readMoreLess').each(function() {
  if($(this).height() > 224) {
    $(this).addClass('-large');
  }
});

$(".JS-toggleDiv").click(function() {
  $(this).parent().toggleClass('-open');
  if ($(this).parent().hasClass('-open')) {
    $(this).text("Ler menos");
  } else {
    $(this).text("Ler mais");
  }
});



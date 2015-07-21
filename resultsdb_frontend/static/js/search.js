/* waiting for reliable CND or own hosting of progressbar.js
   https://github.com/kimmobrunfeldt/progressbar.js


function progressbar(){
  $(".popover #progressbar-animation").removeClass("hide");
  var element = $(".popover #progressbar-animation")[0];
  var circle = new ProgressBar.Circle(element, {
    color: "#428BCA",
    strokeWidth: 0.75,
    fill: "#fff",
    easing: "easeInOut",
    duration: 1200
  });

  function doit(){
  circle.animate(1, function() {
    setTimeout(function(){
      circle.set(0);
      doit();
    }, 150);
  });
  }

  doit();
}
*/

$(function() {
  $("#popover").popover(
    {
      container: 'body',
      html : true,
      title: function() {
        return $("#popover-head").html();
      },
      content: function() {
        return $("#popover-content").html();
      }
  }
  ).on('click', function(){
    $(".popover #query").focus();
    $(".popover #searchform").submit(function(e){

      var query = $(".popover #query").val();
      var testcase = $(".popover #testcase").val();
      var type = $(".popover #type").val();
      var url = $(".popover #url").val() + "?";
      var outcome = $(".popover #outcome").val();

      query = query.replace(/\*/g,"%");

      if(query.indexOf("%") != -1){
        //wildcard match
        url += "item:like=" + query;
      } else {
        //substring match
        url += "item:like=%" + query + "%";
      }

      if(testcase != 0)
        url += "&testcase_name="+testcase;
      if(type != 0)
        url += "&type="+type;
      if(outcome)
        url += "&outcome="+outcome;

      e.preventDefault();

      //progressbar();
      //$(".popover #searchform").hide();

      window.location.href = encodeURI(url);
    });
  });

  $(document).bind('keypress', function(e) {
    if(e.keyCode == 47 && !$(":focus").is("input")) //slash key
    {
      e.preventDefault();
      $("#popover").click();
    }
  });
});


 $(".sign_up").hide();
 $(".sign_in_li").addClass("active");
 
 $(".sign_up_li").click(function(){
   $(this).addClass("active");
   $(".sign_in_li").removeClass("active");
   $(".sign_up").show();
    $(".sign_in").hide();
 })
 
 $(".sign_in_li").click(function(){
   $(this).addClass("active");
   $(".sign_up_li").removeClass("active");
   $(".sign_in").show();
    $(".sign_up").hide();
 })
 
 
 
 
 
 
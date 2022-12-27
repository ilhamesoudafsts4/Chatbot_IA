const chatButton = document.querySelector('.chatbox__button');
const chatContent = document.querySelector('.chatbox__support');
const icons = {
    isClicked: '<img src="{{ url_for("static",filename="styless/images/icons/chatbox-icon.svg") }}" />',
    isNotClicked: '<img src="./images/icons/chatbox-icon.svg" />'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
chatbox.display();
chatbox.toggleIcon(false, chatButton);

// $(".btuton_send").click(function(){
 
//     $.post("/predect",
//     {
//       message: document.getElementById('message').value
      
//     },
//     function(data, status){
//       alert("Data: " + data + "\nStatus: " + status);
//     });
//   });

   
  $(document).ready(function(){
    
    $(".btuton_send").click(function(){
      total=document.getElementById('message').value;
      document.getElementById('mymessage').innerHTML = total;
      
      
    $.ajax({
      type : 'POST',

      
      url : "/predect",
      contentType: 'application/json;',
      data : JSON.stringify(document.getElementById('message').value),
      
      dataType:'json',
      
      success: function(result) {
        console.log("Result:");
        console.log(result);
        console.log(total);
        $("#cover").html(result['message']);
         
        document.getElementsByName("message")[0].value = "";
             
       
        

      }
      
    });
     });
     
    });

    

function upload(){

  var data=new FormData();
          var file = $("#fileupload")[0].files[0];
          if (typeof file == "undefined"){
            alert ("Please choose file.");
            return;
          }
          data.append('file',file);
          $("#txtTest").val("Classifier training in progress. Please wait.....");

          $.ajax({
              url:"/upload",
              type:'POST',
              data:data,
              cache:false,
              processData:false,
              contentType:false,
              error:function(){
                  alert ("Upload error");
                  console.log("upload error");
              },
              success:function(data){
                  console.log(data);
                  $("#txtTest").val("Classifier training complete. Your classifier will be used for violence detection.");
              }
          })
}


/**
Gets input from user, makes call to server and updates DOM based on level of 
offensivebess in text input by user as returned from server.
**/
function detect_offense() {

  // gets input from user
  var classifier = $('#classifiername').find(":selected").text();
  var text = $('#search').val();

  if (text.length < 1){
    alert ("Empty text. Please enter text for violence detection");
    return
  }

  // makes request to server and updates dom
  $.post('/detect', {
      text: text,
      model: classifier,
  }).done(function(response) {
      var level = response['level']
      console.log(level);
      if (level == "NOT"){
        var markup = "<tr><td><strong> <font color = 'blue'>" + text + "</td><td> </font> <font color = 'blue'> <strong> No Offense </font> </strong> </td></tr>";
        $("table tbody").append(markup);
      }


      else {
        var markup = "<tr><td> <strong><font color = 'red'>" + text + "</td><td> </font> <font color = 'red'> <strong> Obscene </font> </strong></td></tr>";
        $("table tbody").append(markup);
      }

  }).fail(function() {
      alert("Could not contact server");
  });
  
} 
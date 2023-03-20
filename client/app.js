  function onClickedPredictTR() {
    console.log("Predicted TR button clicked");
    var user = document.getElementById("uiUser");
    var player = document.getElementById("uiPlayer");
    var actualTR = document.getElementById("uiActualTR")
    var predictedTR = document.getElementById("uiPredictedTR");
  
    var url = "http://127.0.0.1:5000/predict_tr"; //Use this if you are NOT using nginx which is first 7 tutorials
    //var url = "/api/predict_home_price"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  
    $.post(url, {
        user: user.value
    },function(data, status) {
        console.log(data);
        player.innerHTML = "<h3>" + data.player.toString() + "</h3>";
        actualTR.innerHTML = "<h3>" + data.actual_TR.toString() + "</h3>";
        predictedTR.innerHTML = "<h3>" + data.predicted_TR.toString() + "</h3>";
        console.log(status);
    });
  }
  

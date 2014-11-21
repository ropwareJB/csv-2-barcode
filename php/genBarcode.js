var PROG = {current:0, real:0}

function clickGenerate(){
    $("#generateBtn").fadeOut(400, function(){ $("#progress").fadeIn(500);});
    $.get("/genBarcodes.php", null, genComplete).fail(genFail);
    //Start receiving progress
    setTimeout(function() {
      getProgress();
    }, 300);
    updateProgressFrame();
}
function getProgress(){
    $.get("/getProgress.php", recProgressUpdate, "json").fail(recProgressUpdateFail);
}
function genComplete(result){
  console.log(result);
}
function genFail(result){
  alert("Failed!!");
}
function recProgressUpdate(result){
    var val = result.progress;
    PROG.real = val;
    $("#progress").attr("value", val);
    
    if(val<100) getProgress();
}
function updateProgressFrame(){
    PROG.current += (PROG.real - PROG.current)/2;
    if(PROG.real == 100 && PROG.real - PROG.current < 1) PROG.current = 100;
    $("#percent").html(Math.floor(PROG.current)+"%");
    if(PROG.current < 100){
        setTimeout(function() {
          updateProgressFrame();
        }, 50);
    }else{
      $("#progressReporter").fadeOut(400, function(){$(".downloadBtn").fadeIn(300);});
    }
}
function recProgressUpdateFail(result){

}

$("#generateBtn").click(clickGenerate);

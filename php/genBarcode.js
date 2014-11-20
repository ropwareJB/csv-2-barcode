function clickGenerate(){
    $.get("/genBarcodes.php", null, genComplete).fail(genFail);
    //Start receiving progress
    setTimeout(function() {
      getProgress();
    }, 300);
}
function getProgress(){
    $.get("/getProgress.php", recProgressUpdate, "json").fail(recProgressUpdateFail);
}
function genComplete(result){
  alert("Finished!");
  console.log(result);
}
function genFail(result){
  alert("Failed!!");
}
function recProgressUpdate(result){
    console.log(result);
    var val = result.progress;
    $("#progress").attr("value", val);
    if(val<100) getProgress();
}
function recProgressUpdateFail(result){

}

$("#generateBtn").click(clickGenerate);

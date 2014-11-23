var PROG = {current:0, real:0}

function clickGenerate(){
    $( '#uploadForm').submit( function( e ) {
      $.ajax( {
        url: '/genBarcodes.php?font=Brandon_light.php&font-bold=Brandon_reg.php',
        type: 'POST',
        data: new FormData( this ),
        processData: false,
        contentType: false,
        complete: genComplete
      }).fail(genFail);
      e.preventDefault();
    } );
    $("#uploadForm").fadeOut(400, function(){ $(".progressGroup").fadeIn(500);});
    //Start receiving progress
    setTimeout(function() {
      getProgress();
    }, 300);
    updateProgressFrame();
}
function pickedFile(){
  $("#generateBtn").removeAttr("disabled");
}
$("#fileToUpload").change(pickedFile);
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
    
    if(val<100) setTimeout(getProgress, 300);
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

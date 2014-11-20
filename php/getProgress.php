<?php
  session_start();
  echo json_encode(array("progress"=>$_SESSION["progress"]));
?>  

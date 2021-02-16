<?php
  require "myLibrary.php";
  // get
  $scenario = $_POST['scenario'];
  $dsn = 'mysql:host=サーバー名;dbname=DB名';
  $user = 'mysqlのuser名';
  $password = 'パスワード'; 

  try{
    // DB setup
    $dbh = new PDO($dsn, $user, $password);
    // シナリオの登録(拘束する変数は、テーブルのカラム名と同じにする)
    $stmt = $dbh-> prepare('INSERT INTO table名 (title, players, time_h, difficult, num_kp, num_pl, url, comment) VALUES (:title, :players, :time_h, :difficult, :num_kp, :num_pl, :url, :comment)');
    exitQuery($dbh, 'table名', $stmt, $scenario);
    header("location: showTRPG.php");
  }catch(Exception $e){
    echo "Error: can't regist";
  }
?>
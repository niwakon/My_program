<?php
  require "myLibrary.php";
  $dsn = 'mysql:host=サーバー名;dbname=DB名';
  $user = 'mysqlのuser名';
  $password = 'パスワード';
  // 変数の取得
  $val = $_POST['id'];
  $ids = explode(",",$val);
  try{
    // DB setup
    $dbh = new PDO($dsn, $user, $password);
    // idリストを元に１つずつ削除
    foreach($ids as $id){
        $stmt = $dbh-> prepare("DELETE FROM テーブル名 WHERE id = ?");
        $stmt->bindValue(1,$id);
        $stmt->execute();
    }
    header("location: showTRPG.php");
  }catch(Exception $e){
    echo "Error: can't regist";
  }
?>
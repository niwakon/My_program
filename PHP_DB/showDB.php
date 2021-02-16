<?php
  require "myLibrary.php";
  // get(ソートしたいカラム名)
  $sort = strval($_POST['sort']);
  // set DB login info
  $dsn = 'mysql:host=サーバー名;dbname=DB名';
  $user = 'mysqlのuser名';
  $password = 'パスワード';
  try{
    // DB setup
    $dbh = new PDO($dsn, $user, $password);
    if(empty($sort)){
        $query = "SELECT * FROM テーブル名";
        echo (getTable_html($dbh,'テーブル名', $query));
    }else{
        $query = "SELECT * FROM テーブル名 ORDER BY ".$sort;
        echo(getTable_html($dbh, 'テーブル名', $query));
    }
  }catch(Exception $e){
    echo "Error: falt connect";
  }
?>
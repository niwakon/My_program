<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset = "utf-8">
  <link rel="stylesheet" href="showTRPG.css">
  <title>クトゥルフ神話TRPGシナリオ</title>
</head>
<body> 
<h1>
 <font face="Yu Gothic">
  <b>CoCのシナリオ一覧 </b>
 </font>
</h1>
<h2>
  <a href="TRPG.php"> シナリオの追加 </a>
  <br>
  <a href="editTRPG.php"> テーブルの編集 </a>
</h2>
<table>
<tr>
 <td>
  <select id="sort_id" name="sort" >
   <option value="id" selected>id</option>
   <option value="players">PL数</option>
   <option value="time_h">プレイ時間</option>
   <option value="difficult">難易度</option>
  </select>
 </td>
 <td>
  <a class="order" href="javascript:void(0)" data-id="20">
   <button class="order2" type="button">ソート</button>
  </a>
 </td>
</tr>
</table>

<div id="table">
 <?php
  require "myLibrary.php";
  // set DB login info
  $dsn = 'mysql:host=サーバー名;dbname=DB名';
  $user = 'mysqlのuser名';
  $password = 'パスワード';
  try{
    // DB setup
    $dbh = new PDO($dsn, $user, $password);
    showDB($dbh,'テーブル名');
  }catch(Exception $e){
    echo "Error:";
  }
 ?>
</div>
<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
<div>
<script>
// ajaxを用いてテーブルだけ更新
$(function(){
 $('.order').click(function(){
    var id = document.getElementById('sort_id').value;
    // ajax処理
    $.ajax({
        url: '/showDB.php',
        type: 'POST',
        dataType: 'html',
        data: {
            sort: id
        }
    }).done(function(data){
        document.getElementById('table').innerHTML=data;
    }).fail(function(data){
        console.log('error:', data);
        alert('DB失敗');
    });
 });
});
</script>
</div>
</body>
</html>
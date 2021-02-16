<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset = "utf-8">
  <link rel="stylesheet" href="showTRPG.css">
  <title>クトゥルフ神話TRPGシナリオ編集ページ</title>
</head>
<body> 
<h1>
  <b>シナリオの編集</b>
</h1>
<h2>
  <a href="showTRPG.php">
   一覧に戻る
  </a>
</h2>
<input type="button" id="Delete" value="行の削除" onclick="OnDelete();">

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
    $query = "SELECT * FROM  CoC";
    showTable_checkbox($dbh,'CoC', $query);
  }catch(Exception $e){
    echo "Error:";
  }
 ?>

 <script>
     // 出典: https://oc-technote.com/javascript/javascript-post-params-move-to-page/
     function post(path, params, method='post') {
        // The rest of this code assumes you are not using a library.
        // It can be made less wordy if you use one.
        const form = document.createElement('form');
        form.method = method;
        form.action = path;
        for (const key in params) {
            if (params.hasOwnProperty(key)) {
                const hiddenField = document.createElement('input');
                hiddenField.type = 'hidden';
                hiddenField.name = key;
                hiddenField.value = params[key];
                form.appendChild(hiddenField);
            }
        }
        document.body.appendChild(form);
        form.submit();
    }

     function OnDelete(){
        var chbox = document.getElementsByName("id");
        var ids = [];
        for (let i = 0; i < chbox.length; i++){
            if(chbox[i].checked){
                ids.push(chbox[i].value);
            }
        }
        ret = confirm("選択したシナリオを削除します。よろしいですか？");
        if (ret == true){
          post("delete.php", {id:ids});
        }
     }
 </script>
</div>
</body>
</html>
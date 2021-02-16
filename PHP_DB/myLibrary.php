<?php 
 //  $dbh: PDOインスタンス, $tableName: テーブル名
 // テーブルのカラム名の一覧返す
 function getColumnsNmae($dbh, $table){
  $query = "SHOW COLUMNS FROM ".$table;
  $sh = $dbh->query($query);
  $columns = $sh->fetchAll(PDO::FETCH_COLUMN);
  return $columns;
 }
 
 // テーブルの一覧を出力(Select * from)
 function showDB($dbh, $tableName){
  $query = "SELECT * FROM ".$tableName;
  showTable($dbh, $tableName, $query);
 }
 
 // テーブルの一覧の出力(Select * from)($orderの昇順)
 function showDB_order($dbh, $tableName, $order){
  $query = "SELECT * FROM ".$tableName." ORDER BY ".$order;
  showTable($dbh, $tableName, $query);
 }
 
 // テーブルを出力するhtml作成(処理部分)
 function showTable($dbh, $tableName, $query){
  $stmt = $dbh->query($query);
  
  // テーブルからカラム名取得
  $query = "SHOW COLUMNS FROM ".$tableName;
  $sh = $dbh->query($query);
  $columns = $sh->fetchAll(PDO::FETCH_COLUMN);
  ?>
  <table border ="1"><tbody>
   <tr>
    <?php foreach($columns as $column) { ?>
      <th><?php echo($column); ?> </th>
    <?php } ?>
  </tr>
 <?php while($row = $stmt->fetch(PDO::FETCH_ASSOC)){ ?>
   <tr>
     <?php foreach($columns as $column) { ?>
      <td><?php echo htmlspecialchars($row[$column]);?> </td>
    <?php } ?>
   </tr>
<?php
  }
  $dbh = null;
 }

 //  テーブルを出力するhtml作成(チェックボックス付き)
 function showTable_checkbox($dbh, $tableName, $query){
  $stmt = $dbh->query($query);
  
  // テーブルからカラム名取得
  $query = "SHOW COLUMNS FROM ".$tableName;
  $sh = $dbh->query($query);
  $columns = $sh->fetchAll(PDO::FETCH_COLUMN);
  ?>
  <table border ="1"><tbody>
   <tr>
     <th>&nbsp;</th>
    <?php foreach($columns as $column) { ?>
      <th><?php echo($column); ?> </th>
    <?php } ?>
  </tr>
 <?php while($row = $stmt->fetch(PDO::FETCH_ASSOC)){ ?>
   <tr>
     <td><input type="checkbox" name="id" value=<?php echo $row['id'] ?>></td>
     <?php foreach($columns as $column) { ?>
      <td><?php echo htmlspecialchars($row[$column]);?> </td>
    <?php } ?>
   </tr>
<?php
  }
  $dbh = null;
 }
 
 // INSET 文を自動で実行 ($stml: prepareしたクエリー, $value: 挿入したい値の連想配列)
 // $valueのキー名とprepareしたクエリーの変数名がテーブルのカラム名と同じであることが前提
 function exitQuery($dbh, $tableName, $stmt, $value){
   $columns = getColumnsNmae($dbh, $tableName);
   $count = 0;
   foreach($columns as $column){
     if(strcmp($column, 'id')==0){
      $count++;
      continue;
    }
    $state = $dbh->query("SELECT * FROM ".$tableName);
    $info_column = $state->getColumnMeta($count);
    $pdo_type = PDO::PARAM_INT;
    // 挿入するデータの型をチェック
    if(isset($info_column['native_type']) == true)
    {
      switch ($info_column['native_type'])
      {
        case 'TINY':
        case 'SHORT':
        case 'INT24':
        case 'LONG':
        case 'LONGLONG':
          $pdo_type = PDO::PARAM_INT;
          break;
        default:
          $pdo_type = PDO::PARAM_STR;
      }
      $stmt->bindValue(':'.$column, $value[$column], $pdo_type);
    }else{
      echo ('手打ちで一つ一つデータ挿入してください');
      break;
    }
    $count += 1;
  }
  // exit querye
  $stmt->execute();
 }

 // showTableで作成するhtml文をStringで返す関数
 function getTable_html($dbh, $tableName, $query){
  $stmt = $dbh->query($query);
  
  // テーブルからカラム名取得
  $query = "SHOW COLUMNS FROM ".$tableName;
  $sh = $dbh->query($query);
  $columns = $sh->fetchAll(PDO::FETCH_COLUMN);
  $html = '<table border ="1"><tbody> <tr>';
  foreach($columns as $column) {
    $html .= '<th>'.$column.'</th>'; 
  }
  $html .= '</tr> <tr>';
  while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
    foreach($columns as $column) {
      $html .= '<td>'.htmlspecialchars($row[$column]).'</td>';
    }
    $html .= '</tr>';
  }
  $dbh = null;
  return $html;
 }
?>


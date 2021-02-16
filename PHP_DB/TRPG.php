<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<title>TRPGのシナリオ管理ページ</title>
</head>
<body>
  <h1> シナリオ情報記録</h1>
  <form action = "registTRPG.php"  method = "post">
  <p>
  タイトル: 
  </p>
  <input type = "text"  name ="scenario[title]" />
  <p>
  PL数
  </p>
  <input type = "number" min="1"  name ="scenario[players]" />
  <p>
  時間(/時)
  </p>
  <input type = "number" min="0"  name ="scenario[time_h]" />
  <p>
  難易度(5段階)
  </p>
  <input type = "number" min = "1" max = "5"  name ="scenario[difficult]" />
  <p>
  KP回数
  </p>
  <input type = "number" min ="0"  name ="scenario[num_kp]" />
  <p>
  PL回数
  </p>
  <input type = "number" min="0"  name ="scenario[num_pl]" />
  <p>
  シナリオURL or 出典
  </p>
  <input type = "text"  name ="scenario[url]" /> 
  <p>
  コメント
  </p>
  <input type = "text"  name ="scenario[comment]" />
  <input type = "submit"  value ="send" />
  </form>
  
</body>
</html>

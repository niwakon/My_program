# PHP_DB

Webで操作するクトゥルフ神話TRPGのシナリオ管理アプリ

ブラウザ(PHP)を介してDBを操作する

### シナリオの登録
![登録](https://user-images.githubusercontent.com/25600727/108032472-e0353500-7075-11eb-87d5-f0f4c1ed97d2.gif)

### テーブル表示画面(ソート付き)
![ソート](https://user-images.githubusercontent.com/25600727/108032736-49b54380-7076-11eb-8acd-e3486ddd3b0f.gif)

### テーブルから行の削除
![削除](https://user-images.githubusercontent.com/25600727/108032833-6baec600-7076-11eb-9023-7c093c8b9ce4.gif)

## showTRPG.php

　DBからテーブルを取得して表示(メインページ)
  一部のカラムでソートして表示可能

　ソート時にページを更新せずにテーブルのみ更新する(ajax使用)

## addTRPG.php

 必要事項を記入してテーブルに追加するページ
 実際の処理は、記入された変数を「registerTRPG.php」へPostして「registerTRPG.php」が登録処理を行う。

## registerTRPG.php
  
 「addTRPG.php」から変数受け取り、テーブルに登録する。
 Web上では処理を実行して「showTRPG.php」へリダイレクトされる

## editTRPG.php
 
 テーブルの編集を行うページ。現時点ではチェックした行の削除のみできる。

## delete.php
 実際の削除処理を行う(「registerTRPG.php」とほぼ同じ)

 Web上では処理を実行して「showTRPG.php」へリダイレクトされる

## myLibrary.php

 よく使う処理を関数としてまとめたもの。
 テーブルの表示など

## 今後追加予定
・テーブルの編集でPL, KP回数を増やせるようにする

・シナリオ追加の画面などのUI周り

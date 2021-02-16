# PHP_DB

Webで操作するクトゥルフ神話TRPGのシナリオ管理アプリ

ブラウザ(PHP)を介してDBを操作する

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

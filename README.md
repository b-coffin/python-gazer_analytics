# Gazer Analytics

## 概要
gazerでexportした内容を解析するツール

## 使用方法

### .envファイルを用意

```
touch .env
open .env
```

指定する環境変数は下記

* `LOOKER_HOST` : Lookerのホスト名


### ~/.netrcファイルを用意

Lookerの接続情報を記載したファイルを作成

作成方法は[Makefile](Makefile)に記載

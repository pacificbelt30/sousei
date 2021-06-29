# sousei
# ルーティング
- / /userにリダイレクト
- /user 講義選択ページ？
- /kamoku/{kamoku_id} kamoku_idは変数，kamoku_idの示す科目の出欠リストを表とグラフで表示するページ
- /edit 科目規則編集ページ
- /auth ログインページ
- /auth/logout ログアウトページ，ログインページにリダイレクト
- /auth/chpass パスワード変更ページ
- /csv

# ディレクトリ構成

```
sousei
├ app ↓
│
├ run.py --- 実行スクリプト
│
├ docker-compose.yml --- docker-compose
├ dockerrun.sh --- nginxコンテナ作成シェルスクリプト
├ uwsgi.ini --- uwsgi初期化ファイル
```
```
app
├ instance
│ └ config  
│   ├ settings.py
│   └ 
├ app
│ ├ routes --- ルーティング
│ │ ├ route.py
│ │ └ rasp_.py
│ ├ models --- モデル
│ │ ├ model.py
│ │ └ 
│ ├ templates --- htmlファイル
│ │ ├ index.html
│ │ └ 
│ ├ static --- js,cssファイル
│ │ ├ index.css
│ │ └ index.js
│ └ 
├ application.py
├ __init__.py
├ manager.py
└ 
```


# 下準備
以下を実行
```sh
git clone https://github.com/pacificbelt30/sousei
cd sousei
pip install -r requirements.txt
```

app/env.pyを作成し，
- DB_USER
- DB_PASS
- DB_HOST
- DB_PORT
- DB_NAME

を定義する．

実行方法へ

# 実行方法
## nginxにdocker-composeを使用する
以下のコマンドを実行しnginxコンテナを立ち上げる
```sh
docker-compose up -d
```
ブラウザで [http://localhost:5002](http://localhost:5002) に接続

## nginxにdockerを使用する
以下のコマンドを実行しnginxコンテナを立ち上げる
```sh
docker-compose up -d
sh dockerrun.sh
```
ブラウザで [http://localhost:2000](http://localhost:2000) に接続  
windowsの場合はdockerrun.shの中身だけ実行すれば多分ok

## 自前環境
```sh
docker-compose up -d
python run.py
```
ブラウザで [http://localhost:5000](http://localhost:5000) に接続

データベースにデータを入れるために
あらかじめsousei_dbという名前のデータベースを作成し，
http://localhost/makedb にアクセスすればdatabaseが作成される．

or
```sh
    python run.py -mb
```
作り直すためにはdropしてください．

# 必要なもの
- data/  
sousei/以下にdataディレクトリを作成し，各種データをcsvファイルとして入れておく
- app/env.py

# memo
- docker内では ```nginx -g "daemon off;"``` でnginxを起動
- docker内でdbにアクセスする場合ホスト名を localhost -> db に変更
- docker内でwebサーバを用いるとホストマシンで使うより遥かに遅くなる
- 時間設定をどうするか
- 時間オーバーで欠席扱いの人はデータベースに登録するか

# TODO
- 認証 o
- ルーティング o
- 非同期 x
- ラズパイとWEBページのUI
- 例外処理(sqlalchemy.exc.IntegrityError)
- モデル再考 -> 性別やよみがなを追加した．講義回数を数えるやつを足した
- グラフのフォーマット
    - 出席率・遅刻率・の折れ線グラフまたは層になってる棒グラフ
    - 個人の棒グラフ
- フィルタの仕様
    - n回目フィルタ
    - 人名フィルタ
    - 学籍番号フィルタ
- スレッドを止める方法 or inputを止める方法
- printをちゃんと書きましょう
- window.crypto.subtleはhttp環境で違うIPアドレスからのリクエストだと使えないっぽい？
- なんか知らないけどちょくちょくデータベースとの接続が切れるのでなんとかする


# sqlalchemy
テーブル定義はmodels/model.pyに書いてまする．

[SQLAlchemyの使い方](https://qiita.com/tomo0/items/a762b1bc0f192a55eae8#delete)
## create
```
db.session.add(modelclass)
db.session.commit()
```
## read
```
db.session.query(modelclass)
db.session.query(modelclass).filter(条件式).all() # 全件
db.session.query(modelclass).filter(条件式).first() # 最初の1件
```
## update
```
user = db.session.query(modelclass).filter(条件式).first()
user.id = 1
db.session.commit()
```
## delete
```
db.session.query(modelclass).filter(条件式).delete()
db.session.commit()
```

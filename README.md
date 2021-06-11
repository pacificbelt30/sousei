# sousei

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

http://localhost/makedb にアクセスすればdatabaseが作成される．

# 必要なもの
- data/  
sousei/以下にdataディレクトリを作成し，各種データをcsvファイルとして入れておく
- app/env.py

# memo
- docker内では ```nginx -g "daemon off;"``` でnginxを起動
- docker内でdbにアクセスする場合ホスト名を localhost -> db に変更
- docker内でwebサーバを用いるとホストマシンで使うより遥かに遅くなる

# TODO
- 認証

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
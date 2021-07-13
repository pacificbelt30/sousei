# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,url_for,redirect,abort
from flask_login import login_required,current_user
from app.application import app,cache
from app.models.model import *
from app.models.schema import *
from app.routes import rasp_route,edit_route,auth_route
from sqlalchemy.dialects import mysql
import time

"""
@app.route でルーティング
@cache.cached(timeout=60) でキャッシュを設定 (timeoutは秒)
@login_required をつけることでログインが必要なページになる
current_user が現在のログインユーザの情報を格納したLoginUserクラスのインスタンスになる
"""
"""
<li><a href='{{ url_for('kamoku_all') }}'>講義選択</a></li>
<li><a href='{{ url_for('syusseki_all',kamoku=kamoku) }}'>データ閲覧</a></li>
<li><a href='{{ url_for('edit.edit_get',kamoku=kamoku) }}'>時間設定</a></li>
<li><a href='{{ url_for('auth.logout_get') }}'>ログアウト</a></li>
"""

# blueprint登録
#from models.database import init_db
app.register_blueprint(rasp_route.rasp_route)
app.register_blueprint(edit_route.edit_route)
app.register_blueprint(auth_route.auth_route)

# icon
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("img/favicon.ico")

# /user にリダイレクトする
@app.route('/',methods=['GET'])
@login_required
def index():
    return redirect(url_for('kamoku_all'))
    return render_template('index.html',data=data)

# testをしたいとき
@app.route('/test',methods=['GET'])
@login_required
def test():
    data = db.session.query(Kamoku).filter(Kamoku.id=='F1').first()
    print(data.timedef.zikan)
    # ajax cookie test
    return jsonify({"id":current_user.id})

# 科目選択ページ 
# 取得データ
"""
kamoku_data = [KamokuClass1,KamokuClass2]
"""
@app.route('/user',methods=['GET'])
@login_required
#@cache.cached(timeout=60)
def kamoku_all():
    #kyoin = request.args.get('kyoin')
    kyoin = current_user.id
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()
    print('科目選択ページ：')
    print('userid:',current_user.id)
    print('username:',current_user.kyoin.name)
    #print('username:',kamoku_data[0].kyoin.name)
    #return render_template('user.html',kamoku_data=kamoku_data)
    return render_template('select.html',id=current_user.id,kamoku_data=kamoku_data)

# 科目の出席データ
# 取得データ
"""
kamoku：科目id
kamoku_data：教員が担当している科目モデルのクラスの配列 ex)[KamokuClass1,KamokuClass2]
table_header：表のヘッダ(別にいらない) ex)[学籍番号,氏名,1,2,...,15]
risyu_list：履修者リスト
syusseki_data：出席データ ex)[['A','出席',1],['B','出席',2],...]
"""
@app.route('/kamoku/<string:kamoku>',methods=['GET'])
@login_required
@cache.cached(timeout=30)
def syusseki_all(kamoku):
    kyoin = current_user.id
    print('出席データ閲覧ページ：')
    print('userid:',current_user.id)
    print('username:',current_user.kyoin.name)
    print('kamoku:',kamoku)

    # 科目の名前
    kamoku_name = db.session.query(Kamoku).filter(Kamoku.kyoin_id1==current_user.id,Kamoku.id==kamoku).first()
    if kamoku_name is None:
        return abort(404)
    kamoku_name = kamoku_name.name

    # 科目のデータ
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()
    if kamoku_data is None:
        return abort(404)

    # 科目の出席データ
    #data = db.session.query(Syusseki).join(Risyu).filter(\
            #Risyu.kamoku_id==kamoku\
            #).all()

    # sqlを実行し，配列で結果をもらうことで高速化している
    sql = db.session.query(Syusseki).join(Risyu).filter(\
            Risyu.kamoku_id==kamoku\
            )
    sql = str(sql.statement.compile(dialect=mysql.dialect(),\
                                  compile_kwargs={"literal_binds": True}))
    data = db.session.execute(sql)

    # 科目の履修者データ(教員のidでも条件付をしている)
    risyudata = db.session.query(Risyu).join(Kamoku).filter(\
            Risyu.kamoku_id == kamoku,\
            Kamoku.id == Risyu.kamoku_id,\
            Kamoku.kyoin_id1 == kyoin\
            ).all()
    risyujson = RisyuSchema(many=True).dump(risyudata)
    risyujson = [ s['gakusei'] for s in risyujson ]
    #print('syusssekischema',risyujson)
    # [学籍番号,学生氏名] の配列
    risyusya_info_list = risyujson

    # 講義回数のデータ
    lectured = db.session.query(Lectured).filter(\
            Lectured.kamoku_id == kamoku
            ).all()
    if lectured != []:
        lectured_list = [s.kaisu for s in lectured ]
    print('講義開催回：',lectured_list)

    # 履修者データが空->ログインしている教員の担当科目ではない
    if risyudata == []:
        return abort(404)

    # 0列目学籍番号，1列目学生氏名，2~17列目各回の出席データ
    table_header = ['学籍番号','氏名','第1回','第2回','第3回','第4回','第5回','第6回',\
            '第7回','第8回','第9回','第10回','第11回','第12回','第13回','第14回','第15回']

    # [学生氏名,出欠,授業回数] の配列
    table = list()
    #for i in range(len(data)):
    for i,d in enumerate(data):
        table.append([])
        #table[i].append(data[i].risyu.gakusei.name)
        #table[i].append(data[i].syukketu)
        #table[i].append(data[i].kaisu)
        table[i].append(d[12])
        table[i].append(d[2])
        table[i].append(d[3])

    return render_template('view.html',id=current_user.id,\
            kamoku_name=kamoku_name,table_header=table_header,\
            syusseki_data=sorted(table,key=lambda x: x[0]),\
            risyu_list=risyusya_info_list,kamoku_data=kamoku_data,\
            kamoku=kamoku,lectured_list=sorted(lectured_list))
    #いらないかもしれないデータ table_header,kamoku_data

# 科目の出席データ ベンチ用ページ
@app.route('/bench/<string:kamoku>',methods=['GET'])
#@cache.cached(timeout=30)
def bench_syusseki(kamoku):
    kyoin = 'P011'
    print('出席データ閲覧ページ：')
    print('kamoku:',kamoku)

    # 科目の名前
    kamoku_name = db.session.query(Kamoku).filter(Kamoku.kyoin_id1==kyoin,Kamoku.id==kamoku).first().name
    # 科目のデータ
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()

    # 科目の出席データ
    start = time.time()
    #data = db.session.query(Syusseki).join(Risyu).filter(\
            #Risyu.kamoku_id==kamoku\
            #)
    #print(data.statement.compile(dialect=mysql.dialect(),compile_kwargs={"literal_binds":True}))
    sql = db.session.query(Syusseki).join(Risyu).filter(\
            Risyu.kamoku_id==kamoku\
            )
    sql = str(sql.statement.compile(dialect=mysql.dialect(),\
                                  compile_kwargs={"literal_binds": True}))
    data = db.session.execute(sql)
    #for i in data:
        #print(i)
    #print(data)

    #data = db.session.query(Syusseki).all()
    #print(conn.is_connected())
    #cur.execute("select * from syusseki")
    #a = cur.fetchall()
    print(time.time()-start)

    # 科目の履修者データ(教員のidでも条件付をしている)
    risyudata = db.session.query(Risyu).join(Kamoku).filter(\
            Risyu.kamoku_id == kamoku,\
            Kamoku.id == Risyu.kamoku_id,\
            Kamoku.kyoin_id1 == kyoin\
            ).all()
    risyujson = RisyuSchema(many=True).dump(risyudata)
    #print(type(risyudata))
    risyujson = [ s['gakusei'] for s in risyujson ]
    #print('syusssekischema',risyujson)
    #print(data)
    #print(risyudata)
    lectured = db.session.query(Lectured).filter(\
            Lectured.kamoku_id == kamoku
            ).all()
    lectured_list = [s.kaisu for s in lectured ]
    print('講義開催回：',lectured_list)

    # 履修者データが空->ログインしている教員の担当科目ではない
    if risyudata == []:
        return abort(404)

    # 0列目学籍番号，1列目学生氏名，2~17列目各回の出席データ
    table_header = ['学籍番号','氏名','第1回','第2回','第3回','第4回','第5回','第6回',\
            '第7回','第8回','第9回','第10回','第11回','第12回','第13回','第14回','第15回']

    # [学籍番号,学生氏名] の配列
    risyusya_info_list = risyujson

    # [学生氏名,出欠,授業回数] の配列
    table = list()
    #for i in range(len(data)):
    for i,d in enumerate(data):
        table.append([])
        #table[i].append(data[i].risyu.gakusei.name)
        #table[i].append(data[i].syukketu)
        #table[i].append(data[i].kaisu)
        table[i].append(d[12])
        table[i].append(d[2])
        table[i].append(d[3])
        #print(table[i])

    #return render_template('syukketu.html',syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    #return render_template('syukketu2.html',table_header=table_header,syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data,kamoku=kamoku)
    #return render_template('view.html',table_header=table_header,syusseki_data=sorted(table,key=lambda x: x[0]),risyu_list=risyusya_info_list,kamoku_data=kamoku_data,kamoku=kamoku,lectured_list=sorted(lectured_list))
    return render_template('view.html',id=kyoin,\
            kamoku_name=kamoku_name,table_header=table_header,\
            syusseki_data=sorted(table,key=lambda x: x[0]),\
            risyu_list=risyusya_info_list,kamoku_data=kamoku_data,\
            kamoku=kamoku,lectured_list=sorted(lectured_list))


# データベース作成
# 危ないのでそのうち消す
#@app.route('/makedb',methods=['GET'])
def mkdb():
    from app.makedb import makedb
    makedb()
    return '成功'

# 500 Internal Server Error ハンドル
@app.errorhandler(500)
def error_500(e):
    return "内部サーバーエラー"

# 404 Not Found Error ハンドル
@app.errorhandler(404)
def error_404(e):
    return "NOTFOUND"


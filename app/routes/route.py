# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,url_for,redirect,abort
from flask_login import login_required,current_user
from app.application import app,cache
from app.models.model import *
from app.models.schema import *
from app.routes import rasp_route,edit_route,auth_route
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
    return render_template('select.html',kamoku_data=kamoku_data)

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

    # 科目のデータ
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()

    # 科目の出席データ
    data = db.session.query(Syusseki).join(Risyu).filter(\
            Risyu.kamoku_id==kamoku\
            ).all()

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
    risyusya_info_list = list()
    for i in range(len(risyudata)):
        risyusya_info_list.append(list())
        risyusya_info_list[i].append(risyudata[i].gakusei.number)
        risyusya_info_list[i].append(risyudata[i].gakusei.name)

    # [学生氏名,出欠,授業回数] の配列
    table = list()
    for i in range(len(data)):
    #for i in range(1500):
        table.append([])
        table[i].append(data[i].risyu.gakusei.name)
        table[i].append(data[i].syukketu)
        table[i].append(data[i].kaisu)
    risyusya_info_list = risyujson

    #return render_template('syukketu.html',syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    #return render_template('syukketu2.html',table_header=table_header,syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data,kamoku=kamoku)
    return render_template('view.html',table_header=table_header,syusseki_data=sorted(table,key=lambda x: x[0]),risyu_list=risyusya_info_list,kamoku_data=kamoku_data,kamoku=kamoku,lectured_list=lectured_list)

# 科目の出席データ ベンチ用ページ
@app.route('/bench/<string:kamoku>',methods=['GET'])
#@cache.cached(timeout=30)
def bench_syusseki(kamoku):
    kyoin = 'P011'

    # 科目のデータ
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()

    # 科目の出席データ
    data = db.session.query(Syusseki).join(Risyu).filter(\
            Risyu.kamoku_id==kamoku\
            ).all()

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
    print(lectured_list)
    # 履修者データが空->ログインしている教員の担当科目ではない
    if risyudata == []:
        return abort(404)
    # 0列目学籍番号，1列目学生氏名，2~17列目各回の出席データ
    table_header = ['学籍番号','氏名','第1回','第2回','第3回','第4回','第5回','第6回',\
            '第7回','第8回','第9回','第10回','第11回','第12回','第13回','第14回','第15回']

    # [学籍番号,学生氏名] の配列
    risyusya_info_list = list()
    for i in range(len(risyudata)):
        risyusya_info_list.append(list())
        risyusya_info_list[i].append(risyudata[i].gakusei.number)
        risyusya_info_list[i].append(risyudata[i].gakusei.name)

    # [学生氏名,出欠,授業回数] の配列
    table = list()
    for i in range(len(data)):
    #for i in range(1500):
        table.append([])
        table[i].append(data[i].risyu.gakusei.name)
        table[i].append(data[i].syukketu)
        table[i].append(data[i].kaisu)
    risyusya_info_list = risyujson

    #return render_template('syukketu.html',syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    #return render_template('syukketu2.html',table_header=table_header,syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data,kamoku=kamoku)
    return render_template('view.html',table_header=table_header,syusseki_data=sorted(table,key=lambda x: x[0]),risyu_list=risyusya_info_list,kamoku_data=kamoku_data,kamoku=kamoku,lectured_list=lectured_list)


# データベース作成
# 危ないのでそのうち消す
@app.route('/makedb',methods=['GET'])
def mkdb():
    from app.makedb import makedb
    makedb()
    return '成功'

# 
@app.route('/user/<string:name>',methods=['GET'])
def user_index(name):
    print(name)
    return name
    #pass

# テストしたいとき
@app.route('/test/test1',methods=['GET'])
def test1():
    test = db.session.query(Gakusei).filter(Gakusei.id == 12)
    print(test)
    print(test.all())
    print(test.all() == [])
    #print(len(test))
    print(len(test.all()))
    return "true"

# 500 Internal Server Error ハンドル
@app.errorhandler(500)
def error_500(e):
    return "内部サーバーエラー"

# 404 Not Found Error ハンドル
@app.errorhandler(404)
def error_404(e):
    return "NOTFOUND"


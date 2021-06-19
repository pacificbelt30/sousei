# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,url_for,redirect,abort
from flask_login import login_required,current_user
from app.application import app,cache
from app.models.model import *
from app.routes import rasp_route,edit_route,auth_route
import time

"""
@app.route でルーティング
@cache.cached(timeout=60) でキャッシュを設定 (timeoutは秒)
@login_required をつけることでログインが必要なページになる
current_user が現在のログインユーザの情報を格納したLoginUserクラスのインスタンスになる
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

# 
@app.route('/',methods=['GET'])
@login_required
def index():
    return redirect(url_for('kamoku_all'))
    start = time.time()
    #from app.makedb import makedb
    #makedb()
    #print(db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all())
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all()
    print(len(data))
    print(time.time()-start)
    return render_template('index.html',data=data)

# testをしたいとき
@app.route('/test',methods=['GET'])
@login_required
def test():
    data = db.session.query(Kamoku).filter(Kamoku.id=='F1').first()
    print(data.timedef.zikan)
    # ajax cookie test
    return jsonify({"id":current_user.id})

# 教員ページ
@app.route('/user',methods=['GET'])
@login_required
@cache.cached(timeout=60)
def kamoku_all():
    #kyoin = request.args.get('kyoin')
    kyoin = current_user.id
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()
    print('userid:',current_user.id)
    print('username:',current_user.kyoin.name)
    #print('username:',kamoku_data[0].kyoin.name)
    return render_template('user.html',kamoku_data=kamoku_data)

# 科目の出席データ
@app.route('/kamoku/<string:kamoku>',methods=['GET'])
@login_required
@cache.cached(timeout=30)
def syusseki_all(kamoku):
    kyoin = current_user.id
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()
    data = db.session.query(Syusseki).join(Risyu).filter(\
            Risyu.kamoku_id==kamoku\
            ).all()
    #data = db.session.query(Syusseki)
    #data = data.filter(data.risyu.kamoku_id==kamoku).all()
    risyudata = db.session.query(Risyu).join(Kamoku).filter(\
            Risyu.kamoku_id == kamoku,\
            Kamoku.id == Risyu.kamoku_id,\
            Kamoku.kyoin_id1 == kyoin\
            ).all()
    #print(risyudata)
    if risyudata == []:
        return abort(404)
    # 0列目学籍番号，1列目学生氏名，2~17列目各回の出席データ
    table_header = ['学籍番号','氏名','第1回','第2回','第3回','第4回','第5回','第6回',\
            '第7回','第8回','第9回','第10回','第11回','第12回','第13回','第14回','第15回']
    table_array = list()
    for i in range(len(risyudata)):
        table_array.append(list())
        for j in range(17):
            table_array[i].append('')
        table_array[i][0] = risyudata[i].gakusei.number # ここが遅い
        table_array[i][1] = risyudata[i].gakusei.name # ここが遅い
        #table_array[i][0] = ''
        #table_array[i][1] = ''
    for i in data:
        for j in range(len(table_array)):
            if table_array[j][1] == i.risyu.gakusei.name:
                table_array[j][i.kaisu+1] = i.syukketu # ここが遅い
                #table_array[j][i.kaisu+1] = ' '

    #for i in range(len(risyudata)):
        #table_array.append(list())
        #table_array[i][0] = risyudata[i].gakusei.number # ここが遅い
        #table_array[i][1] = risyudata[i].gakusei.name # ここが遅い
    #table_array2 = list()
    #for i in range(len(data)):
        #table_array2.append(list())
        #table_array2[i].append(i.risyu.gakusei_id)
        #table_array2[i].append(i.syukketu)
        #table_array2[i].append(i.kaisu)

    #return render_template('syukketu.html',syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    return render_template('syukketu2.html',table_header=table_header,syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data,kamoku=kamoku)
    #return render_template('test.html')

# 科目の出席データ ベンチ用ページ
@app.route('/bench/<string:kamoku>',methods=['GET'])
@cache.cached(timeout=30)
def bench_syusseki(kamoku):
    kyoin = request.args.get('kyoin')
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()
    data = db.session.query(Syusseki).join(Risyu).filter(\
            Risyu.kamoku_id==kamoku\
            ).all()
    #data = db.session.query(Syusseki)
    #data = data.filter(data.risyu.kamoku_id==kamoku).all()
    risyudata = db.session.query(Risyu).filter(\
            Risyu.kamoku_id == kamoku\
            ).all()
    # 0列目学籍番号，1列目学生氏名，2~17列目各回の出席データ
    table_header = ['学籍番号','氏名','第1回','第2回','第3回','第4回','第5回','第6回',\
            '第7回','第8回','第9回','第10回','第11回','第12回','第13回','第14回','第15回']
    table_array = list()
    for i in range(len(risyudata)):
        table_array.append(list())
        for j in range(17):
            table_array[i].append('')
        table_array[i][0] = risyudata[i].gakusei.number # ここが遅い
        table_array[i][1] = risyudata[i].gakusei.name # ここが遅い
        #table_array[i][0] = ''
        #table_array[i][1] = ''
    for i in data:
        for j in range(len(table_array)):
            if table_array[j][1] == i.risyu.gakusei.name:
                table_array[j][i.kaisu+1] = i.syukketu # ここが遅い
                #table_array[j][i.kaisu+1] = ' '

    #for i in range(len(risyudata)):
        #table_array.append(list())
        #table_array[i][0] = risyudata[i].gakusei.number # ここが遅い
        #table_array[i][1] = risyudata[i].gakusei.name # ここが遅い
    #table_array2 = list()
    #for i in range(len(data)):
        #table_array2.append(list())
        #table_array2[i].append(i.risyu.gakusei_id)
        #table_array2[i].append(i.syukketu)
        #table_array2[i].append(i.kaisu)

    #return render_template('syukketu.html',syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    return render_template('syukketu2.html',table_header=table_header,syusseki_data=sorted(table_array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    #return render_template('test.html')

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


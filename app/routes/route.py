# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,url_for
from app.application import app
from app.models.model import *
from app.routes import rasp_route
import time

#from models.database import init_db
app.register_blueprint(rasp_route.rasp_route)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("img/favicon.ico")

@app.route('/',methods=['GET'])
def hello():
    start = time.time()
    #from app.makedb import makedb
    #makedb()
    #print(db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all())
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all()
    print(len(data))
    print(time.time()-start)
    return render_template('index.html',data=data)

@app.route('/test',methods=['GET'])
def test():
    data = db.session.query(Kamoku).filter(Kamoku.id=='F1').first()
    print(data.timedef.zikan)
    return ''

@app.route('/user',methods=['GET'])
def kamoku_all():
    kyoin = request.args.get('kyoin')
    kamoku_data = db.session.query(Kamoku).join(Kyoin).filter(Kyoin.id==kyoin).all()
    return render_template('user.html',kamoku_data=kamoku_data)

@app.route('/kamoku/<string:kamoku>',methods=['GET'])
def syusseki_all(kamoku):
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
    array = list()
    for i in range(len(risyudata)):
        array.append(list())
        for j in range(17):
            array[i].append('')
        array[i][0] = risyudata[i].gakusei.number # ここが遅い
        array[i][1] = risyudata[i].gakusei.name # ここが遅い
        #array[i][0] = ''
        #array[i][1] = ''
    for i in data:
        for j in range(len(array)):
            if array[j][1] == i.risyu.gakusei.name:
                array[j][i.kaisu+1] = i.syukketu # ここが遅い
                #array[j][i.kaisu+1] = ' '

    #for i in range(len(risyudata)):
        #array.append(list())
        #array[i][0] = risyudata[i].gakusei.number # ここが遅い
        #array[i][1] = risyudata[i].gakusei.name # ここが遅い
    #array2 = list()
    #for i in range(len(data)):
        #array2.append(list())
        #array2[i].append(i.risyu.gakusei_id)
        #array2[i].append(i.syukketu)
        #array2[i].append(i.kaisu)

    #return render_template('syukketu.html',syusseki_data=sorted(array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    return render_template('syukketu2.html',syusseki_data=sorted(array,key=lambda x: x[0]),kamoku_data=kamoku_data)
    #return render_template('test.html')

@app.route('/makedb',methods=['GET'])
def mkdb():
    from app.makedb import makedb
    makedb()
    return '成功'

@app.route('/user/<string:name>',methods=['GET'])
def user_index(name):
    print(name)
    return name
    #pass

@app.route('/test/test1',methods=['GET'])
def test1():
    test = db.session.query(Gakusei).filter(Gakusei.id == 12)
    print(test)
    print(test.all())
    print(test.all() == [])
    #print(len(test))
    print(len(test.all()))
    return "true"

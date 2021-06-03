# -*- coding: utf-8 -*-
"""flask appの初期化を行い、flask appオブジェクトの実体を持つ"""
from flask import Flask, request,jsonify,render_template
from app.application import app
from app.models.model import *
import time

#from models.database import init_db


@app.route('/',methods=['GET'])
def hello():
    start = time.time()
    #import app.makedb
    #app.makedb.makedb()
    #print(db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all())
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all()
    print(len(data))
    print(time.time()-start)
    return render_template('index.html',data=data)

@app.route('/kamoku/<string:kamoku>',methods=['GET'])
def kamoku_all(kamoku):
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(\
            Risyu.id==Syusseki.risyu_id,\
            Risyu.gakusei_id==Gakusei.number,\
            Risyu.kamoku_id==Kamoku.id,\
            Risyu.kamoku_id==kamoku\
            ).all()
    risyudata = db.session.query(Risyu,Gakusei).filter(\
            Risyu.gakusei_id == Gakusei.number,
            Risyu.kamoku_id == kamoku
            ).all()
    array = list()
    for i in range(len(risyudata)):
        array.append(list())
        for j in range(16):
            array[i].append('')
        array[i][0] = risyudata[i].Gakusei.number
        array[i][1] = risyudata[i].Gakusei.name
    for i in data:
        for j in range(len(array)):
            if array[j][1] == i.Gakusei.name:
                array[j][i.Syusseki.kaisu+1] = i.Syusseki.syukketu

    return render_template('syukketu.html',data=sorted(array,key=lambda x: x[0]))

# 履修者データを落とす用
"""
{
"kamoku":"F1",
"start_syusseki":"+20",
"csv":csvdata
}
"""
@app.route('/csv',methods=['GET'])
def csv_get():
    kamoku = request.args.get('kamoku')
    print(type(kamoku))
    #json = request.get_json()
    data = {"kamoku":kamoku,"kisoku":"","csv":list()}
    risyudata = db.session.query(Risyu,Gakusei,Kamoku,KamokuKisoku).filter( \
        Risyu.kamoku_id==kamoku,\
        Risyu.gakusei_id==Gakusei.number,\
        Risyu.kamoku_id==Kamoku.id,\
        Kamoku.id==KamokuKisoku.id\
        ).all()
    csv = list()
    for i in range(len(risyudata)):
        csv.append(list())
        csv[i].append(risyudata[i].Gakusei.id)
        csv[i].append(risyudata[i].Gakusei.number)
        csv[i].append(risyudata[i].Gakusei.name)
        csv[i].append(risyudata[i].Kamoku.name)
        csv[i].append(risyudata[i].KamokuKisoku.start_syusseki)

    tmp = list()
    for i in csv:
        tmp.append(','.join(map(str,i)))
    data["csv"] = '\n'.join(map(str,tmp))
    return jsonify(data)
    #pass

# csvアップロード用
@app.route('/csv',methods=['POST'])
def csv_post():
    json = request.get_json()
    print(json)
    Syusseki.csv_reg_nf(json)
    return jsonify(json)
    #pass

@app.route('/user/<string:name>',methods=['GET'])
def user_index(name):
    print(name)
    return name
    #pass

# 
@app.route('/user/<string:name>/<string:kamoku>',methods=['GET'])
def data(name,kamoku):
    pass

@app.route('/user/<string:name>/<string:kamoku>',methods=['POST'])
def updatedata(name,kamoku):
    pass


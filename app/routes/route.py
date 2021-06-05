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
        for j in range(16):
            array[i].append('')
        array[i][0] = risyudata[i].gakusei.number
        array[i][1] = risyudata[i].gakusei.name
    for i in data:
        for j in range(len(array)):
            if array[j][1] == i.risyu.gakusei.name:
                array[j][i.kaisu+1] = i.syukketu

    return render_template('syukketu.html',syusseki_data=sorted(array,key=lambda x: x[0]),kamoku_data=kamoku_data)

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
    #risyudata = db.session.query(Risyu,Gakusei,Kamoku,KamokuKisoku).filter( \
        #Risyu.kamoku_id==kamoku,\
        #Risyu.gakusei_id==Gakusei.number,\
        #Risyu.kamoku_id==Kamoku.id,\
        #Kamoku.id==KamokuKisoku.id\
        #).all()
    risyudata = db.session.query(Risyu).filter(Risyu.kamoku_id == kamoku).all()
    csv = list()
    for i in range(len(risyudata)):
        csv.append(list())
        csv[i].append(risyudata[i].gakusei.id)
        csv[i].append(risyudata[i].gakusei.number)
        csv[i].append(risyudata[i].gakusei.name)
        csv[i].append(risyudata[i].kamoku.name)

    tmp = list()
    for i in csv:
        tmp.append(','.join(map(str,i)))
    data["csv"] = '\n'.join(map(str,tmp))
    data["start_syusseki"] = risyudata[0].kamoku.kamokukisoku.start_syusseki
    data["start_tikoku"] = risyudata[0].kamoku.kamokukisoku.start_tikoku
    data["end_uketuke"] = risyudata[0].kamoku.kamokukisoku.end_uketuke
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


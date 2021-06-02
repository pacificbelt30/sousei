"""flask appの初期化を行い、flask appオブジェクトの実体を持つ"""
from flask import Flask, request,jsonify,render_template
from app.application import app
from app.models.model import *

#from models.database import init_db


@app.route('/')
def hello():
    import app.makedb
    app.makedb.makedb()
    print(db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all())
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all()
    print(len(data))
    return render_template('index.html',data=data)

@app.route('/csv',methods=['GET'])
def csv_get():
    kamoku = request.args.get('kamoku')
    print(type(kamoku))
    #json = request.get_json()
    data = {"kamoku":kamoku,"kisoku":"","csv":list()}
    risyudata = db.session.query(Risyu).filter(Risyu.kamoku_id==kamoku).all()
    csv = list()
    for i in range(len(risyudata)):
        csv.append(list())
        csv[i].append(risyudata[i].kamoku_id)
        csv[i].append(risyudata[i].gakusei_id)

    tmp = list()
    for i in csv:
        tmp.append(','.join(map(str,i)))
    data["csv"] = '\n'.join(map(str,tmp))
    return jsonify(data)
    #pass

@app.route('/csv',methods=['POST'])
def csv_post():
    json = request.get_json()
    print(json)
    return jsonify(json)
    #pass

@app.route('/user/<string:name>',methods=['GET'])
def user_index(name):
    print(name)
    return name
    #pass

@app.route('/user/<string:name>/<string:kamoku>',methods=['GET'])
def data(name,kamoku):
    pass

@app.route('/user/<string:name>/<string:kamoku>',methods=['POST'])
def updatedata(name,kamoku):
    pass


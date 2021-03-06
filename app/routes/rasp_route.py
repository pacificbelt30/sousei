# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint
#from app.application import app
from app.application import app,cache,db_ping
from app.models.model import *
import json
import time

# /csv をルートとして見る
rasp_route = Blueprint('csv', __name__, url_prefix='/csv')

# csvアップロード用
#/csv からアクセスできる
@rasp_route.route('/',methods=['POST'])
def csv_post():
    db_ping()
    # json = request.get_json()
    # print(json)
    # Syusseki.csv_reg_nf(json)
    # return jsonify(json)
    # #pass
    data = request.get_json()
    print(type(data))
    data_j = json.loads(data)
    print(type(data_j))
    if Syusseki.csv_reg_nf(data_j):
        #return_json = {'status':200,data_j}
        return_json = {'status':200,'data':data_j}
        return jsonify(return_json),200
    else:
        #return_json = {'status':300,data_j}
        return_json = {'status':400,'data':data_j}
        return jsonify(return_json),400

#/csv からアクセスできる
"""
{
    "kamoku":"F1",
    "kisoku":{
        "start_syusseki":20,
        "start_tikoku":20,
        "end_uketuke":90
    },
    "csv":{
        "1":{
            "id":"12e...",
            "name":"秋田県太郎"
            "number":"S0XX"
        },
        "2":{...},"3":{...},...,"n":{...}
    }
}
"""
@rasp_route.route('/',methods=['GET'])
def csv_get():
    db_ping()
    kamoku = request.args.get('kamoku') # getパラメータ取得 ex) /csv?kamoku=F1
    # print(type(kamoku))
    #json = request.get_json()
    data = {"kamoku":kamoku,"kisoku":"","csv":list()} # 送信するデータ
    #risyudata = db.session.query(Risyu,Gakusei,Kamoku,KamokuKisoku).filter( \
        #Risyu.kamoku_id==kamoku,\
        #Risyu.gakusei_id==Gakusei.number,\
        #Risyu.kamoku_id==Kamoku.id,\
        #Kamoku.id==KamokuKisoku.id\
        #).all()
    risyudata = db.session.query(Risyu).filter(Risyu.kamoku_id == kamoku).all()
    jigen = db.session.query(Kamoku).filter(Kamoku.id == kamoku).first().timedef_id
    kaisi = db.session.query(Timedef).filter(Timedef.zigen == jigen).first().zikan
    #csv = list()
    #for i in range(len(risyudata)):
    #    csv.append(list())
    #    csv[i].append(risyudata[i].gakusei.id)
    #    csv[i].append(risyudata[i].gakusei.number)
    #    csv[i].append(risyudata[i].gakusei.name)
    #    csv[i].append(risyudata[i].kamoku.name)
    # db_a = getConnection()
    # cur = db_a.cursor()
    # sql = "select * from gakusei"
    # cur.execute(sql)
    # gakusei = cur.fetchall()
    # cur.close()
    # db_a.close()

    # app=Flask(__name__)
    # ma = Marshmallow(app)
    # class UserSchema(ma.SQLAlchemyAutoSchema):
    #     class Mata:
    #         model = User

    
    # print(risyudata[0].kamoku.kamokukisoku.start_syusseki)
    # csv = UserSchema().dump(risyudata)
    # print(risyudata[0].gakusei.id)
    csv = {}
    
    for i in range(len(risyudata)):
        c = {}
        c['id']=risyudata[i].gakusei.id
        c['name']=risyudata[i].gakusei.name
        c['number']=risyudata[i].gakusei.number
        csv[i]=c
        # csv[i]['id'] = risyudata[i].gakusei.id
        # csv[i]['name'] = risyudata[i].gakusei.name
        # csv[i]['number'] = risyudata[i].gakusei.number
    print(csv)
    
    #tmp = list()
    #for i in csv:
    #    tmp.append(','.join(map(str,i)))
    #data["csv"] ='\n'.join(map(str,tmp))
    #print(gakusei)
    data["csv"] = csv
    tmp=dict()
    tmp["syusseki_gendo"] = risyudata[0].kamoku.kamokukisoku.syusseki_gendo
    tmp["tikoku_gendo"] = risyudata[0].kamoku.kamokukisoku.tikoku_gendo
    # tmp["end_uketuke"] = risyudata[0].kamoku.kamokukisoku.end_uketuke
    tmp["start_kougi"] = kaisi
    data['kisoku']=dict()
    data['kisoku']['1']=tmp
    return jsonify(data)
    #pass

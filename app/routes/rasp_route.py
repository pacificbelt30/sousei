# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint
#from app.application import app
from app.models.model import *
import time

# /csv からのアクセスポイント
rasp_route = Blueprint('csv', __name__, url_prefix='/csv')

# 履修者データを落とす用
"""
{
"kamoku":"F1",
"start_syusseki":"+20",
"csv":csvdata
}
"""
@rasp_route.route('/',methods=['GET'])
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
@rasp_route.route('/',methods=['POST'])
def csv_post():
    json = request.get_json()
    print(json)
    Syusseki.csv_reg_nf(json)
    return jsonify(json)
    #pass



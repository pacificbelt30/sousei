# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint
#from app.application import app
from app.models.model import *
import time

# /csv をルートとして見る
edit_route = Blueprint('edit', __name__, url_prefix='/edit')

# 規則データ編集するようページ
#/edit からアクセスできる
"""
[出席開始時間,遅刻開始時間,受付終了時間]
"""
@edit_route.route('/',methods=['GET'])
def edit_get():
    kamoku = request.args.get('kamoku') # getパラメータ取得 ex) /csv?kamoku=F1
    print(kamoku,type(kamoku))
    #json = request.get_json()
    kisokudata = db.session.query(KamokuKisoku).filter(KamokuKisoku.id == kamoku).all()
    csv = list()
    for i in range(len(kisokudata)):
        csv.append(kisokudata[i].start_syusseki)
        csv.append(kisokudata[i].start_tikoku)
        csv.append(kisokudata[i].end_uketuke)

    return render_template('edit.html',data=kisokudata,csv=csv)
    #pass

# csvアップロード用
#/csv からアクセスできる
"""
[出席開始時間,遅刻開始時間,受付終了時間]
"""
@edit_route.route('/',methods=['POST'])
def edit_post():
    csv = request.form["csv"]
    kamoku = request.form["kamoku"]
    print(csv)
    print(type(csv))
    csv = csv.split(',')
    print(csv)
    print(type(csv[0]))
    print(kamoku)
    kisokudata = db.session.query(KamokuKisoku).filter(KamokuKisoku.id == kamoku).first()
    kisokudata.start_syusseki = csv[0]
    kisokudata.start_tikoku = csv[1]
    kisokudata.end_uketuke = csv[2]
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print("error")
    return render_template('edit.html',data=kisokudata)
    #pass



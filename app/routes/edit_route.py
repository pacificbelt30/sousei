# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint,redirect,url_for
#from app.application import app
from app.models.model import *
from app.models.schema import *
import time

# /csv をルートとして見る
edit_route = Blueprint('edit', __name__, url_prefix='/edit')

# 規則データ編集するようページ
#/edit からアクセスできる
"""
{
start_syusseki：出席終了時間
start_tikoku：遅刻終了時間
end_uketuke：受付終了時間
}
"""
@edit_route.route('/',methods=['GET'])
def edit_get():
    kamoku = request.args.get('kamoku') # getパラメータ取得 ex) /csv?kamoku=F1
    print(kamoku,type(kamoku))
    #json = request.get_json()
    kisokudata = db.session.query(KamokuKisoku).filter(KamokuKisoku.id == kamoku).first()
    print({'status':'ok','kisoku':KamokuKisokuScheme().dump(kisokudata)})
    test = db.session.query(KamokuKisoku).all()
    print({'status':'ok','kisoku':KamokuKisokuScheme(many=True).dump(test)})

    return render_template('edit.html',data=kisokudata,kisoku=KamokuKisokuScheme().dump(kisokudata),kamoku=kamoku)
    #pass

# csvアップロード用
#/csv からアクセスできる
# 送信されることを期待するデータ
"""
{
start_syusseki：出席終了時間
start_tikoku：遅刻終了時間
end_uketuke：受付終了時間
}
"""
@edit_route.route('/',methods=['POST'])
def edit_post():
    kamoku = request.form["kamoku"]
    start_syusseki = request.form["start_syusseki"]
    start_tikoku = request.form["start_tikoku"]
    end_uketuke = request.form["end_uketuke"]
    print(kamoku)
    kisokudata = db.session.query(KamokuKisoku).filter(KamokuKisoku.id == kamoku).first()
    kisokudata.start_syusseki = start_syusseki
    kisokudata.start_tikoku = start_tikoku
    kisokudata.end_uketuke = end_uketuke
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print("TIME_EDIT_ERROR")
    #return render_template('edit.html',data=kisokudata)
    return redirect(url_for('edit.edit_get',kamoku=kamoku)) #     #pass



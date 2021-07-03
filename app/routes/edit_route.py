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

    return render_template('time.html',data=kisokudata,kisoku=KamokuKisokuSchema().dump(kisokudata),kamoku=kamoku)
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
    # フォームのデータを取得
    kamoku = request.form["kamoku"]
    #start_syusseki = request.form["start_syusseki"]
    #start_tikoku = request.form["start_tikoku"]
    #end_uketuke = request.form["end_uketuke"]
    syusseki_gendo = request.form['syusseki_gendo']
    tikoku_gendo = request.form['tikoku_gendo']
    print(kamoku)

    # 科目IDが一致するデータの科目規則を更新する
    kisokudata = db.session.query(KamokuKisoku).filter(KamokuKisoku.id == kamoku).first()
    #kisokudata.start_syusseki = start_syusseki
    #kisokudata.start_tikoku = start_tikoku
    #kisokudata.end_uketuke = end_uketuke
    kisokudata.syusseki_gendo = syusseki_gendo
    kisokudata.tikoku_gendo = tikoku_gendo
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print("TIME_EDIT_ERROR")
    #return render_template('edit.html',data=kisokudata)
    return redirect(url_for('edit.edit_get',kamoku=kamoku)) #     #pass



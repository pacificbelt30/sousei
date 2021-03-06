# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint,redirect,url_for,abort
from flask_login import login_user, logout_user, login_required,current_user
#from app.application import app
from app.application import app,cache,db_ping
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
@login_required
def edit_get():
    db_ping()
    kamoku = request.args.get('kamoku') # getパラメータ取得 ex) /csv?kamoku=F1
    print('規則データ編集ページ：')
    print('userid:',current_user.id)
    print('username:',current_user.kyoin.name)
    print('kamoku:',kamoku)
    kamoku_name = db.session.query(Kamoku).filter(Kamoku.kyoin_id1==current_user.id,Kamoku.id==kamoku).first()
    if kamoku_name is None:
        return abort(404)
    kamoku_name = kamoku_name.name

    #json = request.get_json()
    kisoku_data = db.session.query(KamokuKisoku).filter(KamokuKisoku.id == kamoku).first()
    if kisoku_data is None:
        return abort(404)
    print('kisokudata:syusseki_gendo:',kisoku_data.syusseki_gendo)
    print('kisokudata:tikoku_gendo:',kisoku_data.tikoku_gendo)

    return render_template('time.html',id=current_user.id,kamoku_name=kamoku_name,data=kisoku_data,kisoku=KamokuKisokuSchema().dump(kisoku_data),kamoku=kamoku)
    #pass

# 送信されることを期待するデータ
"""
{
syusseki_gendo：出席限度時間
tikoku_gendo：遅刻限度時間
}
"""
@edit_route.route('/<string:kamoku>',methods=['POST'])
@login_required
def edit_post(kamoku:str):
    db_ping()
    # フォームのデータを取得
    #kamoku = request.form["kamoku"]
    #start_syusseki = request.form["start_syusseki"]
    #start_tikoku = request.form["start_tikoku"]
    #end_uketuke = request.form["end_uketuke"]
    try:
        syusseki_gendo = request.form['syusseki_gendo']
        tikoku_gendo = request.form['tikoku_gendo']
    except:
        return redirect(url_for('edit.edit_get',kamoku=kamoku)) #     #pass
        
    print('規則データ編集ページPOST->',kamoku)
    print('syusseki_gendo:',syusseki_gendo)
    print('tikoku_gendo:',tikoku_gendo)

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



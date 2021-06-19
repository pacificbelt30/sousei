# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint,redirect,url_for,session
from flask_login import login_user, logout_user, login_required,current_user
from app.application import app
from app.models.model import *
import time

# /csv をルートとして見る
auth_route = Blueprint('auth', __name__, url_prefix='/auth')

# ログイン画面
#/auth からアクセスできる
"""
"""
@auth_route.route('/',methods=['GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('kamoku_all'))
    return render_template('login.html')
    #pass

# 
#/auth からアクセスできる
"""
POST
"""
@auth_route.route('/',methods=['POST'])
def login_post():
    try:
        id = request.form.get('id')
        password = request.form.get('password') # sha256
        remember = True if request.form.get('remember') else False
    except:
        import rollback
        rollback.print_exc()
    user = db.session.query(LoginUser).filter(LoginUser.id == id,LoginUser.password == password).first()
    print('id:',id)
    print('pass:',password)
    print('ログイン判定:',user is not None)
    if user is None:
        return redirect(url_for('auth.login_get'))
        #return "失敗"
    #return render_template('edit.html',data=kisokudata)
    #return "成功"
    session.permanent = True
    login_user(user,remember=remember)
    return redirect(url_for('kamoku_all'))

# logout処理
@auth_route.route('/logout',methods=['GET'])
@login_required
def logout_get():
    print('logout:',current_user.kyoin.name)
    logout_user()
    return redirect(url_for('auth.login_get'))

# パスワード変更画面
@auth_route.route('/chpass',methods=['GET'])
@login_required
def chpass_get():
    return render_template('change_password.html',id=current_user.id)

# パスワード変更
@auth_route.route('/chpass',methods=['POST'])
@login_required
def chpass_post():
    if request.form.get('password') is not None:
        current_user.password = request.form.get('password')
    try:
        db.session.commit()
        print('PASSWORD_CHANGE_SUCCESS','id:',current_user.id)
    except:
        db.session.rollback()
        print('PASSWORD_CHANGE_ERROR','id:',current_user.id)
    return redirect(url_for('kamoku_all'))

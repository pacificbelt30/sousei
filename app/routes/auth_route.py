# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint,redirect,url_for
from flask_login import login_user
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

    return render_template('login.html')
    #pass

# 
#/auth からアクセスできる
"""
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
    print(user is None)
    if user is None:
        return redirect(url_for('auth.login_get'))
        #return "失敗"
    #return render_template('edit.html',data=kisokudata)
    #return "成功"
    login_user(user,remember=remember)
    return redirect(url_for('index',kyoin=user.id))

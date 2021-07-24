# -*- coding: utf-8 -*-
from flask import Flask, request,jsonify,render_template,Blueprint,redirect,url_for,session
from flask_login import login_user, logout_user, login_required,current_user
from app.application import app,cache,db_ping
from app.models.model import *
from app.models.schema import *
import time

# /csv をルートとして見る
auth_route = Blueprint('auth', __name__, url_prefix='/auth')

# ログイン画面
#/auth からアクセスできる
# ログインしている場合は/user にリダイレクト
@auth_route.route('/',methods=['GET'])
def login_get():
    db_ping()
    print('ログインページ：')
    if current_user.is_authenticated: # ログインしている場合は科目選択ページへ
        return redirect(url_for('kamoku_all'))
    return render_template('password.html')
    #return render_template('login.html')
    #pass

# 
#/auth からアクセスできる
# 認証成功後/user にリダイレクト
"""
id：教員ID
password：SHA256でハッシュ化されたpassword文字列
"""
@auth_route.route('/',methods=['POST'])
def login_post():
    db_ping()
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
    db_ping()
    print('logout:',current_user.kyoin.name)
    logout_user()
    return redirect(url_for('auth.login_get'))

# パスワード変更画面
@auth_route.route('/chpass',methods=['GET'])
@login_required
def chpass_get():
    db_ping()
    print('パスワード変更ページ：')
    print('userid:',current_user.id)
    print('username:',current_user.kyoin.name)
    return render_template('passchange.html',id=current_user.id)

# パスワード変更
@auth_route.route('/chpass',methods=['POST'])
@login_required
def chpass_post():
    db_ping()
    if request.form.get('password') is not None:
        current_user.password = request.form.get('password')
    try:
        db.session.commit()
        print('PASSWORD_CHANGE_SUCCESS','id:',current_user.id)
    except:
        db.session.rollback()
        print('PASSWORD_CHANGE_ERROR','id:',current_user.id)
    return redirect(url_for('kamoku_all'))

# パスワードリセット
# デフォルトのパスワードは教員IDと同じ
@auth_route.route('/resetpassword',methods=['POST'])
@login_required
def resetpassword_post():
    db_ping()
    import hashlib
    hash=lambda x:hashlib.sha256(x).hexdigest()

    current_user.password = hash(current_user.id)
    try:
        db.session.commit()
        print('RESET_PASSWORD_SUCCESS','id:',current_user.id)
    except:
        db.session.rollback()
        print('RESET_PASSWORD_ERROR','id:',current_user.id)
    logout_user()
    return redirect(url_for('auth.login_get'))

# パスワードリセット，管理者用
@auth_route.route('/resetpassword/<string:user_id>',methods=['GET'])
def resetpassword_get(user_id):
    db_ping()
    get_pass = request.args.get('p') # パスワード指定 
    password = 'team4'
    import hashlib
    hash=lambda x:hashlib.sha256(x).hexdigest()
    password = str(hash(password))
    print(password)
    if password != get_pass:
        print('管理者のパスワードが違います')
        return

    user = db.session.query(LoginUser).filter(LoginUser.id == user_id).first()
    user.password = hash(user_id.encode())
    try:
        db.session.commit()
        print('RESET_PASSWORD_SUCCESS','id:',user_id)
    except:
        db.session.rollback()
        print('RESET_PASSWORD_ERROR','id:',user_id)

    return redirect(url_for('auth.login_get'))


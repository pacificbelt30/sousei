# -*- coding: utf-8 -*-
"""
flask appの初期化を行い、flask appオブジェクトの実体を持つ
"""
from flask import Flask, request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from flask_login import LoginManager
from datetime import timedelta
from app import env
import mysql.connector as mydb
#from models.database import init_db


def create_app():
    app = Flask(__name__)
    #app.config.from_object('models.config.Config')

    #init_db(app)

    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}?charset=utf8'.format(**{
          'user': env.DB_USER,
          'password': env.DB_PASS,
          'host': env.DB_HOST,
          'port': env.DB_PORT,
          'db_name': env.DB_NAME
      })

    app.config["SECRET_KEY"] = env.SECRET_KEY
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)
    #session.permanent = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE"] = 3
    app.config["SQLALCHEMY_POOL_PRE_PING"] = True

    return app
conn = mydb.connect(
          user= env.DB_USER,
          password = env.DB_PASS,
          host = env.DB_HOST,
          port = env.DB_PORT,
          database = env.DB_NAME
        )
cur = conn.cursor()
app = create_app()
db = SQLAlchemy(app)
ma = Marshmallow(app)
cache = Cache(config={"CACHE_TYPE":"simple"})
cache.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login_get"

from app.models.model import *

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return LoginUser.query.get(user_id)

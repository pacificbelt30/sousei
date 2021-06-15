# -*- coding: utf-8 -*-
"""
flask appの初期化を行い、flask appオブジェクトの実体を持つ
"""
from flask import Flask, request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_caching import Cache
from app import env

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
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE"] = 3

    return app

app = create_app()
db = SQLAlchemy(app)
cache = Cache(config={"CACHE_TYPE":"simple"})
cache.init_app(app)


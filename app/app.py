"""flask appの初期化を行い、flask appオブジェクトの実体を持つ"""
from flask import Flask, request,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy, SessionBase
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

    return app

app = create_app()
db = SQLAlchemy(app)

from app.models.model import *

@app.route('/')
def hello():
    #import app.makedb
    #app.makedb.makedb()
    print(db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all())
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all()
    print(len(data))
    return render_template('index.html',data=data)

@app.route('/csv',methods=['GET'])
def csv_get():
    kamoku = request.args.get('kamoku')
    #json = request.get_json()
    test = list()
    test.append({"id":12,"name":"name"})
    test.append({"id":12,"name":"name"})
    test.append({"id":12,"name":kamoku})
    return jsonify(test)
    #pass

@app.route('/csv',methods=['POST'])
def csv_post():
    json = request.get_json()
    print(json)
    return jsonify(json)
    #pass

@app.route('/user/<string:name>',methods=['GET'])
def user_index(name):
    print(name)
    return name
    #pass

@app.route('/user/<string:name>/<string:kamoku>',methods=['GET'])
def data(name,kamoku):
    pass

@app.route('/user/<string:name>/<string:kamoku>',methods=['POST'])
def updatedata(name,kamoku):
    pass


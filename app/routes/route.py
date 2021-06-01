"""flask appの初期化を行い、flask appオブジェクトの実体を持つ"""
from flask import Flask, request,jsonify,render_template
from app import app

#from models.database import init_db

@app.route('/')
def hello():
    return render_template('index.html')

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


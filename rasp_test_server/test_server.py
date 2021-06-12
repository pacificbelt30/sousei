# -*- coding: utf-8 -*-
"""
flask appの初期化を行い、flask appオブジェクトの実体を持つ
"""
from flask import Flask, request,jsonify,render_template

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    start = time.time()
    #from app.makedb import makedb
    #makedb()
    #print(db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all())
    data = db.session.query(Syusseki,Risyu,Gakusei,Kamoku).filter(Risyu.id==Syusseki.risyu_id).filter(Risyu.gakusei_id==Gakusei.number).filter(Risyu.kamoku_id==Kamoku.id).filter(Risyu.kamoku_id=="F1").all()
    print(len(data))
    print(time.time()-start)
    return render_template('index.html',data=data)

if __name__ == "__main__":
    app.run()

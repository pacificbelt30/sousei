# -*- coding: utf-8 -*-
from app.application import db
from app.models.model import *

def makedb():
    #データ登録
    db.create_all()
    Gakusei.csv_reg('data/gakuseilist.csv')
    Kyoin.csv_reg('data/kyoin.csv')
    Timedef.csv_reg()
    Kamoku.csv_reg("data/kougikamokuyoubi.csv")
    KamokuKisoku.csv_reg("data/kougikamokuyoubi.csv")
    kamokudata = db.session.query(Kamoku).all()
    for s in kamokudata:
        Risyu.csv_reg(s.id)

    # テストデータ
    for i in range(1,16):
        Syusseki.csv_reg("data/syusseki2.csv","F1",i)
    Syusseki.csv_reg("data/syusseki2.csv","M2",1)
    Syusseki.csv_reg("data/syusseki2.csv","M2",3)
    LoginUser.csv_reg()


from app.app import db
from app.models.model import *
def makedb():
    db.create_all()
    #データ登録
    Gakusei.csv_reg('data/gakuseilist.csv')
    Kyoin.csv_reg('data/kyoin.csv')
    Timedef.csv_reg()
    Kamoku.csv_reg("data/kougikamoku.csv")
    KamokuKisoku.csv_reg("data/kougikamoku.csv")
    kamokudata = db.session.query(Kamoku).all()
    for s in kamokudata:
        Risyu.csv_reg(s.id)
    Syusseki.csv_reg("data/syusseki.csv","F1",1)
    Syusseki.csv_reg("data/syusseki.csv","F1",2)


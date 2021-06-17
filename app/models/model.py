# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, SessionBase
from app.models import csvread
#from app import env
from app.application import db
"""
データベーステーブル定義
学生データ    ：Gakusei
教員データ    ：Kyoin
時間データ    ：Timedef
科目データ    ：Kamoku
科目規則データ：KamokuKisoku
履修データ    ：Risyu
出席データ    ：Syusseki
ログインデータ：LoginUser
"""

# 後に教員のログイン用のIDパスワードのテーブルとなるかもしれないやつ
class LoginUser(UserMixin,db.Model):
#class LoginUser(db.Model):
    __tablename__ = 'loginuser'

    id = db.Column(db.String(20),db.ForeignKey('kyoin.id'),nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(256), unique=False)
    kyoin = db.relationship('Kyoin',lazy='joined')


    def __init__(self, id, password):
        self.id = id
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.id

    @staticmethod
    def csv_reg():
        import hashlib
        hash=lambda x:hashlib.sha256(x).hexdigest()
        kyoin = db.session.query(Kyoin).all()
        for i in kyoin:
            print(i.id)
            db.session.add(LoginUser(i.id,hash(i.id.encode('utf-8'))))
        try:
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()


#学生データ
class Gakusei(db.Model):
    __tablename__ = 'gakusei'

    id = db.Column(db.String(20),nullable=False, unique=True, primary_key=True) # IDm
    name = db.Column(db.String(80),nullable=False, unique=False)
    gakunen = db.Column(db.Integer,nullable=False,unique=False)
    number = db.Column(db.String(120),nullable=False,unique=True) # 学籍番号

    def __init__(self, id, name, gakunen, number):
        self.id = id
        self.name = name
        self.gakunen = gakunen
        self.number = number

    def __repr__(self):
        return '<Gakusei %s>' % self.id
        #pass

    @staticmethod
    def csv_reg(filename):
        data = csvread.csv_reader(filename)
        dbdata = [Gakusei(s[4],s[1],0,s[0]) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            db.session.rollback()
            return False
        return True

    @staticmethod
    def add(id,name,gakunen,number):
        try:
            db.session.add(Gakusei(id,name,gakunen,number))
            db.session.commit()
        except:
            return False
        return True


# 教員データ
class Kyoin(db.Model):
    __tablename__ = 'kyoin'

    #id = db.Column(db.Integer,autoincrement=True,nullable=False, unique=True, primary_key=True)
    id = db.Column(db.String(20),nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(20),nullable=False, unique=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Kyoin %s>' % self.id
        #pass

    @staticmethod
    def csv_reg(filename):
        data = csvread.csv_reader(filename)
        dbdata = [Kyoin(s[0],s[1]) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True


# 講義時間定義
class Timedef(db.Model):
    __tablename__ = 'timedef'

    id = db.Column(db.Integer,autoincrement=True,nullable=False, unique=True,primary_key=True) # 
    zigen = db.Column(db.Integer,nullable=False, unique=True) # 
    zikan = db.Column(db.String(80),nullable=False, unique=True) # 

    def __init__(self, zigen, zikan):
        #self.id = id
        self.zigen = zigen
        self.zikan = zikan

    def __repr__(self):
        return '<Timedef %r>' % self.id
        #pass

    @staticmethod
    def csv_reg():
        dbdata = [Timedef(1,'9:00'),Timedef(2,'10:40'),Timedef(3,'13:00'),Timedef(4,'14:40'),Timedef(5,'16:20')]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True


# 科目データ,教員3人登録できる
class Kamoku(db.Model):
    __tablename__ = 'kamoku'

    #id = db.Column(db.Integer,autoincrement=True,nullable=False, unique=True, primary_key=True)
    id = db.Column(db.String(20),nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String(80),nullable=False, unique=False)
    timedef_id = db.Column(db.Integer,db.ForeignKey('timedef.id'),nullable=False,unique=False)
    room = db.Column(db.String(120),nullable=False,unique=False)
    youbi = db.Column(db.String(10),nullable=False,unique=False)
    kyoin_id1 = db.Column(db.String(20),db.ForeignKey('kyoin.id'),nullable=False,unique=False)
    #kyoin_id2 = db.Column(db.String(20),db.ForeignKey('kyoin.id'),nullable=False,unique=False)
    #kyoin_id3 = db.Column(db.String(20),db.ForeignKey('kyoin.id'),nullable=False,unique=False)
    timedef = db.relationship("Timedef")
    kamokukisoku = db.relationship("KamokuKisoku",uselist=False,backref='kamoku')
    #kamokukisoku = db.relationship("KamokuKisoku",backref=backref('kamoku', lazy='dynamic'))
    #kamokukisoku = db.relationship("KamokuKisoku")
    kyoin = db.relationship("Kyoin")

    def __init__(self, id, name, timedef_id, room, youbi, kyoin_id1, kyoin_id2, kyoin_id3):
        self.id = id
        self.name = name
        self.timedef_id = timedef_id
        self.room = room
        self.youbi = youbi
        self.kyoin_id1 = kyoin_id1
        self.kyoin_id2 = kyoin_id2
        self.kyoin_id3 = kyoin_id3

    def __repr__(self):
         return '<Kamoku %s>' % self.id
        #pass

    @staticmethod
    def csv_reg(filename):
        data = csvread.csv_reader(filename)
        dbdata = [Kamoku(s[0],s[1],db.session.query(Timedef).filter(s[5] == Timedef.zikan).first().id,'unknown',s[4],s[2],s[2],s[2]) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True


# 履修者データ,科目と学生の組み合わせは重複なし
class Risyu(db.Model):
    __tablename__ = 'risyu'
    __table_args__  =  ( db.UniqueConstraint ( 'kamoku_id' , 'gakusei_id' ),{}) 

    id = db.Column(db.Integer,autoincrement=True,nullable=False, unique=False, primary_key=True)
    kamoku_id = db.Column(db.String(20),db.ForeignKey('kamoku.id'),nullable=False, unique=False)
    gakusei_id = db.Column(db.String(20),db.ForeignKey('gakusei.number'),nullable=False, unique=False)
    kamoku = db.relationship('Kamoku',lazy='joined')
    gakusei = db.relationship('Gakusei',lazy='joined')

    def __init__(self, kamoku_id,gakusei_id):
        #self.id = id
        self.kamoku_id = kamoku_id
        self.gakusei_id = gakusei_id

    def __repr__(self):
        return '<Risyu %r>' % self.id
        #pass

    @staticmethod
    def csv_reg(kamoku):
        filename = "data/risyusya-"+kamoku+".csv"
        data = csvread.csv_reader(filename)
        dbdata = [Risyu(kamoku,s[0]) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True

    
# 科目規則，受付開始時間，遅刻開始時間，終了時間
class KamokuKisoku(db.Model):
    __tablename__ = 'kamokukisoku'

    #id = db.Column(db.Integer,autoincrement=True,nullable=False, unique=True, primary_key=True) # 科目IDを外部キーにもつ
    id = db.Column(db.String(20),db.ForeignKey('kamoku.id'),nullable=False, unique=True, primary_key=True) # 科目IDを外部キーにもつ
    start_syusseki = db.Column(db.Integer,nullable=False, unique=False) # 出席開始時間（相対時間）
    start_tikoku = db.Column(db.Integer,nullable=False, unique=False) # 遅刻開始時間（相対時間）
    end_uketuke = db.Column(db.Integer,nullable=False, unique=False) # 受付終了時間（相対時間）
    #kamoku = db.relationship('Kamoku',uselist=False,backref='kamokukisoku')
    #kamoku = db.relationship('Kamoku')

    def __init__(self, id, start_syusseki, start_tikoku, end_uketuke):
        self.id = id
        self.start_syusseki = start_syusseki
        self.start_tikoku = start_tikoku
        self.end_uketuke = end_uketuke

    def __repr__(self):
        return '<KamokuKisoku %s>' % self.id
        #pass

    @staticmethod
    def csv_reg(filename):
        data = csvread.csv_reader(filename)
        #kamokujoindata = db.session.join(Kamoku,Timedef)
        #dbdata = [KamokuKisoku(s[0],s[6],s[7],db.session.query(Kamoku,Timedef).join(Kamoku,Kamoku.timedef_id==Timedef.id).filter(s[0]==Kamoku.id).first().Timedef.zikan) for s in data]
        dbdata = [KamokuKisoku(s[0],s[7],s[8],90) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True


# 出席データ
class Syusseki(db.Model):
    __tablename__ = 'syusseki'
    __table_args__  =  ( db.UniqueConstraint ( 'risyu_id' , 'kaisu' ),{}) 

    id = db.Column(db.Integer,autoincrement=True,nullable=False, unique=True, primary_key=True) # 
    risyu_id = db.Column(db.Integer,db.ForeignKey('risyu.id'),nullable=False, unique=False) # 
    syukketu = db.Column(db.String(20),nullable=False, unique=False) # 
    kaisu = db.Column(db.Integer,nullable=False, unique=False) # 
    regist_date = db.Column(db.Float,nullable=False, unique=False) # UNIX時間？
    risyu = db.relationship('Risyu',lazy='joined')

    def __init__(self, risyu_id, syukketu, kaisu,regist_date):
        self.risyu_id = risyu_id
        self.syukketu = syukketu
        self.kaisu = kaisu
        self.regist_date = regist_date

    def __repr__(self):
        return '<Syusseki %r>' % self.id
        #pass

    @staticmethod
    def csv_reg(filename,kamoku,kaisu):
        import time
        data = csvread.csv_reader(filename)
        dbdata = list()
        for s in data:
            try:
                risyu = db.session.query(Risyu).filter(s[0]==Risyu.gakusei_id,kamoku == Risyu.kamoku_id).first().id
                dbdata.append(Syusseki(risyu,s[1],kaisu,time.time()))
            except:
                import traceback
                traceback.print_exc()
                db.session.rollback()
        #dbdata = [Syusseki(,s[0]) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True

    @staticmethod
    def csv_reg_nf(json):
        import time
        data = json["csv"].splitlines()
        print(data)
        data = [s.split(',') for s in data]
        print(data)
        dbdata = list()
        for s in data:
            try:
                risyu = db.session.query(Risyu).filter(\
                        s[0]==Risyu.gakusei_id,\
                        json["kamoku"] == Risyu.kamoku_id\
                        ).first().id
                dbdata.append(Syusseki(risyu,s[1],json["kaisu"],time.time()))
            except:
                import traceback
                traceback.print_exc()
                db.session.rollback()
        #dbdata = [Syusseki(,s[0]) for s in data]
        try:
            db.session.add_all(dbdata)
            db.session.commit()
        except:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
        return True


class CRUD:
    @staticmethod
    def add(model):
        try:
            db.session.add(model)
            db.session.commit()
        except:
            return False
        return True

    @staticmethod
    def read(model):
        db.session.query(model)

    @staticmethod
    def update(model):
        db.session.query(model)

    @staticmethod
    def delete(model):
        pass


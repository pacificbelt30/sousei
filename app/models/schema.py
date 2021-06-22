# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, SessionBase
from flask_marshmallow.fields import fields
#from marshmallow_sqlalchemy import fields
from marshmallow import Schema
#from app import env
from app.application import db,ma
from app.models.model import *
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
講義回数データ：kougikaisu
"""


class GakuseiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gakusei
        load_instance = True
        include_fk = True
        include_relationships = True
    name = ma.auto_field()


class KyoinSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Kyoin
        load_instance = True
        include_fk = True
        include_relationships = True


class TimedefSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Timedef
        load_instance = True
        include_fk = True
        include_relationships = True


class KamokuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Kamoku
        load_instance = True
        include_fk = True
        include_relationships = True


class RisyuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Risyu
        load_instance = True
        include_fk = True
        include_relationships = True
    gakusei = fields.Nested(GakuseiSchema)
    #kana = fields.Pluck(GakuseiSchema,'kana')
    #number = fields.Pluck(GakuseiSchema,'number')

    
class KamokuKisokuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KamokuKisoku
        load_instance = True
        include_fk = True
        include_relationships = True


class SyussekiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Syusseki
        load_instance = True
        include_fk = True
        include_relationships = True


class KougiKaisuSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Kougikaisu
        load_instance = True
        include_fk = True
        include_relationships = True




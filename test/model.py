# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask,json
from flask_sqlalchemy import SQLAlchemy, SessionBase
from app.models import csvread
from app.models.model import *
#from app import env
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.application import db

def csv_reg_nf(json_data):
    import time
    #data = json["csv"].splitlines()
    #print(data)
    #data = [s.split(',') for s in data]
    #print(data)
    # data = json.dumps(json_data["data"])
    # print(type(data))
    
    data=list()
    s_data=list()
    for i in range(len(json_data['csv'])):
        data.append(json_data['csv'][i]['number'])
        s_data.append(json_data['csv'][i]['shusseki'])

    dbdata = list()
    for s in range(len(data)):
        try:
            print('data[s]:',data[s])
            #print(type(data[s]))
            # print(json_data["kamoku"])
            risyu = db.session.query(Risyu).filter(\
                    data[s]==Risyu.gakusei_id,\
                    json_data["kamoku"] == Risyu.kamoku_id\
                    ).first().id
            print('risyu:',risyu)
            #dbdata.append(Syusseki(risyu,s_data[s],json_data["kaisu"],time.time()))
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

if __name__=='__main__':
    json_data = {"kaisu":1,"kamoku":"F1","csv":[{"number":"S056","shusseki":"attend"},{"number":"S100","shusseki":"late"}]}
    csv_reg_nf(json_data)


# -*- coding: utf-8 -*-
from app.application import app
from app.models.model import *
from app.routes.route import *
from app.makedb import makedb as mb
def run():
    app.run(host='0.0.0.0')
    #app.run(host='0.0.0.0',threaded=True)

def makedb(flag):
    mb(flag)

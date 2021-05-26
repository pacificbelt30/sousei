from flask import Flask
from flask_sqlalchemy import SQLAlchemy, SessionBase

app = Flask(__name__)
app.config.from_pyfile('instance/config/settings.py')
db = SQLAlchemy(app)



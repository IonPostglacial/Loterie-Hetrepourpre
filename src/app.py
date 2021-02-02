from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_FILE = 'sqlite:///lottery.sq3'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_FILE
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
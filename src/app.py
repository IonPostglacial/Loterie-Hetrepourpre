from flask import Flask
from database import LocalSession
from sqlalchemy.orm import scoped_session


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.session = scoped_session(LocalSession)
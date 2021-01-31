from flask import Flask
from flask import render_template
from markupsafe import escape
from database import create_tables

import sqlite3

DB_FILE = 'lottery.sq3'

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/choice/')
def hello_world():
    return render_template('choice.html', solved_ticket_count=13, unsolved_ticket_count=25)
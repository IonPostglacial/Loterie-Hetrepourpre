from flask import Flask
from flask import render_template
from markupsafe import escape
from database import get_all_categories

import sqlite3

DB_FILE = 'lottery.sq3'

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    cur.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (1, "Hello"))
    cur.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (2, "Goodbye"))
    cur.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (3, "Mymy"))

    categories = [cat for cat in get_all_categories(cur)]

    cur.close()
    con.close()
    return render_template('admin.html', categories=categories)

@app.route('/choice/')
def hello_world():
    return render_template('choice.html', solved_ticket_count=13, unsolved_ticket_count=25)
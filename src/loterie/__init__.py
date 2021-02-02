from flask import Flask, render_template, session, request, redirect, url_for
from markupsafe import escape
from database import create_tables, get_all_categories, get_all_users, create_user, check_credentials

import sqlite3

DB_FILE = 'lottery.sq3'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=["GET", "POST"])
def home_page():
    url_for('static', filename='style.css')
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login_page():
    url_for('static', filename='style.css')
    if request.method == "POST":
        login = request.form['username']
        password = request.form['password']
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        if check_credentials(cur, login, password):
            session['login'] = login
            return redirect(url_for('home_page'))
        else:
            return redirect(url_for('login_page'))
    else:
        return render_template('login.html')

@app.route('/admin', methods=["GET", "POST"])
def admin_page():
    url_for('static', filename='style.css')
    if 'login' in session:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        categories = [cat for cat in get_all_categories(cur)]
        users = [user for user in get_all_users(cur)]

        cur.close()
        con.close()
        return render_template('admin.html', categories=categories, users=users)
    else:
        return redirect(url_for('login'))

@app.route('/choice', methods=["GET", "POST"])
def choice_page():
    url_for('static', filename='style.css')
    if 'login' in session:
        return render_template('choice.html', solved_ticket_count=13, unsolved_ticket_count=25)
    else:
        return redirect(url_for('login'))
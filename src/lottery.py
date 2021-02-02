from flask import render_template, session, request, redirect, url_for
from markupsafe import escape
from app import app
from model import User, Category

import users


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
        if users.check_credentials(login, password):
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
        categories = Category.query.all()
        users = User.query.all()
        return render_template('admin.html', categories=categories, users=users)
    else:
        return redirect(url_for('login_page'))


@app.route('/choice', methods=["GET", "POST"])
def choice_page():
    url_for('static', filename='style.css')
    if 'login' in session:
        return render_template('choice.html', solved_ticket_count=13, unsolved_ticket_count=25)
    else:
        return redirect(url_for('login'))
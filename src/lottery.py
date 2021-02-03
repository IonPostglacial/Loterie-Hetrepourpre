from flask import render_template, session, request, redirect, url_for
from markupsafe import escape
from app import app
from model import User, Category

import users
import database


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
        all_categories = Category.query.all()
        all_users = User.query.all()
        if request.method == "POST":
            if "add-category" in request.form:
                category = Category(name=request.form["category-name"])
                all_categories.append(category)
                database.session.add(category)
            elif "delete-category" in request.form:
                Category.query.filter_by(id=int(request.form["delete-category"])).delete()
            elif "add-user" in request.form:
                user = users.create(
                    request.form["user-login"], 
                    request.form["user-password"], 
                    request.form["user-first-name"],
                    request.form["user-last-name"])
                all_users.append(user)
                database.session.add(user)
            elif "delete-user" in request.form:
                User.query.filter_by(login=request.form["delete-user"]).delete()
            database.session.commit()
        return render_template('admin.html', categories=all_categories, users=all_users)
    else:
        return redirect(url_for('login_page'))


@app.route('/choice', methods=["GET", "POST"])
def choice_page():
    url_for('static', filename='style.css')
    if 'login' in session:
        return render_template('choice.html', solved_ticket_count=13, unsolved_ticket_count=25)
    else:
        return redirect(url_for('login'))
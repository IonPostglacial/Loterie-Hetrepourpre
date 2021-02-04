from flask import render_template, session, request, redirect, url_for
from markupsafe import escape
from app import app
from model import User, Category, Ticket

import users
import database
import functools


def connected_only(f):
    @functools.wraps(f)
    def connected_only_fn(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_page'))
    return connected_only_fn


def admins_only(f):
    @functools.wraps(f)
    @connected_only
    def admins_only_fn(*args, **kwargs):
        current_user = User.query.filter_by(login=session['login']).first()
        is_admin = False
        if current_user is not None:
            is_admin = current_user.is_admin
        if is_admin:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login_page'))
    return admins_only_fn


@app.route('/', methods=["GET", "POST"])
@connected_only
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
@admins_only
def admin_page():
    url_for('static', filename='style.css')
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
                request.form["user-last-name"],
                "user-is-admin" in request.form)
            all_users.append(user)
            database.session.add(user)
        elif "delete-user" in request.form:
            User.query.filter_by(login=request.form["delete-user"]).delete()
        database.session.commit()
    return render_template('admin.html', categories=all_categories, users=all_users)


@app.route('/admin/tickets/new', methods=['GET', 'POST'])
@app.route('/admin/tickets/new/<int:category_id>', methods=['GET', 'POST'])
@admins_only
def create_ticket(category_id: int = None):
    current_user = User.query.filter_by(login=session['login']).first()
    if request.method == 'POST':
        if 'btn-save' in request.form:
            new_ticket = Ticket(
                category_id=request.form['ticket-category'],
                owner_login=request.form['ticket-owner'],
                name=request.form['ticket-name'],
                description=request.form['ticket-description'])
            database.session.add(new_ticket)
            database.session.commit()
            return redirect(url_for('list_tickets'))
    all_categories = Category.query.all()
    all_users = User.query.all()
    if category_id is not None:
        selected_category = Category.query.filter_by(id=category_id).first()
    else:
        selected_category = all_categories[0]
    return render_template('create-ticket.html',
        categories=all_categories,
        users=all_users,
        selected_category=selected_category)


@app.route('/admin/tickets/list', methods=['GET'])
@admins_only
def list_tickets():
    all_categories = Category.query.all()
    return render_template('tickets.html', categories=all_categories)


@app.route('/choice', methods=["GET", "POST"])
@connected_only
def choice_page():
    url_for('static', filename='style.css')
    return render_template('choice.html', solved_ticket_count=13, unsolved_ticket_count=25)
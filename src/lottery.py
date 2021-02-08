from flask import render_template, session, request, redirect, url_for
from markupsafe import escape
from app import app
from model import User, Category, Ticket
from sqlalchemy import and_

import database
import functools
import html
import random
import users


def connected_only(f):
    @functools.wraps(f)
    def connected_only_fn(*args, **kwargs):
        if 'login' in session:
            url_for('static', filename='style.css')
            url_for('static', filename='machine-lotterie.png')
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
    is_ticket_available = True
    if request.method == "POST":
        if 'pick-ticket' in request.form:
            available_tickets = Ticket.query.filter(and_(Ticket.owner_login == "", Ticket.category_id == int(request.form['ticket-category']))).all()
            if len(available_tickets) > 0:
                picked_ticket_index = random.randint(0, len(available_tickets) - 1)
                picked_ticket = available_tickets[picked_ticket_index]
            else:
                is_ticket_available = False
                picked_ticket = None
        elif 'accept-ticket' in request.form:  
            picked_ticket = database.session.query(Ticket).get(int(request.form['accept-ticket']))
            picked_ticket.owner = database.session.query(User).get(session['login'])
            database.session.commit()
            return redirect(url_for('home_page'))
        elif 'unpick-ticket' in request.form:
            picked_ticket = database.session.query(Ticket).get(int(request.form['unpick-ticket']))
            picked_ticket.owner = None
            database.session.commit()
            return redirect(url_for('home_page'))
        elif 'resolve-ticket' in request.form:
            picked_ticket = database.session.query(Ticket).get(int(request.form['resolve-ticket']))
            picked_ticket.is_treated = True
            database.session.commit()
            return redirect(url_for('home_page'))
        else:
            picked_ticket = None
    else:
        picked_ticket = None
    current_user = User.query.filter_by(login=session['login']).first()
    owned_ticket = Ticket.query.filter(and_(Ticket.is_treated == False, Ticket.owner == current_user)).first()
    if owned_ticket is None:
        solved_count = database.session.query(Ticket.id).filter_by(is_treated=True).count()
        ticket_count = database.session.query(Ticket.id).count()
        all_categories = Category.query.all()
        return render_template('choice.html',
            solved_ticket_count=solved_count,
            unsolved_ticket_count=ticket_count,
            picked_ticket=picked_ticket,
            categories=all_categories,
            is_ticket_available=is_ticket_available,
            is_admin=current_user.is_admin)
    else:
        return render_template('index.html', user=current_user, ticket=owned_ticket, is_admin=current_user.is_admin)


@app.route('/disconnect')
def disconnect_page():
    del session['login']
    return redirect(url_for('login_page'))


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
    return render_template('admin.html', categories=all_categories, users=all_users, is_admin=True)


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
                description=html.escape(request.form['ticket-description']),
                is_treated=False)
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
        selected_category=selected_category,
        is_admin=True)


@app.route('/admin/tickets/list', methods=['GET', 'POST'])
@admins_only
def list_tickets():
    if request.method == "POST":
        if "delete-ticket" in request.form:
            Ticket.query.filter_by(id=int(request.form["delete-ticket"])).delete()
            database.session.commit()
    all_categories = Category.query.all()
    return render_template('tickets.html', categories=all_categories, is_admin=True)

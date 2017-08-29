from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm
from .models import User


@app.before_request
def before_request():
    g.user = current_user


#after user logs in
@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User(lincoln_id=request.form['lincoln_id'], lincoln_email=request.form['lincoln_email'].lower(),
                    password=request.form['password'])

        #if user clicks register
        if request.form['btn'] == 'register':
            if User.query.filter_by(lincoln_email=user.lincoln_email).first():
                flash('This email address has already been registered')
            else:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))

        #if user clicks log in
        elif request.form['btn'] == 'login':
            user = User.query.filter_by(lincoln_email=request.form['lincoln_email'].lower()).first()
            if request.form['lincoln_email'].lower() == user.lincoln_email and request.form['password'] == user.password:
                return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


#load user from database
@lm.user_loader
def load_user(lincoln_id):
    return User.query.get(lincoln_id)


def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
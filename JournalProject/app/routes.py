from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import SignUpForm, LoginForm
from app.models import User, Journal
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/") 
def home():
    return render_template("home.html")

@app.route("/mainpage") 
def mainpage():
    return render_template("mainpage.html")

@app.route("/calendar") 
def calendar():
    return render_template("calendar.html")

@app.route("/journal") 
def journal():
    return render_template("journal.html")

@app.route("/habittracker") 
def habittracker():
    return render_template("habittracker.html")

@app.route("/moodtracker") 
def moodtracker():
    return render_template("moodtracker.html")

@app.route("/info") 
def info():
    return render_template("info.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('mainpage'))
        else:
            flash('Login Unsuccessful. Please check password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('mainpage.html', title='Account')
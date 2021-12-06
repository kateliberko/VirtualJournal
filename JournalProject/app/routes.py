from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import SignUpForm, LoginForm
from app.models import User, Journal, Event, Habit
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from app.counter import Counter

@app.route("/") 
def home():
  
    return render_template("home.html")

@app.route("/mainpage") 
def mainpage():
    todays_date= datetime.now().date()
    event= Event.query.filter_by(user_id=current_user.id)
    habits = current_user.habits
    habitlist = habits.split(",")
    count= Counter
    return render_template("mainpage.html", todays_date=todays_date, event=event, habits=habitlist, count=count)

@app.route("/calendar") 
def calendar():
    return render_template("index.html")

@app.route("/journal") 
def journal():
    alljournals = Journal.query.filter_by(user_id=current_user.id) # only display logged in users info
    return render_template("journal.html", alljournals=alljournals)

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
        user = User(username=form.username.data, password=hashed_password, habits= request.form.get("habitlist"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('mainpage'))
        else:
            flash('Login Unsuccessful. Please check username and password') 
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
def account():
    return render_template('mainpage.html')


@app.route("/journal/new", methods=['GET', 'POST'])
@login_required
def new_journal():
    journal = request.form.get("journal")
    if journal: # ensures no empty journal entries
        journalLog = Journal(content=journal, user_id=current_user.id)
        db.session.add(journalLog)
        db.session.commit()
        return redirect(url_for('mainpage'))
    return render_template('mainpage.html')

@app.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    event = request.form.get("name")
    date = request.form.get("date")
    starttime = request.form.get("starttime")
    endtime = request.form.get("endtime")
    category = request.form.get("category")
    type = request.form.get("type")
    location = request.form.get("location")
    if event: # ensures no empty events
        newEvent = Event(event_name=event, date=date, start_time=starttime, end_time=endtime, category=category, event_type=type, location=location, user_id=current_user.id)
        db.session.add(newEvent)
        db.session.commit()
        return redirect(url_for('mainpage'))
    return render_template('mainpage.html')
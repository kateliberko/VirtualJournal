from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import SignUpForm, LoginForm
from app.models import User, Journal, Event, Habit, Todo, Moods
from datetime import date, timedelta
from flask_login import login_user, current_user, logout_user, login_required
from app.counter import Counter

@app.route("/") 
def home():

    return render_template("home.html")

@app.route("/mainpage") 
@login_required
def mainpage():
    todays_date= date.today()
    habits = current_user.habits
    habitlist = habits.split(",")
    count= Counter
    todolist= Todo.query.all()
    journalcheck= Journal.query.filter_by(user_id=current_user.id, date_posted=todays_date).first() # will only ever be one journal
    moods = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    return render_template("mainpage.html", todays_date=todays_date, habits=habitlist, count=count, journal=journalcheck, todolist=todolist, moods=moods)

@app.route("/calendar") 
@login_required
def calendar():
    return render_template("index.html")

@app.route("/journal") 
@login_required
def journal():
    alljournals = Journal.query.filter_by(user_id=current_user.id) # only display logged in users info
    return render_template("journal.html", alljournals=alljournals)

@app.route("/habittracker") 
@login_required
def habittracker():
    habits = current_user.habits
    habitlist = habits.split(",")
    count= Counter
    todays_date= date.today()
    lastweek= todays_date - timedelta(days=7)
    return render_template("habittracker.html", habits=habitlist, count=count, todays_date=todays_date, lastweek=lastweek)

@app.route("/moodtracker") 
@login_required
def moodtracker():
    moods = Moods.query.filter_by(user_id=current_user.id)
    todays_date= date.today()
    lastweek= todays_date - timedelta(days=7)
    return render_template("moodtracker.html", moods = moods, todays_date= todays_date, lastweek=lastweek)

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
        user = User(username=form.username.data, password=hashed_password, habits= form.habits.data)
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
@login_required
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

@app.route("/journal/<int:journal_id>")
@login_required
def viewjournal(journal_id):
    journal = Journal.query.get_or_404(journal_id)
    return render_template('single_journal.html',  journal=journal )


@app.route("/journal/<int:journal_id>/update", methods=['GET', 'POST'])
@login_required
def update_journal(journal_id):
    journal = Journal.query.get_or_404(journal_id)
    if journal.user_id != current_user.id: # make sure no other users can 'somehow' update other's journals
        abort(403)
    journalcontent= request.form.get("journal")
    if journalcontent:
        journal.content = journalcontent
        db.session.commit()
        flash('Your journal has been updated!', 'success')
        if request.form.get("flag") == 'fromjournal':
            return render_template('single_journal.html',  journal=journal )
        else:
            redirect(url_for('mainpage'))
   
    return redirect(url_for('mainpage'))

@app.route("/add_todo", methods=['GET', 'POST'])
@login_required
def add_todo():
    todo = request.form.get("todo")
    if todo: # ensures no empty todo entries
        todoEntry = Todo(task=todo, user_id=current_user.id)
        db.session.add(todoEntry)
        db.session.commit()
        return redirect(url_for('mainpage'))
    return render_template('mainpage.html')

@app.route("/add_moods", methods=['GET', 'POST'])
@login_required
def add_moods():
    todays_date = date.today()
    
    checkedmoods = request.form.getlist('mood')
    checkedmoods = ' '.join([str(elem) for elem in checkedmoods])
    print(checkedmoods)
    mooditem = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    if checkedmoods:
        if mooditem:
            mooditem.moodlist = checkedmoods
            db.session.commit()
            return redirect(url_for('mainpage'))    
        else:
            mooditem = Moods(moodlist=checkedmoods, user_id=current_user.id)    
            db.session.add(mooditem)
            db.session.commit()
        return redirect(url_for('mainpage'))
    return redirect(url_for('mainpage'))
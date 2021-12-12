from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import SignUpForm, LoginForm
from app.models import User, Journal, Event, Habit, Todo, Moods
from datetime import date, time, timedelta
from flask_login import login_user, current_user, logout_user, login_required
from app.counter import Counter
import math

@app.route("/") 
def home():
    return render_template("home.html")

@app.route("/mainpage", methods=['GET', 'POST']) 
@login_required
def mainpage():
    todays_date= date.today()
    count= Counter
    todolist= Todo.query.filter_by(user_id=current_user.id)
    journal= Journal.query.filter_by(user_id=current_user.id, date_posted=todays_date).first() # will only ever be one journal
    moods = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    habit = Habit.query.filter_by(user_id = current_user.id).first()
    
    if habit is not None: 
        
        habits = Habit.query.filter_by(user_id = current_user.id)
        return render_template("mainpage.html", todays_date=todays_date, habits=habits, count=count, journal=journal, todolist=todolist, moods=moods)
     
    if habit is None: # if habits don't exist(first time login) we must create them
        habitform = request.form.getlist("myhabit")
    
        if len(habitform)!=0:
            for habit in habitform:
                habitLog = Habit(habit_name= habit, user_id=current_user.id)
                db.session.add(habitLog)
                db.session.commit()
            
            habitlist = Habit.query.filter_by(user_id = current_user.id)
            return render_template("mainpage.html", todays_date=todays_date, habits=habitlist, count=count, journal=journal, todolist=todolist, moods=moods)
   
        return render_template("habitcreate.html")
    return render_template("mainpage.html", todays_date=todays_date, habits=habit, count=count, journal=journal, todolist=todolist, moods=moods)

 
    

@app.route("/calendar") 
@login_required
def calendar():
    return render_template("calendar.html")
@app.route("/journal") 
@login_required
def journal():
    count= Counter
    alljournals = Journal.query.filter_by(user_id=current_user.id) # only display logged in users info
    return render_template("journal.html", alljournals=alljournals, count=count)

@app.route("/habittracker") 
@login_required
def habittracker():
    # habits = current_user.habits
    # habitlist = habits.split(",")
    count= Counter
    todays_date= date.today()
    lastweek= todays_date - timedelta(days=7)
    return render_template("habittracker.html", count=count, todays_date=todays_date, lastweek=lastweek)

@app.route("/moodtracker") 
@login_required
def moodtracker():
    todays_date= date.today()
    lastweek = todays_date - timedelta(days=7)
    mood1 = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    mood2 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1)).first()
    mood3 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2)).first()
    mood4 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3)).first()
    mood5 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4)).first()
    mood6 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=5)).first()
    mood7 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=6)).first()
    return render_template("moodtracker.html", mood1=mood1, todays_date=todays_date, lastweek=lastweek, mood2=mood2, mood3=mood3, mood4=mood4, mood5=mood5, mood6=mood6, mood7=mood7)

@app.route("/info") 
def info():
    return render_template("info.html")

@app.route("/test") 
def test():
    return render_template("turn_test.html")

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


@app.route("/habitcreate")
@login_required
def account():
    return render_template('habitcreate.html')

@app.route("/habit/update", methods=['GET', 'POST'])
@login_required
def updatehabit():
    habits = Habit.query.filter_by(user_id = current_user.id)
    habit0 = request.form.get("habit0")
    habit1 = request.form.get("habit1")
    print(habit0 + "this is both" + habit1)
    if habit0 == 'True':
        habits[0].habit_done = True
    if habit0 == 'False':
        habits[0].habit_done = False
    if habit1 == 'True':
        habits[1].habit_done = True
    if habit1 == 'False':
        habits[1].habit_done = False
    db.session.commit()
 
    return redirect(url_for('mainpage'))

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

    

@app.route("/nextmoodtracker", methods=['GET', 'POST'])
@login_required
def nextmoodtracker(): 
    spot = request.form.get("daytag")
    todays_date = date.fromisoformat(spot) + timedelta(days=7)
    lastweek = todays_date - timedelta(days=7)
    mood1 = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    mood2 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1)).first()
    mood3 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2)).first()
    mood4 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3)).first()
    mood5 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4)).first()
    mood6 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=5)).first()
    mood7 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=6)).first()
    return render_template("moodtracker.html", mood1=mood1, todays_date= todays_date, lastweek=lastweek, mood2=mood2, mood3=mood3, mood4=mood4, mood5=mood5, mood6=mood6, mood7=mood7)
    
@app.route("/prevmoodtracker", methods=['GET', 'POST'])
@login_required
def prevmoodtracker():
    spot = request.form.get("daytag")
    todays_date = date.fromisoformat(spot) - timedelta(days=7)
    lastweek = todays_date - timedelta(days=7)
    mood1 = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    mood2 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1)).first()
    mood3 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2)).first()
    mood4 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3)).first()
    mood5 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4)).first()
    mood6 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=5)).first()
    mood7 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=6)).first()
    return render_template("moodtracker.html", mood1=mood1, todays_date= todays_date, lastweek=lastweek, mood2=mood2, mood3=mood3, mood4=mood4, mood5=mood5, mood6=mood6, mood7=mood7)
    

@app.route("/newEvent", methods=['GET', 'POST'])
@login_required
def new_event():
    event = request.form.get("eventTitleInput")
    date = request.form.get("date")
    if event: # ensures no empty events
        newEvent = Event(event_name=event, date=date, user_id=current_user.id)
        db.session.add(newEvent)
        db.session.commit()
        return redirect(url_for('calendar'))
    return render_template('calendar.html')
    
app.route("/deleteEvent/<int:event_id>", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('calendar'))
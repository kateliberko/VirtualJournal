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
    habit = Habit.query.filter_by(user_id = current_user.id, date = todays_date).first()
    
    if habit is not None: # habits exist for this user today
        habits = Habit.query.filter_by(user_id = current_user.id, date = todays_date)
        return render_template("mainpage.html", todays_date=todays_date, habits=habits, count=count, journal=journal, todolist=todolist, moods=moods)
     
    if habit is None: # if habits don't exist for this user today
        newcheck = Habit.query.filter_by(user_id = current_user.id).first()
        if newcheck is not None: # user has previous habits
            # must make new habits with existing habit names but with todays date
            mostrecenthabits = Habit.query.filter_by(user_id = current_user.id).order_by(Habit.id.desc()).first() #finds most recent creation date
            habits = Habit.query.filter_by(user_id = current_user.id, date = mostrecenthabits.date) #grabs habits from most recent creation date
            for habit in habits: # creates new habits with same name, but new date
                    habitLog = Habit(habit_name= habit.habit_name, user_id=current_user.id)
                    db.session.add(habitLog)
                    db.session.commit()
            habitlist = Habit.query.filter_by(user_id = current_user.id, date=todays_date)
        else: # first time user, must create new habits from habit form
            habitform = request.form.getlist("myhabit")
        
            if len(habitform)!=0: # check that user has filled out form
                for habit in habitform:
                    habitLog = Habit(habit_name= habit, user_id=current_user.id)
                    db.session.add(habitLog)
                    db.session.commit()
                
                habitlist = Habit.query.filter_by(user_id = current_user.id, date=todays_date)
                return render_template("mainpage.html", todays_date=todays_date, habits=habitlist, count=count, journal=journal, todolist=todolist, moods=moods)
    
    return render_template("habitcreate.html")



# SIGNUP
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated: # will automatically login you in if you didn't log out last time
        return redirect(url_for('mainpage'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


# LOGIN
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # will automatically login you in if you didn't log out last time
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


# LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


    
# CALENDAR
@app.route("/calendar") 
@login_required
def calendar():
    return render_template("calendar.html")



# JOURNAL
@app.route("/journal") # display all current users' journals
@login_required
def journal():
    count= Counter
    alljournals = Journal.query.filter_by(user_id=current_user.id) 
    return render_template("journal.html", alljournals=alljournals, count=count)

@app.route("/journal/<int:journal_id>") # view a single journal with the given id
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
        journal.content = journalcontent # updates journal content to newly submitted content
        db.session.commit()
        if request.form.get("flag") == 'fromjournal': # checks to see which page the journal was submitted on, so it can return to proper page
            return render_template('single_journal.html',  journal=journal )
        else:
            redirect(url_for('mainpage'))
   
    return redirect(url_for('mainpage'))

@app.route("/journal/new", methods=['GET', 'POST'])
@login_required
def new_journal():
    journal = request.form.get("journal")
    if journal: # ensures no empty journal entries
        journalLog = Journal(content=journal, user_id=current_user.id) # create new journal entry for todays date containing inputed content
        db.session.add(journalLog)
        db.session.commit()
        return redirect(url_for('mainpage'))
    return render_template('mainpage.html')



# HABIT
@app.route("/habittracker") 
@login_required
def habittracker():
    todays_date= date.today()
    lastweek= todays_date - timedelta(days=7)
    habit0 = Habit.query.filter_by(user_id=current_user.id, date=todays_date)
    if habit0.first() is None:
        habit0= 'Null'
    habit1 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1))
    if habit1.first() is None:
        habit1= 'Null'
    habit2 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2))
    if habit2.first() is None:
        habit2= 'Null'
    habit3 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3))
    if habit3.first() is None:
        habit3= 'Null'
    habit4 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4))
    if habit4.first() is None:
        habit4= 'Null'
   
    return render_template("habittracker.html", todays_date=todays_date, lastweek=lastweek, habit1=habit1, habit2=habit2, habit3=habit3, habit4=habit4, habit0=habit0)

@app.route("/habitdone/update", methods=['GET', 'POST'])
@login_required
def updatehabitdone():
    todays_date= date.today()
    habits = Habit.query.filter_by(user_id = current_user.id, date=todays_date)
    habit0 = request.form.get("habit0")
    habit1 = request.form.get("habit1")
    habit2 = request.form.get("habit2")
    habit3 = request.form.get("habit3")
    habit4 = request.form.get("habit4")
    if habit0 == 'True':    # makes sure to update habits according to what was selected
        habits[0].habit_done = True
    if habit0 == 'False':
        habits[0].habit_done = False
    if habit1 == 'True':
        habits[1].habit_done = True
    if habit1 == 'False':
        habits[1].habit_done = False
    if habit2 == 'True':
        habits[2].habit_done = True
    if habit2 == 'False':
        habits[2].habit_done = False
    if habit3 == 'True':
        habits[3].habit_done = True
    if habit3 == 'False':
        habits[3].habit_done = False
    if habit3 == 'True':
        habits[4].habit_done = True
    if habit4 == 'False':
        habits[4].habit_done = False
    db.session.commit()
    return redirect(url_for('mainpage'))

@app.route("/prevhabittracker", methods=['GET', 'POST'])
@login_required
def prevhabittracker():
    spot = request.form.get("daytag")
    todays_date = date.fromisoformat(spot) - timedelta(days=7) # moving backward one week
    lastweek = todays_date - timedelta(days=7)
    habit0 = Habit.query.filter_by(user_id=current_user.id, date=todays_date)
    if habit0.first() is None:
        habit0= 'Null'
    habit1 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1))
    if habit1.first() is None:
        habit1= 'Null'
    habit2 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2))
    if habit2.first() is None:
        habit2= 'Null'
    habit3 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3))
    if habit3.first() is None:
        habit3= 'Null'
    habit4 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4))
    if habit4.first() is None:
        habit4= 'Null'
    
    return render_template("habittracker.html", todays_date=todays_date, lastweek=lastweek, habit1=habit1, habit2=habit2, habit3=habit3, habit4=habit4, habit0=habit0)

@app.route("/nexthabittracker", methods=['GET', 'POST'])
@login_required
def nexthabittracker():
    spot = request.form.get("daytag")
    todays_date = date.fromisoformat(spot) + timedelta(days=7) # moving backward one week
    lastweek = todays_date - timedelta(days=7)
    habit0 = Habit.query.filter_by(user_id=current_user.id, date=todays_date)
    if habit0.first() is None:
        habit0= 'Null'
    habit1 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1))
    if habit1.first() is None:
        habit1= 'Null'
    habit2 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2))
    if habit2.first() is None:
        habit2= 'Null'
    habit3 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3))
    if habit3.first() is None:
        habit3= 'Null'
    habit4 = Habit.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4))
    if habit4.first() is None:
        habit4= 'Null'

    return render_template("habittracker.html", todays_date=todays_date, lastweek=lastweek, habit1=habit1, habit2=habit2, habit3=habit3, habit4=habit4, habit0=habit0)

@app.route("/habit_update", methods=['GET', 'POST'])
@login_required
def updatehabit():
    todays_date= date.today()
    habits = Habit.query.filter_by(user_id = current_user.id, date=todays_date)
    habitform = request.form.getlist("myhabit")
        
    if len(habitform)!=0: # check that user has filled out form
        for each in habits: # delete all old habits
            db.session.delete(each)
            db.session.commit()
        for habit in habitform: # create all new habits
            habitLog = Habit(habit_name= habit, user_id=current_user.id)
            db.session.add(habitLog)
            db.session.commit()
        return redirect(url_for('habittracker'))
    
    return render_template("habitedit.html", habits=habits)
    



# MOOD
@app.route("/moodtracker") 
@login_required
def moodtracker():
    todays_date= date.today()
    todaysactualdate= date.today()
    lastweek = todays_date - timedelta(days=7)
    mood1 = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first() # grabbing moodlist for each day in the week
    mood2 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1)).first()
    mood3 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2)).first()
    mood4 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3)).first()
    mood5 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4)).first()
    mood6 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=5)).first()
    mood7 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=6)).first()
    return render_template("moodtracker.html",todaysactualdate=todaysactualdate, mood1=mood1, todays_date=todays_date, lastweek=lastweek, mood2=mood2, mood3=mood3, mood4=mood4, mood5=mood5, mood6=mood6, mood7=mood7)

@app.route("/add_moods", methods=['GET', 'POST'])
@login_required
def add_moods():
    todays_date = date.today()
    checkedmoods = request.form.getlist('mood')
    checkedmoods = ' '.join([str(elem) for elem in checkedmoods]) # makes the seperate emojis one mood list
    mooditem = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first()
    if checkedmoods: # ensures moods were entered
        if mooditem: # if a moodlist exists for this date, update it
            mooditem.moodlist = mooditem.moodlist + checkedmoods # keeps running list of selected moods (does not accoutn for duplicates)
            db.session.commit()
            return redirect(url_for('mainpage'))    
        else: # moodlist does not exist for this date, create one
            mooditem = Moods(moodlist=checkedmoods, user_id=current_user.id)    
            db.session.add(mooditem)
            db.session.commit()
        return redirect(url_for('mainpage'))
    return redirect(url_for('mainpage'))

@app.route("/prevmoodtracker", methods=['GET', 'POST'])
@login_required
def prevmoodtracker():
    todaysactualdate= date.today()
    spot = request.form.get("daytag")
    todays_date = date.fromisoformat(spot) - timedelta(days=7) # moving backward one week
    lastweek = todays_date - timedelta(days=7)
    mood1 = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first() # grabbing moods from different days
    mood2 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1)).first()
    mood3 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2)).first()
    mood4 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3)).first()
    mood5 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4)).first()
    mood6 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=5)).first()
    mood7 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=6)).first()
    return render_template("moodtracker.html", todaysactualdate=todaysactualdate, mood1=mood1, todays_date= todays_date, lastweek=lastweek, mood2=mood2, mood3=mood3, mood4=mood4, mood5=mood5, mood6=mood6, mood7=mood7)

@app.route("/nextmoodtracker", methods=['GET', 'POST'])
@login_required
def nextmoodtracker(): 
    todaysactualdate= date.today()
    spot = request.form.get("daytag")
    todays_date = date.fromisoformat(spot) + timedelta(days=7) # moving forward one week
    lastweek = todays_date - timedelta(days=7)
    mood1 = Moods.query.filter_by(user_id=current_user.id, date=todays_date).first() # grabbing moods from different days
    mood2 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=1)).first()
    mood3 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=2)).first()
    mood4 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=3)).first()
    mood5 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=4)).first()
    mood6 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=5)).first()
    mood7 = Moods.query.filter_by(user_id=current_user.id, date=todays_date-timedelta(days=6)).first()
    return render_template("moodtracker.html", todaysactualdate=todaysactualdate, mood1=mood1, todays_date= todays_date, lastweek=lastweek, mood2=mood2, mood3=mood3, mood4=mood4, mood5=mood5, mood6=mood6, mood7=mood7)
    
    
# INFO
@app.route("/info") 
def info():
    return render_template("info.html")


@app.route("/test") 
def test():
    return render_template("turn_test.html")



# todo LIST
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

@app.route("/delete_todo/<int:todo_id>", methods=['GET', 'POST'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != current_user.id:
            abort(403)
    if request.form.get('delete'):
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('mainpage'))
    if request.form.get(str(todo_id)):
        todo.checked = True
        db.session.commit()
        return redirect(url_for('mainpage'))
    if todo.checked==True:
            todo.checked = False
            db.session.commit()
    return redirect(url_for('mainpage'))


from flask import Flask, render_template, url_for, flash, redirect
from forms import SignUpForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY']='9f7615199c57c5ce0b76e926041133b3'

@app.route("/") 
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
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('mainpage'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('mainpage'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

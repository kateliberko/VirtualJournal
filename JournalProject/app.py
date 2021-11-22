
from flask import Flask, render_template

app = Flask(__name__)

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
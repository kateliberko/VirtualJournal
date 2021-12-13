from datetime import date, datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.Date, nullable=False, default= date.today())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Journal('{self.date_posted}', '{self.content}')"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.Date, nullable=False, default=date.today())
    task = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    checked = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Todo('{self.date_posted}', '{self.task}')"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), unique=False, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    def __repr__(self):
        return f"Event('{self.id}'')"

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_name = db.Column(db.String(50), unique=False, nullable=False)
    habit_done = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today())

    def __repr__(self):
        return f"Habit('{self.id}'')"

class Moods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date= db.Column(db.Date, nullable=False, default= date.today())
    moodlist = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Moods('{self.id}')"
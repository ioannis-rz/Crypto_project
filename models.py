from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

PEPPER = os.environ["PASSWORD_PEPPER"]

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    progress = db.relationship('Progress', backref='user', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('UserStats', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password + PEPPER, salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + PEPPER)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20), nullable=False)  
    subject = db.Column(db.String(20), nullable=False)  
    percentage = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'level', 'subject', name='_user_level_subject_uc'),
    )

class UserStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_time = db.Column(db.Integer, default=0)  
    exercises_completed = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)  
    last_activity_date = db.Column(db.Date, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
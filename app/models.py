from .database import db
import sqlalchemy as sa

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(10), nullable=False)
    role = db.Column(sa.Enum('student', 'faculty', 'admin', 'alumni', 'tpc', 'eventorgs', name='user_roles'), nullable=False)


class Alumni(db.Model):
    __tablename__ = 'alumni'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    passout_year=db.Column(db.Integer,nullable=False)
    occupation=db.Column(db.String(50),nullable=False)
    registration_no=db.Column(db.String(50),nullable=False)

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    batch=db.Column(db.String(50),nullable=False)
    passout_year=db.Column(db.Integer,nullable=False)
    registration_no=db.Column(db.String(50),nullable=False)

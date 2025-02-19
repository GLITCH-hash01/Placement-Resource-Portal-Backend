from .database import db
import sqlalchemy as sa,sqlalchemy

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
    stack=db.Column(db.String(50),nullable=False)
    registration_no=db.Column(db.String(50),nullable=False)


class Notes(db.Model):
    __tablename__ = 'notes'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    desc=db.Column(db.String(255),nullable=True)
    title=db.Column(db.String(50),nullable=False)
    submitted_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    submitted_on=db.Column(db.DateTime,nullable=False)
    doc_url=db.Column(db.String(255),nullable=False) 
    likes=db.Column(db.Integer,nullable=False)
    category=db.Column(sa.Enum('academics','placement',name='note_categories'),nullable=False)

class AcademicNotes(db.Model):
    __tablename__='academic_notes'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    note_id=db.Column(db.Integer,db.ForeignKey('notes.id'),nullable=False)
    semester=db.Column(db.Integer,nullable=False)
    course_code=db.Column(db.String(50),nullable=False)
    module=db.Column(db.Integer,nullable=False)
    scheme=db.Column(db.Integer,nullable=False)
    year=db.Column(db.Integer,nullable=False)

    db.relationship('Notes',backref='academic_notes')


class Events(db.Model):
    __tablename__ = 'events'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    desc=db.Column(db.String(255),nullable=True)
    title=db.Column(db.String(50),nullable=False)
    submitted_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    submitted_on=db.Column(db.DateTime,nullable=False)
    poster_url=db.Column(db.String(255),nullable=False) 

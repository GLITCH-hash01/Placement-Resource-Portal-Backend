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

    db.relationship('Student',backref='users',uselist=False)

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


class Roadmaps(db.Model):
    __tablename__ = 'roadmaps'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    department=db.Column(db.String(50),nullable=False)
    year=db.Column(db.Integer,nullable=False)
    course=db.Column(db.String(255),nullable=True)

class RoadmapCourses(db.Model):
    __tablename__ = 'roadmap_courses'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    roadmap_id=db.Column(db.Integer,db.ForeignKey('roadmaps.id'),nullable=False)
    course_title=db.Column(db.String(150),nullable=False)
    course_resourses=db.Column(db.String(255),nullable=False)

class Queries(db.Model):
    __tablename__ = 'queries'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    query_title=db.Column(db.String(255),nullable=False)
    query_desc=db.Column(db.String(255),nullable=False)
    submitted_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    submitted_on=db.Column(db.DateTime,nullable=False)
    stack=db.Column(db.String(50),nullable=True)

    responses=db.relationship('Responses',backref='queries',cascade='all,delete-orphan')
    queries_likes=db.relationship('QueriesLikes',backref='queries',cascade='all,delete-orphan')

class Responses(db.Model):
    __tablename__ = 'responses'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    query_id=db.Column(db.Integer,db.ForeignKey('queries.id'),nullable=False)
    response=db.Column(db.String(255),nullable=False)
    responded_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    responded_on=db.Column(db.DateTime,nullable=False)

    db.relationship('QueriesLikes',backref='responses',cascade='all,delete-orphan')


class QueriesLikes(db.Model):
    __tablename__ = 'queries_likes'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    query_id=db.Column(db.Integer,db.ForeignKey('queries.id'),nullable=False)
    liked_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    response_id=db.Column(db.Integer,db.ForeignKey('responses.id'),nullable=True)

    db.relationship('Queries',backref='queries_likes')
    db.relationship('Responses',backref='queries_likes')

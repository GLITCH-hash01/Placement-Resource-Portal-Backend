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

class Notes(db.Model):
    __tablename__ = 'notes'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(50),nullable=False)
    submitted_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    submitted_on=db.Column(db.DateTime,nullable=False)
    doc_url=db.Column(db.String(255),nullable=False) 

    category=db.Column(sa.Enum('academics','placement',name='note_categories'),nullable=False)

class AcademicNotes(db.Model):
    __tablename__='academic_notes'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    note_id=db.Column(db.Integer,db.ForeignKey('notes.id',ondelete="CASCADE"),nullable=False)
    semester=db.Column(db.Integer,nullable=False)
    course_code=db.Column(db.String(50),nullable=False)
    module=db.Column(db.Integer,nullable=False)
    scheme=db.Column(db.Integer,nullable=False,default=2019)
    department=db.Column(db.String(50),nullable=True)
    year=db.Column(db.Integer,nullable=False)

    db.relationship('Notes',backref='academic_notes')


class Events(db.Model):
    __tablename__ = 'events'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(50),nullable=False)
    submitted_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    category=db.Column(sa.Enum('event','internship',name='event_categories'),nullable=False,default='event')
    submitted_on=db.Column(db.DateTime,nullable=False)
    poster_url=db.Column(db.String(255),nullable=False) 
    know_more=db.Column(db.String(255),nullable=True,default='https://www.google.com')


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
    

    responses=db.relationship('Responses',backref='queries',cascade='all,delete-orphan')
    

class Responses(db.Model):
    __tablename__ = 'responses'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    query_id=db.Column(db.Integer,db.ForeignKey('queries.id'),nullable=False)
    response=db.Column(db.String(255),nullable=False)
    responded_by=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    responded_on=db.Column(db.DateTime,nullable=False)

    db.relationship('QueriesLikes',backref='responses',cascade='all,delete-orphan')

class CourseList(db.Model):
    __tablename__ = 'course_list'   
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    department=db.Column(db.String(50),nullable=False)
    course_code=db.Column(db.String(50),nullable=False)
    course_title=db.Column(db.String(150),nullable=False)
    semester=db.Column(db.Integer,nullable=False)
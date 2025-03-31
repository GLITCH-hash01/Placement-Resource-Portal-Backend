from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token,jwt_required
from app.models import Users
from werkzeug.security import generate_password_hash,check_password_hash
from app.database import db
from flask_cors import cross_origin

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['POST'])
@cross_origin()
def login():
  request_data=request.get_json()
  email=request_data['email']
  password=request_data['password']

  user=Users.query.filter_by(email=email).first()

  if user is None:
    return jsonify({'message':'User doesn\'t exist'}),401
  
  if check_password_hash(user.password_hash,password):
    access_token=create_access_token(identity=str(user.id))
    response={
    'message':'User logged in successfully',
    'access_token':access_token,
    'data':{
      'username':user.username,
      'email':user.email,
      'department':user.department,
      'role':user.role
    }
    }
    return jsonify(response),200
  else:
    return jsonify({'message':'Invalid username or password'}),401

@auth.route('/signup',methods=['POST'])
def signup():
  request_data=request.get_json()
  username=request_data['username']
  password=request_data['password']
  email=request_data['email']
  department=request_data['department']
  role=request_data['role']

  if role not in ['student', 'faculty', 'admin', 'alumni', 'tpc', 'eventorgs']:
    return jsonify({'message':'Invalid role'}),400
  
  if Users.query.filter_by(email=email).first() is not None:
    return jsonify({'message':'User already exists'}),400

  password_hash=generate_password_hash(password)
  


  user=Users(username=username,password_hash=password_hash,email=email,department=department,role=role)
  
  try:
    db.session.add(user)
  except:
    return jsonify({'message':'user already exists'}),400
  db.session.commit()

  access_token=create_access_token(identity=str(user.id))
  reponse={
    'message':'User created successfully',
    'data':{
      'access_token':access_token,
      'user':{
      'id':user.id,
      'username':username,
      'email':email,
      'department':department,
      'role':role
      }
    }
  }

  return jsonify(reponse),200
from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Events
import cloudinary.uploader as uploader
from datetime import datetime
from app.database import db

events_bp=Blueprint('events',__name__)

@events_bp.route('/upload',methods=['POST'])
@jwt_required()
def upload_events():

  request_data=request.form.to_dict()

  if 'poster' not in request.files:
    return jsonify({'message':'No file part'}),400
  
  required_fields = ['title', 'desc']
  for field in required_fields:
      if field not in request_data:
          return jsonify({'message': f'Missing field: {field}'}), 400

  title=request_data['title']
  desc=request_data['desc']

  file=request.files['poster']
  if file.filename=='':
    return jsonify({'message':'No selected file'}),400
  
  allowed_mimetypes = [ 'text/plain', 'image/jpeg', 'image/png']
  if file.mimetype not in allowed_mimetypes:
      return jsonify({'message': 'Invalid file type'}), 400
  
  try:
    result=uploader.upload(file)
  except Exception as e:
    print(e)
    return jsonify({'message':"Error in file uploading"}),500
  


  new_event= Events(
    title=title,
    submitted_by=int(get_jwt_identity()),
    submitted_on=datetime.now(),
    poster_url=result['secure_url'],
    desc=desc
  )

  try:
    db.session.add(new_event)
    db.session.commit()
  except Exception as e:
    return jsonify({'message':'Error saving event',"error":f"{str(e)}"}),500
  
  
  
  return jsonify({'message':'Event uploaded successfully','data':{'url':result['secure_url']}}),200
  
  

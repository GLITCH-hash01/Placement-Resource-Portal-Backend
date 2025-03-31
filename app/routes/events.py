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
  
  required_fields = ['title','category','know_more']
  for field in required_fields:
      if field not in request_data:
          return jsonify({'message': f'Missing field: {field}'}), 400

  title=request_data['title']
  category=request_data['category']
  know_more=request_data['know_more']
  if category not in ['event','internship']:
    return jsonify({'message': 'Invalid category'}), 400

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
    category=category,
    know_more=know_more,
    poster_url=result['secure_url'],
   
  )

  try:
    db.session.add(new_event)
    db.session.commit()
  except Exception as e:
    return jsonify({'message':'Error saving event',"error":f"{str(e)}"}),500
  
  
  
  return jsonify({'message':'Event uploaded successfully','data':{'url':result['secure_url']}}),200
  

@events_bp.route('/me/get',methods=['GET'])
@jwt_required()
def get_my_events():
  user_id=int(get_jwt_identity())
  events=Events.query.filter_by(submitted_by=user_id).all()
  event_list=[]
  for event in events:
    
    event_list.append({'id':event.id,'title':event.title,'poster_url':event.poster_url,'know_more':event.know_more,'category':event.category})
  return jsonify({'events':event_list}),200

@events_bp.route('/get-all',methods=['GET'])
@jwt_required()
def get_all_events():
  events=Events.query.all()
  event_list=[]
  for event in events:
    if event.category=='event':
      event_list.append({'title':event.title,'poster_url':event.poster_url,'know_more':event.know_more})
    
  return jsonify({'events':event_list}),200

@events_bp.route('/latest',methods=['GET'])
@jwt_required()
def get_latest_events():
  events=Events.query.order_by(Events.submitted_on.desc()).limit(5).all()
  event_list=[]
  for event in events:
    
    event_list.append({'title':event.title,'poster_url':event.poster_url,'know_more':event.know_more})

  return jsonify({'events':event_list}),200

@events_bp.route('/get/<int:event_id>',methods=['GET'])
@jwt_required()
def get_event(event_id):
  event=Events.query.filter_by(id=event_id).first()
  if not event:
    return jsonify({'message':'Event not found'}),404
  return jsonify({'title':event.title,'poster_url':event.poster_url,"submitted_by":event.submitted_by,'know_more':event.know_more}),200

@events_bp.route('/internships/latest',methods=['GET'])
@jwt_required()
def get_latest_internships():
  events=Events.query.filter_by(category='internship').order_by(Events.submitted_on.desc()).limit(5).all()
  event_list=[]
  for event in events:
    event_list.append({'title':event.title,'poster_url':event.poster_url,'know_more':event.know_more})
  return jsonify({'events':event_list}),200

@events_bp.route('/delete/<int:event_id>',methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
  event=Events.query.filter_by(id=event_id).first()
  if not event:
    return jsonify({'message':'Event not found'}),404
  
  user_id=int(get_jwt_identity())
  if event.submitted_by!=user_id:
    return jsonify({'message':'You are not authorized to delete this event'}),403

  try:
    db.session.delete(event)
    db.session.commit()
  except Exception as e:
    return jsonify({'message':'Error deleting event','error':str(e)}),500
  
  return jsonify({'message':'Event deleted successfully'}),200
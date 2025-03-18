from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Notes,AcademicNotes
import cloudinary.uploader as uploader
from datetime import datetime
from app.database import db

notes_bp=Blueprint('notes',__name__)

@notes_bp.route('/upload',methods=['POST'])
@jwt_required()
def upload_note():

  request_data=request.form.to_dict()

  if 'note' not in request.files:
    return jsonify({'message':'No file part'}),400
  
  required_fields = ['module', 'semester', 'course_code', 'scheme', 'year']
  for field in required_fields:
      if field not in request_data:
          return jsonify({'message': f'Missing field: {field}'}), 400

  module=request_data['module']
  semester=request_data['semester']
  course_code=request_data['course_code']
  scheme=request_data['scheme']
  year=request_data['year']

  file=request.files['note']
  if file.filename=='':
    return jsonify({'message':'No selected file'}),400
  
  allowed_mimetypes = ['application/pdf', 'text/plain']
  if file.mimetype not in allowed_mimetypes:
      return jsonify({'message': 'Invalid file type'}), 400
  
  try:
    result=uploader.upload(file)
  except Exception as e:
    print(e)
    return jsonify({'message':"Error in file uploading"}),500
  


  new_note= Notes(
    title=f'{course_code}_S{semester}_M{module}',
    submitted_by=int(get_jwt_identity()),
    submitted_on=datetime.now(),
    doc_url=result['secure_url'],
    likes=0,
    category='academics'
  )

  try:
    db.session.add(new_note)
    db.session.commit()
  except:
    return jsonify({'message':'Error saving note'}),500
  
  academic_details=AcademicNotes(
    note_id=new_note.id,
    semester=semester,
    course_code=course_code,
    module=module,
    scheme=scheme,
    year=year
  )
  try:
    db.session.add(academic_details)
    db.session.commit()
  except Exception as e:
    return jsonify({'message':f'Error saving academic details:{str(e)}'}),500
  
  return jsonify({'message':'Note uploaded successfully','data':{'url':result['secure_url']}}),200
  
  
@notes_bp.route('/me/get',methods=['GET'])
@jwt_required()
def get_submitted_by_me():
  user_id=int(get_jwt_identity())
  notes=Notes.query.filter_by(submitted_by=user_id).all()
  note_list=[]
  for note in notes:
    note_list.append({
      'title':note.title,
      'submitted_on':note.submitted_on,
      'doc_url':note.doc_url,
      'likes':note.likes
    })
  return jsonify({'notes':note_list}),200


@notes_bp.route('/all/get',methods=['GET'])
def get_submitted_by_all():
  notes=Notes.query.all()
  note_list=[]
  for note in notes:
    note_list.append({
      'title':note.title,
      'submitted_on':note.submitted_on,
      'doc_url':note.doc_url,
      'likes':note.likes
    })
  return jsonify({'notes':note_list}),200

@notes_bp.route('/placements',methods=['GET'])
@jwt_required()
def get_all_placements():
  placements=Notes.query.filter_by(category='placement').all()
  placement_list=[]
  for placement in placements:
    placement_list.append({
      'title':placement.title,
      'submitted_on':placement.submitted_on,
      'doc_url':placement.doc_url,
      'likes':placement.likes
    })
  return jsonify({'placements':placement_list}),200

@notes_bp.route('/<string:dep>/<int:scheme>/<int:sem>/<string:course>/<int:mod>',methods=['GET'])
@jwt_required()
def get_course_notes(dep,scheme,sem,course,mod):
  
  note=AcademicNotes.query.filter_by(scheme=scheme,semester=sem,course_code=course,module=mod).first()
  course=Notes.query.filter_by(id=note.note_id).first()
  print(note.note_id)
  return jsonify({'title':course.title,'submitted_on':course.submitted_on,'doc_url':course.doc_url}),200


  
@notes_bp.route('/latest',methods=['GET'])
@jwt_required()
def get_latest_notes():
  notes=Notes.query.order_by(Notes.submitted_on.desc()).limit(5).all()
  note_list=[]
  for note in notes:
    if note.category=='academics':
      academic_details=AcademicNotes.query.filter_by(note_id=note.id).first()
      note_list.append({
        'title':note.title,
        'submitted_on':note.submitted_on,
        'doc_url':note.doc_url,
        'likes':note.likes,
        'semester':academic_details.semester,
        'course_code':academic_details.course_code,
        'module':academic_details.module,
        'scheme':academic_details.scheme,
        'year':academic_details.year
      })
    else:
      note_list.append({
      'title':note.title,
      'submitted_on':note.submitted_on,
      'doc_url':note.doc_url,
      'likes':note.likes
    })
  return jsonify({'notes':note_list}),200
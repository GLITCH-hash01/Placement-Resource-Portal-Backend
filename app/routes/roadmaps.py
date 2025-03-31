from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Roadmaps,RoadmapCourses,Users
from app.database import db

roadmaps_bp=Blueprint('roadmaps',__name__)

@roadmaps_bp.route('/upload',methods=['POST'])
def upload_roadmap():
    data=request.get_json()
    department=data.get('department')
    courses=data.get('courses')

    i=1
    for course in courses:
      print(courses[course])
      roadmap=Roadmaps(department=department,course=courses[course],year=i)
      db.session.add(roadmap)
      i+=1
    db.session.commit()

    return jsonify({'msg':'Roadmap uploaded successfully'}),200

@roadmaps_bp.route('/upload/<string:dep>/<int:year>',methods=['POST'])
def upload_roadmap_courses(dep,year):
    data=request.get_json()
    roadmap_id=Roadmaps.query.filter_by(department=dep,year=year).first().id
    courses=data.get('courses')

    if roadmap_id is None:
      return jsonify({'msg':'Roadmap not found'}),404

    if Roadmaps.query.filter_by(id=roadmap_id).first() is None:
      return jsonify({'msg':'Roadmap not found'}),404
    
    for course in courses:
      print(course)
      roadmap_course=RoadmapCourses(roadmap_id=roadmap_id,course_title=course.get('course_title'),course_resourses=course.get('course_resources'))
      db.session.add(roadmap_course)
       


    try:
      db.session.commit()
    except Exception as e:
      return jsonify({'msg':f'Error occured while uploading roadmap courses \n Error : {str(e)}'}),500
    return jsonify({'msg':'Roadmap courses uploaded successfully'}),200

@roadmaps_bp.route('/get/<string:dep>',methods=['GET'])
@jwt_required()
def get_roadmap(dep):
    roadmaps=Roadmaps.query.filter_by(department=dep).all()
    year=request.args.get('year',type=int)
    if year:
      roadmap=Roadmaps.query.filter_by(department=dep,year=year).first()
      if roadmap is None:
        return jsonify({'msg':'Roadmap not found'}),404
      roadmap_courses=RoadmapCourses.query.filter_by(roadmap_id=roadmap.id).all()
      course_list=[]
      for course in roadmap_courses:
        
        course_list.append({'course_id':course.id,'course_title':course.course_title,'course_resources':course.course_resourses})
      return jsonify({'roadmap':{
         'title':roadmap.course,
        'year':roadmap.year,
        'courses':course_list
      }}),200


    roadmap_list=[]
    for roadmap in roadmaps:
      roadmap_list.append({'year':roadmap.year,'course':roadmap.course})
    return jsonify({'roadmaps':roadmap_list}),200

@roadmaps_bp.route('/update/<string:dep>',methods=['PUT'])
@jwt_required()
def update_roadmap(dep):
    data=request.get_json()
    
    year=data.get('year')
    course=data.get('course')
    user=get_jwt_identity()
    userdata=Users.query.filter_by(id=user).first()
    print(userdata.role)
    if userdata.role!='tpc':
      return jsonify({'msg':'You are not authorized to update roadmap'}),403
    
    roadmap=Roadmaps.query.filter_by(department=dep,year=year).first()
    if roadmap is None:
      return jsonify({'msg':'Roadmap not found'}),404 
    
    roadmap.course=course
    db.session.commit()
    return jsonify({'msg':'Roadmap updated successfully'}),200

@roadmaps_bp.route('/update/course/<int:roadmap_id>',methods=['PUT'])
@jwt_required()
def update_roadmap_courses(roadmap_id):
    user_id=get_jwt_identity()
    user=Users.query.filter_by(id=user_id).first()
    if user.role!='tpc':
      return jsonify({'msg':'You are not authorized to update roadmap'}),403
    data=request.get_json()
    course_title=data.get('course_title')
    course_resources=data.get('course_resources')
    roadmap=RoadmapCourses.query.filter_by(id=roadmap_id).first()
    if roadmap is None:
      return jsonify({'msg':'Roadmap not found'}),404
    roadmap.course_title=course_title
    roadmap.course_resourses=course_resources
    db.session.commit()
    return jsonify({'msg':'Roadmap course updated successfully'}),200

@roadmaps_bp.route('/delete/<int:roadmap_id>',methods=['DELETE'])
@jwt_required()
def delete_roadmap(roadmap_id):
    user=get_jwt_identity()
    userdata=Users.query.filter_by(id=user).first()
    if userdata.role!='tpc':
      return jsonify({'msg':'You are not authorized to delete roadmap'}),403
    roadmap=RoadmapCourses.query.filter_by(id=roadmap_id).first()
    if roadmap is None:
      return jsonify({'msg':'Roadmap not found'}),404
    db.session.delete(roadmap)
    db.session.commit()
    return jsonify({'msg':'Roadmap deleted successfully'}),200
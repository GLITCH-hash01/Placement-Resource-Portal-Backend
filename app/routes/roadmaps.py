from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.models import Roadmaps,RoadmapCourses
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
        course_list.append({'course_title':course.course_title,'course_resources':course.course_resourses})
      return jsonify({'roadmap':{
         'title':roadmap.course,
        'year':roadmap.year,
        'courses':course_list
      }}),200


    roadmap_list=[]
    for roadmap in roadmaps:
      roadmap_list.append({'year':roadmap.year,'course':roadmap.course})
    return jsonify({'roadmaps':roadmap_list}),200
from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Users, Queries, Responses
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

queries_bp=Blueprint('queries',__name__)

def time_ago(submitted_on):
    now = datetime.now()
    diff = now - submitted_on

    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds // 3600 > 0:
        return f"{diff.seconds // 3600} hours ago"
    elif diff.seconds // 60 > 0:
        return f"{diff.seconds // 60} minutes ago"
    else:
        return "just now"

@queries_bp.route('/test',methods=['GET'])
def test():
    return 'Queries route working'

@queries_bp.route('/add',methods=['POST'])
@jwt_required()
def add_query():
    data=request.get_json()
    user_id=get_jwt_identity()

    required_fields=['query_title','query_desc']
    for field in required_fields:
        if field not in data:
            return jsonify({'message':f'{field} is required'}),400
    
    if 'stack' not in data:
        data['stack']=''

    user=db.session.query(Users).filter(Users.id==user_id).first()
    query=Queries(submitted_by=user.id,query_title=data['query_title'],query_desc=data['query_desc'],stack=data['stack'] ,submitted_on=datetime.now())
    db.session.add(query)
    
    db.session.commit()
    return jsonify({'message':'Query added successfully'}), 200

@queries_bp.route('/respond/<int:query_id>',methods=['POST'])
@jwt_required()
def respond_query(query_id):
    data=request.get_json()
    user_id=get_jwt_identity()

    required_fields=['response']
    for field in required_fields:
        if field not in data:
            return jsonify({'message':f'{field} is required'}),400
    
    user=db.session.query(Users).filter(Users.id==user_id).first()
    query=db.session.query(Queries).filter(Queries.id==query_id).first()
    if not query:
        return jsonify({'message':'Query not found'}),404
    
    response=Responses(query_id=query.id,response=data['response'],responded_by=user.id,responded_on=datetime.now())
    try:
        db.session.add(response)
        db.session.commit()
    except:
        return jsonify({'message':'Error adding response'}),500
    
    return jsonify({'message':'Response added successfully'}),200

@queries_bp.route('/get/all',methods=['GET'])
def get_queries():
    queries=db.session.query(Queries).order_by(Queries.submitted_on.desc()).limit(20)
    
    query_list=[]
    for query in queries:
        response_list=[]
        if query.responses:
            response_list=[{
                'response':response.response,
                'responded_by':Users.query.filter(Users.id==response.responded_by).first().username,
                'responded_on':response.responded_on
            } for response in query.responses]
        user = Users.query.filter(Users.id == query.submitted_by).first()
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,  # Include other fields as needed
            'role': user.role
        } if user else None
        query_list.append({
            'query_id':query.id,
            'query_title':query.query_title,
            'query_desc':query.query_desc,
            'responses':response_list,
            'stack':query.stack,
            'submitted_by':user_data,
            
            'submitted_on':time_ago(query.submitted_on)
        })
    return jsonify({'queries':query_list}),200

@queries_bp.route('/get/me',methods=['GET'])
@jwt_required()
def get_my_queries():
    user_id=get_jwt_identity()
    queries=db.session.query(Queries).filter(Queries.submitted_by==user_id).order_by(Queries.submitted_on.desc()).limit(20)
    
    query_list=[]
    for query in queries:
        response_list=[]
        if query.responses:
            for response in query.responses:
                user = Users.query.filter(Users.id == response.responded_by).first()

                response_list.append({
                    'response':response.response,
                    'responded_by':{
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,  # Include other fields as needed
                        'role': user.role
                    },
                    'responded_on':time_ago(response.responded_on)
                })
           
        user = Users.query.filter(Users.id == query.submitted_by).first()
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,  # Include other fields as needed
            'role': user.role
        } if user else None
        query_list.append({
            'query_id':query.id,
            'query_title':query.query_title,
            'query_desc':query.query_desc,
            'responses':response_list,
            'stack':query.stack,
            'submitted_by':user_data,
            'submitted_on':time_ago(query.submitted_on)
        })
    return jsonify({'queries':query_list}),200

@queries_bp.route('/like/query/<int:query_id>',methods=['POST'])
@jwt_required()
def like_query(query_id):
    user_id=get_jwt_identity()
    query=db.session.query(Queries).filter(Queries.id==query_id).first()
    if not query:
        return jsonify({'message':'Query not found'}),404
    
    like=db.session.query(QueriesLikes).filter(QueriesLikes.query_id==query_id,QueriesLikes.liked_by==user_id).first()
    if like:
        return jsonify({'message':'Query already liked'}),400
    
    like=QueriesLikes(query_id=query_id,liked_by=user_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message':'Query liked successfully'}),200

@queries_bp.route('/like/response/<int:response_id>',methods=['POST'])
@jwt_required()
def like_response(response_id):
    user_id=get_jwt_identity()
    response=db.session.query(Responses).filter(Responses.id==response_id).first()
    if not response:
        return jsonify({'message':'Response not found'}),404
    
    like=db.session.query(QueriesLikes).filter(QueriesLikes.response_id==response_id,QueriesLikes.liked_by==user_id).first()
    if like:
        return jsonify({'message':'Response already liked'}),400
    
    like=QueriesLikes(response_id=response_id,liked_by=user_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message':'Response liked successfully'}),200 

@queries_bp.route('/get/<int:query_id>',methods=['GET'])
@jwt_required()
def get_query(query_id):
    query=db.session.query(Queries).filter(Queries.id==query_id).first()
    if not query:
        return jsonify({'message':'Query not found'}),404
    
    response_list=[]
    if query.responses:
        for response in query.responses:
            user = Users.query.filter(Users.id == response.responded_by).first()

            response_list.append({
                'response':response.response,
                'responded_by':{
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,  # Include other fields as needed
                    'role': user.role
                },
                'responded_on':time_ago(response.responded_on)
            })
    
    user = Users.query.filter(Users.id == query.submitted_by).first()
    
    return jsonify({"query":{
        'query_id':query.id,
        'query_title':query.query_title,
        'query_desc':query.query_desc,
        'response_count':len(response_list),
        'responses':response_list,
        'stack':query.stack,
        'submitted_by':{
            'id': user.id,
            'username': user.username,
            'email': user.email,  # Include other fields as needed
            'role': user.role
        },
        'submitted_on':time_ago(query.submitted_on)
    }}),200
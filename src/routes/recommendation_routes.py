from flask import Blueprint, request, jsonify
from services.recommendation_service import RecommendationService
from app import mongo
from bson import ObjectId
from datetime import datetime

recommendation_bp = Blueprint('recommendation_bp', __name__)
recommendation_service = RecommendationService()

@recommendation_bp.route('/user/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    # Get user profile
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get available courses
    available_courses = list(mongo.db.courses.find())
    
    # Get personalized recommendations
    recommendations = recommendation_service.get_course_recommendations(
        user_profile=user,
        available_courses=available_courses
    )
    
    # Convert ObjectId to string
    for rec in recommendations:
        rec['_id'] = str(rec['_id'])
    
    return jsonify(recommendations), 200

@recommendation_bp.route('/feedback', methods=['POST'])
def process_feedback():
    data = request.get_json()
    user_id = data['user_id']
    course_id = data['course_id']
    feedback = data['feedback']
    
    # Store feedback
    mongo.db.feedback.insert_one({
        'user_id': user_id,
        'course_id': course_id,
        'feedback': feedback,
        'timestamp': datetime.utcnow()
    })
    
    # Update recommendations based on feedback
    current_recommendations = list(mongo.db.recommendations.find({'user_id': user_id}))
    updated_recommendations = recommendation_service.update_recommendations(
        feedback,
        current_recommendations
    )
    
    return jsonify({'message': 'Feedback processed successfully'}), 200 
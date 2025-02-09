from flask import Blueprint, request, jsonify
from models.user import User
from services.profile_service import ProfileService
from database import mongo
from bson import ObjectId
from utils.helpers import hash_password, verify_password

user_bp = Blueprint('user_bp', __name__)
profile_service = ProfileService()

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user exists
    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hash_password(data['password']),
        preferences=data.get('preferences'),
        goals=data.get('goals')
    )
    
    # Insert into MongoDB
    result = mongo.db.users.insert_one(user.to_dict())
    
    return jsonify({'message': 'User registered successfully', 'user_id': str(result.inserted_id)}), 201

@user_bp.route('/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user['_id'] = str(user['_id'])
    return jsonify(user), 200

@user_bp.route('/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    data = request.get_json()
    
    # Update user profile
    result = mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'preferences': data.get('preferences'),
            'goals': data.get('goals')
        }}
    )
    
    if result.modified_count:
        return jsonify({'message': 'Profile updated successfully'}), 200
    return jsonify({'error': 'User not found'}), 404 
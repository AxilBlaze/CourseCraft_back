from flask import Blueprint, request, jsonify
from services.tutor_service import TutorService
from app import mongo
from datetime import datetime

tutor_bp = Blueprint('tutor_bp', __name__)
tutor_service = TutorService()

@tutor_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        user_id = data.get('user_id', 'test-user')
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"Processing message: {message}")
        
        # Get AI response
        response = tutor_service.generate_response(message)
        
        # Store chat history
        chat_entry = {
            'user_id': user_id,
            'message': message,
            'response': response,
            'timestamp': datetime.utcnow()
        }
        
        try:
            mongo.db.chat_history.insert_one(chat_entry)
        except Exception as e:
            print(f"Warning: Could not save chat history: {e}")
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow()
        }), 200
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@tutor_bp.route('/history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    try:
        history = list(mongo.db.chat_history.find(
            {'user_id': user_id},
            {'_id': 0}
        ).sort('timestamp', -1).limit(50))
        
        return jsonify(history), 200
    except Exception as e:
        print(f"Error fetching chat history: {str(e)}")
        return jsonify({'error': str(e)}), 500 
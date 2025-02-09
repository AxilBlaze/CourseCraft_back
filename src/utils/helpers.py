from datetime import datetime
from typing import List, Dict
from passlib.hash import pbkdf2_sha256
import secrets

def format_chat_history(history: List[Dict]) -> List[Dict]:
    """Format chat history for frontend display"""
    formatted_history = []
    for entry in history:
        formatted_history.append({
            'type': 'user',
            'content': entry['message'],
            'timestamp': entry['timestamp']
        })
        formatted_history.append({
            'type': 'assistant',
            'content': entry['response'],
            'timestamp': entry['timestamp']
        })
    return formatted_history

def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256"""
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return pbkdf2_sha256.verify(password, password_hash)

def generate_token() -> str:
    """Generate a secure token"""
    return secrets.token_urlsafe(32) 
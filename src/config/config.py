import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/adaptive_learning')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    HF_API_KEY = os.getenv('HF_API_KEY', '')  # Hugging Face API key 
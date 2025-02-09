from pymongo import MongoClient
from dotenv import load_dotenv
import os

def test_simple_connection():
    load_dotenv()
    
    # Get MongoDB URI
    mongo_uri = os.getenv('MONGO_URI')
    print("Testing MongoDB connection...")
    
    try:
        # Create client
        client = MongoClient(mongo_uri)
        
        # Test connection
        client.admin.command('ping')
        
        print("Successfully connected to MongoDB!")
        
        # Test database access
        db = client['adaptive_learning']
        
        # Create a test document
        test_collection = db['test']
        result = test_collection.insert_one({"test": "connection"})
        print("Successfully inserted test document!")
        
        # Clean up
        test_collection.delete_one({"test": "connection"})
        print("Successfully cleaned up test document!")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_connection() 
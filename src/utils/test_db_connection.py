from pymongo import MongoClient
from dotenv import load_dotenv
import os

def test_mongodb_connection():
    load_dotenv()
    
    # Get MongoDB URI from environment variable
    mongo_uri = os.getenv('MONGO_URI')
    
    if not mongo_uri:
        print("Error: MONGO_URI not found in environment variables")
        return False
    
    try:
        # Create a MongoDB client
        client = MongoClient(mongo_uri)
        
        # Try to get server info
        server_info = client.server_info()
        
        print("Successfully connected to MongoDB!")
        print(f"Server version: {server_info.get('version')}")
        
        # List available databases
        databases = client.list_database_names()
        print("\nAvailable databases:")
        for db in databases:
            print(f"- {db}")
            
        # Get specific database
        db = client['adaptive_learning']
        
        # List collections in the database
        collections = db.list_collection_names()
        print("\nCollections in 'adaptive_learning' database:")
        for collection in collections:
            print(f"- {collection}")
            # Count documents in each collection
            count = db[collection].count_documents({})
            print(f"  Documents: {count}")
            
        return True
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return False
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_mongodb_connection() 
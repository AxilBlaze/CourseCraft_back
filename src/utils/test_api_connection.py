import requests
import os
from dotenv import load_dotenv
import time

def test_huggingface_api():
    load_dotenv()
    api_key = os.getenv('HF_API_KEY')
    api_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    test_message = "What is Python programming?"
    
    try:
        print("Testing Hugging Face API connection...")
        payload = {
            "inputs": test_message
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ API connection successful!")
                result = response.json()
                print("\nTest Response:")
                print(result[0]['generated_text'])
                return True
            elif response.status_code == 503:
                print(f"Model is loading (attempt {attempt + 1}/{max_retries}), waiting 5 seconds...")
                time.sleep(5)
                continue
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return False
                
        print("❌ Max retries reached, model still loading")
        return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_huggingface_api() 
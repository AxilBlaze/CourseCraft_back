from transformers import pipeline
import os
from dotenv import load_dotenv

def test_simple_model():
    load_dotenv()
    print("Starting simple Hugging Face test...")
    
    try:
        # Try loading a very small model first
        print("Loading small text classification model...")
        classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1
        )
        
        # Test the model
        test_text = "I love learning programming!"
        result = classifier(test_text)
        print(f"\nTest successful!")
        print(f"Input: {test_text}")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_model() 
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv

def test_hugging_face_connection():
    load_dotenv()
    
    # Get Hugging Face API key
    hf_api_key = os.getenv('HF_API_KEY')
    model_name = "microsoft/DialoGPT-medium"
    
    if not hf_api_key:
        print("Warning: HF_API_KEY not found in environment variables")
    
    try:
        print("Testing Hugging Face connection...")
        print(f"Attempting to load {model_name} model...")
        
        # Load tokenizer and model with caching
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="./models")
        model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir="./models")
        
        # Create pipeline with cached model
        chat_model = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=-1  # Use CPU
        )
        
        print("Successfully loaded DialoGPT model!")
        
        # Test generation
        test_input = "Hello, how can you help me learn programming?"
        print("\nTesting model with input:", test_input)
        
        response = chat_model(
            test_input,
            max_length=50,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        
        print("\nModel response:", response[0]['generated_text'])
        return True
        
    except Exception as e:
        print(f"\nError testing Hugging Face connection: {str(e)}")
        
        print("\nTrying fallback model (GPT-2)...")
        try:
            chat_model = pipeline(
                "text-generation",
                model="gpt2",
                device=-1
            )
            print("Successfully loaded GPT-2 fallback model!")
            
            # Test generation with fallback model
            test_input = "Hello, how can you help me learn programming?"
            print("\nTesting fallback model with input:", test_input)
            
            response = chat_model(
                test_input,
                max_length=50,
                num_return_sequences=1
            )
            
            print("\nFallback model response:", response[0]['generated_text'])
            return True
            
        except Exception as e2:
            print(f"\nError loading fallback model: {str(e2)}")
            return False

if __name__ == "__main__":
    test_hugging_face_connection() 
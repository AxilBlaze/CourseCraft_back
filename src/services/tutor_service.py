import requests
import os
from dotenv import load_dotenv
import time

class TutorService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HF_API_KEY')
        # Using a more stable model for API access
        self.api_url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        print("TutorService initialized with API configuration")

    def generate_response(self, user_message: str) -> str:
        try:
            # Format the prompt to be more tutor-like
            formatted_prompt = self._format_prompt(user_message)
            
            payload = {
                "inputs": formatted_prompt,
                "parameters": {
                    "max_new_tokens": 250,
                    "temperature": 0.7,
                    "top_k": 50,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            print(f"Sending request with prompt: {formatted_prompt}")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if isinstance(result, list) and result:
                        return self._format_response(result[0]['generated_text'])
                    return "I'm not sure how to explain that. Could you rephrase your question?"
                except Exception as e:
                    print(f"Error parsing response: {e}")
                    print(f"Raw response: {response.text}")
                    return "I had trouble generating a detailed explanation. Could you try asking in a different way?"
            elif response.status_code == 503:
                print("Model is loading, retrying in 5 seconds...")
                time.sleep(5)
                return self.generate_response(user_message)
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return "I'm having trouble connecting. Please try again in a moment."
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return "Sorry, I encountered an error. Please try again."

    def _format_prompt(self, message: str) -> str:
        """Format the user message into a tutor-like prompt"""
        base_prompt = """You are a helpful programming tutor. Provide clear, detailed explanations with examples.
        
Question: {message}

Answer: Let me explain this in detail."""

        # Detect the type of question
        message = message.lower()
        if "explain" in message or "what is" in message or "what are" in message:
            return base_prompt.format(message=message)
        elif "how to" in message or "how do" in message:
            return base_prompt.format(message=f"Show me step by step: {message}")
        elif "difference between" in message or "compare" in message:
            return base_prompt.format(message=f"Compare and contrast: {message}")
        elif "debug" in message or "error" in message or "fix" in message:
            return base_prompt.format(message=f"Debug this issue: {message}")
        else:
            return base_prompt.format(message=message)

    def _format_response(self, response: str) -> str:
        """Format the response to be more structured and readable"""
        # Clean up the response
        response = response.strip()
        
        # Add code formatting if there's code in the response
        if "```" not in response and ("import " in response or "=" in response or "(" in response):
            lines = response.split("\n")
            formatted_lines = []
            in_code = False
            
            for line in lines:
                if any(code_indicator in line for code_indicator in ["import ", "=", "(", "def ", "class "]):
                    if not in_code:
                        formatted_lines.append("\n```python")
                        in_code = True
                    formatted_lines.append(line)
                else:
                    if in_code:
                        formatted_lines.append("```\n")
                        in_code = False
                    formatted_lines.append(line)
            
            if in_code:
                formatted_lines.append("```")
            
            response = "\n".join(formatted_lines)
        
        # Add structure to the response if it's not already structured
        if not any(header in response for header in ["Step 1:", "1.", "First,"]):
            parts = response.split("\n\n")
            if len(parts) == 1:
                parts = response.split(". ")
            
            if len(parts) > 1:
                response = "\n\n".join([
                    "Here's a detailed explanation:\n",
                    *[f"{i+1}. {part.strip()}" for i, part in enumerate(parts)]
                ])
        
        return response 
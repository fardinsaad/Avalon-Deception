import os
import backoff
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load environment variables from the .env file
# print("Before loading .env:", os.getenv('GEMINI_API_KEY'))
load_dotenv(override=True)  # Force override existing environment variables
# print("After loading .env:", os.getenv('GEMINI_API_KEY'))

# Set Gemini API key from environment variable
key = os.getenv('GEMINI_API_KEY')

if not key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=key)

@backoff.on_exception(backoff.expo, errors.ClientError, max_time=120)
def get_gemini_completion(**kwargs):
    """
    Get completion from Gemini API with backoff in case of errors.
    
    Usage:
        response = get_gemini_completion(
            model="gemini-2.0-flash-exp",
            prompt="Your prompt here",
            temperature=0.5,
            max_output_tokens=1024
        )
    """
    model_name = kwargs.get('model', 'gemini-2.0-flash-exp')
    prompt = kwargs.get('prompt', kwargs.get('messages', ''))
    temperature = kwargs.get('temperature', 0.5)
    max_output_tokens = kwargs.get('max_output_tokens', kwargs.get('max_tokens', 1024))
    
    # Handle messages format (OpenAI-style) for compatibility
    if isinstance(prompt, list):
        # Convert messages list to single prompt
        prompt_text = ""
        for msg in prompt:
            role = msg.get('role', '')
            content = msg.get('content', '')
            if role == 'system':
                prompt_text += f"{content}\n\n"
            elif role == 'user':
                prompt_text += content
        prompt = prompt_text
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config={
            'temperature': temperature,
            'max_output_tokens': max_output_tokens,
        }
    )
    
    # Return response in a format similar to OpenAI
    class GeminiResponse:
        def __init__(self, text):
            self.text = text.strip()
            self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': self.text})()})]
    
    return GeminiResponse(response.text)

def get_response(prompt):
    """Function to interact with Gemini and generate a response."""
    response = client.models.generate_content(
        model='gemma-3-27b-it',
        contents=prompt,
        config={'max_output_tokens': 512}
    )
    return response.text.strip()

# Main function to run the script and test the API connection
if __name__ == '__main__':
    # Check if the API key is correctly loaded
    
    if key:
        print("API key loaded successfully.")
        # List all available Gemini models
        print("\nModels available for this API key:")
        try:
            models = client.models.list()
            for model in models:
                print(f"  {model.name}")
        except Exception as e:
            print(f"Error listing models: {e}")
            
        # Test with a sample prompt
        print("\nTesting API with sample prompt...")
        test_prompt = "Name a country that starts with K?"
        try:
            result = get_response(test_prompt)
            print(f"Gemini Response: {result}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("API key not found. Please set it in your .env file.")

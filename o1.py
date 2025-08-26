import openai
import os
import backoff
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError  # Directly import RateLimitError

# Load environment variables from the .env file
# print("Before loading .env:", os.getenv('OPENAI_API_KEY'))
load_dotenv()
# print("After loading .env:", os.getenv('OPENAI_API_KEY'))

# Set OpenAI API key from environment variable
key = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
client = OpenAI(api_key  = key)

@backoff.on_exception(backoff.expo, RateLimitError, max_time=100)  # Use RateLimitError directly
def get_completion_with_backoff(**kwargs):
    """Get completion from OpenAI API with backoff in case of RateLimitError."""
    return client.chat.completions.create(**kwargs)  # Corrected method for chat-based models like GPT-4

def get_response_o1(prompt):
    """Function to interact with GPT-4o and generate a response."""
    
    # Define the messages in a variable called 'msgs'
    msgs = [
        {"role": "user", "content": prompt}
    ]
    
    Model = "o1-preview"
    
    response = client.chat.completions.create(
        model=Model,
        messages=msgs,
        # max_completion_tokens=1024, #for gpt o1
        # max_tokens=1024,
        # temperature=0.3,
        #top_p = 0.9
    )
    # if response.choices and response.choices[0].message:
    #     print("Generated text:", response.choices[0].message.content)
    # else:
    #     print("No message content returned by the model.")
    return response.choices[0].message.content

# Main function to run the script and test the API connection
if __name__ == '__main__':
    # Check if the API key is correctly loaded
    
    if key:
        print("API key loaded successfully.")
        #PRINT THE LIST OF models for this key
        # print(key)
        # models = client.models.list()
        # print("Models available for this API key:")
        # for model in models:
        #     print(model.id)
            
        # Test with a sample prompt
        test_prompt = "What is the capital of Bangladesh?"
        result = get_response_o1(test_prompt)
        print("GPT Response:", result)
    else:
        print("API key not found. Please set it in your .env file.")


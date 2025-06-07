from openai import OpenAI
from openai import RateLimitError
from config import OPENAI_API_KEY

client = OpenAI()
client.api_key = OPENAI_API_KEY

def ask_ai(user_prompt):
    """Send a user message to model and return the response"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except RateLimitError as e:
        print(f"Rate limit exceeded. Please try again later. Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

try:
    reply = ask_ai("What is the capital of France?")
    if reply:
        print(reply)
    else:
        print("Failed to get response from AI")
except Exception as e:
    print(f"Unexpected error: {e}")
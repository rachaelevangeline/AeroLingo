# netlify/functions/decode.py
import os
import json
from openai import OpenAI # Using OpenAI as per your previous choice and code structure

def handler(event, context):
    # Ensure it's a POST request
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Method Not Allowed. This function only accepts POST requests."})
        }

    # Parse the request body
    try:
        body = json.loads(event['body'])
        phrase = body.get('phrase')
    except (json.JSONDecodeError, AttributeError):
        return {
            'statusCode': 400,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Invalid JSON format in request body or missing 'phrase'."})
        }

    if not phrase:
        return {
            'statusCode': 400,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Missing 'phrase' in request body."})
        }

    # Access the API Key securely from Netlify's Environment Variables
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set in Netlify environment variables.")
        return {
            'statusCode': 500,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Server configuration error: API key not found. Please contact support."})
        }

    # Initialize OpenAI client and make the API call
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Recommended for free tier and performance
            messages=[
                {"role": "system", "content": "You are an expert aviation instructor. Explain any Air Traffic Control (ATC) or pilot phrase in simple, clear, and beginner-friendly English. Be concise and focus on the meaning relevant to flight operations."},
                {"role": "user", "content": phrase}
            ],
            temperature=0.7, # Adjust creativity (0.0-1.0), lower for more factual
            max_tokens=150 # Limit response length to keep it concise
        )

        explanation = chat_completion.choices[0].message.content

        return {
            'statusCode': 200,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"explanation": explanation})
        }

    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        return {
            'statusCode': 500,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": f"Failed to get explanation from AI: {str(e)}"})
        }

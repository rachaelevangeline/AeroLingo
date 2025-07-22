# netlify/functions/decode.py
import os
import json
import google.generativeai as genai # We will need to install this library

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
    # This name (GEMINI_API_KEY) must match what you set in Netlify!
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY is not set in Netlify environment variables.")
        return {
            'statusCode': 500,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Server configuration error: API key not found. Please contact support."})
        }

    # Configure Google Generative AI
    genai.configure(api_key=GEMINI_API_KEY)

    try:
        # Use gemini-pro or gemini-flash
        model = genai.GenerativeModel('gemini-pro')

        # Construct the prompt for the AI
        prompt = f"""
        You are an expert aviation instructor. Explain the following Air Traffic Control (ATC) or ICAO phrase in simple, clear, and beginner-friendly English. Be concise and focus on the meaning relevant to flight operations.

        Phrase: "{phrase}"

        Explanation:
        """

        # Make the API call to Gemini
        response = model.generate_content(prompt)

        # Extract the explanation text
        explanation = response.text.strip()
        if not explanation:
            explanation = "No clear explanation found. The AI might not have understood the phrase."

        return {
            'statusCode': 200,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"explanation": explanation})
        }

    except Exception as e:
        print(f"An error occurred with Gemini API: {e}")
        return {
            'statusCode': 500,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": f"Failed to get explanation from AI: {str(e)}"})
        }

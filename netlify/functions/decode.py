# netlify/functions/decode.py
import os
import json
import google.generativeai as genai

def handler(event, context):
    """
    Netlify Function to decode ATC phrases using Google Gemini API.
    """
    # 1. Ensure it's a POST request
    if event['httpMethod'] != 'POST':
        print("DEBUG: Method Not Allowed.")
        return {
            'statusCode': 405,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Method Not Allowed. This function only accepts POST requests."})
        }

    # 2. Parse the request body from the frontend
    try:
        body = json.loads(event['body'])
        phrase = body.get('phrase')
        print(f"DEBUG: Received phrase: '{phrase}'")
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"ERROR: Failed to parse request body or get phrase: {e}")
        return {
            'statusCode': 400,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Invalid JSON format in request body or missing 'phrase'."})
        }

    if not phrase:
        print("DEBUG: Phrase is empty.")
        return {
            'statusCode': 400,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Missing 'phrase' in request body."})
        }

    # 3. Access the Gemini API Key securely from Netlify's Environment Variables
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY is not set in Netlify environment variables.")
        return {
            'statusCode': 500,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": "Server configuration error: API key not found. Please contact support."})
        }
    else:
        print("DEBUG: GEMINI_API_KEY successfully loaded.") # Confirm key presence without printing value

    # 4. Configure Google Generative AI with the API Key
    genai.configure(api_key=GEMINI_API_KEY)

    # 5. Make the API call to Gemini
    try:
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        You are an expert aviation instructor. Explain the following Air Traffic Control (ATC) or ICAO phrase in simple, clear, and beginner-friendly English. Be concise and focus on the meaning relevant to flight operations.

        Phrase: "{phrase}"

        Explanation:
        """
        print(f"DEBUG: Sending prompt to Gemini (first 200 chars): {prompt[:200]}...")

        # --- CRITICAL DEBUGGING LINE ---
        # This will capture the full response object from Gemini
        gemini_response = model.generate_content(prompt)
        print(f"DEBUG: Raw Gemini API response object: {gemini_response}")
        # --- END CRITICAL DEBUGGING LINE ---
        
        # Check if the response contains text content
        explanation = ""
        if hasattr(gemini_response, 'text') and gemini_response.text:
            explanation = gemini_response.text.strip()
        else:
            # If 'text' attribute is missing or empty, check for other parts like 'parts' or 'safety_ratings'
            # This is an advanced check, but useful if 'text' is consistently empty
            if hasattr(gemini_response, 'parts') and gemini_response.parts:
                print(f"DEBUG: Gemini response has 'parts': {gemini_response.parts}")
            if hasattr(gemini_response, 'prompt_feedback') and gemini_response.prompt_feedback:
                print(f"DEBUG: Gemini response has 'prompt_feedback': {gemini_response.prompt_feedback}")
            if hasattr(gemini_response, 'candidates') and gemini_response.candidates:
                print(f"DEBUG: Gemini response has 'candidates': {gemini_response.candidates}")
                # You might need to iterate through candidates and parts to find text
                # For example: gemini_response.candidates[0].content.parts[0].text
            
            print("DEBUG: Gemini response 'text' attribute was empty or missing.")

        if not explanation:
            explanation = "No clear explanation found. The AI might not have understood the phrase or provided an empty response."
            print(f"DEBUG: Final explanation set to fallback: '{explanation}'")

        return {
            'statusCode': 200,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"explanation": explanation})
        }

    except Exception as e:
        print(f"ERROR: An error occurred during Gemini API call or processing: {e}")
        return {
            'statusCode': 500,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({"error": f"Failed to get explanation from AI: {str(e)}. Please check the phrase or try again later."})
        }

#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env locally
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def test_gemini_api():
    try:
        # Configure the API
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Create model instance
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Test with a simple prompt
        test_prompt = "Hello, can you respond with a simple greeting?"
        
        print("Testing Gemini API...")
        response = model.generate_content(test_prompt)
        
        if response and response.text:
            print("✅ API Test Successful!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ API Test Failed: No response text")
            return False
            
    except Exception as e:
        print(f"❌ API Test Failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api()
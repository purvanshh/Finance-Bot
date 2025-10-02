#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env locally
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def list_available_models():
    try:
        # Configure the API
        genai.configure(api_key=GEMINI_API_KEY)
        
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Model: {m.name}")
        
    except Exception as e:
        print(f"❌ Error listing models: {str(e)}")

if __name__ == "__main__":
    list_available_models()
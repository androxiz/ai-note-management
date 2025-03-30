import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def summaraze_note(text: str):
    model = genai.GenerativeModel('gemini-2.0-flash')
    try:
        request = model.generate_content(f'Make a little summary about the note {text}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return request.text.strip()

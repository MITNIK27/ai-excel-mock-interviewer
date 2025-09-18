import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# # Load environment variables
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (ImportError, KeyError):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
if not GEMINI_API_KEY:
    raise ValueError("⚠️ Missing GEMINI_API_KEY in .env file")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Pick model
MODEL_NAME = "gemini-1.5-flash"  # free-tier friendly


def generate_questions(tech_stack: str, keywords: str, yoe: int, num_questions: int = 5):
    """
    Generate interview questions dynamically from Gemini based on skill keywords + YOE.
    """
    prompt = f"""
    You are an AI mock interviewer.
    Generate {num_questions} structured interview questions for a candidate.
    
    Candidate details:
    - Tech stack: {tech_stack}
    - Keywords: {keywords}
    - Years of experience: {yoe}

    Rules:
    - For fresher (0-1 YOE): focus on basics + medium difficulty.
    - For 2-3 YOE: mix medium + advanced questions.
    - For 4+ YOE: focus on advanced, scenario-based questions.
    - Return as a numbered list, plain text (no explanations).
    """

    response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
    return response.text.strip()


def _parse_json_response(text: str, default: dict = None):
    """
    Try parsing Gemini response into JSON.
    Handles cases where response is wrapped in ```json ... ```.
    """
    if default is None:
        default = {}

    try:
        # Remove markdown fences if present
        cleaned = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()
        return json.loads(cleaned)
    except Exception:
        print("⚠️ Response was not valid JSON:", text)
        return default


def evaluate_answer(question: str, answer: str):
    """
    Evaluate a candidate's answer.
    Returns a dict with score, strengths, weaknesses.
    """
    prompt = f"""
    You are an AI evaluator.
    Question: {question}
    Candidate's Answer: {answer}

    Task:
    - Give a score from 0-10
    - List 2 strengths
    - List 2 weaknesses

    Return strictly in JSON format:
    {{
        "score": <int>,
        "strengths": ["..", ".."],
        "weaknesses": ["..", ".."]
    }}
    """

    response = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
    return _parse_json_response(response.text.strip())

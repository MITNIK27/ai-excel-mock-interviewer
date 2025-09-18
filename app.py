from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
from utils import excel_handler as eh 
import streamlit as st

# Load environment variables
load_dotenv()

app = Flask(__name__)

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (ImportError, KeyError):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-001:generateContent"

# In-memory session storage
sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    session_id = request.json.get('session_id')
    sessions[session_id] = {
        "questions_asked": 0,
        "score": 0,
        "transcript": []
    }
    return jsonify({"message": "Interview started! Ready for the first question."})

@app.route('/question', methods=['GET'])
def question():
    session_id = request.args.get('session_id')
    if session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    questions = [
        "Explain the use of VLOOKUP in Excel.",
        "How would you use conditional formatting?",
        "What is the purpose of pivot tables?",
        "How do you protect cells or a worksheet?",
        "Describe how to create a chart based on a dataset."
    ]
    
    q_index = sessions[session_id]["questions_asked"]
    if q_index >= len(questions):
        return jsonify({"message": "No more questions"}), 200
    
    question_text = questions[q_index]
    sessions[session_id]["current_question"] = question_text
    return jsonify({"question": question_text})

@app.route('/answer', methods=['POST'])
def answer():
    session_id = request.json.get('session_id')
    answer_text = request.json.get('answer')
    
    if session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    session = sessions[session_id]
    question = session.get("current_question")
    
    # Prepare prompt for Gemini
    prompt = f"Question: {question}\nAnswer: {answer_text}\nEvaluate this answer. Is it correct, partially correct, or incorrect? Provide feedback."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.7
    }
    
    response = requests.post(GEMINI_URL, json=data, headers=headers)
    result = response.json()
    feedback = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No feedback available.")
    
    # Update session
    session["questions_asked"] += 1
    session["transcript"].append({
        "question": question,
        "answer": answer_text,
        "feedback": feedback
    })
    
    return jsonify({"feedback": feedback})

@app.route('/end', methods=['GET'])
def end():
    session_id = request.args.get('session_id')
    if session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400
    
    session = sessions.pop(session_id)

    # ✅ Save transcript & summary in Excel
    candidate_id = request.args.get('candidate_id')
    if candidate_id:
        # Create a backend summary
        avg_score = None  # (you can add scoring logic if needed)
        summary = {
            "total_questions": session["questions_asked"],
            "transcript": session["transcript"],
            "average_score": avg_score
        }
        eh.update_candidate(candidate_id, {
            "transcript_json": session["transcript"],
            "summary_json": summary
        })

    # ✅ Only send clean message to frontend
    return jsonify({
        "message": "✅ Interview completed. Your answers have been recorded and will be reviewed."
    })

@app.route('/admin/transcript/<session_id>', methods=['GET'])
def admin_transcript(session_id):
    # This would normally check authentication before exposing!
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Transcript not found"}), 404
    return jsonify({"transcript": session["transcript"]})


if __name__ == "__main__":
    app.run(debug=True)

from utils import excel_handler as eh
from utils import gemini_handler as gh
import json

def generate_and_store_questions(candidate_id: str, num_questions: int = 5):
    """
    Fetch candidate info from Excel, generate questions using Gemini,
    and update the candidate row in Excel.
    """
    candidate = eh.get_candidate(candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found.")

    tech_stack = candidate.get("tech_stack")
    keywords = candidate.get("keywords")
    yoe = int(candidate.get("yoe", 0))

    # Generate questions from Gemini
    questions_text = gh.generate_questions(tech_stack, keywords, yoe, num_questions)

    # Convert numbered list text to structured JSON
    structured_questions = []
    for line in questions_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Remove leading numbering (e.g., "1. ")
        q_text = line.split(". ", 1)[-1] if ". " in line else line
        structured_questions.append({
            "question": q_text,
            "answer": "",   # empty placeholder
            "score": None,
            "strengths": [],
            "weaknesses": []
        })

    # Update candidate in Excel
    eh.update_candidate(candidate_id, {
        "questions_json": structured_questions,
        "transcript_json": []  # initialize empty transcript
    })

    return structured_questions

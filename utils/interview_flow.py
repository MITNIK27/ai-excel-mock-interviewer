# from utils import excel_handler as eh
# from utils import gemini_handler as gh
# import datetime
# import json

# def conduct_interview(candidate_id: str, answers: dict = None):
#     """
#     Conduct mock interview for candidate.
#     Stores transcript & summary in Excel.
#     Returns only a minimal status message for frontend.
#     """
#     candidate = eh.get_candidate(candidate_id)
#     if not candidate:
#         raise ValueError(f"Candidate {candidate_id} not found.")

#     # Handle questions_json
#     questions = candidate.get("questions_json", [])
#     if isinstance(questions, str):
#         try:
#             questions = json.loads(questions)
#         except json.JSONDecodeError:
#             questions = []

#     if not questions:
#         raise ValueError(f"No questions found for candidate {candidate_id}.")

#     # Handle transcript_json
#     transcript = candidate.get("transcript_json") or []
#     if isinstance(transcript, str):
#         try:
#             transcript = json.loads(transcript)
#         except json.JSONDecodeError:
#             transcript = []

#     # Conduct the interview
#     for q in questions:
#         question_text = q["question"]
#         answer_text = answers.get(question_text, "") if answers else ""

#         # Evaluate answer
#         evaluation_raw = gh.evaluate_answer(question_text, answer_text)
#         if isinstance(evaluation_raw, dict):
#             evaluation = evaluation_raw
#         else:
#             try:
#                 evaluation = json.loads(evaluation_raw)
#             except json.JSONDecodeError:
#                 evaluation = {"score": None, "strengths": [], "weaknesses": []}

#         transcript_entry = {
#             "question": question_text,
#             "answer": answer_text,
#             "score": evaluation.get("score"),
#             "strengths": evaluation.get("strengths", []),
#             "weaknesses": evaluation.get("weaknesses", [])
#         }
#         transcript.append(transcript_entry)

#     # Save transcript
#     eh.update_candidate(candidate_id, {
#         "transcript_json": transcript,
#         "status": "completed",
#         "timestamp": datetime.datetime.now().isoformat()
#     })

#     # Generate summary
#     summary = {}
#     if transcript:
#         valid_scores = [t["score"] for t in transcript if t["score"] is not None]
#         avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None
#         all_strengths = [s for t in transcript for s in t["strengths"]]
#         all_weaknesses = [w for t in transcript for w in t["weaknesses"]]

#         summary = {
#             "average_score": avg_score,
#             "strengths": all_strengths,
#             "weaknesses": all_weaknesses
#         }
#         eh.update_candidate(candidate_id, {"summary_json": summary})

#     # ⚡ Instead of returning transcript → just return confirmation
#     return {
#         "message": "✅ Interview completed. Transcript & summary stored securely.",
#         "average_score": summary.get("average_score")
#     }

from utils import excel_handler as eh
from utils import gemini_handler as gh
import datetime
import json

def _safe_load(value, default=None):
    """Return Python object for JSON-like Excel cell values (string, list, NaN)."""
    if default is None:
        default = []
    if value is None:
        return default
    # pandas often returns float('nan') for empty cells
    try:
        import math
        if isinstance(value, float) and math.isnan(value):
            return default
    except Exception:
        pass
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return default
        try:
            return json.loads(value)
        except Exception:
            # maybe a plain string representing a single question
            return default
    if isinstance(value, (list, dict)):
        return value
    # fallback
    return default


def conduct_interview(candidate_id: str, answers: dict = None, keep_history: bool = True):
    """
    Conduct a single interview for candidate_id.
    - Always generates a NEW transcript (fresh) for this interview and stores it as last_interview_json.
    - Optionally appends to interview_history (kept for analytics).
    - Returns only a minimal confirmation dict (no full transcript).
    """
    candidate = eh.get_candidate(candidate_id)
    if not candidate:
        raise ValueError(f"Candidate {candidate_id} not found.")

    # Parse questions safely
    questions_raw = candidate.get("questions_json", [])
    questions = _safe_load(questions_raw, default=[])
    # If questions field is a simple string or single question, try to coerce:
    if not questions and isinstance(questions_raw, str) and questions_raw.strip():
        # Try splitting by newlines as fallback
        lines = [ln.strip() for ln in questions_raw.splitlines() if ln.strip()]
        questions = [{"question": ln} for ln in lines] if lines else []

    # Ensure questions is a list of dicts
    if not isinstance(questions, list):
        questions = []

    # Start a fresh transcript for this interview
    transcript = []

    for q in questions:
        # q might be a dict or plain string
        if isinstance(q, dict):
            question_text = q.get("question") or q.get("text") or str(q)
        else:
            question_text = str(q)

        answer_text = answers.get(question_text, "") if answers else ""

        # Evaluate via Gemini
        evaluation_raw = gh.evaluate_answer(question_text, answer_text)
        # evaluation_raw might be dict already or a string
        if isinstance(evaluation_raw, dict):
            evaluation = evaluation_raw
        else:
            try:
                evaluation = json.loads(evaluation_raw)
            except Exception:
                evaluation = {"score": None, "strengths": [], "weaknesses": []}

        transcript_entry = {
            "question": question_text,
            "answer": answer_text,
            "score": evaluation.get("score"),
            "strengths": evaluation.get("strengths", []),
            "weaknesses": evaluation.get("weaknesses", [])
        }
        transcript.append(transcript_entry)

    # Build summary
    valid_scores = [t["score"] for t in transcript if isinstance(t.get("score"), (int, float))]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None
    all_strengths = [s for t in transcript for s in (t.get("strengths") or [])]
    all_weaknesses = [w for t in transcript for w in (t.get("weaknesses") or [])]

    summary = {
        "average_score": avg_score,
        "strengths": all_strengths,
        "weaknesses": all_weaknesses,
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Save last interview (overwrite previous last_interview_json)
    eh.update_candidate(candidate_id, {
        "last_interview_json": transcript,
        "transcript_json": transcript,  # keep compatibility if other parts use transcript_json
        "summary_json": summary,
        "status": "completed",
        "timestamp": datetime.datetime.now().isoformat()
    })

    # Optionally append to history (keeps record of all interviews)
    if keep_history:
        history_raw = candidate.get("interview_history", "")
        history = _safe_load(history_raw, default=[])
        # push a compact history record
        history_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "summary": summary,
            # don't store full transcript in history to keep file smaller; store small extract
            "num_questions": len(transcript)
        }
        history.append(history_record)
        eh.update_candidate(candidate_id, {"interview_history": history})

    # Return only confirmation to the frontend (no transcript)
    return {
        "message": "✅ Interview completed. Transcript & summary stored securely.",
        # Do NOT leak detailed summary to candidates — only include that backend has stored it.
        # Optionally include a boolean to indicate success
        "ok": True
    }

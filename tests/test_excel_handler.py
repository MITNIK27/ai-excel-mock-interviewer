import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import excel_handler as eh

def run_test():
    candidate_id = "c001"  # make sure this exists in your candidates.xlsx
    
    # Get candidate
    c = eh.get_candidate(candidate_id)
    print("Before update:", c)

    # Update status
    eh.set_status(candidate_id, "in_progress")

    # Append transcript entry
    sample_eval = {
        "question": "What is VLOOKUP?",
        "answer": "It searches for a value in the first column and returns from another column.",
        "score": 8,
        "strengths": ["understands purpose"],
        "weaknesses": ["did not mention exact syntax"]
    }
    eh.append_transcript(candidate_id, sample_eval)

    # Fetch updated candidate
    c2 = eh.get_candidate(candidate_id)
    print("After update:", c2)


if __name__ == "__main__":
    run_test()

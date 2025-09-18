import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import question_generator as qg
from utils import excel_handler as eh
import json

def run_test():
    candidate_id = "c001"

    print("=== Generating Questions for Candidate ===")
    questions = qg.generate_questions_for_candidate(candidate_id, num_questions=3)
    for i, q in enumerate(questions, start=1):
        print(f"{i}. {q['question']}")

    # Verify Excel update
    updated_candidate = eh.get_candidate(candidate_id)
    print("\n=== Stored in Excel (questions_json) ===")
    print(json.dumps(updated_candidate.get("questions_json"), indent=2))

    print("\n=== Transcript JSON Initialized ===")
    print(updated_candidate.get("transcript_json"))


if __name__ == "__main__":
    run_test()

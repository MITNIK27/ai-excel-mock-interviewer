import sys
import os
import json

# Ensure parent folder is in path so utils can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import gemini_handler as gh


def run_test():
    # Step 1: Generate Questions
    print("=== Generating Questions ===")
    questions = gh.generate_questions(
        tech_stack="Excel",
        keywords="VLOOKUP, Pivot Table, Conditional Formatting",
        yoe=2,
        num_questions=3
    )
    print(questions)
    print("\n")

    # Step 2: Evaluate a mock answer
    print("=== Evaluating Answer ===")
    question = "What is VLOOKUP in Excel?"
    candidate_answer = (
        "It is used to search a value in the first column of a table "
        "and return a value from another column."
    )

    evaluation = gh.evaluate_answer(question, candidate_answer)

    # Now `evaluation` is already a dict, so just pretty-print
    if isinstance(evaluation, dict) and evaluation:
        print(json.dumps(evaluation, indent=2))
    else:
        print("⚠️ Evaluation failed or returned empty.")
        print(evaluation)


if __name__ == "__main__":
    run_test()

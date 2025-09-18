import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import interview_flow as iflow
from utils import excel_handler as eh
import json

def run_test():
    candidate_id = "c001"

    # Example answers
    answers = {
        "Explain how you would use VLOOKUP to find a corresponding value in a separate table, and describe a scenario where it might be inefficient and what alternative function you might consider.": 
        "I would use VLOOKUP to find matching values. If efficiency is a problem, INDEX-MATCH could be better.",

        "You have a large dataset with sales figures across different regions and product categories.  Explain how you would use Pivot Tables to analyze the data to identify the top performing region and product combination.": 
        "I would use Pivot Tables, group by region and product, and sort by sum of sales.",

        "Describe a situation where you would use conditional formatting and provide a specific example of how you would apply it to highlight important data in a spreadsheet.": 
        "I would highlight cells above a certain threshold with a color to identify high-performing metrics."
    }

    transcript = iflow.conduct_interview(candidate_id, answers)

    print("\n=== Interview Transcript Stored in Excel ===")
    print(json.dumps(transcript, indent=2))

    candidate = eh.get_candidate(candidate_id)
    print("\n=== Summary JSON ===")
    print(json.dumps(candidate.get("summary_json"), indent=2))
    print("\n=== Candidate Status ===", candidate.get("status"))


if __name__ == "__main__":
    run_test()

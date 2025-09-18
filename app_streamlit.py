# import streamlit as st
# from utils import excel_handler as eh
# from utils import question_generator as qg
# from utils import interview_flow as iflow
# import json

# st.set_page_config(page_title="AI Excel Mock Interviewer", layout="wide")

# st.title("💼 AI-Powered Excel Mock Interviewer")

# # --- Step 1: Select Candidate ---
# candidates_df = eh._load_candidates()
# candidate_list = candidates_df["candidate_id"].tolist()
# selected_candidate_id = st.selectbox("Select Candidate ID", candidate_list)

# if selected_candidate_id:
#     candidate = eh.get_candidate(selected_candidate_id)
#     st.subheader(f"Candidate Info: {candidate['name']} ({candidate['email']})")
#     st.text(f"Tech Stack: {candidate['tech_stack']}")
#     st.text(f"Years of Experience: {candidate['yoe']}")
    
#     # --- Step 2: Generate / Load Questions ---
#     if st.button("Generate Questions"):
#         questions = qg.generate_and_store_questions(selected_candidate_id)
#         st.success("✅ Questions generated and stored in Excel.")
#     else:
#         questions_raw = candidate.get("questions_json")
#         if isinstance(questions_raw, str):
#             questions = json.loads(questions_raw)
#         else:
#             questions = questions_raw or []

#     if questions:
#         st.subheader("Interview Questions")
#         answers = {}
#         for idx, q in enumerate(questions):
#             answers[q["question"]] = st.text_area(f"Q{idx+1}: {q['question']}", height=80)

#         # --- Step 3: Conduct Interview ---
#         if st.button("Submit Answers & Evaluate"):
#             transcript = iflow.conduct_interview(selected_candidate_id, answers)
#             st.success("✅ Interview completed. Transcript & summary updated.")

#             st.subheader("📄 Interview Transcript")
#             for t in transcript:
#                 st.markdown(f"**Question:** {t['question']}")
#                 st.markdown(f"**Answer:** {t['answer']}")
#                 st.markdown(f"**Score:** {t['score']}")
#                 st.markdown(f"**Strengths:** {', '.join(t['strengths'])}")
#                 st.markdown(f"**Weaknesses:** {', '.join(t['weaknesses'])}")
#                 st.markdown("---")

#             # --- Step 4: Summary ---
#             summary_raw = eh.get_candidate(selected_candidate_id).get("summary_json")
#             if isinstance(summary_raw, str):
#                 summary = json.loads(summary_raw)
#             else:
#                 summary = summary_raw or {}

#             st.subheader("📊 Summary")
#             st.text(f"Average Score: {summary.get('average_score')}")
#             st.text(f"Strengths: {', '.join(summary.get('strengths', []))}")
#             st.text(f"Weaknesses: {', '.join(summary.get('weaknesses', []))}")

import streamlit as st
from utils import excel_handler as eh
from utils import question_generator as qg
from utils import interview_flow as iflow
import json
import math

st.set_page_config(page_title="AI Excel Mock Interviewer", layout="wide")
st.title("💼 AI-Powered Excel Mock Interviewer")

def _safe_load_field(val, default=None):
    if default is None:
        default = []
    if val is None:
        return default
    # handle pandas NaN (float)
    if isinstance(val, float):
        try:
            if math.isnan(val):
                return default
        except Exception:
            pass
    if isinstance(val, str):
        if val.strip() == "":
            return default
        try:
            return json.loads(val)
        except Exception:
            # Could be plain text; return default
            return default
    if isinstance(val, (list, dict)):
        return val
    return default

# --- Step 1: Select Candidate ---
candidates_df = eh._load_candidates()
candidate_list = candidates_df["candidate_id"].tolist()
selected_candidate_id = st.selectbox("Select Candidate ID", candidate_list)

if selected_candidate_id:
    candidate = eh.get_candidate(selected_candidate_id)
    st.subheader(f"Candidate Info: {candidate.get('name','-')} ({candidate.get('email','-')})")
    st.text(f"Tech Stack: {candidate.get('tech_stack','-')}")
    st.text(f"Years of Experience: {candidate.get('yoe','-')}")

    # --- Step 2: Generate / Load Questions ---
    if st.button("Generate Questions"):
        qg.generate_and_store_questions(selected_candidate_id)
        # refresh candidate object
        candidate = eh.get_candidate(selected_candidate_id)
        st.success("✅ Questions generated and stored in Excel.")

    questions_raw = candidate.get("questions_json")
    questions = _safe_load_field(questions_raw, default=[])
    # fallback: sometimes stored as newline-separated text
    if not questions and isinstance(questions_raw, str) and questions_raw.strip():
        lines = [ln.strip() for ln in questions_raw.splitlines() if ln.strip()]
        questions = [{"question": ln} for ln in lines]

    if questions:
        st.subheader("Interview Questions")
        answers = {}
        for idx, q in enumerate(questions):
            q_text = q.get("question") if isinstance(q, dict) else str(q)
            answers[q_text] = st.text_area(f"Q{idx+1}: {q_text}", height=80)

        if st.button("Submit Answers & Evaluate"):
            with st.spinner("Evaluating answers... Please wait ⏳"):
                transcript = iflow.conduct_interview(selected_candidate_id, answers)
            st.success("✅ Interview completed. Transcript & summary updated.")
            st.caption("Detailed transcript & summary are stored and accessible to admin only.")
    else:
        st.info("No questions exist for this candidate. Click 'Generate Questions' to create them.")

import streamlit as st
from utils import excel_handler as eh
import json
import pandas as pd
import math


st.set_page_config(page_title="Admin Dashboard - AI Interviewer", layout="wide")
st.title("🛠️ Admin Dashboard - AI Excel Mock Interviewer")

def _safe_load_field(val, default=None):
    if default is None:
        default = []
    if val is None:
        return default
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
            return default
    if isinstance(val, (list, dict)):
        return val
    return default

candidates_df = eh._load_candidates()
# Add filter before building candidate list
filter_status = st.radio("Filter candidates by status", ["All", "Completed", "Pending"])
if filter_status != "All":
    candidates_df = candidates_df[candidates_df["status"] == filter_status.lower()]

if candidates_df.empty:
    st.warning("⚠️ No candidates found.")
else:
    st.subheader("📋 Candidate List")
    st.dataframe(candidates_df[["candidate_id", "name", "email", "status", "timestamp"]])

    candidate_list = candidates_df["candidate_id"].tolist()
    selected_candidate_id = st.selectbox("Select Candidate ID", candidate_list)

    if selected_candidate_id:
        candidate = eh.get_candidate(selected_candidate_id)
        st.subheader(f"Candidate: {candidate.get('name','-')} ({candidate.get('email','-')})")

        # Prefer last_interview_json (latest single interview)
        last_raw = candidate.get("last_interview_json", "") or candidate.get("transcript_json", "")
        last_interview = _safe_load_field(last_raw, default=[])

        if last_interview and isinstance(last_interview, list):
            st.subheader("📄 Last Interview Transcript")
            try:
                transcript_df = pd.DataFrame(last_interview)
                st.dataframe(transcript_df)
                st.download_button(
                    label="📥 Download Transcript (CSV)",
                    data=transcript_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{selected_candidate_id}_last_transcript.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error("Unable to construct transcript table: " + str(e))
        else:
            st.info("No transcript available for the last interview for this candidate.")

        # --- Summary (stored per last interview)
        summary_raw = candidate.get("summary_json", "")
        summary = _safe_load_field(summary_raw, default={})
        if isinstance(summary, dict) and summary:
            st.subheader("📊 Summary (Last Interview)")
            avg = summary.get("average_score")
            st.metric("Average Score", f"{avg:.2f}" if isinstance(avg, (int, float)) else "N/A")
            st.text(f"Strengths: {', '.join(summary.get('strengths', []))}")
            st.text(f"Weaknesses: {', '.join(summary.get('weaknesses', []))}")

            st.download_button(
                label="📥 Download Summary (JSON)",
                data=json.dumps(summary, indent=2),
                file_name=f"{selected_candidate_id}_summary.json",
                mime="application/json"
            )
        else:
            st.info("No summary available for this candidate yet.")

        # Optional: show interview history (compact)
        history_raw = candidate.get("interview_history", "")
        history = _safe_load_field(history_raw, default=[])
        if history:
            st.subheader("🕘 Interview History (compact)")
            st.write(history)
            # maybe offer CSV/JSON download
            st.download_button(
                label="📥 Download Interview History (JSON)",
                data=json.dumps(history, indent=2),
                file_name=f"{selected_candidate_id}_history.json",
                mime="application/json"
            )

# import matplotlib.pyplot as plt

# if summary.get("average_score") is not None:
#     st.subheader("📊 Score Distribution")
#     scores = [t["score"] for t in transcript if t["score"] is not None]
#     fig, ax = plt.subplots()
#     ax.hist(scores, bins=5, edgecolor="black")
#     st.pyplot(fig)

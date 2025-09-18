# Design Document – AI-Powered Excel Mock Interviewer

## 1. Problem Understanding
The company needs to rapidly scale hiring in Finance, Operations, and Data Analytics roles. A key skill is **advanced Excel proficiency**. Current manual interviews:
- Consume senior analysts’ time
- Are inconsistent
- Slow down the hiring pipeline  

An **AI-driven mock interviewer** can automate this process by simulating structured Excel interviews, evaluating answers, and generating reports.

---

## 2. Solution Overview
We built an **AI-Powered Excel Mock Interviewer** with the following features:
- **Structured Interview Flow**: Multi-turn conversation with candidates (intro, questions, summary).
- **AI Answer Evaluation**: Candidate answers are evaluated on correctness, clarity, and depth.
- **State Management**: Each interview session tracks questions, answers, and scores per candidate.
- **Constructive Feedback**: A summary report is generated for admin review.
- **Admin Portal**: HR/admins can log in, filter candidates, and access transcripts, scores, and feedback.

---

## 3. System Design

### Architecture
- **Frontend (Candidate & Admin)**: Streamlit apps (`app_streamlit.py`, `app_admin.py`)
- **Backend**: Python-based logic with session/state management
- **LLM Integration**: Google Gemini API (free-tier key used)
- **Storage**: Local JSON files to persist interviews (simulating a DB in PoC)

### Flow
1. Candidate selects their name → generates Excel interview questions.
2. Candidate answers questions in text fields → answers are evaluated by the AI.
3. Transcript, summary, and score are stored.
4. Admin portal displays latest interview data, with candidate status filters.

---

## 4. Technology Stack
- **Python 3.10+**
- **Streamlit** (interactive web apps)
- **Pandas** (tabular transcript display)
- **Google Gemini API** (for AI-driven Q&A and evaluation)  
  ⚡ *Used free-tier API key. With paid service (higher model variants, dedicated quota), evaluation accuracy, latency, and scalability would improve significantly.*

---

## 5. Key Design Decisions
- **Lightweight Storage**: JSON chosen for PoC instead of a database → easy to run anywhere. Future production version could use PostgreSQL or Firebase.
- **Separation of Roles**: Candidate and Admin UIs split into separate apps for clarity.
- **Fail-Safe Defaults**: If no questions/answers exist, user is prompted clearly.
- **Cold Start Problem**: Interview questions are dynamically generated via LLM. Over time, logs can be curated into a dataset → bootstrap fine-tuned models.

---

## 6. Limitations & Improvements
- **Current PoC**:
  - Limited to text-based Excel Q&A (no live spreadsheet tasks yet).
  - Uses free LLM, so responses may vary.
  - Storage is local and single-machine.
- **Future Enhancements**:
  - Paid LLM services → faster, more reliable evaluations.
  - Cloud DB (Postgres/Firebase) for scalable candidate management.
  - Integration with real Excel sheets (Google Sheets API, OfficeJS).
  - Dashboard with analytics for recruiters.

---

## 7. Success Metrics
- Reduce interview time per candidate by 80%
- Improve evaluation consistency (LLM scoring vs. multiple human evaluators)
- Scale to 100+ interviews/day without analyst involvement

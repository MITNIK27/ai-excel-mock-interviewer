# AI-Powered Excel Mock Interviewer

An AI-driven system to automate Excel skill interviews.  
It simulates real interviews, evaluates candidate answers, and generates feedback reports.  
Includes a **candidate-facing app** and an **admin portal**.

---

## 🚀 Features
- Multi-turn structured Excel interview
- AI-based answer evaluation (using Google Gemini API – free-tier)
- Automatic transcript + summary generation
- Admin dashboard:
  - View candidate transcripts
  - Filter by interview status (completed/pending)
  - Access feedback reports

---

## 🌐 Live Deployment Links
- **Candidate App:** [Open Candidate Interviewer](https://ai-excel-mock-interviewer-candidate.streamlit.app/)
- **Admin Portal:** [Open Admin Dashboard](https://ai-excel-mock-interview-handler.streamlit.app/)

> Note: As a Proof-of-Concept, both apps are currently accessible directly without authentication. For production-ready usage, a secure login/authentication layer will be integrated to ensure controlled access.

---

## 📂 Project Structure
.
├── app_streamlit.py # Candidate-facing app
├── app_admin.py # Admin portal
├── interview_flow.py # Core logic (interview, evaluation, storage)
├── data/ # Stores candidate data (JSON files)
├── docs/
│ └── design_document.md
├── requirements.txt
├── README.md
└── .gitignore

---

## 🛠️ Tech Stack
- Python 3.10+
- Streamlit
- Pandas
- Google Gemini API (free-tier key used)
- Local JSON storage

---

## 📦 Installation & Running Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/excel-mock-interviewer.git
   cd excel-mock-interviewer

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # (Linux/Mac)
    venv\Scripts\activate      # (Windows)

3. Install dependencies:
    ```bash
    pip install -r requirements.txt


4. Set your Gemini API key (free-tier):
    ```bash
    export GEMINI_API_KEY="your_api_key_here"   # Linux/Mac
    set GEMINI_API_KEY="your_api_key_here"      # Windows

5. Run the candidate app:
    ```bash
    streamlit run app_streamlit.py


6. Run the admin app:
    ```bash
    streamlit run app_admin.py

---

## 📊 Sample Flow

- Candidate selects their name → answers Excel interview questions
- AI evaluates responses and stores transcript + summary
- Admin logs into portal → views candidate’s latest interview report

---

## ⚡ Notes

- Free-tier LLM used (Gemini).
- In production, paid/enterprise APIs could improve:
    - Faster response time
    - Higher accuracy
    - Robust scaling for 100+ candidates
- Storage is local JSON → can be swapped with cloud DB in production.

--- 

## ✅ Deliverables

- Design Document (docs/design_document.md)
- Candidate Interviewer App (app_streamlit.py)
- Admin Portal (app_admin.py)
- Deployment-ready repo
- Sample transcripts stored locally

---

## 👩‍💻 Author

Designed and Built by Paarth Sahni (Founding AI Product Engineer candidate).

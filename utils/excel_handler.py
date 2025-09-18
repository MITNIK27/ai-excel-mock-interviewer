import pandas as pd
from openpyxl import load_workbook
from pathlib import Path
import datetime
import json
import shutil

# Path constants
CANDIDATES_FILE = Path(__file__).resolve().parent.parent / "candidates.xlsx"
BACKUP_DIR = Path(__file__).resolve().parent.parent / "data" / "backups"

# Ensure backup dir exists
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def _backup_excel():
    """Create a timestamped backup of the Excel file."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"candidates_backup_{ts}.xlsx"
    shutil.copy(CANDIDATES_FILE, backup_path)
    return backup_path


def _load_candidates():
    """Load Excel into pandas DataFrame with safe dtypes (avoid float warnings)."""
    df = pd.read_excel(CANDIDATES_FILE, engine="openpyxl", dtype=str)

    # Ensure essential columns exist
    for col in ["transcript_json", "summary_json", "status", "timestamp"]:
        if col not in df.columns:
            df[col] = ""  # initialize empty column

    return df


def _save_candidates(df):
    """Write DataFrame back to Excel (with backup)."""
    _backup_excel()
    df.to_excel(CANDIDATES_FILE, index=False, engine="openpyxl")


def get_candidate(candidate_id: str):
    """Return candidate row as dict (or None)."""
    df = _load_candidates()
    row = df[df["candidate_id"] == candidate_id]
    if row.empty:
        return None
    return row.iloc[0].to_dict()


def update_candidate(candidate_id: str, updates: dict):
    """
    Update candidate row with given dict {col: value}.
    Handles JSON serialization for dict/list automatically.
    Auto-creates new columns if missing.
    """
    df = _load_candidates()
    idx = df.index[df["candidate_id"] == candidate_id]

    if len(idx) == 0:
        raise ValueError(f"Candidate {candidate_id} not found.")

    for col, val in updates.items():
        # Create column if missing
        if col not in df.columns:
            df[col] = ""

        # Serialize JSON if dict or list
        if isinstance(val, (dict, list)):
            val = json.dumps(val, ensure_ascii=False)

        df.at[idx[0], col] = val

    _save_candidates(df)
    return True


def set_status(candidate_id: str, status: str):
    """Convenience: update candidate status."""
    return update_candidate(candidate_id, {
        "status": status,
        "timestamp": datetime.datetime.now().isoformat()
    })


def append_transcript(candidate_id: str, new_entry: dict):
    """Append one QA evaluation to transcript_json column."""
    candidate = get_candidate(candidate_id)
    transcript_raw = candidate.get("transcript_json")

    transcript = []
    if transcript_raw and isinstance(transcript_raw, str):
        try:
            transcript = json.loads(transcript_raw)
        except json.JSONDecodeError:
            transcript = []

    transcript.append(new_entry)
    return update_candidate(candidate_id, {"transcript_json": transcript})

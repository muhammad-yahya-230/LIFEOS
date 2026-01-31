from config import GYM_LOGS_FILE
from src.data.crud import save_record, get_all_records
from typing import List, Dict, Optional
import pandas as pd

def log_set(date: str, exercise: str, weight: float, reps: int, rpe: int, notes: str = "") -> None:
    """Logs a single set."""
    data = {
        "date": date,
        "exercise_name": exercise,
        "weight_kg": weight,
        "reps": reps,
        "rpe": rpe,
        "notes": notes,
        # "set_number" handling could be improved by checking prev logs for same day/exercise
        # but for simplicity, we treat every log as a sequential entry in DB
    }
    save_record(GYM_LOGS_FILE, data)

def get_exercise_history(exercise_name: str) -> pd.DataFrame:
    """Returns history for a specific exercise as DataFrame."""
    records = get_all_records(GYM_LOGS_FILE)
    if not records:
        return pd.DataFrame()
    
    df = pd.DataFrame(records)
    # Filter
    df = df[df["exercise_name"] == exercise_name]
    if not df.empty:
        df = df.sort_values("date", ascending=False)
    return df

def get_last_session_stats(exercise_name: str) -> Optional[Dict]:
    """Returns max weight/reps from the LAST session for this exercise."""
    df = get_exercise_history(exercise_name)
    if df.empty:
        return None
    
    # Get most recent date
    last_date = df.iloc[0]["date"]
    last_session = df[df["date"] == last_date]
    
    # Find max weight
    max_weight_row = last_session.loc[last_session["weight_kg"].idxmax()]
    
    return {
        "date": last_date,
        "weight": max_weight_row["weight_kg"],
        "reps": max_weight_row["reps"]
    }

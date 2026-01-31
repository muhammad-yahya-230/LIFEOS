from config import SYSTEMS_REVIEWS_FILE, SYSTEMS_OKRS_FILE, DAILY_EXECUTION_FILE, GYM_LOGS_FILE
from src.data.crud import save_record, get_all_records, update_record
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

def get_weekly_review_data() -> Dict:
    """Aggregates data from the last 7 days for review context."""
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Execution Stats
    exec_recs = get_all_records(DAILY_EXECUTION_FILE)
    study_hours = 0
    gym_count = 0
    avg_mood = 0
    mood_count = 0
    
    if exec_recs:
        df = pd.DataFrame(exec_recs)
        df["date"] = pd.to_datetime(df["date"])
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        week_df = df[mask]
        
        if not week_df.empty:
            study_hours = week_df["study_hours_actual"].sum()
            # gym_done stored as bool in csv, need to ensure correct parsing
            # Assuming 'True'/'False' strings or booleans
            gym_count = week_df["gym_done"].apply(lambda x: 1 if str(x).lower() == 'true' else 0).sum()
            avg_mood = week_df["mood_score"].mean()
            
    return {
        "study_hours": round(study_hours, 1),
        "gym_count": int(gym_count),
        "avg_mood": round(avg_mood, 1)
    }

def save_review(week_start: str, wins: str, challenges: str, focus: str, score: int) -> None:
    """Saves a weekly review."""
    data = {
        "week_start": week_start,
        "wins": wins,
        "challenges": challenges,
        "focus": focus,
        "score": score,
        "reviewed_at": datetime.now().isoformat()
    }
    save_record(SYSTEMS_REVIEWS_FILE, data)

def save_okr(quarter: str, objective: str, key_results: str, status: str) -> None:
    """Saves an Objective and Key Result."""
    data = {
        "quarter": quarter,
        "objective": objective,
        "key_results": key_results,
        "status": status # "On Track", "At Risk", "Completed"
    }
    save_record(SYSTEMS_OKRS_FILE, data)

def get_okrs(quarter: str = "") -> pd.DataFrame:
    """Retrieves OKRs."""
    records = get_all_records(SYSTEMS_OKRS_FILE)
    if not records:
        return pd.DataFrame()
        
    df = pd.DataFrame(records)
    if quarter:
        df = df[df["quarter"] == quarter]
    return df

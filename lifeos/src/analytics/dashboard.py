from config import DAILY_EXECUTION_FILE
from src.data.crud import get_all_records
import pandas as pd

def get_dashboard_metrics():
    """Aggregates key metrics for the dashboard."""
    records = get_all_records(DAILY_EXECUTION_FILE)
    if not records:
        return {
            "avg_score": 0,
            "study_total": 0,
            "gym_sessions": 0,
            "streak": 0
        }
    
    df = pd.DataFrame(records)
    
    # Simple aggregations
    study_total = df["study_hours_actual"].fillna(0).sum()
    gym_sessions = df["gym_done"].apply(lambda x: 1 if str(x).lower() == 'true' else 0).sum()
    
    # Streak logic (simplified)
    # Sort by date, check consecutive
    # Placeholder
    
    return {
        "avg_score": 0, # Need to store score or calc on fly
        "study_total": round(study_total, 1),
        "gym_sessions": gym_sessions
    }

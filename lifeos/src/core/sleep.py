from config import DAILY_EXECUTION_FILE
from src.data.crud import get_all_records
from datetime import datetime
import pandas as pd

IDEAL_SLEEP_HOURS = 8.0

def calculate_sleep_debt_days(days=7) -> float:
    """Calculates accumulated sleep debt over the last N days."""
    records = get_all_records(DAILY_EXECUTION_FILE)
    if not records:
        return 0.0
        
    df = pd.DataFrame(records)
    
    # Needs actual logic to parse HH:MM sleep/wake to duration.
    # For now, let's assume we store duration or can calculate it.
    # The current model stores 'sleep_time_actual' and 'wake_time_actual'.
    # I need to implement a helper to calc duration.
    
    debt = 0.0
    # Sort by date desc
    df = df.sort_values("date", ascending=False).head(days)
    
    for _, row in df.iterrows():
        s_time = row.get("sleep_time_actual")
        w_time = row.get("wake_time_actual")
        
        if s_time and w_time:
            try:
                # Simple crossing midnight check
                s_dt = datetime.strptime(s_time, "%H:%M")
                w_dt = datetime.strptime(w_time, "%H:%M")
                
                if w_dt < s_dt:
                    # Crossed midnight (e.g. 23:00 to 07:00)
                    # Add 24h to wake time for calc
                    duration = (w_dt.hour + 24 - s_dt.hour) + (w_dt.minute - s_dt.minute)/60
                else:
                    duration = (w_dt.hour - s_dt.hour) + (w_dt.minute - s_dt.minute)/60
                
                diff = IDEAL_SLEEP_HOURS - duration
                debt += diff
            except:
                pass
                
    return round(debt, 1)

from config import DAILY_EXECUTION_FILE
from src.data.crud import get_all_records
import pandas as pd
from typing import List, Dict

def get_insights() -> List[Dict]:
    """Analyzes data to find correlations."""
    records = get_all_records(DAILY_EXECUTION_FILE)
    if not records:
         return []
         
    df = pd.DataFrame(records)
    
    # Needs columns: study_hours_actual, mood_score, gym_done, morning_routine_done
    # We also need Sleep data (from daily plan or logging). 
    # Current execution.py doesn't strictly log sleep duration actual (it's in plan). 
    # For now, let's correlate Mood vs Study vs Gym.
    
    insights = []
    
    if "mood_score" in df.columns and "study_hours_actual" in df.columns:
        df["mood_score"] = pd.to_numeric(df["mood_score"], errors='coerce').fillna(5)
        df["study_hours_actual"] = pd.to_numeric(df["study_hours_actual"], errors='coerce').fillna(0)
        
        # 1. Does Mood affect Study?
        high_mood = df[df["mood_score"] >= 7]["study_hours_actual"].mean()
        low_mood = df[df["mood_score"] < 7]["study_hours_actual"].mean()
        
        diff = high_mood - low_mood
        if abs(diff) > 0.5:
            impact = "positive" if diff > 0 else "negative"
            insights.append({
                "question": "Does Mood affect Study?",
                "answer": f"Yes. You study {round(abs(diff), 1)}h more when Mood is high (7+).",
                "impact": impact
            })
        else:
            insights.append({
                "question": "Does Mood affect Study?",
                "answer": "Not significantly.",
                "impact": "neutral"
            })

    # 2. Does Gym affect Mood?
    if "gym_done" in df.columns and "mood_score" in df.columns:
        # gym_done might be string 'True'
        df["gym_bool"] = df["gym_done"].apply(lambda x: str(x).lower() == 'true')
        
        gym_mood = df[df["gym_bool"] == True]["mood_score"].mean()
        no_gym_mood = df[df["gym_bool"] == False]["mood_score"].mean()
        
        diff = gym_mood - no_gym_mood
        if abs(diff) > 0.5:
             insights.append({
                "question": "Does Gym improve Mood?",
                "answer": f"Yes. Your mood is {round(diff, 1)} points higher on Gym days.",
                "impact": "positive" if diff > 0 else "negative"
            })
    
    return insights

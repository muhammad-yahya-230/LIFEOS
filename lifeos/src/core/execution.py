from config import DAILY_EXECUTION_FILE, DAILY_PLAN_FILE
from src.data.crud import save_record, get_record, update_record, get_all_records
from typing import Optional, Dict

def log_execution(date: str, execution_data: Dict) -> None:
    """Logs or updates daily execution."""
    existing = get_record(DAILY_EXECUTION_FILE, "date", date)
    execution_data["date"] = date
    
    if existing:
        update_record(DAILY_EXECUTION_FILE, existing["id"], execution_data)
    else:
        save_record(DAILY_EXECUTION_FILE, execution_data)

def get_execution(date: str) -> Optional[Dict]:
    return get_record(DAILY_EXECUTION_FILE, "date", date)

def calculate_day_score(date: str) -> float:
    """Calculates a score (0-100) based on plan vs execution."""
    plan = get_record(DAILY_PLAN_FILE, "date", date)
    execution = get_record(DAILY_EXECUTION_FILE, "date", date)
    
    if not plan or not execution:
        return 0.0
    
    score = 0
    total_points = 0
    
    # 1. Study Hours (40%)
    planned_study = float(plan.get("study_hours_planned", 0))
    if planned_study > 0:
        actual_study = float(execution.get("study_hours_actual", 0))
        study_score = min(actual_study / planned_study, 1.2) * 40 # Cap at 120%
        score += study_score
        total_points += 40
    
    # 2. Gym (30%)
    if str(plan.get("gym_planned")).lower() == "true":
        gym_done = str(execution.get("gym_done", "false")).lower() == "true"
        if gym_done:
            score += 30
        total_points += 30
    
    # 3. Morning Routine (15%)
    if str(plan.get("morning_routine_planned")).lower() == "true":
        routine_done = str(execution.get("morning_routine_done", "false")).lower() == "true"
        if routine_done:
            score += 15
        total_points += 15
        
    # Normalize if total_points < 100 (e.g. rest day)
    # But for now, let's keep it simple: Base score on adherence to *active* plans.
    if total_points == 0:
        return 100.0 # Nothing planned, perfect day?
        
    return round(score, 1)

def get_weekly_execution_stats():
    # Placeholder for broader analytics
    records = get_all_records(DAILY_EXECUTION_FILE)
    # Process...
    return records

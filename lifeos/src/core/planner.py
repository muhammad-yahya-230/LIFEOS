from config import DAILY_PLAN_FILE
from src.data.crud import save_record, get_record, update_record
from ..data.models import DailyPlan
from typing import Optional, Dict

def create_or_update_plan(date: str, plan_data: Dict) -> None:
    """Creates or updates a daily plan."""
    existing = get_record(DAILY_PLAN_FILE, "date", date)
    
    # Ensure date is in data
    plan_data["date"] = date
    
    if existing:
        update_record(DAILY_PLAN_FILE, existing["id"], plan_data)
    else:
        # Validate with model (optional, but good practice)
        # model = DailyPlan(**plan_data) # Might fail if extra keys
        save_record(DAILY_PLAN_FILE, plan_data)

def get_daily_plan(date: str) -> Optional[Dict]:
    """Retrieves the plan for a specific date."""
    return get_record(DAILY_PLAN_FILE, "date", date)

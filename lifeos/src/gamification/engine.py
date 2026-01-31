from config import DAILY_EXECUTION_FILE, GYM_LOGS_FILE, KNOWLEDGE_NOTES_FILE, FINANCE_TRANSACTIONS_FILE
from src.data.crud import get_all_records
import pandas as pd
from typing import Dict

def calculate_rpg_stats() -> Dict:
    """Calculates player stats (XP, Level, Attributes) based on all data."""
    
    # 1. Fetch Data
    exec_recs = get_all_records(DAILY_EXECUTION_FILE)
    gym_recs = get_all_records(GYM_LOGS_FILE)
    notes_recs = get_all_records(KNOWLEDGE_NOTES_FILE)
    finance_recs = get_all_records(FINANCE_TRANSACTIONS_FILE)
    
    # 2. Calculate XP Sources
    # Study XP: 100 XP per hour
    study_hours = sum([float(r.get("study_hours_actual", 0)) for r in exec_recs]) 
    study_xp = int(study_hours * 100)
    
    # Gym XP: 200 XP per set logged (Simple proxy for effort)
    # Better: 50 XP per set
    gym_sets = len(gym_recs)
    gym_xp = gym_sets * 50
    
    # Knowledge XP: 50 XP per note
    note_xp = len(notes_recs) * 50
    
    # Discipline XP: Day Score total
    # If day score is stored, sum it? Or calculate. 
    # Let's assume day score isn't stored historically in simple format, so use count of gym/routine done
    routine_count = sum([1 for r in exec_recs if str(r.get("morning_routine_done")).lower() == 'true'])
    discipline_xp = routine_count * 150
    
    # 3. Total
    total_xp = study_xp + gym_xp + note_xp + discipline_xp
    
    # 4. Level Config
    # Level 1: 0-1000
    # Level 2: 1000-2500
    # Formula: Level = (XP / 1000) + 1 (Linear for simplicity)
    level = int(total_xp / 1000) + 1
    next_level_xp = level * 1000
    current_level_xp_start = (level - 1) * 1000
    xp_in_level = total_xp - current_level_xp_start
    xp_needed = 1000 # Constant 1000 xp per level
    progress = min(xp_in_level / xp_needed, 1.0)
    
    return {
        "level": level,
        "total_xp": total_xp,
        "xp_progress": progress,
        "attributes": {
            "STR": gym_sets // 10,  # 1 STR per 10 sets
            "INT": int(study_hours) // 5, # 1 INT per 5 hours
            "WIS": len(notes_recs) // 2, # 1 WIS per 2 notes
            "DIS": routine_count # 1 DIS per routine day
        }
    }

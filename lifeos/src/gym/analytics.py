from .workouts import get_last_session_stats, get_exercise_history
import pandas as pd

def check_progressive_overload(exercise_name: str, current_weight: float, current_reps: int) -> str:
    """Checks if current set beats the last session's best."""
    last = get_last_session_stats(exercise_name)
    if not last:
        return "New Exercise! 💪"
    
    prev_weight = float(last["weight"])
    prev_reps = int(last["reps"])
    
    if current_weight > prev_weight:
        return "🔥 Weight PR!"
    elif current_weight == prev_weight and current_reps > prev_reps:
        return "🔥 Rep PR!"
    elif current_weight == prev_weight and current_reps == prev_reps:
        return "Maintenance"
    else:
        return "" # Lower performance (deload or fatigue)

def calculate_weekly_volume() -> pd.DataFrame:
    """Returns volume (weight * reps) per muscle group per week."""
    # This requires joining logs with library to get muscle group
    # For now, minimal implementation using just exercise logs
    # We would need to load library and map names
    return pd.DataFrame() 

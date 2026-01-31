from dataclasses import dataclass, asdict
from typing import Optional, List
from datetime import datetime

@dataclass
class DailyPlan:
    date: str
    morning_routine_planned: bool = False
    study_hours_planned: float = 0.0
    gym_planned: bool = False
    sleep_time_planned: str = "23:00"
    wake_time_planned: str = "07:00"
    priorities: str = "" # JSON or comma separated
    
    def to_dict(self):
        return asdict(self)

@dataclass
class DailyExecution:
    date: str
    morning_routine_done: bool = False
    study_hours_actual: float = 0.0
    gym_done: bool = False
    sleep_time_actual: str = ""
    wake_time_actual: str = ""
    mood_score: int = 5
    notes: str = ""
    
    def to_dict(self):
        return asdict(self)

@dataclass
class GymLog:
    date: str
    exercise_name: str
    set_number: int
    reps: int
    weight_kg: float
    rpe: int = 0
    notes: str = ""

    def to_dict(self):
        return asdict(self)

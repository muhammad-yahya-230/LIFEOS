from config import EXERCISES_FILE
from src.data.crud import get_all_records, save_record
from typing import List, Dict

DEFAULT_EXERCISES = [
    {"name": "Squat", "muscle": "Legs", "type": "Compound"},
    {"name": "Bench Press", "muscle": "Chest", "type": "Compound"},
    {"name": "Deadlift", "muscle": "Back", "type": "Compound"},
    {"name": "Overhead Press", "muscle": "Shoulders", "type": "Compound"},
    {"name": "Pull Up", "muscle": "Back", "type": "Compound"},
    {"name": "Dumbbell Row", "muscle": "Back", "type": "Isolation"},
    {"name": "Lateral Raise", "muscle": "Shoulders", "type": "Isolation"},
    {"name": "Bicep Curl", "muscle": "Arms", "type": "Isolation"},
    {"name": "Tricep Extension", "muscle": "Arms", "type": "Isolation"},
]

def get_exercises() -> List[Dict]:
    """Returns all available exercises, initializing defaults if empty."""
    exercises = get_all_records(EXERCISES_FILE)
    if not exercises:
        for ex in DEFAULT_EXERCISES:
            save_record(EXERCISES_FILE, ex)
        return DEFAULT_EXERCISES
    return exercises

def add_exercise(name: str, muscle: str, type: str) -> None:
    """Adds a new exercise to the library."""
    data = {"name": name, "muscle": muscle, "type": type}
    save_record(EXERCISES_FILE, data)

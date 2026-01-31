import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Data Files
DAILY_PLAN_FILE = DATA_DIR / "daily_plan.csv"
DAILY_EXECUTION_FILE = DATA_DIR / "daily_execution.csv"
GYM_LOGS_FILE = DATA_DIR / "gym_logs.csv"
HABITS_FILE = DATA_DIR / "habits.csv"
HABIT_LOGS_FILE = DATA_DIR / "habit_logs.csv"
STUDY_SESSIONS_FILE = DATA_DIR / "study_sessions.csv"
EXERCISES_FILE = DATA_DIR / "exercises.csv"

# Finance Files
FINANCE_TRANSACTIONS_FILE = DATA_DIR / "finance_transactions.csv"
FINANCE_BUDGETS_FILE = DATA_DIR / "finance_budgets.csv"
FINANCE_CATEGORIES_FILE = DATA_DIR / "finance_categories.csv"

# Knowledge Files
KNOWLEDGE_NOTES_FILE = DATA_DIR / "knowledge_notes.csv"

# Systems Files
SYSTEMS_REVIEWS_FILE = DATA_DIR / "sys_reviews.csv"
SYSTEMS_OKRS_FILE = DATA_DIR / "sys_okrs.csv"

# App Settings
APP_TITLE = "LifeOS"
THEME_COLOR = "#FF4B4B"

from config import FINANCE_TRANSACTIONS_FILE, FINANCE_BUDGETS_FILE, FINANCE_CATEGORIES_FILE
from src.data.crud import save_record, get_all_records, update_record
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime

DEFAULT_CATEGORIES = ["Food", "Transport", "Rent", "Fun", "Subscriptions", "Other", "Salary", "Freelance"]

def get_categories() -> List[str]:
    """Retrieves finance categories, defaulting if empty."""
    records = get_all_records(FINANCE_CATEGORIES_FILE)
    if not records:
        # Initialize defaults if file doesn't exist
        for cat in DEFAULT_CATEGORIES:
            save_record(FINANCE_CATEGORIES_FILE, {"name": cat})
        return sorted(DEFAULT_CATEGORIES)
    
    return sorted([r["name"] for r in records])

def add_category(name: str) -> None:
    """Adds a new category if it doesn't exist."""
    current = get_categories()
    if name not in current:
        save_record(FINANCE_CATEGORIES_FILE, {"name": name})

def delete_category(name: str) -> None:
    """Deletes a category (Note: does not retroactively update transactions)."""
    # This is a bit tricky with CSV only crud. Ideally we'd rewrite the file.
    # For now, let's just stick to adding. Deletion is risky without rewrite.
    pass

def add_transaction(date: str, amount: float, type: str, category: str, description: str) -> None:
    """Logs a financial transaction."""
    data = {
        "date": date,
        "amount": amount,
        "type": type, # 'Income' or 'Expense'
        "category": category,
        "description": description
    }
    save_record(FINANCE_TRANSACTIONS_FILE, data)

def get_monthly_summary(month_str: str) -> Dict:
    """Calculates income, expense, and savings for a given month (YYYY-MM)."""
    records = get_all_records(FINANCE_TRANSACTIONS_FILE)
    if not records:
        return {"income": 0.0, "expense": 0.0, "savings": 0.0}
        
    df = pd.DataFrame(records)
    # Filter by month
    df["date"] = pd.to_datetime(df["date"])
    mask = df["date"].dt.strftime("%Y-%m") == month_str
    month_df = df[mask]
    
    if month_df.empty:
        return {"income": 0.0, "expense": 0.0, "savings": 0.0}
        
    income = month_df[month_df["type"] == "Income"]["amount"].sum()
    expense = month_df[month_df["type"] == "Expense"]["amount"].sum()
    
    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "savings": round(income - expense, 2)
    }

def get_category_breakdown(month_str: str) -> pd.DataFrame:
    """Returns expense breakdown by category."""
    records = get_all_records(FINANCE_TRANSACTIONS_FILE)
    if not records:
        return pd.DataFrame()
        
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    mask = (df["date"].dt.strftime("%Y-%m") == month_str) & (df["type"] == "Expense")
    month_df = df[mask]
    
    if month_df.empty:
        return pd.DataFrame()
    
    return month_df.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)

def set_budget(category: str, amount: float) -> None:
    """Sets a monthly budget for a category."""
    existing = get_all_records(FINANCE_BUDGETS_FILE)
    
    # Simple overwrite logic since we don't have IDs for budgets yet easily accessible, 
    # or we just append and take latest.
    # Cleaner: Read, update df, save.
    
    data = {"category": category, "monthly_limit": amount}
    
    # We can use update_record if we knew ID, but let's just use a simple overwrite for now
    # or better: check if exists.
    
    df = pd.DataFrame(existing)
    if not df.empty and "category" in df.columns:
        if category in df["category"].values:
            # Update
            idx = df[df["category"] == category].index[0]
            df.at[idx, "monthly_limit"] = amount
            df.at[idx, "updated_at"] = datetime.now().isoformat()
            df.to_csv(FINANCE_BUDGETS_FILE, index=False)
            return

    save_record(FINANCE_BUDGETS_FILE, data)

def get_budget_status(month_str: str) -> pd.DataFrame:
    """Compares actual spending vs budget for the month."""
    # Get actuals
    breakdown = get_category_breakdown(month_str)
    if breakdown.empty:
        actuals = {}
    else:
        actuals = dict(zip(breakdown["category"], breakdown["amount"]))
        
    # Get budgets
    budgets = get_all_records(FINANCE_BUDGETS_FILE)
    if not budgets:
        return pd.DataFrame() # No budgets set
        
    rows = []
    for b in budgets:
        cat = b["category"]
        limit = float(b["monthly_limit"])
        spent = actuals.get(cat, 0.0)
        remaining = limit - spent
        rows.append({
            "category": cat,
            "limit": limit,
            "spent": spent,
            "remaining": remaining,
            "percent": min(spent/limit, 1.0) if limit > 0 else 0
        })
        
    return pd.DataFrame(rows)

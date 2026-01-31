import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Optional, Union, Any
import uuid
from datetime import datetime

def flatten_path(path_obj_or_str):
    return str(path_obj_or_str)

def read_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """Reads a CSV file into a DataFrame. Returns empty DF if file doesn't exist."""
    file_path = flatten_path(file_path)
    if not os.path.exists(file_path):
        return pd.DataFrame()
    try:
        return pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def save_record(file_path: Union[str, Path], data: Dict) -> None:
    """Appends a single record to a CSV file."""
    file_path = flatten_path(file_path)
    
    # Add metadata
    if "id" not in data:
        data["id"] = str(uuid.uuid4())
    if "created_at" not in data:
        data["created_at"] = datetime.now().isoformat()
    data["updated_at"] = datetime.now().isoformat()
    
    df = read_csv(file_path)
    new_record = pd.DataFrame([data])
    
    if df.empty:
        df = new_record
    else:
        df = pd.concat([df, new_record], ignore_index=True)
        
    df.to_csv(file_path, index=False)

def update_record(file_path: Union[str, Path], record_id: str, updates: Dict) -> bool:
    """Updates a record by ID."""
    file_path = flatten_path(file_path)
    df = read_csv(file_path)
    
    if df.empty or "id" not in df.columns:
        return False
        
    if record_id not in df["id"].values:
        return False
        
    idx = df[df["id"] == record_id].index[0]
    
    for key, value in updates.items():
        if key in df.columns: # Only update existing columns to avoid schema drift for now, or allow?
             # For flexibility, we might want to allow new columns, but for now strict.
             # Actually, let's allow updating any key, but pandas handles it.
             # If column doesn't exist, pandas creates it.
             pass
        df.at[idx, key] = value
        
    df.at[idx, "updated_at"] = datetime.now().isoformat()
    df.to_csv(file_path, index=False)
    return True

def get_record(file_path: Union[str, Path], column: str, value: Any) -> Optional[Dict]:
    """Retrieves a single record where column matches value."""
    file_path = flatten_path(file_path)
    df = read_csv(file_path)
    if df.empty or column not in df.columns:
        return None
    
    # Ensure types match if possible, or string compare
    filtered = df[df[column].astype(str) == str(value)]
    if filtered.empty:
        return None
    
    return filtered.iloc[0].to_dict()

def get_all_records(file_path: Union[str, Path]) -> List[Dict]:
    """Returns all records as a list of dictionaries."""
    df = read_csv(file_path)
    return df.to_dict(orient="records")

from config import KNOWLEDGE_NOTES_FILE
from src.data.crud import save_record, get_all_records, update_record
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime

def add_note(title: str, content: str, tags: str) -> None:
    """Creates a new note."""
    data = {
        "title": title,
        "content": content,
        "tags": tags.lower(), # Store lowercase for search
        "created_at": datetime.now().isoformat(),
        "review_date": datetime.now().isoformat()
    }
    save_record(KNOWLEDGE_NOTES_FILE, data)

def get_notes(search_query: str = "") -> List[Dict]:
    """Retrieves notes, optionally filtered by search."""
    records = get_all_records(KNOWLEDGE_NOTES_FILE)
    if not records:
        return []
    
    if not search_query:
        # Sort by created desc
        return sorted(records, key=lambda x: x.get("created_at", ""), reverse=True)
    
    query = search_query.lower()
    filtered = []
    for r in records:
        if (query in str(r.get("title", "")).lower() or 
            query in str(r.get("tags", "")).lower() or
            query in str(r.get("content", "")).lower()):
            filtered.append(r)
            
    return sorted(filtered, key=lambda x: x.get("created_at", ""), reverse=True)

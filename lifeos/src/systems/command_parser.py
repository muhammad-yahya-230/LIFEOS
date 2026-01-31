from datetime import datetime
from src.finance.manager import add_transaction
from src.gym.workouts import log_set
from src.knowledge.notes import add_note
from src.core.planner import create_or_update_plan, get_daily_plan

def parse_and_execute(command: str) -> str:
    """Parses a command string and executes the corresponding action."""
    parts = command.strip().split(" ")
    if not parts:
        return "Empty command."
        
    cmd = parts[0].lower()
    
    # Quick Finance: "20 lunch" -> $20 for Food (default cat logic needed needed or explicit)
    # Better: "$ 20 lunch"
    if cmd == "$" or cmd.isdigit():
        # Finance Mode
        # Case 1: "$ 20 lunch"
        # Case 2: "20" (Just amount, ask cat? No, CLI should be fast. Default to 'Other' or try to guess)
        
        amount = 0.0
        desc = "Quick Log"
        cat = "Other"
        
        if cmd == "$":
            if len(parts) > 1:
                try:
                    amount = float(parts[1])
                except:
                    return "Invalid amount."
                if len(parts) > 2:
                    desc_check = parts[2].lower()
                    # Simple heuristic for category mapping
                    if desc_check in ["food", "lunch", "dinner", "burger", "coffee"]: cat = "Food"
                    elif desc_check in ["uber", "taxi", "bus", "gas"]: cat = "Transport"
                    elif desc_check in ["gym", "protein"]: cat = "Health" # Need to ensure cat exists
                    
                    desc = " ".join(parts[2:])
        elif cmd.isdigit():
             amount = float(cmd)
             if len(parts) > 1:
                 desc = " ".join(parts[1:])
                 desc_check = parts[1].lower()
                 if desc_check in ["food", "lunch", "dinner"]: cat = "Food"
                 
        add_transaction(datetime.now().strftime("%Y-%m-%d"), amount, "Expense", cat, desc)
        return f"💸 Logged ${amount} to {cat} ({desc})"

    # Gym Mode: "gym squat 100 5"
    elif cmd == "gym":
        if len(parts) < 4:
            return "Usage: gym [exercise] [weight] [reps] (e.g. gym squat 100 5)"
        
        ex_name = parts[1] # fuzzy match needed? For now exact or simple
        try:
            weight = float(parts[2])
            reps = int(parts[3])
        except:
            return "Invalid numbers. Usage: gym [ex] [weight] [reps]"
            
        rpe = 8 # Default
        if len(parts) > 4:
            rpe = int(parts[4])
            
        # We need to ensure exercise exists or use closest match
        # For prototype, we pass raw name. The underlying log_set might handle it or we should verify.
        # Let's assume user knows exact name or we add simple correction.
        
        log_set(datetime.now().strftime("%Y-%m-%d"), ex_name, weight, reps, rpe)
        return f"🏋️ Logged {ex_name}: {weight}kg x {reps}"
        
    # Note Mode: "note buy milk"
    elif cmd == "note":
        content = " ".join(parts[1:])
        add_note("Quick Note", content, "cli-capture")
        return "📝 Note saved."
        
    # Plan Mode: "wake 7:00"
    elif cmd == "wake":
        time_str = parts[1]
        # Basic validation omitted for speed
        plan = get_daily_plan(datetime.now().strftime("%Y-%m-%d")) or {}
        plan["wake_time_planned"] = time_str
        create_or_update_plan(datetime.now().strftime("%Y-%m-%d"), plan)
        return f"⏰ Wake time set to {time_str}"
        
    return f"Unknown command: {cmd}"

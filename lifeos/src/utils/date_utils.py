from datetime import datetime, timedelta

def get_today_str():
    return datetime.now().strftime("%Y-%m-%d")

def get_date_str(date_obj):
    return date_obj.strftime("%Y-%m-%d")

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def get_week_start(date_str):
    dt = parse_date(date_str)
    start = dt - timedelta(days=dt.weekday())
    return get_date_str(start)

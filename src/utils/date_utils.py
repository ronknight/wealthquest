from datetime import datetime

def calculate_days_remaining(due_date_str: str) -> int:
    """Calculates days remaining until due_date. Negative if overdue."""
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        today = datetime.now()
        # Reset today to midnight for pure day difference
        today = datetime(today.year, today.month, today.day)
        delta = due_date - today
        return delta.days
    except (ValueError, TypeError):
        return 0

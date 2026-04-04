from sqlalchemy.orm import Session
from datetime import datetime
from ..models import database
from ..utils.date_utils import calculate_days_remaining
from .notifications import process_card_alert

def check_and_trigger_alerts(db: Session):
    """
    Checks all cards and triggers alerts if days_remaining <= alert_threshold.
    Includes deduplication logic to prevent multiple alerts on the same day.
    """
    cards = db.query(database.Card).all()
    today = datetime.now().date()
    
    for card in cards:
        days_remaining = calculate_days_remaining(card.due_date)
        if days_remaining <= card.alert_threshold:
            # Deduplication: Check if a successful alert was already sent today for this card
            last_alert = db.query(database.Alert).filter(
                database.Alert.card_id == card.id,
                database.Alert.status == "sent"
            ).order_by(database.Alert.timestamp.desc()).first()
            
            if last_alert:
                last_alert_date = datetime.fromisoformat(last_alert.timestamp).date()
                if last_alert_date == today:
                    continue
            
            try:
                process_card_alert(db, card.name, card.id, days_remaining)
            except Exception:
                # process_card_alert already handles logging
                pass

import subprocess
import shutil
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import database

logger = logging.getLogger(__name__)

def send_notification(title: str, message: str):
    """Sends a notification via termux-notification."""
    if not shutil.which("termux-notification"):
        logger.error("termux-notification not found in PATH")
        raise RuntimeError("termux-api not installed or termux-notification not in PATH")
    
    try:
        subprocess.run(
            ["termux-notification", "--title", title, "--content", message],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Notification sent: {title}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to send notification: {e.stderr}")
        raise RuntimeError(f"Failed to send notification: {e.stderr}")

def log_alert(db: Session, card_id: int, alert_type: str, status: str, error_message: str = None):
    """Logs an alert attempt to the database."""
    alert_log = database.Alert(
        timestamp=datetime.now().isoformat(),
        card_id=card_id,
        type=alert_type,
        status=status,
        error_message=error_message
    )
    db.add(alert_log)
    db.commit()

def process_card_alert(db: Session, card_name: str, card_id: int, days_remaining: int):
    """Sends a card alert and logs the result."""
    title = f"Credit Card Due: {card_name}"
    if days_remaining < 0:
        message = f"{card_name} is OVERDUE by {abs(days_remaining)} days!"
    elif days_remaining == 0:
        message = f"{card_name} is due TODAY!"
    else:
        message = f"{card_name} is due in {days_remaining} days."
    
    try:
        send_notification(title, message)
        log_alert(db, card_id, "card_due", "sent")
    except Exception as e:
        log_alert(db, card_id, "card_due", "failed", str(e))
        raise

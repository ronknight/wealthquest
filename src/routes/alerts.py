from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import database, schemas
from ..services import notifications
from ..utils import auth

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["alerts"],
)

@router.post("/test")
def test_notification(db: Session = Depends(database.get_db)):
    """Trigger a test notification."""
    try:
        notifications.send_notification("Test Alert", "This is a test notification from Fin.")
        return {"status": "success", "message": "Notification triggered"}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[schemas.Alert])
def get_alert_history(
    card_id: Optional[int] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: database.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Retrieve notification log history with pagination."""
    query = db.query(database.Alert)
    
    # Internal filter
    if not auth.is_root(current_user):
        query = query.filter(database.Alert.type != "debug")
        
    if card_id:
        query = query.filter(database.Alert.card_id == card_id)
    return query.order_by(database.Alert.timestamp.desc()).offset(offset).limit(limit).all()

@router.post("/debug")
def log_debug_info(
    message: str = Query(...),
    current_user: database.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Add a debug log entry. Accessible to all logged-in users to help trace issues."""
    from datetime import datetime
    new_debug = database.Alert(
        timestamp=datetime.now().isoformat(),
        type="debug",
        status="info",
        error_message=message
    )
    db.add(new_debug)
    db.commit()
    return {"status": "logged"}

@router.delete("/{id}", status_code=204)
def delete_alert(id: int, db: Session = Depends(database.get_db)):
    """Delete a specific alert log."""
    db_alert = db.query(database.Alert).filter(database.Alert.id == id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(db_alert)
    db.commit()
    return None

@router.delete("", status_code=204)
def clear_alerts(db: Session = Depends(database.get_db)):
    """Clear all alert logs."""
    db.query(database.Alert).delete()
    db.commit()
    return None

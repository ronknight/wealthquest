from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json
from ..models import database, schemas
from ..utils import auth

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
)

@router.get("/export")
def export_database(current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    """Export all database tables to a JSON object."""
    data = {
        "transactions": [
            {"amount": t.amount, "date": t.date, "source": t.source, "tax_flag": t.tax_flag} 
            for t in db.query(database.Transaction).all()
        ],
        "cards": [
            {"name": c.name, "statement_date": c.statement_date, "due_date": c.due_date, "balance": c.balance, "alert_threshold": c.alert_threshold} 
            for c in db.query(database.Card).all()
        ],
        "alerts": [
            {"timestamp": a.timestamp, "card_id": a.card_id, "type": a.type, "status": a.status, "error_message": a.error_message} 
            for a in db.query(database.Alert).all()
        ],
        "users": [
            {"username": u.username, "hashed_password": u.hashed_password, "role": u.role} 
            for u in db.query(database.User).all()
        ]
    }
    return data

@router.post("/import")
async def import_database(file: UploadFile = File(...), current_user: database.User = Depends(auth.require_admin), db: Session = Depends(database.get_db)):
    """Import database from a JSON file. WARNING: This clears existing data."""
    try:
        contents = await file.read()
        data = json.loads(contents)
        
        # Clear existing data
        db.query(database.Alert).delete()
        db.query(database.Transaction).delete()
        db.query(database.Card).delete()
        db.query(database.User).delete()
        
        # Import Users
        for u in data.get("users", []):
            db.add(database.User(**u))
        
        # Import Cards
        for c in data.get("cards", []):
            db.add(database.Card(**c))
            
        # Import Transactions
        for t in data.get("transactions", []):
            db.add(database.Transaction(**t))
            
        # Import Alerts
        for a in data.get("alerts", []):
            db.add(database.Alert(**a))
            
        db.commit()
        return {"status": "success", "message": "Database imported successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")

@router.get("/host-info")
def get_host_info():
    """Get the local IP address of the host for LAN access."""
    import socket
    try:
        # Create a dummy socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return {"ip": ip, "port": 8000, "url": f"http://{ip}:8000"}
    except Exception:
        return {"ip": "localhost", "port": 8000, "url": "http://localhost:8000"}

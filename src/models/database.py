from sqlalchemy import create_engine, Column, Integer, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    date = Column(Text, nullable=False)
    source = Column(Text)
    category = Column(Text, default="side") # 'main' or 'side'
    tax_flag = Column(Integer, default=0)
    notes = Column(Text) # Added for comprehensive entries

class RecurringPattern(Base):
    __tablename__ = "recurring_patterns"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    source = Column(Text, nullable=False)
    category = Column(Text, default="side")
    frequency = Column(Text, nullable=False) # 'daily', 'weekly', 'monthly'
    next_run_date = Column(Text, nullable=False)
    tax_flag = Column(Integer, default=0)
    notes = Column(Text)
    is_active = Column(Integer, default=1)

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    statement_date = Column(Text)
    due_date = Column(Text, nullable=False)
    balance = Column(Float, default=0.0)
    alert_threshold = Column(Integer, default=3)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    role = Column(Text, default="user") # admin, user

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(Text, nullable=False)
    card_id = Column(Integer, nullable=True) # Optional for system alerts
    type = Column(Text, nullable=False)
    status = Column(Text, default="sent")
    error_message = Column(Text)

# Database setup
DATABASE_URL = "sqlite:///./finance.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
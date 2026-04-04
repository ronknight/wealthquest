from pydantic import BaseModel, Field
from typing import Optional

class PaymentBase(BaseModel):
    amount: float
    date: str
    source: Optional[str] = None
    category: Optional[str] = "side"
    tax_flag: Optional[int] = 0

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

    class Config:
        from_attributes = True

class CardBase(BaseModel):
    name: str
    statement_date: Optional[str] = None
    due_date: str
    balance: Optional[float] = 0.0
    alert_threshold: Optional[int] = 3

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int
    days_remaining: Optional[int] = None

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    timestamp: str
    card_id: Optional[int] = None
    type: str
    status: Optional[str] = "sent"
    error_message: Optional[str] = None

class Alert(AlertBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

from pydantic import BaseModel
from pydantic import Field
from pydantic import Optional
from datetime import datetime
from decimal import Decimal

class Wallet(BaseModel):
    id: int
    amount: Decimal = Field(default=Decimal(0))
    owner_id: int
    name: Optional[str] = "Основной счёт"

class Transaction(BaseModel):
    id: int
    amount: Decimal = Field(gt=0, description="Величина транзакции должна быть больше 0")
    date_time: datetime = Field(default=datetime.now())
    sender_wallet_id: int
    receiver_wallet_id: int
    comment: Optional[str] = None
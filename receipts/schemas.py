from decimal import Decimal
from typing import List
from uuid import UUID
from pydantic import BaseModel


class Item(BaseModel):
    shortDescription: str
    price: Decimal

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: List[Item]
    total: Decimal

class PostReceiptResponse(BaseModel):
    id: UUID

class GetReceiptResponse(BaseModel):
    points: int
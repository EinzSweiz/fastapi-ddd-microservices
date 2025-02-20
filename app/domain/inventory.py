from dataclasses import dataclass, field
from datetime import datetime
import uuid
from app.domain.exceptions.inventory_exception import ZeroQuantityException, InventoryOutOfStockException

@dataclass
class Inventory:
    name: str
    description: str
    stock: int
    price: float
    product_id: str = field(default_factory=lambda:str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now())

    def __post_init__(self):
        """Ensure created_at is always a datetime object"""
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
    def decrease_stock(self, quantity: int):
        if quantity == 0:
            raise ZeroQuantityException()
        if self.stock < quantity:
            raise InventoryOutOfStockException()
        self.stock -= quantity
    
    def increase_stock(self, quantity: int):
        if quantity <= 0:
            raise ZeroQuantityException()
        self.stock += quantity

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "stock": self.stock,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
        }
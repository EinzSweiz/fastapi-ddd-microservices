from dataclasses import dataclass, field, replace
from datetime import datetime
from app.domain.exceptions.order_exception import InvalidOrderStatusException
import uuid

@dataclass
class Order:
    user_id: str
    product_id: str
    status: str = "pending"
    paid: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now())
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))


    def update_status(self, new_status: str):
        allowed_statuses = {"pending", "paid", "shipped", "delivered", "cancelled"}
        if new_status not in allowed_statuses:
            raise InvalidOrderStatusException(f"Invalid order status: {new_status}")
        return replace(self, status=new_status)

    def mark_paid(self):
        if self.status == 'pending':
            return replace(self, paid=True, status='paid')
        else:
            raise InvalidOrderStatusException(f"Cannot mark order as paid. Current status: {self.status}")


    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

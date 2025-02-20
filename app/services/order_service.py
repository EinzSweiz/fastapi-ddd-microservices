from app.infastructure.repositories.order_repository import OrderRepository
from app.domain.exceptions.order_exception import OrderNotFoundException
from app.domain.order import Order
from fastapi import Depends
from typing import Annotated
class OrderService:
    def __init__(self, repository: Annotated[OrderRepository, Depends()]):
        self.repository = repository
    

    async def create_order(self, user_id: str, product_id: str):
        order = Order(user_id=user_id, product_id=product_id)
        await self.repository.save(order=order)
        return order

    async def get_order_by_id(self, order_id: str):
        try:
            return await self.repository.get_by_id(order_id=order_id)
        except OrderNotFoundException as e:
            raise e
    

    async def update_order_status(self, order_id: str, new_status: str):
        try:
            order = await self.repository.get_by_id(order_id=order_id)
            order.update_status(new_status=new_status)
            await self.repository.update(order=order)
            return order
        except OrderNotFoundException as e:
            raise e

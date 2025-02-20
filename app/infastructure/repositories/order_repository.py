from app.domain.order import Order
from app.domain.exceptions.order_exception import OrderNotFoundException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Annotated
from fastapi import Depends
from app.infastructure.database import get_db

class OrderRepository:
    def __init__(self, db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]):
        self.collection = db["orders"]


    async def save(self, order: Order):
        await self.collection.insert_one(order.to_dict())

    
    async def get_by_id(self, order_id: str):
        data = await self.collection.find_one({"order_id": order_id})
        if not data:
            raise OrderNotFoundException()
        data.pop('_id', None)
        return Order(**data)
    
    async def update(self, order: Order):
        result = await self.collection.update_one(
            {'order_id': order.order_id},
            {"$set": order.to_dict()}
            )
        if result.matched_count == 0:
            raise OrderNotFoundException()
        
        
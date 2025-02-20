from app.domain.inventory import Inventory
from app.domain.exceptions.inventory_exception import InventoryNotFoundException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Annotated
from fastapi import Depends
import datetime
from app.infastructure.database import get_db

#db: Annotated[AsyncIOMotorDatabase, Depends(get_db)]
class InventoryRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db['inventory']


    async def save(self, inventory: Inventory):
        await self.collection.insert_one(inventory.to_dict())

    async def get_inventory_by_id(self, product_id: str) -> Inventory:
        data = await self.collection.find_one({'product_id': product_id})
        if not data:
            raise InventoryNotFoundException()
        data.pop('_id', None)
        if isinstance(data.get('created_at'), str):
            data['created_at'] = datetime.datetime.fromisoformat(data['created_at'])

        return Inventory(**data)
    
    async def update_stock(self, product_id: str, quantity: int, decrease: bool = True):
        product = await self.get_inventory_by_id(product_id=product_id)
        if not product:
            raise InventoryNotFoundException()
        if decrease:
            product.decrease_stock(quantity=quantity)
        else:
            product.increase_stock(quantity=quantity)

        result = await self.collection.update_one({'product_id': product_id}, {"$set": product.to_dict()})

        if result.matched_count == 0:
            raise InventoryNotFoundException()
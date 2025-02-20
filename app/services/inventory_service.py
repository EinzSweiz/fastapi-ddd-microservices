from app.infastructure.repositories.inventory_repository import InventoryRepository
from app.domain.exceptions.inventory_exception import InventoryNotFoundException
from app.domain.inventory import Inventory
from fastapi import Depends
from typing import Annotated

#repository: Annotated[InventoryRepository, Depends()]

class InventoryService:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository 

    async def create_inventory(self, name: str, description: str, price: float, stock: int):
        inventory = Inventory(name=name, description=description, price=price, stock=stock)
        await self.repository.save(inventory=inventory)
        return inventory
    
    async def get_inventory_by_id(self, product_id: str):
        try:
            return await self.repository.get_inventory_by_id(product_id=product_id)
        except InventoryNotFoundException as e:
            raise e

    async def decrease_stock(self, product_id: str, quantity: int):
        """Decrease stock quantity for a product."""
        try:
            return await self.repository.update_stock(product_id=product_id, quantity=quantity, decrease=True)
        except InventoryNotFoundException as e:
            raise e

    async def increase_stock(self, product_id: str, quantity: int):
        """Increase stock quantity for a product."""
        try:
            return await self.repository.update_stock(product_id=product_id, quantity=quantity, decrease=False)
        except InventoryNotFoundException as e:
            raise e

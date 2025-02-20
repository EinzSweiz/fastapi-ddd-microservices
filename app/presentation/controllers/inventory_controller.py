# from fastapi import APIRouter, HTTPException, Path, status, Depends
# from typing import Annotated
# from app.services.inventory_service import InventoryService
# from app.domain.exceptions.inventory_exception import InventoryNotFoundException, InventoryOutOfStockException
# import logging
# from app.presentation.schemas.inventory_schema import StockRequest, InventoryCreatSchema
# logger = logging.getLogger(__name__)


# inventory_router = APIRouter(tags=['Inventory'])



# @inventory_router.post('/inventory/create')
# async def create_inventory(data: InventoryCreatSchema, inventory_service: Annotated[InventoryService, Depends()]):
#     try:
#         order = await inventory_service.create_inventory(name=data.name, description=data.description, price=data.price, stock=data.stock)
#         return order.to_dict()
#     except Exception as e :
#         logger.error(f"Error during inventory creation: {e}")
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error happened during creation')

# @inventory_router.get('/inventory/{product_id}')
# async def get_inventory_by_id(product_id: Annotated[str, Path()], inventory_service: Annotated[InventoryService, Depends()]):
#     try:
#         inventory = await inventory_service.get_inventory_by_id(product_id=product_id)
#         return inventory.to_dict()
#     except InventoryNotFoundException as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# @inventory_router.patch('/inventory/decrease/{product_id}')
# async def decrease_stock(product_id: Annotated[str, Path()], inventory_service: Annotated[InventoryService, Depends()], data: StockRequest):
#     try:
#         await inventory_service.decrease_stock(product_id=product_id, quantity=data.quantity)
#         return {"message": f"Stock decreased by {data.quantity} for product {product_id}"}
#     except InventoryNotFoundException as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#     except InventoryOutOfStockException as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock available")
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")
    
# @inventory_router.patch('/inventory/increase/{product_id}')
# async def increase_stock(product_id: Annotated[str, Path()], data: StockRequest, inventory_service: Annotated[InventoryService, Depends()]):
#     """Increase stock quantity for a product."""
#     try:
#         await inventory_service.increase_stock(product_id, data.quantity)
#         return {"message": f"Stock increased by {data.quantity} for product {product_id}"}
#     except InventoryNotFoundException as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

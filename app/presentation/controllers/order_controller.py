# from fastapi import APIRouter, HTTPException, Path, status, Depends
# from typing import Annotated
# from app.domain.exceptions.order_exception import OrderNotFoundException
# from app.services.order_service import OrderService
# from typing import Annotated


# order_router = APIRouter(tags=['Order'])


# @order_router.get('/order/{order_id}')
# async def get_order(order_id: Annotated[str, Path()], order_service: Annotated[OrderService, Depends()]):
#     try:
#         order = await order_service.get_order_by_id(order_id=order_id)
#         return order.to_dict()
#     except OrderNotFoundException as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
# @order_router.post('/order/create')
# async def create_order(user_id: str, product_id: str, order_service: Annotated[OrderService, Depends()]):
#     try:
#         order = await order_service.create_order(user_id=user_id, product_id=product_id)
#         return order.to_dict()
#     except:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error happened during creation')
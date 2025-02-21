# import pytest
# from httpx import AsyncClient

# @pytest.mark.asyncio
# async def test_create_order(test_client: AsyncClient):
#     response = await test_client.post("/order/create", params={"user_id": "1", "product_id": "101"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "order_id" in data
#     assert data["user_id"] == "1"
#     assert data["product_id"] == "101"
#     assert data["status"] == "pending"


# @pytest.mark.asyncio
# async def test_get_order_not_found(test_client: AsyncClient):
#     response = await test_client.get('/order/invalid-id')
#     assert response.status_code == 404
#     assert response.json()['detail'] == 'This order was not found please contact our customer service'


# @pytest.mark.asyncio
# async def test_get_order_success(test_client: AsyncClient):
#     create_response = await test_client.post("/order/create", params={"user_id": "2", "product_id": "202"})
#     created_order = create_response.json()

#     order_id = created_order['order_id']
#     get_response = await test_client.get(f"/order/{order_id}")

#     assert get_response.status_code == 200
#     retrieved_order = get_response.json()
#     assert retrieved_order["order_id"] == order_id
#     assert retrieved_order["user_id"] == "2"
#     assert retrieved_order["product_id"] == "202"
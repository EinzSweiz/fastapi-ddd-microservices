# import pytest
# from httpx import AsyncClient


# @pytest.mark.asyncio
# async def test_create_inventory_success(test_client: AsyncClient, create_inventory):
#     assert create_inventory.status_code == 200
#     json_response = create_inventory.json()
#     assert json_response['name'] == 'Books'
#     assert json_response['price'] == 200
#     assert json_response['stock'] == 20


# @pytest.mark.asyncio
# async def test_create_inventory_fail(test_client: AsyncClient):
#     data = {
#         'name': 'Books',
#         'description': 'Cool Books',
#         'price': 'Riad',
#         'stock': 20
#     }
#     response = await test_client.post('/inventory/create', json=data)
#     assert response.status_code == 422



# @pytest.mark.asyncio
# async def test_get_iventory_by_id(test_client: AsyncClient, create_inventory):
   
#     json_item = create_inventory.json()

#     response = await test_client.get(f"/inventory/{json_item['product_id']}")


#     assert response.status_code == 200
#     response_json = response.json()
#     assert response_json['name'] == 'Books'
#     assert response_json['price'] == 200


# @pytest.mark.asyncio
# async def test_decrease_stock(test_client: AsyncClient, create_inventory):
#     json_item = create_inventory.json()

#     response = await test_client.patch(
#         f"/inventory/decrease/{json_item['product_id']}",
#         json={"quantity": 2}
#     )

#     print("DEBUG RESPONSE STATUS:", response.status_code)
#     print("DEBUG RESPONSE BODY:", response.json())  # ✅ Print error message

#     assert response.status_code == 200
#     assert response.json() == {"message": f"Stock decreased by 2 for product {json_item['product_id']}"}


#     updated_response = await test_client.get(f"/inventory/{json_item['product_id']}")
#     updated_json = updated_response.json()

#     assert updated_json['stock'] == 18



# @pytest.mark.asyncio
# async def test_increase_stock(test_client: AsyncClient, create_inventory):
#     json_item = create_inventory.json()

#     response = await test_client.patch(f'/inventory/increase/{json_item['product_id']}', json={'quantity': 2})

#     assert response.status_code == 200
#     assert response.json() == {"message": f"Stock increased by {2} for product {json_item['product_id']}"}

#     updated_response = await test_client.get(f"/inventory/{json_item['product_id']}")
#     updated_json = updated_response.json()

#     assert updated_json['stock'] == 22

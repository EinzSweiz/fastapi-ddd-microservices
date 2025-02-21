# import pytest
# from httpx import AsyncClient

# @pytest.fixture
# async def test_client():
#     """Fixture that returns an async test client for FastAPI app."""
#     async with AsyncClient(base_url="http://localhost:8002") as client:
#         yield client


# @pytest.fixture(scope='function')
# async def create_inventory(test_client: AsyncClient):
#     data = {
#         'name': 'Books',
#         'description': 'Cool Books',
#         'price': 200,
#         'stock': 20
#     }
#     response = await test_client.post('/inventory/create', json=data)
#     return response
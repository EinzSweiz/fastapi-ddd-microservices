import pytest
import json
import asyncio
import websockets

@pytest.mark.asyncio
async def test_websocket_connection():
    url = "ws://web:8002/ws"

    async with websockets.connect(url) as websocket:
        message = {"event": "create", "name": "NEW", "description": "NEW", "stock": 2, "price": 1}
        await websocket.send(json.dumps(message))

        response = await websocket.recv()

        # Parse the received message
        actual_data = json.loads(response)['data']

        expected_data = {
            "name": "NEW",
            "description": "NEW",
            "stock": 2,
            "price": 1
        }

        actual_data.pop('created_at', None)
        actual_data.pop('product_id', None)

        assert actual_data == expected_data

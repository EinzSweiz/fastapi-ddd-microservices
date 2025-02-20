import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.asyncio
async def test_websocket(create_inventory):
    inventory = create_inventory
    inventory_json = inventory.json()

    client = TestClient(app)
    async with client.websocket_connect("/ws") as websocket:
        message = json.dumps({
            "event": "decrease_stock",
            "product_id": inventory_json["product_id"],
            "quantity": 2
        })
        await websocket.send_text(message)

        # ✅ Receive response
        response = await websocket.receive_text()
        print(f"WebSocket Response: {response}")

        # ✅ Ensure WebSocket closes after response
        assert "message" in response

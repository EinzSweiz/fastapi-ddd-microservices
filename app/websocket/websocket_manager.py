from fastapi import WebSocket
from typing import List
import json

class WebsocketManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"✅ WebSocket connection established with {websocket.client}")

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"❌ WebSocket connection closed with {websocket.client}")

    async def send_message(self, message: str, data: dict = None):
        """Send a message to all connected WebSocket clients."""
        message_data = {
            "message": message,
            "data": data
        }
        message_data_json = json.dumps(message_data)
        print(f"📤 Sending message to WebSocket: {message_data_json}")
        print('ACTIVE CONNECTIONS:', self.active_connections)
        for connection in self.active_connections:
            try:
                print('Connetion:', connection.client_state)
                await connection.send_text(message_data_json)
                print(f"📤 Message sent to {connection.client}")
            except Exception as e:
                print(f"WebSocket Error: {e}")
                await self.disconnect(connection)

ws_manager = WebsocketManager()
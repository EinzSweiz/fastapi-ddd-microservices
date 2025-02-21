import json
import asyncio
import logging
from fastapi import WebSocket
from typing import List
from app.infastructure.redis_client import redis_client

logger = logging.getLogger(__name__)

class WebsocketManager:
    """Manages WebSocket connections & listens to Redis Pub/Sub."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis_pubsub = None  # Redis connection for Pub/Sub
        self.redis_task = None

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str, data: dict = None):
        """Send message to all connected WebSocket clients."""
        message_data_json = json.dumps({"message": message, "data": data})

        for connection in self.active_connections:
            try:
                await connection.send_text(message_data_json)
            except:
                await self.disconnect(connection)

    async def listen_to_redis(self):
        """Continuously listen for Redis Pub/Sub messages."""
        self.redis_pubsub = await redis_client.get_redis_pubsub()

        async with self.redis_pubsub.pubsub() as pubsub:
            await pubsub.subscribe("websocket_channel")
            print("📡 WebSocket Manager subscribed to Redis Pub/Sub...")
            logger.info("📡 WebSocket Manager subscribed to Redis Pub/Sub...")

            async for message in pubsub.listen():
                print(f"📡 RAW Redis Message: {message}")  # Debug log
                logger.info(f"📡 RAW Redis Message: {message}")

                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        print(f"📡 Received from Redis: {data}")
                        logger.info(f"📡 Received from Redis: {data}")
                        await self.send_message(data["message"], data["data"])
                    except Exception as e:
                        print(f"❌ WebSocket Redis Listen Error: {e}")
                        logger.error(f"❌ WebSocket Redis Listen Error: {e}")

    async def start_redis_listener(self):
        if not self.redis_task:
            print("🚀 Starting Redis Pub/Sub Listener for WebSockets...")
            self.redis_task = asyncio.create_task(self.listen_to_redis())

ws_manager = WebsocketManager()

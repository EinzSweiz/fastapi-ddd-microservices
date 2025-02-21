import asyncio
from confluent_kafka import Consumer, KafkaError
import json
import logging
import time
from app.services.inventory_service import InventoryService
from app.websocket.websocket_manager import WebsocketManager
from app.infastructure.redis_client import redis_client

logger = logging.getLogger(__name__)

class KafkaConsumerService:
    def __init__(self, inventory_service: InventoryService, consumer_group: str = "inventory-consumer-group"):
        self.inventory_service = inventory_service
        self.redis_pubsub = None
        self.consumer_group = consumer_group
        self.consumer = self.create_kafka_consumer_with_retry()

    def create_kafka_consumer_with_retry(self, retries: int = 5, backoff: float = 1.0) -> Consumer:
        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Attempting to connect to Kafka... (Attempt {attempt + 1})")
                consumer = Consumer({
                    'bootstrap.servers': 'kafka:9092',
                    'group.id': self.consumer_group,
                    'auto.offset.reset': 'earliest',  # Start from the earliest available message
                    'socket.timeout.ms': 30000,  # Set the socket timeout for long running processes
                    'enable.auto.commit': True,
                })
                consumer.subscribe([
                    "inventory.decrease_stock",
                    "inventory.increase_stock",
                    "inventory.create",
                    "inventory.fetch"
                ])
                logging.info("Connected to Kafka!")
                print("✅ Kafka is up!")
                return consumer
            except KafkaError as e:
                logging.error(f"Kafka connection failed: {e}")
                print(f"❌ Kafka not ready, retrying {retries}...")
                attempt += 1
                if attempt >= retries:
                    logging.error("Max retries reached. Exiting.")
                    raise e
                logging.info(f"Retrying in {backoff} seconds...")
                time.sleep(backoff)

    async def setup_redis(self):
        """Initialize Redis Pub/Sub."""
        try:
            self.redis_pubsub = await redis_client.get_redis_pubsub()
            logger.info("Connected to Redis Pub/Sub!")
        except Exception as e:
            logger.error(f"Failed to initialize Redis Pub/Sub: {e}")

    async def consume_messages(self):
        """Consumes messages from Kafka in an infinite loop."""
        loop = asyncio.get_event_loop()
        while True:
            logger.info("Polling Kafka for new messages...")
            msg = await loop.run_in_executor(None, self.consumer.poll, 1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"❌ Kafka Consumer Error: {msg.error()}")
                continue
            await self.process_message(msg)

    async def process_message(self, msg):
        """Processes a single Kafka message."""
        event = json.loads(msg.value().decode("utf-8"))
        product_id = event.get("product_id", "unknown")
        print(f"📥 Received Kafka Event: {event}")
        logger.info(f"📥 Received Kafka Event: {event}")

        response = {}

        try:
            if msg.topic() == "inventory.create":
                inventory = await self.inventory_service.create_inventory(
                    name=event['name'],
                    description=event['description'],
                    stock=event['stock'],
                    price=event['price']
                )
                response = {
                    "message": "✅ Inventory Created Successfully",
                    "data": inventory.to_dict()
                }
                print('✅ Inventory was created')
                logger.info('✅ Inventory was created')

            elif msg.topic() == "inventory.fetch":
                inventory = await self.inventory_service.get_inventory_by_id(product_id=product_id)
                response = {
                    "message": "Inventory Fetched",
                    "data": inventory.to_dict()
                }

            elif msg.topic() == "inventory.increase_stock":
                updated_stock = await self.inventory_service.increase_stock(product_id, event["quantity"])
                response = {
                    "message": "✅ Stock increased successfully",
                    "data": {"product_id": product_id, "new_stock": updated_stock}
                }

            elif msg.topic() == "inventory.decrease_stock":
                updated_stock = await self.inventory_service.decrease_stock(product_id, event["quantity"])
                response = {
                    "message": "✅ Stock decreased successfully",
                    "data": {"product_id": product_id, "new_stock": updated_stock}
                }

            # 🔹 Try publishing to Redis
            if self.redis_pubsub:
                print(f"📡 Publishing to Redis: {response}")
                logger.info(f"📡 Publishing to Redis: {response}")

                try:
                    await self.redis_pubsub.publish("websocket_channel", json.dumps(response))
                    print(f"✅ Published to Redis Pub/Sub: {response}")
                    logger.info(f"✅ Published to Redis Pub/Sub: {response}")
                except Exception as e:
                    print(f"❌ Redis Publish Error: {e}")
                    logger.error(f"❌ Redis Publish Error: {e}")
            else:
                print("❌ Redis Pub/Sub is not initialized.")
                logger.error("❌ Redis Pub/Sub is not initialized.")

        except KafkaError as e:
            print(f"❌ Kafka Error: {e}")
            logger.error(f"❌ Kafka Error: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            response = {"error": f"❌ Unexpected error: {str(e)}"}
            print(f"Error during message processing: {response}")
            logger.error(f"Error during message processing: {response}")

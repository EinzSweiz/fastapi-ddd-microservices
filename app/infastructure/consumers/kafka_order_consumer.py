from confluent_kafka import Consumer, KafkaError
import json
import asyncio
from app.domain.order import Order
from app.services.order_service import OrderService
from app.infastructure.redis_client import redis_client
from app.domain.exceptions.order_exception import OrderNotFoundException, InvalidOrderStatusException
import logging
import time
BOOTSTRAP_SERVERS = "kafka:9092"

logger = logging.getLogger(__name__)

class KafkaOrderConsumerService:
    
    def __init__(self, order_service: OrderService, consumer_group: str = "order-consumer-group"):
        self.order_service = order_service
        self.redis_pubsub = None
        self.consumer_group = consumer_group
        self.consumer = self.create_kafka_consumer_with_retry()


    def create_kafka_consumer_with_retry(self, retries: int = 5, backoff: float = 1.0) -> Consumer:
        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Attempting to connect to Kafka... (Attempt {attempt + 1})")
                consumer = Consumer({
                    'bootstrap.servers': BOOTSTRAP_SERVERS,
                    'group.id': self.consumer_group,
                    'auto.offset.reset': 'earliest',
                    'socket.timeout.ms': 30000,
                    'enable.auto.commit': True,
                })
                consumer.subscribe([
                    'order.get',
                    'order.create',
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

    async def consume_message(self):
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
        event = json.loads(msg.value().decode('utf-8'))
        order_id = event.get("order_id", "unknown")
        product_id = event.get("product_id", "unknown")
        user_id = event.get('user_id', "unknown")
        print(f"📥 Received Kafka Event: {event}")
        logger.info(f"📥 Received Kafka Event: {event}")

        response = {}

        try:
            if msg.topic() == "order.create":
                inventory = await self.order_service.create_order(
                    user_id=user_id,
                    product_id=product_id
                )
                response = {
                    "message": "✅ Order Created Successfully",
                    "data": inventory.to_dict()
                }
                print('✅ Order was created')
                logger.info('✅ Order was created')

            elif msg.topic() == "order.get":
                inventory = await self.order_service.get_order_by_id(order_id=order_id)
                response = {
                    "message": "Inventory Fetched",
                    "data": inventory.to_dict()
                }
            if self.redis_pubsub:
                print(f"📡 Publishing to Redis: {response}")
                logger.info(f"📡 Publishing to Redis: {response}")
                try:
                    await self.redis_pubsub.publish('websocket_channel', json.dumps(response))
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

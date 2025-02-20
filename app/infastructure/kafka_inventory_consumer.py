from confluent_kafka import Consumer, KafkaError
import json
import logging
import time
from app.services.inventory_service import InventoryService
from app.websocket.websocket_manager import WebsocketManager

class KafkaConsumerService:
    def __init__(self, inventory_service: InventoryService, consumer_group: str = "inventory-consumer-group", ws_manager: WebsocketManager = None):
        self.inventory_service = inventory_service
        self.ws_manager = ws_manager
        
        # Kafka consumer group (different for each consumer)
        self.consumer_group = consumer_group
        
        # Kafka Consumer
        self.consumer = self.create_kafka_consumer_with_retry()

    def create_kafka_consumer_with_retry(self, retries: int = 5, backoff: float = 2.0) -> Consumer:
        attempt = 0
        while attempt < retries:
            try:
                logging.info(f"Attempting to connect to Kafka... (Attempt {attempt + 1})")
                consumer = Consumer({
                    'bootstrap.servers': 'kafka:9092',
                    'group.id': self.consumer_group,  # Unique group ID per consumer
                    'auto.offset.reset': 'earliest',
                    'socket.timeout.ms': 30000
                })
                consumer.subscribe([
                    "inventory.decrease_stock",
                    "inventory.increase_stock",
                    "inventory.create",
                    "inventory.fetch"
                ])
                logging.info("Connected to Kafka!")
                return consumer
            except KafkaError as e:
                logging.error(f"Kafka connection failed: {e}")
                attempt += 1
                if attempt >= retries:
                    logging.error("Max retries reached. Exiting.")
                    raise e
                logging.info(f"Retrying in {backoff} seconds...")
                time.sleep(backoff)

    async def consume_messages(self):
        """Continuously listen for Kafka messages and process them."""
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"❌ Kafka Consumer Error: {msg.error()}")
                continue

            event = json.loads(msg.value().decode("utf-8"))
            product_id = event.get("product_id", "unknown")
            print(f"📥 Received Kafka Event: {event}")

            response = {}

            try:
                if msg.topic() == "inventory.create":
                    print(f"📌 Processing Inventory Creation for {event['name']}...")
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
                    print(f"✅ Inventory Created: {inventory.to_dict()}")

                elif msg.topic() == "inventory.fetch":
                    print(f"📌 Fetching Inventory for product_id={product_id}...")
                    inventory = await self.inventory_service.get_inventory_by_id(product_id=product_id)
                    response = {
                        "message": "Inventory Fetched",
                        "data": inventory.to_dict()
                    }
                    print(f"✅ Inventory Data Retrieved: {inventory.to_dict()}")
                    await self.ws_manager.send_message(response["message"], response["data"])


                elif msg.topic() == "inventory.increase_stock":
                    print(f"📌 Increasing Stock for Product {product_id} by {event['quantity']}...")
                    updated_stock = await self.inventory_service.increase_stock(product_id, event["quantity"])
                    response = {
                        "message": "✅ Stock increased successfully",
                        "data": {"product_id": product_id, "new_stock": updated_stock}
                    }
                    print(f"✅ Stock Increased: {response}")

                elif msg.topic() == "inventory.decrease_stock":
                    print(f"📌 Decreasing Stock for Product {product_id} by {event['quantity']}...")
                    updated_stock = await self.inventory_service.decrease_stock(product_id, event["quantity"])
                    response = {
                        "message": "✅ Stock decreased successfully",
                        "data": {"product_id": product_id, "new_stock": updated_stock}
                    }
                    print(f"✅ Stock Decreased: {response}")

            except Exception as e:
                response = {"error": f"❌ Unexpected error: {str(e)}"}
                print(response)
import asyncio
import logging
import os
from app.infastructure.kafka_inventory_consumer import KafkaConsumerService
from app.services.inventory_service import InventoryService
from app.infastructure.repositories.inventory_repository import InventoryRepository
from app.infastructure.database import get_db

async def run_consumer():
    """Initialize Kafka Consumer independently from FastAPI"""
    logging.info("Starting Kafka Consumer Service...")

    db = await get_db()
    repository = InventoryRepository(db=db)
    inventory_service = InventoryService(repository=repository)
    # Get consumer group dynamically from environment variable
    consumer_group = os.getenv("CONSUMER_GROUP", "inventory-group-default")
    kafka_consumer = KafkaConsumerService(inventory_service=inventory_service, consumer_group=consumer_group)

    await kafka_consumer.setup_redis()

    await kafka_consumer.consume_messages()

if __name__ == "__main__":
    asyncio.run(run_consumer())

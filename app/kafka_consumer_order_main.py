import asyncio
import logging
import os
from app.infastructure.consumers.kafka_order_consumer import KafkaOrderConsumerService
from app.services.order_service import OrderService
from app.infastructure.repositories.order_repository import OrderRepository
from app.infastructure.database import get_db

async def run_consumer():
    """Initialize Kafka Consumer independently from FastAPI"""
    logging.info("Starting Kafka Consumer Service...")

    db = await get_db()
    repository = OrderRepository(db=db)
    order_service = OrderService(repository=repository)
    # Get consumer group dynamically from environment variable
    consumer_group = os.getenv("CONSUMER_GROUP1", "order-consumer-group")
    kafka_consumer = KafkaOrderConsumerService(order_service=order_service, consumer_group=consumer_group)

    await kafka_consumer.setup_redis()

    await kafka_consumer.consume_message()

if __name__ == "__main__":
    asyncio.run(run_consumer())

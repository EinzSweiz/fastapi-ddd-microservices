import logging
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.websocket.websocket_service import websocket_router
from app.websocket.websocket_manager import ws_manager
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

# async def wait_for_topic_ready(kafka_topic_manager: KafkaTopicManager, topic_name: str, retries: int = 10, backoff: float = 2.0):
#     """Asynchronously wait for Kafka topic to be ready."""
#     attempt = 0
#     while attempt < retries:
#         if kafka_topic_manager.existing_topics(topic_name):
#             logging.info(f"Topic {topic_name} is ready.")
#             return True
#         logging.info(f"Waiting for topic {topic_name} to be ready... (Attempt {attempt + 1}/{retries})")
#         await asyncio.sleep(backoff)  # Use asyncio.sleep to prevent blocking the event loop
#         attempt += 1
#     logging.error(f"Failed to find topic {topic_name} after {retries} attempts.")
#     return False

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Startup and shutdown events"""    
#     db = await get_db()
#     repository = InventoryRepository(db=db)
#     inventory_service = InventoryService(repository=repository)
    
#     # Initialize KafkaTopicManager and create topics if they don't exist
#     kafka_topic_manager = KafkaTopicManager(bootstrap_servers='kafka:9092')
#     kafka_topics_to_create = [
#         "inventory.decrease_stock",
#         "inventory.increase_stock",
#         "inventory.create",
#         "inventory.fetch"
#     ]
    
#     # Create topics and wait for them to be ready
#     for topic in kafka_topics_to_create:
#         if not kafka_topic_manager.existing_topics(topic_name=topic):
#             logging.info(f"Creating Kafka topic: {topic}")
#             kafka_topic_manager.create_topic(topic)
#             success = await wait_for_topic_ready(kafka_topic_manager, topic)
#             if not success:
#                 logging.error(f"Failed to create and verify Kafka topic: {topic}")
#                 raise Exception(f"Kafka topic {topic} was not ready in time.")
    
#     # Initialize Kafka Consumer
#     kafka_consumer = KafkaConsumerService(inventory_service=inventory_service)
#     consumer_task = asyncio.create_task(kafka_consumer.consume_messages())

#     try:
#         yield  # App runs
#     finally:
#         consumer_task.cancel()
#         try:
#             await consumer_task
#         except asyncio.CancelledError:
#             logging.info("Kafka Consumer stopped.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event: Start and cleanup resources."""
    print("🚀 FastAPI Application is starting...")
    logger.info("🚀 FastAPI Application is starting...")

    # Start Redis Pub/Sub listener
    task = asyncio.create_task(ws_manager.start_redis_listener())
    
    print("📡 Redis listener started!")
    logger.info("📡 Redis listener started!")

    yield  # Run the application

    print("🛑 FastAPI Application is shutting down...")
    logger.info("🛑 FastAPI Application is shutting down...")
    
    # Cleanup task on shutdown
    task.cancel()


# ✅ Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# ✅ CORS Configuration (Adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register Routers
app.include_router(websocket_router)


# import logging
# import asyncio
# from fastapi import FastAPI
# from contextlib import asynccontextmanager
# from app.infastructure.kafka_consumer import KafkaConsumerService
# from app.infastructure.kafka_topics import KafkaTopicManager
# from app.infastructure.database import get_db
# from app.services.inventory_service import InventoryService
# from app.websocket.websocket_service import websocket_router
# from app.infastructure.repositories.inventory_repository import InventoryRepository
# from fastapi.middleware.cors import CORSMiddleware

# consumer_task = None  # Store the task globally

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Startup and shutdown events"""    
#     global consumer_task  # Use a global variable to store the task reference

#     db = await get_db()
#     repository = InventoryRepository(db=db)
#     inventory_service = InventoryService(repository=repository)
    
#     # ✅ Initialize Kafka Consumer
#     kafka_consumer = KafkaConsumerService(inventory_service=inventory_service)

#     # ✅ Start the consumer as a background task (so it doesn't block FastAPI startup)
#     consumer_task = asyncio.create_task(kafka_consumer.consume_messages())

#     try:
#         yield  # ✅ Allow FastAPI to start properly
#     finally:
#         # ✅ Shutdown the consumer properly
#         if consumer_task:
#             consumer_task.cancel()
#             try:
#                 await consumer_task
#             except asyncio.CancelledError:
#                 logging.info("✅ Kafka Consumer stopped.")

# # ✅ Initialize FastAPI with the fixed `lifespan`
# app = FastAPI(lifespan=lifespan)

# # ✅ CORS Configuration (Adjust for production)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ Register Routers
# app.include_router(websocket_router)

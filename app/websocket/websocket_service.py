from fastapi import WebSocket, APIRouter
from app.infastructure.kafka_producer import KafkaProducerService
from app.websocket.websocket_manager import ws_manager
import json
websocket_router = APIRouter(tags=['Websocket'])
producer = KafkaProducerService()

@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket server that listens for client events and forwards them to Kafka."""
    await ws_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received WebSocket Message: {data}")
            event = json.loads(data)
            if event.get('type') == 'order':
                topic = f'order.{event['event']}'
            elif event.get('type') == 'inventory':
                topic = f"inventory.{event['event']}"
            else:
                print("⚠️ Unknown event type, ignoring...")
                continue
            producer.send_message(topic, event)
            print(f"Sent event to Kafka: {event}")

            #Send immediate response back
            # await websocket.send_text(json.dumps({
            #     "message": 'Event received and processed',
            #     "data": event
            # }))
            

    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await ws_manager.disconnect(websocket)

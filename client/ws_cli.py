import asyncio
import websockets
import json

async def chat_client():
    uri = "ws://localhost:8000/ws/room1"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"user": "alice", "message": "שלום"}))
        while True:
            response = await websocket.recv()
            print("הודעה מהשרת:", response)

asyncio.run(chat_client())
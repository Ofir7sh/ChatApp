import websocket
import threading
import json

def on_message(ws, message):
    msg = json.loads(message)
    print(f"[{msg['username']}] {msg['content']}")

def on_open(ws):
    def run():
        while True:
            msg = input()
            if msg.strip():
                payload = {
                    "username": "ofir", 
                    "content": msg
                }
                ws.send(json.dumps(payload))
    threading.Thread(target=run).start()

def start_ws(room_name):
    ws = websocket.WebSocketApp(f"ws://localhost:8000/ws/{room_name}",
                                on_message=on_message,
                                on_open=on_open)
    ws.run_forever()

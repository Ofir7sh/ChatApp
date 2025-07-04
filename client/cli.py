import typer
import requests
import os
import threading
import time
import platform
import asyncio
import websockets
import json

from app.config import BASE_URL, TOKEN_FILE, USERNAME_FILE

app = typer.Typer()

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def save_token(token: str):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token() -> str | None:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def save_username(username: str):
    with open(USERNAME_FILE, "w") as f:
        f.write(username)

def load_username() -> str | None:
    if os.path.exists(USERNAME_FILE):
        with open(USERNAME_FILE, "r") as f:
            return f.read().strip()
    return None

def authenticated_headers():
    token = load_token()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

def fetch_chatrooms():
    res = requests.get(f"{BASE_URL}/chatrooms/", headers=authenticated_headers())
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to get chatrooms: {res.text}")
        return []

def check_user_exists(username):
    res = requests.get(f"{BASE_URL}/users/exists/{username}")
    if res.status_code != 200:
        print("Error checking user:", res.text)
        raise typer.Exit()
    return res.json().get("exists", False)

async def websocket_chat(room_name, username, stop_event):
    # חיבור ל-WebSocket
    # חשוב: תתאימי את הכתובת לשרת שלך בהתאם (החלף localhost:8000 לכתובת שלך)
    uri = f"ws://localhost:8000/ws/{room_name}"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket room: {room_name}")

            async def send_messages():
                while not stop_event.is_set():
                    content = await asyncio.get_event_loop().run_in_executor(None, input)
                    if content.strip() == ":back":
                        stop_event.set()
                        break
                    elif content.strip() == ":clear":
                        clear_screen()
                    elif content.strip():
                        message = {"username": username, "content": content.strip()}
                        await websocket.send(json.dumps(message))

            async def receive_messages():
                while not stop_event.is_set():
                    try:
                        response = await websocket.recv()
                        msg = json.loads(response)
                        # הדפסת ההודעה בזמן אמת
                        print(f"[{msg.get('timestamp', '')}] {msg['username']}: {msg['content']}")
                    except websockets.ConnectionClosed:
                        print("WebSocket connection closed")
                        stop_event.set()

            # להריץ במקביל שליחה וקבלה
            await asyncio.gather(send_messages(), receive_messages())

    except Exception as e:
        print(f"WebSocket connection error: {e}")
        stop_event.set()

@app.command()
def cli():
    username = input("Enter username: ").strip()
    save_username(username)

    user_exists = check_user_exists(username)
    if user_exists:
        password = typer.prompt("Enter your password", hide_input=True)
        res = requests.post(f"{BASE_URL}/users/login", json={"username": username, "password": password})
        if res.status_code != 200:
            print("Login failed:", res.text)
            raise typer.Exit()
        print("Login successful.")
    else:
        print("User not found. Creating new user.")
        password = typer.prompt("Choose a password", hide_input=True)
        res = requests.post(f"{BASE_URL}/users/register", json={"username": username, "password": password})
        if res.status_code != 200:
            print("Registration failed:", res.text)
            raise typer.Exit()
        print("Registered successfully.")

    token = res.json()["access_token"]
    save_token(token)
    print("Logged in successfully.")

    while True:
        chatrooms = fetch_chatrooms()
        print("\nAvailable chat rooms:")
        for idx, room in enumerate(chatrooms):
            print(f"{idx + 1}. {room['name']}")
        print("0. Create new chat room")
        print("-1. Exit")

        try:
            choice = int(input("Choose chat room by number: "))
        except ValueError:
            print("Invalid input.")
            continue

        if choice == -1:
            print("Goodbye!")
            raise typer.Exit()

        if choice == 0:
            new_room_name = input("Enter new chat room name: ").strip()
            res = requests.post(f"{BASE_URL}/chatrooms/", json={"name": new_room_name}, headers=authenticated_headers())
            if res.status_code != 200:
                print("Failed to create chat room:", res.text)
                continue
            room_name = new_room_name
        else:
            if choice < 1 or choice > len(chatrooms):
                print("Invalid choice.")
                continue
            room_name = chatrooms[choice - 1]["name"]

        print(f"\nEntered chat room: {room_name}")
        stop_event = threading.Event()

        # הפעלת WebSocket בלולאת אירועים אסינכרונית בתוך Thread נפרד
        def start_ws_loop():
            asyncio.run(websocket_chat(room_name, username, stop_event))

        ws_thread = threading.Thread(target=start_ws_loop, daemon=True)
        ws_thread.start()

        print("Type your messages below.")
        print("Use ':back' to return to room selection, ':clear' to clear the screen, or Ctrl+C to exit.")

        try:
            while not stop_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            stop_event.set()
            raise typer.Exit()


if __name__ == "__main__":
    app()

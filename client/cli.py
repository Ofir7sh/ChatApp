import typer
import requests
import os
import threading
import time
import platform
import asyncio
import websockets
import json
from typing import Optional
from app.core.config import BASE_URL, TOKEN_FILE, USERNAME_FILE, WS_BASE_URL

app = typer.Typer()

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def save_file(path: str, data: str):
    with open(path, "w") as f:
        f.write(data)

def load_file(path: str) -> Optional[str]:
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read().strip()
    return None

def save_token(token: str):
    save_file(TOKEN_FILE, token)

def load_token() -> Optional[str]:
    return load_file(TOKEN_FILE)

def save_username(username: str):
    save_file(USERNAME_FILE, username)

def load_username() -> Optional[str]:
    return load_file(USERNAME_FILE)

def authenticated_headers():
    token = load_token()
    return {"Authorization": f"Bearer {token}"} if token else {}

def fetch_chatrooms():
    res = requests.get(f"{BASE_URL}/chatrooms/", headers=authenticated_headers())
    if res.ok:
        return res.json()
    print(f"Failed to get chatrooms: {res.text}")
    return []
def fetch_messages(room_name):
    res = requests.get(f"{BASE_URL}/messages/{room_name}", headers=authenticated_headers())
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to get messages: {res.text}")
        return []
def check_user_exists(username: str) -> bool:
    res = requests.get(f"{BASE_URL}/users/exists/{username}")
    if not res.ok:
        print("Error checking user:", res.text)
        raise typer.Exit()
    return res.json().get("exists", False)

async def websocket_chat(room_name: str, username: str, stop_event: threading.Event, token: str):
    uri = f"{WS_BASE_URL}/ws/{room_name}?token={token}"
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
                        print(f"[{msg.get('timestamp', '')}] {msg['username']}: {msg['content']}")
                    except websockets.ConnectionClosed:
                        print("WebSocket connection closed")
                        stop_event.set()

            await asyncio.gather(send_messages(), receive_messages())

    except Exception as e:
        print(f"WebSocket connection error: {e}")
        stop_event.set()

@app.command()
def cli():
    """Interactive CLI Chat Application - WenSocket"""
    username = typer.prompt("Enter username").strip()
    save_username(username)

    if check_user_exists(username):
        password = typer.prompt("Enter your password", hide_input=True)
        res = requests.post(f"{BASE_URL}/users/login", json={"username": username, "password": password})
        if not res.ok:
            print("Login failed:", res.text)
            raise typer.Exit()
        print("Login successful.")
    else:
        print("User not found. Creating new user.")
        password = typer.prompt("Choose a password", hide_input=True)
        res = requests.post(f"{BASE_URL}/users/register", json={"username": username, "password": password})
        if not res.ok:
            print("Registration failed:", res.text)
            raise typer.Exit()
        print("Registered successfully.")

    token = res.json()["access_token"]
    save_token(token)
    print("Logged in successfully.")

    while True:
        chatrooms = fetch_chatrooms()
        typer.echo("\nAvailable chat rooms:")
        for idx, room in enumerate(chatrooms):
            typer.echo(f"{idx + 1}. {room['name']}")
        typer.echo("0. Create new chat room")
        typer.echo("-1. Exit")

        choice = typer.prompt("Choose chat room by number")
        if not choice.isdigit() and choice != "-1":
            typer.echo("Invalid input.")
            continue

        choice = int(choice)
        if choice == -1:
            typer.echo("Goodbye!")
            raise typer.Exit()

        if choice == 0:
            room_name = typer.prompt("Enter new chat room name").strip()
            res = requests.post(f"{BASE_URL}/chatrooms/", json={"name": room_name}, headers=authenticated_headers())
            if not res.ok:
                typer.echo(f"Failed to create chat room: {res.text}")
                continue
        else:
            if choice < 1 or choice > len(chatrooms):
                typer.echo("Invalid choice.")
                continue
            room_name = chatrooms[choice - 1]["name"]

        stop_event = threading.Event()  

        typer.echo(f"\nEntered chat room: {room_name}")

        old_messages = fetch_messages(room_name)
        print(old_messages)
        if old_messages:
            typer.echo("Previous messages:")
            for msg in old_messages:
                ts = msg.get("timestamp", "")
                typer.echo(f"[{ts}] {msg['username']}: {msg['content']}")
        else:
            typer.echo("No previous messages found.")

        def start_ws_loop(token):
            asyncio.run(websocket_chat(room_name, username, stop_event, token))

        ws_thread = threading.Thread(target=start_ws_loop, args=(token,), daemon=True)
        ws_thread.start()

        typer.echo("Type your messages below.")
        typer.echo("Use ':back' to return, ':clear' to clear the screen, or Ctrl+C to exit.")

        try:
            while not stop_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            typer.echo("\nGoodbye!")
            stop_event.set()
            raise typer.Exit()

if __name__ == "__main__":
    app()

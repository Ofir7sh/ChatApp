import typer
import requests
import os
import threading
import time

app = typer.Typer()
BASE_URL = "http://127.0.0.1:8000"
TOKEN_FILE = ".chatapp_token"
USERNAME_FILE = ".chatapp_user"

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

def fetch_messages(room_name):
    res = requests.get(f"{BASE_URL}/messages/{room_name}", headers=authenticated_headers())
    if res.status_code == 200:
        return res.json()
    else:
        print(f"Failed to get messages: {res.text}")
        return []

def send_message(room_name, content, username):
    res = requests.post(
        f"{BASE_URL}/messages/{room_name}",
        json={"content": content, "username": username},
        headers=authenticated_headers()
    )
    if res.status_code != 200:
        print(f"Failed to send message: {res.text}")

def refresh_messages_periodically(room_name, username):
    last_seen = set()
    while True:
        messages = fetch_messages(room_name)
        new_msgs = [m for m in messages if m["id"] not in last_seen]
        for msg in new_msgs:
            ts = msg["timestamp"]
            print(f"[{ts}] {msg['username']}: {msg['content']}")
            last_seen.add(msg["id"])
        time.sleep(5)

@app.command()
def cli():
    username = input("Enter username: ").strip()
    save_username(username)

    password = typer.prompt("Password", hide_input=True)
    res = requests.post(f"{BASE_URL}/users/login", json={"username": username, "password": password})
    if res.status_code == 400:
        print("User not found, registering new user...")
        password = typer.prompt("Choose a password", hide_input=True)
        res = requests.post(f"{BASE_URL}/users/register", json={"username": username, "password": password})
        if res.status_code != 200:
            print("Registration failed:", res.text)
            raise typer.Exit()
        print("Registered successfully.")
    elif res.status_code != 200:
        print("Login failed:", res.text)
        raise typer.Exit()

    token = res.json()["access_token"]
    save_token(token)
    print("Logged in successfully.")

    chatrooms = fetch_chatrooms()
    print("Available chat rooms:")
    for idx, room in enumerate(chatrooms):
        print(f"{idx + 1}. {room['name']}")
    print("0. Create new chat room")
    choice = int(input("Choose chat room by number: "))

    if choice == 0:
        new_room_name = input("Enter new chat room name: ").strip()
        res = requests.post(f"{BASE_URL}/chatrooms/", json={"name": new_room_name}, headers=authenticated_headers())
        if res.status_code != 200:
            print("Failed to create chat room:", res.text)
            raise typer.Exit()
        room_name = new_room_name
    else:
        if choice < 1 or choice > len(chatrooms):
            print("Invalid choice.")
            raise typer.Exit()
        room_name = chatrooms[choice - 1]["name"]

    print(f"Entered chat room: {room_name}")


    threading.Thread(target=refresh_messages_periodically, args=(room_name, username), daemon=True).start()

    print("Type your messages below. Ctrl+C to exit.")
    try:
        while True:
            content = input()
            if content.strip():
                send_message(room_name, content.strip(), username)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        raise typer.Exit()

if __name__ == "__main__":
    app()

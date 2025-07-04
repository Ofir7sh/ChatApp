import typer
import requests
import os
import threading
import time
import platform

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

def check_user_exists(username):
    res = requests.get(f"{BASE_URL}/users/exists/{username}")
    if res.status_code != 200:
        print("Error checking user:", res.text)
        raise typer.Exit()
    return res.json().get("exists", False)

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

    # MAIN LOOP – Room selection
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

        # Start background refresher thread
        stop_flag = threading.Event()

        def refresher():
            last_seen = set()
            while not stop_flag.is_set():
                messages = fetch_messages(room_name)
                new_msgs = [m for m in messages if m["id"] not in last_seen]
                for msg in new_msgs:
                    ts = msg["timestamp"]
                    print(f"[{ts}] {msg['username']}: {msg['content']}")
                    last_seen.add(msg["id"])
                time.sleep(5)

        thread = threading.Thread(target=refresher, daemon=True)
        thread.start()

        print("Type your messages below.")
        print("Use ':back' to return to room selection, ':clear' to clear the screen, or Ctrl+C to exit.")
        try:
            while True:
                content = input()
                if content.strip() == ":back":
                    stop_flag.set()
                    time.sleep(0.1)
                    break  # Return to room list
                elif content.strip() == ":clear":
                    clear_screen()
                elif content.strip():
                    send_message(room_name, content.strip(), username)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            stop_flag.set()
            raise typer.Exit()
    
if __name__ == "__main__":
    app()

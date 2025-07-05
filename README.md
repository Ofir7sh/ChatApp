# ChatApp - CLI-based Chat Application

ChatApp is a simple chat application built with FastAPI, MSSQL, and a CLI interface powered by Typer.
It uses Docker Compose to build a full environment, including: FastAPI server,Microsoft SQL Server database, CLI client, database initialization service 

Supports two stages:
✅ Stage A – CLI Chat API-based

✅ Stage B – Real-time chat with WebSocket integration

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd ChatApp
```

### 2. Configure environment variables:

Create a `.env` file with the following contents:

```env
DB_USER = "sa"
DB_PASSWORD=YourStrongPassword
DB_HOST = "db"
DB_PORT = 1433
DB_NAME = "ChatAppDB"
BASE_URL = "http://server:8000"
WS_BASE_URL=ws://server:8000
```

### 3. Build the Containers
Make sure you have the following installed:
    Docker

    Docker Compose

```bash
docker-compose build
```
### 4. Run the Application

```bash
docker-compose up
```

This will start:

    * The MSSQL database
    * The DB initialization service
    * The FastAPI server
    * The CLI container (ready for client use:) )

Optional: Use this to troubleshoot and monitor Server requests:
```bash
docker-compose logs -f server
```
### 5. Start the CLI

To run an interactive CLI session:

```bash
docker-compose run --rm -it cli
```

Or if you prefer to enter the CLI container shell manually:

```bash
sudo docker exec -it chatapp-cli sh
python cli.py
```

## 🧪 Usage

After running the CLI, follow the instructions:

1. **Enter username** – A new user will be registered if not found.

2. **Enter password** – Either for login or to register.

3. **Select a chat room**:

   * View existing rooms
   * Create a new one (option `0`)

4. **Inside the chat room**:

   * Type your message and hit `Enter` to send
   * Use commands:

     * `:back` → Return to room selection
     * `:clear` → Clear terminal
     * `Ctrl+C` → Exit

    💡 a-stage (main) - Messages are automatically refreshed and displayed every 5 seconds

    💡 b-stage - Real-time, two-way communication baset WebSocket  

        once a room is selected:

            WebSocket connection is opened: ws://server:8000/ws/<room_name>?token=...

            Users can send and receive messages in real time


    🔐 After login, All requests to protected endpoints include JWT token in the Authorization: Bearer <token> header. 
    
 
## 🧱 Components

### server

FastAPI server that handles CRUD operations using endpoints for:

* Users (register, login)
* Chat rooms (list, create)
* Messages (send, fetch)
* WebSocket-based chat messaging (Stage B)

### cli

Typer-based Python CLI that lets users:

* Register/login
* View chat rooms list, Create new chat roon, Enter chat rooms
* Send & receive messages
* Communicate in real-time via WebSocket (Stage B)

## 🗃️ Database

* SQL Server 2022-latest container via Docker
* Tables: `users`, `chat_rooms`, `messages`
    * Initialized automatically using SQLAlchemy (in 'init_db' python script) during containers startup

## 🛠️ Technologies

* Python3.12
* FastAPI
* Typer
* MSSQL (SQL Server)
* SQLAlchemy
* Pydantic
* WebSockets
* Docker + Docker Compose
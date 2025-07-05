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
# Pay attention to SQL Server password policy requirements: The password must be at least 8 characters long and contain characters from three of the following four sets: Uppercase letters, Lowercase letters, Base 10 digits, and Symbols

```env
DB_USER="sa"
DB_PASSWORD="YourStrongPassword"
DB_HOST="db"
DB_PORT=1433
DB_NAME="ChatAppDB"
BASE_URL="http://server:8000"
WS_BASE_URL="ws://server:8000"
```

### 3. Build the Containers
Make sure you have the following installed:

    Docker,Docker Compose

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
---

## 🧪 Using the CLI

- Enter your username. If new, you will be prompted to create a password.  
- Log in with your username and password to receive a JWT token.  
- Select a chat room from the list or create a new one (option 0).  
- Inside the chat room:  
  - Type messages and press Enter to send  
  - Commands:  
    - `:back` → Return to room selection  
    - `:clear` → Clear terminal screen  
    - `Ctrl+C` → Exit the CLI  

---

## 💡 Key Features

- **Stage A** – Auto-refreshes messages every 5 seconds  
- **Stage B** – Real-time two-way communication via WebSocket  
- **Security** – JWT tokens for authenticated API requests  

---

## 🧱 System Components

### Server Side - FastAPI (`app/`)

- **API Endpoints:**  
  - Users (register, login)  
  - Chat rooms (list, create)  
  - Messages (send, fetch)  
  - WebSocket for real-time chat (Stage B)  

- **Technologies:**  
  - FastAPI  
  - SQLAlchemy ORM  
  - MSSQL (SQL Server 2022)  
  - Pydantic schemas 
  - WebSockets  
  - JWT authentication  

### Client Side - CLI (`client/`)

- Python CLI built with Typer  
- User registration/login, room selection, messaging  
- WebSocket support for real-time communication  

### Database Initialization (`init_db/`)

- MSSQL 2022 container  
- Tables: users, chat_rooms, messages  
- Automatic initialization via Python script on container startup  

---

## 🗃️ Database Schema Overview (define in app/models)

| Table         | Key Columns                                      | Notes                       |
|---------------|-------------------------------------------------|-----------------------------|
| **users**     | id, username, hashed_password                   | Stores user credentials securely |
| **chat_rooms**| id, name                                        | Chat rooms 
| **messages**  | id, content, username,timestamp,chat_room_id    | Messages within chat rooms  |

## 🔄 Volumes
Docker volumes are used in this project to persist data
```
volumes:
  mssql_data:
 ```
---

## 🗂️ Project Structure

```plaintext
ChatApp/
├── docker-compose.yml          
├── .gitignore
├── README.md
│
├── app/                        # FastAPI backend
│   ├── Dockerfile             
│   ├── __init__.py
│   ├── main.py                  # App entrypoints
│   ├── database.py              # DB connection setup
│   ├── requirements.txt
│   │
│   ├── core/                    # Configuration & security
│   │   ├── config.py           
│   │   └── security.py         
│   │
│   ├── crud/                    # CRUD logic
│   │   ├── user.py             
│   │   ├── chat_room.py        
│   │   └── message.py          
│   │
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py
│   │   ├── chat_room.py
│   │   └── message.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── chat_room.py
│   │   └── message.py
│   │
│   └── routes/                 # API routes
│       ├── user.py            
│       ├── chat_room.py       
│       └── message.py  
        └── message_ws.py        # WebSocket connection
│
├── client/                     # CLI client
│   ├── Dockerfile              
│   ├── cli.py                  # CLI main script
│   ├── requirements.txt
│   └── __pycache__/            
│
├── init_db/                    # DB initialization + tables creation
│   ├── Dockerfile
│   ├── init_db.py              # DB init script
│   ├── wait-for-it.sh          # Wait-for-DB script
│   └── requirements.txt
```

---

## 🛠️ Technologies Used

- **Language:** Python 3.12  
- **Backend:** FastAPI  
- **CLI:** Typer  
- **Database:** MSSQL (SQL Server 2022)
- **ORM:** SQLAlchemy  
- **Security:** JWT, password hashing  
- **Realtime:** WebSockets  
- **Containerization:** Docker + Docker Compose  
- **Helpers:** pymssql, Pydantic, wait-for-it.sh  

---

## 🏗️ Container Architecture

| Container Name   | Purpose                      | Dependencies                |
|------------------|------------------------------|-----------------------------|
| **db**           | MSSQL Server database         | None                        |
| **init_db**      | Database initialization       | Depends on `db`             |
| **server**       | FastAPI backend API           | Depends on `db`             |
| **cli**          | CLI client                    | None         |

- All containers run in a shared Docker network.  
- CLI communicates with the server via `http://server:8000`  
- WebSocket connections use `ws://server:8000/ws/...` in Stage B  

---

## Flow Diagram - Client, Server, and Database Communication

high-level flow of the components and their communication:

```plaintext
+------------+        HTTP/API        +------------+        SQL Queries       +------------+
|   CLI      | <--------------------> |  FastAPI   | <---------------------> |   MSSQL    |
| (Typer)    |                        |  Server    |      ORM (SQLAlchemy)   |  Database  |
+------------+                       +------------+                       +------------+
       |                                      |
       | WebSocket (Stage B)                   |
       +--------------------------------------+

- CLI sends HTTP requests to FastAPI for login/registeration, room selection/creation, message fetch/post.
- FastAPI handles API logic, validates JWT tokens, accesses DB via ORM.
- MSSQL stores all data: users, chat rooms, messages.
- For realtime chat (Stage B), CLI opens WebSocket connection to FastAPI to send/receive messages live.
- Application full enviroments build with docker-compose.
```
✅ ## TODO:
- Implenent c-stage:
  
    - define the user who created the room as an ADMIN
      
    - Admin user could decide whether the room is private / public
      
    - Admin could block and remove users from a room_chat
      
    - Enter privte chat root would be allowed only with uniq secret code
  
 
    ** ServerSide:
  
        ** /models
  
          - chat_rooms: add: admin_id, is_private, secret_code
  
          - Create new table - BlockedUsersInRoom
  
        ** /schemas
  
              - update ChatRoomBase, ChatRoomCreate: is_private, secrect_code
  
              - add schema to "blocking"
  
       ** CRUD (/crud)
  
          - add func to chat_room.py (check admin, block user, add user to private room)
  
       ** /routes
  
            - chat_rooms - add routes
  
       ** /websocket
  
  ** Client side:
  
      - add functionality:
  
          - private room -> enter private key
  
          - admin_user -> block users, add to private room, remove users, set room (private/public)
  
  ** DB (MSSQL):
  
      tables:
  
      - chat_rooms: add admin_id, is_private, secret_code
  
      - blocked_users
- Enhance logging (e.g., log levels, file logging, error tracking)
- Improve database initialization and data persistence workflow to improve maintainability and scalability
- Optimize performance
- Implement QA process
- Improve CLI UX

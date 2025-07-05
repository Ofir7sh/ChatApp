import os
from dotenv import load_dotenv
from pathlib import Path
# Load params from .env
env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
MASTER_DATABASE_URL = f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/master"

BASE_URL=f"http://{DB_HOST}:{DB_PORT}"
TOKEN_FILE = os.environ["TOKEN_FILE"]
USERNAME_FILE = os.environ["USERNAME_FILE"]
WS_BASE_URL=os.environ["WS_BASE_URL"]

# If API_HOST is not define so use 'localhost'
API_HOST = os.environ.get("API_HOST", "localhost") 
BASE_URL = f"http://{API_HOST}:8000"
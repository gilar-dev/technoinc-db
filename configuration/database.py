from typing import Any
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from supabase import Client, create_client
from configuration.config import MONGODB_URI, SUPABASE_URL, SUPABASE_SECRET_KEY

# For mongodb wiki articles database
client: AsyncMongoClient[dict[str, Any]] = AsyncMongoClient(MONGODB_URI, server_api=ServerApi("1"))
db = client.get_database("technoinc-db")

# For supabase postgresql contributors databse
if SUPABASE_URL is None or SUPABASE_SECRET_KEY is None:
    raise RuntimeError("Supabase URL and publishable key must be configured")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)
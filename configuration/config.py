import os
from dotenv import load_dotenv

load_dotenv()

DB_WIKI = os.getenv("MONGO_WIKI")
DB_CONTRIBUTOR = os.getenv("MONGO_CONTRIBUTOR")

origins = [
    "https://technoinc.world",
    "https://technoinc-next.netlify.app",
    "http://localhost:3000"
]
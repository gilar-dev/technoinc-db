import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("MONGO_URI")

origins = [
    "https://technoinc.world",
    "https://technoinc-next.netlify.app",
    "http://localhost:3000"
]
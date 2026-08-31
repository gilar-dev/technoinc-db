import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("MONGO_URI")

origins = [
    "https://technoinc.world",
    "https://technoinc.netlify.app",
    "http://localhost:5173",
    "http://localhost:3000",
    "https://technoinc-next.netlify.app"
]
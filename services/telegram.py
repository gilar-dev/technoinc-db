import httpx, os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_updated_article(title: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"""
⭐ An article is edited just now!

✅ Successful update for article '<b>{title}</b>'

⬇️ Check the article in here:
https://technoinc.world/wiki/{title}
"""
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"

        }
    )
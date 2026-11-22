import httpx, os
from pydantic import BaseModel
from dotenv import load_dotenv

class ModifyInfo(BaseModel):
    user: str
    sum: str
    date: str

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

async def send_created_article(title: str, modify_info: ModifyInfo) -> None:
    message = f"""
🌟 New article is created just now!

<b>Article</b>: {title.replace("_", " ")}
<b>Editor</b>: {modify_info.user}
<b>Summary</b>: {modify_info.sum or "<i>No summary added</i>"}
<b>Date</b>: {modify_info.date}

⬇️ Check the article in here:
https://technoinc.world/wiki/{title}
"""
    async with httpx.AsyncClient() as client:
        await client.post(URL, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })

async def send_updated_article(title: str, modify_info: ModifyInfo) -> None:
    message = f"""
⭐ An article is edited just now!

✅ Successful update for article '<b>{title.replace("_", " ")}</b>'

<b>Article</b>: {title.replace("_", " ")}
<b>Editor</b>: {modify_info.user}
<b>Summary</b>: {modify_info.sum or "<i>No summary added</i>"}
<b>Date</b>: {modify_info.date}

⬇️ Check the article in here:
https://technoinc.world/wiki/{title}
"""
    async with httpx.AsyncClient() as client:
        await client.post(URL, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"

        }
    )
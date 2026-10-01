import httpx, os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

async def send_created_article(title: str, modify_info: dict) -> None:
    message = f"""
🌟 New article is created just now!

<b>Article</b>: {title.replace("_", " ")}
<b>Editor</b>: {modify_info.get("user")}
<b>Summary</b>: {modify_info.get("sum") or "<i>No summary added</i>"}
<b>Date</b>: {modify_info.get("date")}

⬇️ Check the article in here:
https://technoinc.world/wiki/{title}
"""
    async with httpx.AsyncClient() as client:
        await client.post(URL, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })

async def send_updated_article(title: str, modify_info: dict) -> None:
    message = f"""
⭐ An article is edited just now!

✅ Successful update for article '<b>{title.replace("_", " ")}</b>'

<b>Article</b>: {title.replace("_", " ")}
<b>Editor</b>: {modify_info.get("user")}
<b>Summary</b>: {modify_info.get("sum") or "<i>No summary added</i>"}
<b>Date</b>: {modify_info.get("date")}

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
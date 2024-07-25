from telethon import TelegramClient
import json
from pathlib import Path
from dotenv import load_dotenv
import os
from config import *

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

async def main(chat_name, limit):
    async with TelegramClient(session_name, api_id, api_hash) as client:
        chat_info = await client.get_entity(chat_name)
        messages = await client.get_messages(entity=chat_info, limit=limit)
        return ({"messages": messages, "channel": chat_info})




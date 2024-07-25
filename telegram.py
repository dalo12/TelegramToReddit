from telethon import TelegramClient
import json
from pathlib import Path
from dotenv import load_dotenv
import os
from config import *

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

print(api_id)
print(api_hash)


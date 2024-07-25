from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from dotenv import load_dotenv
import os
import config as Config

# Unused
import json
import asyncio
from pathlib import Path

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("PHONE_NUM")
session_name = Config.session_name
channel_name = Config.channel_name

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start(phone_number)

    # Ensure you're authorized
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input("Enter the code: "))
        except SessionPasswordNeededError:
            await client.sign_in(password=input("Password: "))

    # Get the channel entity
    channel = await client.get_entity(channel_name)

    # Get messages from channel
    history = await client(GetHistoryRequest(
        peer=PeerChannel(channel.id),
        limit=1,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    messages = history.messages

    for message in messages:
        client.download_media(message)
        print(message.message)

with client:
    client.loop.run_until_complete(main())

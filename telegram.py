from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerChannel, PeerChannel
from dotenv import load_dotenv
import os
import config as Config
from datetime import datetime
import warnings

# Unused
import json
import asyncio
from pathlib import Path

load_dotenv()

# Suppress specific warning
warnings.filterwarnings("ignore", category=UserWarning, message=".*the session already had an authorized user.*")

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("PHONE_NUM")
session_name = Config.session_name
channel_name = Config.channel_name

client = TelegramClient(session_name, api_id, api_hash)

def main():
    now = datetime.now()
    now_formatted = now.strftime("%Y.%m.%d.%H.%M")    

    createMediaFolder(now_formatted)

    #with client:
    #    client.loop.run_until_complete(downloadFromTelegram())

async def downloadFromTelegram():
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
        print(message.message)
        if message.media:
            file_path = await client.download_media(message)

def createMediaFolder(dir_name):
    # Define the name of the subdirectory
    subdirectory_name = f"media/{dir_name}"

    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full path for the new subdirectory
    subdirectory_path = os.path.join(current_directory, subdirectory_name)

    # Create the new subdirectory
    os.makedirs(subdirectory_path, exist_ok=True)


main()
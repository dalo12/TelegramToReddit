from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerChannel, PeerChannel
from dotenv import load_dotenv
import os
import config as Config
from datetime import datetime
import warnings
import re

load_dotenv()

# Suppress specific warning
warnings.filterwarnings("ignore", category=UserWarning, message=".*the session already had an authorized user.*")

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("PHONE_NUM")
session_name = Config.session_name
channel_name = Config.channel_name
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await downloadMessagesFromTelegram()

async def downloadMessagesFromTelegram():
    print("Starting connection")
    await client.start(phone_number)

    # Ensure you're authorized
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input("Enter the code: "))
        except SessionPasswordNeededError:
            await client.sign_in(password=input("Password: "))
    print("User authorized")

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
    print(f"Downloading messages from Telegram channel {channel_name}")
    messages = history.messages

    await downloadMedia(messages)

async def downloadMedia(messages):
    print("Downloading messages media")
    for message in messages:
        date_string = formatDate(message.date)
        message_text = extractEnglishWords(message.message)
        message_text = formatText(message_text, date_string)
        
        directory_name = createMediaFolder(date_string)
        createMessageTextFile(directory_name, message.id, message_text)

        print("Downloading photo or video")
        if message.photo or message.video:
            file_path = await client.download_media(message, directory_name)

def createMediaFolder(dir_name):
    print("Creating corresponding media directory")
    # Define the name of the subdirectory
    subdirectory_name = f"media/{dir_name}"

    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full path for the new subdirectory
    subdirectory_path = os.path.join(current_directory, subdirectory_name)

    # Create the new subdirectory
    os.makedirs(subdirectory_path, exist_ok=True)

    return f"{subdirectory_path}"

def createMessageTextFile(dir_name, file_name, text):
    print("Creating message file")

    with open(f'{dir_name}/{file_name}.txt', 'w') as file:
        file.write(text)

def formatDate(date):
    date_format = "%Y.%m.%d.%H%M"
    date_string = date.strftime(date_format)
    return date_string

def extractEnglishWords(text):
    # Regular expression pattern for matching English words
    pattern = r'\b[a-zA-Z]+\b'
    
    # Find all English words using the pattern
    english_words = re.findall(pattern, text)
    
    english_words = ' '.join(english_words)
    return english_words

# Only for Lexie Liu's Telegram channel
def formatText(text, date):
    words = text.split()
    
    if len(words) <= 2:
        return ''

    words = words[1:-1]
    return_text = ' '.join(words)
    return_text = f"{date[:-5]} - {return_text}"

    return return_text

# Run the main function using the event loop
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
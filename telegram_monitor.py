import re
import json
import asyncio
from telethon import TelegramClient, events

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

api_id = config['api_id']
api_hash = config['api_hash']
phone = config['phone']
post_channel_ids = config['post_channel_ids']
channel_ids = config['channel_ids']
track_users = config['track_users']

client = TelegramClient('session_name', api_id, api_hash)

async def send_message_to_channels(message_text):
    for post_channel_id in post_channel_ids:
        await client.send_message(post_channel_id, message_text)

async def analyze_message(message_text):
    solana_memecoin_regex = re.compile(r'([1-9A-HJ-NP-Za-km-z]{32,44})')

    match = solana_memecoin_regex.search(message_text)
    if match:
        address = match.group(1)
        return address

@client.on(events.NewMessage(chats=channel_ids))
async def handler(event):
    channel_id = event.chat_id
    message_text = event.message.message    
    user_id = event.sender_id

    ca_address = await analyze_message(message_text)
    if ca_address:
        if str(channel_id).lstrip("-100") in track_users:
            if user_id in track_users[str(channel_id).lstrip("-100")]:
                await send_message_to_channels(ca_address)
            else:
                return
        else:
            await send_message_to_channels(ca_address)

async def main():
    await client.start(phone=phone)
    print("Listening for new messages...")
    await client.run_until_disconnected()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nStopping the script...")
except Exception as e:
    print(f"An error occurred: {e}")
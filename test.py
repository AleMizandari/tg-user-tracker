from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

async def print_topic_ids(channel_id):
    try:
        # Fetch the list of dialogs (topics)
        dialogs = await client(GetDialogsRequest(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=100,
            hash=0
        ))

        for dialog in dialogs.chats:
            if dialog.id == channel_id:
                print(f"Channel: {dialog.title}")
                for topic in dialog.threads:
                    print(f"Topic ID: {topic.id}, Topic Name: {topic.title}")
    except Exception as e:
        print(f"Failed to retrieve topics: {e}")

channel_id = 2449351682
with client:
    client.loop.run_until_complete(print_topic_ids(channel_id))
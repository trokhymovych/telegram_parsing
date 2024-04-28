import configparser
from telethon import TelegramClient
import joblib
from tqdm import tqdm
import glob
import os

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

input_data_path = config['comments_parsing']['input_data']
output_data_path = config['comments_parsing']['output_path']

input_files = glob.glob(input_data_path)


async def get_comments(client: TelegramClient, channel: str, message_id: int):
    messages = []
    async for message in client.iter_messages(channel, reply_to=message_id):
        try:
            reactions = []
            if message.reactions:
                for r in message.reactions.results:
                    try:
                        reactions.append({"emoticon": r.reaction.emoticon, "count": r.count})
                    except:
                        pass  # Usually means some custom emoticon that we are skipping

            sender_is_user = message.from_id.to_dict()["_"] == "PeerUser"
            if sender_is_user:
                sender_id = message.from_id.user_id
            else:
                try:
                    sender_id = message.from_id.channel_id
                except:
                    sender_id = None

            messages.append({
            "channel_name": message.peer_id.channel_id,
            "message_id": message.id,
            "message_text": message.message,
            "date": message.date,
            "sender_is_user": sender_is_user,
            "sender_id": sender_id,
            "via_bot_id": message.via_bot_id,
            "via_business_bot_id": message.via_business_bot_id,
            "reply_to_msg_id": message.reply_to.reply_to_msg_id,
            "reply_to_top_id": message.reply_to.reply_to_top_id,
            "reactions": reactions,
            "views": message.views,
            "replies": message.replies,
            "forwards": message.forwards,
            "is_media": message.media is not None,
            })
        except:
            print(channel, message_id)
    return messages


client = TelegramClient(username, api_id, api_hash)

with client:
    for file in tqdm(input_files):
        file_data = joblib.load(file)
        for message in tqdm(file_data):
            try:
                comments = client.loop.run_until_complete(get_comments(client, channel=message["channel_name"], message_id=message["message_id"]))
                if len(comments) > 0:
                    if not os.path.exists(f"{output_data_path}/{message['channel_name']}"):
                        os.makedirs(f"{output_data_path}/{message['channel_name']}")
                    joblib.dump(comments, f"{output_data_path}/{message['channel_name']}/{message['message_id']}.data")
            except Exception as e:
                print(e)
                print(message)
                print("Skipping...")

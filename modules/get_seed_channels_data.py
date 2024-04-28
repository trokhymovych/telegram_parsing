import configparser
from telethon import TelegramClient
import joblib
import pandas as pd
from tqdm import tqdm
import datetime

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

start_time = datetime.datetime.strptime(
    config['get_seed_channels_data']['data_min'],
    '%m/%d/%Y %H:%M:%S %Z',
).replace(tzinfo=datetime.timezone.utc)
finish_time = datetime.datetime.strptime(
    config['get_seed_channels_data']['data_max'],
    '%m/%d/%Y %H:%M:%S %Z',
).replace(tzinfo=datetime.timezone.utc)
input_data_path = config['get_seed_channels_data']['input_data']
output_data_path = config['get_seed_channels_data']['output_path']


async def get_messages(client: TelegramClient, channel_id, date_from=start_time, date_to=finish_time):
    messages = []
    async for message in client.iter_messages(channel_id, offset_date=date_to):
        reactions = []
        if message.reactions:
            for r in message.reactions.results:
                try:
                    reactions.append({"emoticon": r.reaction.emoticon, "count": r.count})
                except:
                    pass  # Usually means some custom emoticon that we are skipping
        forward_id = None
        forward_name = None
        if message.fwd_from:
            try:
                forward_id = message.fwd_from.from_id.channel_id
            except:
                forward_name = message.fwd_from.from_name

        if message.date < date_from:
            return messages

        messages.append({
           "channel_name": message.peer_id.channel_id,
           "message_id": message.id,
           "message_text": message.text,
           "reactions": reactions,
           "date": message.date,
           "views": message.views,
           "forwards": message.forwards,
           "forward_from": forward_id,
           "forward_name": forward_name,
           "is_media": message.media is not None,
        })
    return messages

client = TelegramClient(username, api_id, api_hash)
input_channels = pd.read_csv(input_data_path)
with client:
    for channel_id, channel_name in tqdm(zip(input_channels.ids, input_channels.names)):
        try:
            messages = client.loop.run_until_complete(get_messages(client, channel_id=channel_id))
            if len(messages) > 0:
                channel_id_ = messages[0]["channel_name"]
                joblib.dump(messages, f'{output_data_path}/{channel_id_}.data')
        except ValueError as ve:
            print(channel_id, str(ve))
            print("Attempting with the name: ", channel_name)
            try:
                messages = client.loop.run_until_complete(get_messages(client, channel_id=channel_name))
                if len(messages) > 0:
                    channel_id_ = messages[0]["channel_name"]
                    joblib.dump(messages, f'{output_data_path}/{channel_id_}.data')
            except:
                print(channel_id, str(e))
                print("Skipping...")
        except Exception as e:
            print(channel_id, str(e))
            print("Skipping...")

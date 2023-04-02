import configparser
from telethon import TelegramClient
import pickle


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']


async def get_comments(client: TelegramClient, channel: str, message_id: int):
    async for dialog in client.iter_dialogs():
        pass
    res = []
    async for message in client.iter_messages(channel, reply_to=message_id):
        full_comment_obj = message.to_dict()  # in JSON-Format
        res += [full_comment_obj]
    return res

async def get_messages(client: TelegramClient, channel_name):
    messages = []
    async for message in client.iter_messages(channel_name):
        
        reactions = []
        if message.reactions:
            for r in message.reactions.results:
                reactions.append({"emoticon": r.reaction.emoticon, "count": r.count})

        messages.append({
           "channel_name": channel_name,
           "message_id": message.id,
           "message_text": message.text,
           "reactions": reactions,
           "date": message.date,
           "views": message.views,
           "forwards": message.forwards
        })
    return messages

async def get_user_details(client: TelegramClient, user_ids):
    users_info = {}
    for user_id in user_ids:
        users_info[user_id] = await client.get_entity(user_id)
        users_info[user_id] = users_info[user_id].__dict__
    return users_info



# Remember to use your own values from my.telegram.org!
client = TelegramClient(username, api_id, api_hash)
print(client.__dict__)

# getting all comments to the given message
with client:
    print("Getting all comments to specific post...")
    res = client.loop.run_until_complete(get_comments(client, channel='FEDOROV', message_id=3020))
    with open('data/parsed_comments.pickle', 'wb') as handle:
        pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print("Getting all messages of the channel...")
    messages = client.loop.run_until_complete(get_messages(client, channel_name='FEDOROV'))
    with open('data/parsed_messages.pickle', 'wb') as handle:
        pickle.dump(messages, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("Getting users info...")
    users_to_collect = [r["from_id"]["user_id"] for r in res]
    users_info = client.loop.run_until_complete(get_user_details(client, user_ids=users_to_collect))
    with open('data/users_info.pickle', 'wb') as handle:
        pickle.dump(users_info, handle, protocol=pickle.HIGHEST_PROTOCOL)
                                   
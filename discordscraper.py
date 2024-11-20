import requests
import json
import os
from dotenv import load_dotenv

def update_log(entry):
    print(entry, end='')
    log.write(entry)

load_dotenv('channel_id.env')
channel_ids = os.getenv('CHANNEL_IDS').split(',')

load_dotenv('token.env')
discord_token = os.getenv('DISCORD_TOKEN')

path = input("Enter the file save directory: ")
limit = int(input("Enter the iteration limit: "))

headers = {
    'authorization': discord_token
}

for channel_id in channel_ids:
    save_dir = os.path.join(path, f"{channel_id}")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    request = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}', headers=headers)
    messages = json.loads(request.text)

    log_file = os.path.join(save_dir, 'log.txt')

    with open(log_file, 'w', encoding='utf-8') as log:
        for message in messages[::-1]:
            update_log(f"{message['author']['username']}: {message['content']}\n")

            if message.get('attachments') != []:
                for attachment in message['attachments']:
                    update_log(f">> {attachment['filename']} ({attachment['url']})\n")

                    file_path = os.path.join(save_dir, f"{attachment['id']}_{attachment['filename']}")
                    with requests.get(attachment['url'], stream=True) as request:
                        with open(file_path, 'wb') as file:
                            for chunk in request.iter_content(chunk_size=8192):
                                file.write(chunk)
                    
                    update_log(f">>> Saved as {attachment['id']}_{attachment['filename']}\n")
from datetime import date, datetime
from telethon import TelegramClient
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetDialogsRequest
import json

# read configs
f = open('config.json')

configs = json.load(f)
api_id = configs['api_id']
api_hash = configs['api_hash']
msg_to_monitor = configs['msg_to_monitor']
chats_to_monitor = configs['chats_to_monitor']
days_to_monitor = configs['days_to_monitor'] # 0 == only today
keywords = configs['keywords']
phone = configs['phone']

f.close();

# initialize telegram instance
client = TelegramClient(phone, api_id, api_hash)

def checkForKeywoards(msg):
    for keyword in keywords:
        if keyword in msg:
            return True
    return False

async def main():
    result_file=open("result.txt", "w")

    me = await client.get_me()
    
    async for dialog in client.iter_dialogs():
        result_file.write(str(dialog.id) + " --- " + str(dialog.name) + "\n")

    async for dialog in client.iter_dialogs():
        if dialog.name in chats_to_monitor:
            messages = await client.get_messages(dialog.id, limit= msg_to_monitor) #pass your own args
            result_file.write("----------------------- " + dialog.name + " -------------------------\n")
            
            for x in messages:
                if (x.text and checkForKeywoards(x.text)):
                    if ((date.today().day - x.date.day) <= days_to_monitor  and x.date.month == date.today().month):
                        result_file.write(x.text + "\n------------------------------------------------\n")

    result_file.close()

if __name__ == '__main__':  
    with client:
        client.loop.run_until_complete(main())
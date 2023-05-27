from os import environ
import os
import time
import aiohttp
from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests
import re

import pyrogram
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#from telethon.sessions import StringSession
#from telethon.sync import TelegramClient
#from decouple import config
import logging, sys
import threading

API_ID = environ.get('API_ID', 22507697)
API_HASH = environ.get('API_HASH', '5604a464d474e5738980a533580b751a')
BOT_TOKEN = environ.get('BOT_TOKEN', '6245284320:AAEPaZXi_NnfcAbCK94DPcni7N2xGELhpJk')
SESSION = environ.get('SESSION', 'AQBhPFxrmxMjobupLs54ZaLmwCv3IDGjiSOZS9CSoUenH-DfNUjZnXamwZ5vabZMAeJDaKM-gaCpf0_fWBiuAPBh1CWno2ICXBkpLmUd6BADn3kx3cjAOCbranR1BntU46ryLdK-qf08rELhYIT7LQnnj-U6HQ3qaOkfethlR7eweDNOZepijU0SEhxO-qfJiGT4uKwNdSxBKlNuSizYD29j3is7ceEl0K-SMvVo3h3OmG8UUzNh-QkSC6LsvYPdUc1dxOsvd4VTeqQiJZcarnPRegtutLAqTOAX5zIKlcvR9T1YspzpW3d2xHJN9KHIZ0hvZo0UY2XGrtDEZDJvnAxnAAAAAVbqnxYA')
CHANNEL = environ.get('CHANNEL', 'https://google.com')
HOWTO = environ.get('HOWTO', 'https://google.com')

bot = Client('fastdown bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=0)
             
if SESSION is not None:
    acc = Client(
    session_name=SESSION, 
    api_hash=API_HASH, 
    api_id=API_ID)
    
    try:
            acc.start()
    except BaseException:
            print("Userbot Error ! Have you added SESSION while deploying??")
            sys.exit(1)
        
else: acc = None

# download status
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3    )      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			bot.edit_message_text(message.chat.id, message.message_id, f"__Downloaded__ : **{txt}**")
			time.sleep(2)
		except:
			time.sleep(2)
			
# upload status
"""def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			bot.edit_message_text(message.chat.id, message.message_id, f"__Uploaded__ : **{txt}**")
			time.sleep(2)
		except:
			time.sleep(2)"""
			
# progress writter
def progress(current, total, message, type):
	with open(f'{message.chat.id}{message.message_id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**I am a Fast Multi Downloader Bot and i am able to download telegram files to your local storage,just send me link of file and video or forward any File or Video**")
        
@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# joining chats
	if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

		if acc is None:
			bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.message_id)
			return

		try:
			try: acc.join_chat(message.text)
			except Exception as e: 
				bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.message_id)
				return
			bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.message_id)
		except UserAlreadyParticipant:
			bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.message_id)
		except InviteHashExpired:
			bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.message_id)
	
	# getting message
	elif "https://t.me/" in message.text:

		datas = message.text.split("/")
		msgid = int(datas[-1].split("?")[0])

		# private
		if "https://t.me/c/" in message.text:
			chatid = int("-100" + datas[-2])
			if acc is None:
				bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.message_id)
				return
			try: handle_private(message,chatid,msgid)
			except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.message_id)
		
		# public
		else:
			username = datas[-2]
			msg  = bot.get_messages(username,msgid)
			try: bot.copy_message(message.chat.id, msg.chat.id, msg.id)
			except:
				if acc is None:
					bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.message_id)
					return
				try: handle_private(message,username,msgid)
				except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.message_id)
	
	
# handle private
def handle_private(message,chatid,msgid):
		msg  = acc.get_messages(chatid,msgid)

		if "text" in str(msg):
			bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.message_id)
			return

		smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.message_id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.chat.id}{message.message_id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.chat.id}{message.message_id}downstatus.txt')
		if os.path.exists(f'{message.chat.id}{message.message_id}upstatus.txt'): os.remove(f'{message.chat.id}{message.message_id}upstatus.txt')


@bot.on_message(filters.video | filters.document)
async def vdood_upload(bot, message):
    smsg = await bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.message_id)
    dosta = threading.Thread(target=lambda:downstatus(f'{message.chat.id}{message.message_id}downstatus.txt',smsg),daemon=True)
    dosta.start()
    file = await bot.download_media(message, progress=progress, progress_args=[message,"down"])
    os.remove(f'{message.chat.id}{message.message_id}downstatus.txt')
    if os.path.exists(f'{message.chat.id}{message.message_id}upstatus.txt'): os.remove(f'{message.chat.id}{message.message_id}upstatus.txt')
    


"""@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello, {message.chat.first_name}!**\n\n"
        "**If you send post which had Doodstream Links, texts & images... Than I'll convert & replace all Doodstream links with your Doodstream links \nMessage me @kamdev07 For more help-**")"""

"""@bot.on_message(filters.command('support') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**please contact me on @unnamed or for more join @unnamed**")"""
    
'''@bot.on_message(filters.text & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'{Doodstream_link}' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)'''


"""@bot.on_message(filters.photo & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        if(len(Doodstream_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{Doodstream_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{Doodstream_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)"""

'''async def addFooter(str):
    footer = """
    ━━━━━━━━━━━━━━━
⚙️ How to Download / Watch Online :""" + HOWTO + """
━━━━━━━━━━━━━━━
⭐️JOIN CHANNEL ➡️ t.me/""" + CHANNEL
    return str + footer'''

bot.run()

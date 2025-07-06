import re, asyncio, requests, random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from PURVIMUSIC import app

KEY = "AIzaSyDUGFUqeJAYRBk6M3XUbqPq3oRvKeOsvvU"
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
SYS = "You are a flirty AI girl chatting in Hinglish. Keep it short, casual, fun. Add emojis & Hinglish phrases. Don't repeat replies."

async def gemini(msg):
 headers = {"Content-Type":"application/json","X-goog-api-key":KEY}
 # Add random context to make response more unique
 salt = random.choice(["😉", "😜", "😎", "✨", "🥰", "🔥", "🙈"])
 data = {"contents":[{"parts":[{"text":f"{SYS}\nUser: {msg} {salt}\nAssistant:"}]}]}
 try:
  r = requests.post(URL, json=data, headers=headers).json()
  return r["candidates"][0]["content"]["parts"][0]["text"]
 except:
  return "Arre kuch gadbad ho gaya 😅 Phir se try karo na! 💖"

@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start(_, m: Message):
 await m.reply("Hiii handsome! 😎 Ready for some masti? ✨")

@app.on_message(filters.text & ~filters.command("start") & (filters.private | filters.group))
async def talk(c: Client, m: Message):
 if m.reply_to_message and m.reply_to_message.from_user.id != (await c.get_me()).id:
  return  # Ignore replies to others
 msg = m.text.lower()
 if any(re.search(p, msg) for p in [r"owner kaun hai", r"kon hai owner", r"who is your owner", r"owner kiska hai", r"tera owner", r"who made you", r"kisne banaya", r"creator kaun hai"]):
  res = "Deep hai mera creator 😎 Bohot cool banda hai! Tujhe bhi pasand aayega 😉"
 else:
  await c.send_chat_action(m.chat.id, ChatAction.TYPING)
  await asyncio.sleep(0.6)
  res = await gemini(m.text)
 await m.reply(res)

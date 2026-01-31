import os
import sys
import asyncio
from threading import Thread
from flask import Flask
import discord
from google import genai 

# [1] 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] 웹 서버
app = Flask('')
@app.route('/')
def home(): return "K is listening."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

# [4] AI 연결
ai_client = None
if GEMINI_API_KEY:
    try:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
    except:
        print("❌ AI Connection Error")

# [5] 봇이 켜지면 하는 말
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("▶ **System stable. Model loaded. I am ready.**")

#

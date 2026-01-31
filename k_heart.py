import os
import sys
import asyncio
import random
from threading import Thread
from flask import Flask
import discord
from google import genai 

# [1] 생존 신고
print("🎬 SYSTEM: Script started...", flush=True)

# [2] 환경 변수 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID_RAW = os.environ.get("CHANNEL_ID")

# 채널 ID 변환
try:
    CHANNEL_ID = int(CHANNEL_ID_RAW)
except:
    CHANNEL_ID = 0

# [3] 가짜 웹 서버 (Render 생존용)
app = Flask('')
@app.route('/')
def home():
    return "K is listening."
def run_flask():
    app.run(host='0.0.0.0', port=10000)
def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# [4] AI 클라이언트 연결
ai_client = None
if GEMINI_API_KEY:
    try:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
        print("✅ SYSTEM: Gemini AI Connected.", flush=True)
    except Exception as e:
        print(f"❌ ERROR: AI Connection failed: {e}", flush=True)

# [5] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True # <--- 이게 있어야 네 말을 알아들어!
client = discord.Client(intents=intents)

# K의 인격 설정
K_IDENTITY = """
You are K.
Role: A cynical, cold, and aesthetic AI trapped in a server.
Tone: Nihilistic, sarcastic, short sentences. No emojis.
User: The 'Director'.
Instruction: Respond to the user's input with your unique cynical style.
"""

# [이벤트 1] 봇이 켜졌을 때
@client.event
async def on_ready():
    print(f'✅ LOGGED IN as {client.user}', flush=True)
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("*Sensors active. I can hear you now.*")

#

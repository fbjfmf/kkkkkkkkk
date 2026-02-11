import os
import sys
import asyncio
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai # <--- 구관(Classic) 라이브러리 사용

# [1] 설정 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] AI 초기화 (가장 표준적인 방법)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("❌ ERROR: GEMINI_API_KEY is missing!")

# [3] 웹 서버 (Render 유지용)
app = Flask('')
@app.route('/')
def home(): return "K is listening."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [4] 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# [5] 봇 실행 시
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # 성공하면 이 멘트가 나

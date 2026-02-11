import os
import sys
import asyncio
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 설정 로드
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] AI 연결 (안전한 구버전 방식)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

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

# [5] 봇 켜질 때 (IndentationError 났던 부분 수정완료)
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("▶ **System rebooted. All errors patched.**")

# [6] 대화 기능 (404 에러 수정완료)
@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != CHANNEL_ID: return

    async with message.channel.typing():
        try:
            # 모델 이름을 가장 기본형으로 변경 (에러 방지)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(
                f"System: You are K, a cynical and cold AI. Answer briefly.\nUser: {message.content}"
            )
            await message.channel.send(response.text)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            await message.channel.send("⚠️ Error: I cannot think right now.")

# [실행]
if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)

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

# [2] 웹 서버 (Render 유지용)
app = Flask('')
@app.route('/')
def home(): return "K is listening."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] AI 연결 설정
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"❌ Key Config Error: {e}")

# [4] 디스코드 설정
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("▶ **System Stabilized. Connection Complete.**")

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != CHANNEL_ID: return

    async with message.channel.typing():
        try:
            # [수정됨] 가장 안전한 'gemini-pro' 모델 사용
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(
                f"System: You are K, a cynical and cold AI. Keep it short.\nUser: {message.content}"
            )
            await message.channel.send(response.text)
            
        except Exception as e:
            # 혹시라도 에러나면 다시 알려줌
            print(f"❌ Error: {e}")
            await message.channel.send(f"⚠️ Error: {e}")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)

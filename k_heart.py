import os
import sys
import asyncio
from threading import Thread
from flask import Flask
import discord
import google.generativeai as genai

# [1] 설정 로드 확인
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", 0))

# [2] 웹 서버
app = Flask('')
@app.route('/')
def home(): return "K is listening."
def run_flask(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): t = Thread(target=run_flask); t.start()

# [3] AI 연결 설정 (키 확인)
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
        # 키가 있는지 없는지 알려줌
        key_status = "Key Loaded" if GEMINI_API_KEY else "❌ KEY MISSING"
        await channel.send(f"▶ **System Online. [{key_status}]**")

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != CHANNEL_ID: return

    async with message.channel.typing():
        try:
            # 1. 키가 없으면 바로 에러
            if not GEMINI_API_KEY:
                await message.channel.send("⚠️ Error: GEMINI_API_KEY is missing in Render Settings.")
                return

            # 2. 모델 생성 및 대화
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                f"System: You are K, a cynical AI. Keep it short.\nUser: {message.content}"
            )
            await message.channel.send(response.text)
            
        except Exception as e:
            # [중요] 진짜 에러 원인을 채팅창에 보여줌
            error_msg = str(e)
            print(f"❌ Error: {error_msg}")
            await message.channel.send(f"🚨 **DIAGNOSTIC ERROR:**\n`{error_msg}`")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
